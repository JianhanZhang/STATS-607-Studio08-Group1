import numpy as np

from scenarios import make_scenarios
from src.dgps import DGP_CLASSES
from src.simulation import simulate_ridgeless_ols


def test_simulation_returns_person3_schema_with_mse_and_se():
    observations = iter([1.0, 3.0])

    def generate_data(n, p, rng):
        return np.ones((1, 1)), np.array([next(observations)]), np.zeros(1)

    scenarios = {
        "gamma_0_5_reps_2": {"n": 1, "p": 1, "gamma": 0.5, "n_sim": 2},
    }
    results = simulate_ridgeless_ols(scenarios, generate_data, seed=19)

    assert results.columns.tolist() == ["n_sim", "gamma", "MSE", "se"]
    assert results.loc[0, "MSE"] == 5.0
    assert results.loc[0, "se"] == 4.0


def test_single_replication_has_nan_standard_error():
    def generate_data(n, p, rng):
        return np.ones((1, 1)), np.array([2.0]), np.zeros(1)

    scenarios = {"one_rep": {"n": 1, "p": 1, "gamma": 1.0, "n_sim": 1}}
    results = simulate_ridgeless_ols(scenarios, generate_data, seed=19)

    assert results.loc[0, "MSE"] == 4.0
    assert np.isnan(results["se"].to_numpy(dtype=np.float64)[0])


def test_person1_scenarios_and_dgp_match_simulation_contract():
    scenarios = make_scenarios()
    assert len(scenarios) == 5105
    assert sum(settings["nsim"] for settings in scenarios.values()) == 15000

    scenario_id = next(iter(scenarios))
    settings = scenarios[scenario_id]
    result = simulate_ridgeless_ols(
        {scenario_id: {**settings, "n": 12, "p": 4, "nsim": 2}},
        dgp_classes=DGP_CLASSES,
        seed=23,
        r2=5.0,
    )

    assert result.columns.tolist() == ["n_sim", "gamma", "MSE", "se"]
    assert result.loc[0, "n_sim"] == 2
    assert np.isfinite(result["MSE"].to_numpy(dtype=np.float64)[0])
    assert np.isfinite(result["se"].to_numpy(dtype=np.float64)[0])