"""Run the Studio 08 ridgeless OLS study and save Person 3's input file."""

import argparse
from pathlib import Path

from scenarios import make_scenarios
from src.dgps import DGP_CLASSES
from src.simulation import simulate_ridgeless_ols


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=20261015)
    parser.add_argument("--output", type=Path, default=Path("simulation_results.pkl"))
    parser.add_argument("--expected-fits", type=int, default=15000)
    args = parser.parse_args()

    scenarios = make_scenarios()
    missing = [scenario_id for scenario_id, settings in scenarios.items()
               if "n_sim" not in settings and "nsim" not in settings]
    if missing:
        raise SystemExit(
            "Person 1's scenarios must include nsim (or n_sim) for each gamma/regime; "
            f"missing in: {', '.join(missing[:5])}"
        )

    total_fits = sum(int(settings.get("n_sim", settings.get("nsim", 0)))
                     for settings in scenarios.values())
    if args.expected_fits > 0 and total_fits != args.expected_fits:
        raise SystemExit(
            f"Scenario design requests {total_fits:,} fits; "
            f"expected {args.expected_fits:,}. Check Person 1's scenario grid."
        )

    results = simulate_ridgeless_ols(
        scenarios, seed=args.seed, dgp_classes=DGP_CLASSES, r2=5.0)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    results.to_pickle(temporary)
    temporary.replace(args.output)
    print(f"Completed {total_fits:,} OLS fits; saved {len(results)} rows to {args.output}")


if __name__ == "__main__":
    main()