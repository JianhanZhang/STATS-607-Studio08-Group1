"""Run or resume the scenarios; no student implementation is needed here."""

import argparse
import logging
from pathlib import Path

from scenarios import make_scenarios
from src.simulation import SimulationStudy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reps", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20261015)
    parser.add_argument("--out", type=Path, default=Path("results/raw"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    study = SimulationStudy(make_scenarios(), n_reps=args.reps,
                            seed=args.seed, out_dir=args.out)
    results = study.run()
    logging.info("Saved %s rows (%s) to %s", len(results), study.study_id, args.out)


if __name__ == "__main__":
    main()
