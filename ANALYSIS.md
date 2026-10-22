# Interpretation of the completed example

The design covers p/n from 0.05 to 0.9 under each error law, and puts more
correlation values near one, where estimation may become unstable. Equal
error variances and paired method fits make the comparisons fair; all 26
scenarios and their exact settings are listed in `results/raw/design.csv`.

## Does the correctly specified MLE always win?

OLS is the MLE under normal errors and has lower coefficient MSE throughout
this grid. LAD is the MLE under Laplace errors, but its MSE relative to OLS
increases from 0.73 at p/n=0.05 to 1.35 at p/n=0.9. The Laplace ratio is 0.98
at p/n=0.3 and 1.09 at p/n=0.4; the bars show uncertainty in the location of
the transition. Classical fixed-dimension asymptotic MLE efficiency does
not guarantee the best finite-sample MSE when p is substantial relative to n.

## Do poor coefficients imply poor predictions?

For OLS, coefficient MSE rises from 1.04 at rho=0 to 98.66 at rho=0.99,
while prediction MSE stays close to one (1.04 and 1.01 at these endpoints).
Coefficient error in directions of small predictor variance contributes
little to the covariance-weighted prediction loss, so large coefficient
errors need not produce large signal-prediction errors. LAD shows the same
qualitative separation, with higher prediction MSE here. This concerns new
predictors from the same distribution and does not guarantee performance
under a change in predictor covariance.

## Monte Carlo uncertainty and scope

There are 100 replicates per scenario and 5,200 fitted models, with no failed
fits. The figures display +/-2 Monte Carlo SE; Figure A uses the covariance
between paired losses through the supplied ratio helper. These bars quantify
simulation noise, not uncertainty intervals for a fitted coefficient vector.
The study uses one sample size and signal specification; more replicates
and a finer p/n grid near the crossing could sharpen the first finding.
