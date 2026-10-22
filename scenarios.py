"""Specify the simulation design in one place."""


def make_scenarios():
    """Return {scenario_id: settings} for experiments A and B.

    IDs are unique, stable, filename-safe strings. Each settings dictionary
    has exactly experiment ('A'/'B'), n (int), p (int), rho (float), and
    error_distribution ('normal'/'laplace'). Assume 0 < p < n, 0 <= rho < 1.
    The study supplies all generation, fitting, evaluation, and replication.

    Keep n=200. For A, use rho=0 and both error laws over the SAME chosen
    p/n values. For B, use normal errors and p=100 and choose rho values.
    Choose the values yourselves; the handout grid is only an example.
    """
    scenarios = {}
    n = 200
    for distribution in ["normal", "laplace"]:
        for gamma in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
            p = round(n * gamma)
            scenarios[f"A_{distribution}_p{p:03d}"] = {
                "experiment": "A", "n": n, "p": p, "rho": 0.0,
                "error_distribution": distribution}
    for rho in [0.0, 0.5, 0.8, 0.9, 0.95, 0.99]:
        scenarios[f"B_rho{round(100 * rho):02d}"] = {
            "experiment": "B", "n": n, "p": 100, "rho": rho,
            "error_distribution": "normal"}
    return scenarios
