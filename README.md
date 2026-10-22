# Studio 07: completed simulation and analysis

This is the instructor solution. Distribute the sibling `student/` directory.
The student version leaves only scenario design, aggregation, and the two
figures unfinished; the simulation engine, tests, and workflow are identical.

## Run

Use the course Python environment, or install `requirements.txt`:

```bash
python3 -m pip install -r requirements.txt
make test
make all
```

`make simulate REPS=2` runs a small check. The default is 100 replicates and
master seed 20261015. `make simulate`, `make analyze`, and `make figures` are
independent stages. `make all` runs them in order. Running the simulation
again resumes completed scenario batches; `make clean` removes all generated
results and checkpoints. Use `make PYTHON=python` if needed.

The included 26-scenario study takes roughly two minutes in the authoring
environment; local runtime varies. Inspect `results/raw/design.csv` for the
full design. `ADEMP.md` explains the statistical design and performance
measures; `ASSIGNMENT.md` is the student-facing assignment.

## Layout

| Location | Contents |
| --- | --- |
| `scenarios.py` | Complete design, in one parameter dictionary |
| `src/dgps.py` | DGP interface and normal/Laplace subclasses |
| `src/methods.py` | Estimator interface and OLS/LAD subclasses |
| `src/metrics.py` | Realized losses and paired-ratio MCSE helper |
| `src/simulation.py` | Study runner, stable streams, checkpoints, provenance |
| `simulate.py`, `analyze.py` | Drivers for simulation, aggregation, and plotting |
| `tests/` | Five supplied engine tests |
| `results/raw/` | Raw CSV, design matrix, metadata, and scenario checkpoints |
| `results/summary.csv` | Means, MCSEs, and fit counts |
| `results/figures/` | Two figures in PNG/PDF plus provenance |

No dataset cache is needed: data regenerate from stable streams. NPZ
checkpoints retain coefficient estimates, truth, covariance, and method IDs
so additional losses can be computed without refitting. Read with
`np.load(path, allow_pickle=False)`. The CSV checkpoint is published after
its numeric output and marks a completed scenario batch.

The study fingerprint covers all scenario/method settings, seed, replication
count, simulation source hashes, and environment versions. Metadata records
the precise stream rule. Data and each method have separate generators;
methods share each replicate's dataset. Scenario streams depend on IDs, so
reordering or extending the grid preserves draws for existing IDs. The same
settings given different IDs use distinct data, including A/B overlap.

Failed fits remain in raw results with missing estimates/losses and a message;
warnings are recorded. Summaries report counts, and the analysis driver
reports the number of failures. Figure A uses complete pairs and a paired
delta-method MCSE for the ratio; both figures display +/-2 MCSE.

Expected findings: under normal errors OLS beats LAD; under Laplace errors
LAD wins at small p/n but can lose at larger p/n. Correlated predictors can
produce large coefficient error while prediction error remains stable.
