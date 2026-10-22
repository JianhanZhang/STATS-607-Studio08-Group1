# ADEMP: robust regression

**Aims.** Compare OLS and LAD as p/n grows under normal and Laplace errors;
distinguish coefficient estimation from in-distribution prediction as
predictor correlation grows. Predict the patterns before running.

**Data-generating mechanisms.** Generate independent rows of X from
N_p(0, Sigma), with Sigma[j,k]=rho**abs(j-k), and y=X beta+epsilon.
Use n=200, beta[j]=1/sqrt(p), and errors independent of X. Normal errors
have variance one. Laplace errors have location zero and scale 1/sqrt(2),
also giving variance one. A fresh dataset is generated in each replicate.

| Experiment | Vary | Hold fixed |
| --- | --- | --- |
| A | Chosen p/n values, both normal and Laplace errors | n=200, rho=0 |
| B | Chosen rho values | n=200, p=100, normal errors |

Choose the exact values in `scenarios.py`. The driver exports the complete
design matrix, one row per scenario, as `results/raw/design.csv`. The saved
metadata includes every setting, the replicate count, seed, and stream rule.

**Estimands/targets.** The coefficient vector beta and the conditional mean
X_new beta for independent new predictors from the same distribution.

**Methods.** OLS and unpenalized median regression (LAD), without intercepts.
Fit both methods to the same dataset within each replicate. The sample size,
signal, and error variance match across methods and error distributions.

**Performance measures.** Average squared coefficient error ||beta_hat-beta||^2
and signal prediction error (beta_hat-beta)' Sigma (beta_hat-beta), without
dividing by p or adding response noise. Report replicate SD/sqrt(B) as the
MCSE of a mean. Figure A uses the ratio of mean coefficient losses, with a
paired MCSE from the supplied helper; Figure B uses the two estimated MSEs.
Keep fit counts visible and report failures if any occur.

The starter uses 100 replicates and master seed 20261015. Identical commands
resume completed scenario batches; code/configuration changes produce a
new study ID. Scenario and replicate IDs identify stable, independent task
streams. Discuss your grid choices and limitations in `ANALYSIS.md`.

## Complete example design

| Scenario ID | Experiment | n | p | p/n | rho | Errors |
| --- | --- | --- | --- | --- | --- | --- |
| A_normal_p010 | A | 200 | 10 | 0.05 | 0.0 | normal |
| A_normal_p020 | A | 200 | 20 | 0.10 | 0.0 | normal |
| A_normal_p040 | A | 200 | 40 | 0.20 | 0.0 | normal |
| A_normal_p060 | A | 200 | 60 | 0.30 | 0.0 | normal |
| A_normal_p080 | A | 200 | 80 | 0.40 | 0.0 | normal |
| A_normal_p100 | A | 200 | 100 | 0.50 | 0.0 | normal |
| A_normal_p120 | A | 200 | 120 | 0.60 | 0.0 | normal |
| A_normal_p140 | A | 200 | 140 | 0.70 | 0.0 | normal |
| A_normal_p160 | A | 200 | 160 | 0.80 | 0.0 | normal |
| A_normal_p180 | A | 200 | 180 | 0.90 | 0.0 | normal |
| A_laplace_p010 | A | 200 | 10 | 0.05 | 0.0 | laplace |
| A_laplace_p020 | A | 200 | 20 | 0.10 | 0.0 | laplace |
| A_laplace_p040 | A | 200 | 40 | 0.20 | 0.0 | laplace |
| A_laplace_p060 | A | 200 | 60 | 0.30 | 0.0 | laplace |
| A_laplace_p080 | A | 200 | 80 | 0.40 | 0.0 | laplace |
| A_laplace_p100 | A | 200 | 100 | 0.50 | 0.0 | laplace |
| A_laplace_p120 | A | 200 | 120 | 0.60 | 0.0 | laplace |
| A_laplace_p140 | A | 200 | 140 | 0.70 | 0.0 | laplace |
| A_laplace_p160 | A | 200 | 160 | 0.80 | 0.0 | laplace |
| A_laplace_p180 | A | 200 | 180 | 0.90 | 0.0 | laplace |
| B_rho00 | B | 200 | 100 | 0.50 | 0.0 | normal |
| B_rho50 | B | 200 | 100 | 0.50 | 0.5 | normal |
| B_rho80 | B | 200 | 100 | 0.50 | 0.8 | normal |
| B_rho90 | B | 200 | 100 | 0.50 | 0.9 | normal |
| B_rho95 | B | 200 | 100 | 0.50 | 0.95 | normal |
| B_rho99 | B | 200 | 100 | 0.50 | 0.99 | normal |
