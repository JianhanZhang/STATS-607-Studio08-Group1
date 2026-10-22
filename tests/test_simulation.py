"""Supplied checks for the simulation engine, not student plotting choices."""

import numpy as np
import pandas as pd

from src.dgps import LaplaceDGP, NormalDGP
from src.methods import LAD, OLS, Method
from src.metrics import evaluate, paired_ratio
from src.simulation import SimulationStudy


def test_dgps_have_stated_covariance_and_variance_one_errors():
    for dgp_class in [NormalDGP, LaplaceDGP]:
        dgp = dgp_class(n=30000, p=3, rho=0.6)
        data = dgp.generate(np.random.default_rng(97))
        errors = data["y"] - data["X"] @ data["beta_true"]
        np.testing.assert_allclose(np.cov(data["X"], rowvar=False),
                                   dgp.covariance, atol=0.025)
        assert abs(errors.mean()) < 0.025
        assert abs(errors.var() - 1) < 0.04
        np.testing.assert_allclose(data["beta_true"], np.ones(3) / np.sqrt(3))


def test_methods_recover_noiseless_coefficients():
    data = NormalDGP(30, 4, 0.3).generate(np.random.default_rng(11))
    data["y"] = data["X"] @ data["beta_true"]
    for method in [OLS(), LAD()]:
        estimate = method.fit(data, np.random.default_rng(12))
        np.testing.assert_allclose(estimate, data["beta_true"], atol=1e-7)


def test_losses_and_paired_ratio_account_for_covariance():
    data = {"beta_true": np.zeros(2), "covariance": np.array([[1., .5], [.5, 1.]])}
    assert evaluate(np.array([1., -1.]), data) == {
        "coefficient_error": 2., "prediction_error": 1.}
    ratio, mcse = paired_ratio(np.array([2., 4., 6.]), np.array([1., 2., 3.]))
    assert ratio == 2
    assert mcse == 0  # Perfect pairing: the ratio is constant across replicates.


def test_study_is_reproducible_alone_and_after_grid_reordering(tmp_path):
    settings = {"experiment": "A", "n": 16, "p": 3, "rho": 0.2,
                "error_distribution": "laplace"}
    scenarios = {"first": settings, "second": {**settings, "error_distribution": "normal"}}
    combined = SimulationStudy(scenarios, n_reps=3, seed=41, out_dir=tmp_path / "both").run()
    reversed_grid = SimulationStudy(dict(reversed(list(scenarios.items()))), n_reps=3,
                                    seed=41, out_dir=tmp_path / "reverse").run()
    alone = SimulationStudy({"first": settings}, n_reps=3, seed=41,
                            out_dir=tmp_path / "alone").run()
    columns = ["scenario_id", "rep", "method", "coefficient_error", "prediction_error"]
    def ordered(frame):
        return frame[columns].sort_values(columns[:3]).reset_index(drop=True)
    pd.testing.assert_frame_equal(ordered(combined), ordered(reversed_grid))
    pd.testing.assert_frame_equal(ordered(combined[combined.scenario_id == "first"]), ordered(alone))
    assert len(combined) == 12
    assert combined.coefficient_error.nunique() == 12


def test_failed_fits_are_saved_and_completed_batches_resume(tmp_path, monkeypatch):
    class BrokenMethod(Method):
        name, settings = "broken", {}

        def fit(self, data, rng):
            raise RuntimeError("deliberate test failure")

    scenarios = {"check": {"experiment": "A", "n": 12, "p": 2, "rho": 0.,
                            "error_distribution": "normal"}}
    study = SimulationStudy(scenarios, n_reps=2, out_dir=tmp_path,
                            methods=[OLS(), BrokenMethod()])
    results = study.run()
    failed = results[results.method == "broken"]
    assert len(failed) == 2
    assert (failed.status == "failed").all()
    assert failed.coefficient_error.isna().all()
    assert failed.message.str.contains("deliberate test failure").all()
    with np.load(study.study_dir / "check.npz", allow_pickle=False) as saved:
        assert saved["estimates"].shape == (2, 2, 2)
        assert np.isnan(saved["estimates"][:, 1, :]).all()
    def no_generation(self, rng):
        raise AssertionError("A completed batch should not generate new data")
    monkeypatch.setattr(NormalDGP, "generate", no_generation)
    resumed = study.run()
    pd.testing.assert_frame_equal(results, resumed, check_dtype=False)
