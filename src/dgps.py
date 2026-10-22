"""Regression DGPs sharing the generate(rng) interface from Lecture 6."""

from abc import ABC, abstractmethod

import numpy as np


class RegressionDGP(ABC):
    """Gaussian predictors, fixed beta, and an interchangeable error law.

    Parameters satisfy 0 < p < n and 0 <= rho < 1. generate() takes a
    NumPy Generator and returns X, y, beta_true, covariance in a dictionary.
    Array shapes are (n, p), (n,), (p,), (p, p), respectively.
    """

    def __init__(self, n, r2, gamma):
        self.n, self.gamma = n, gamma
        self.p = int(self.gamma * self.n)
        self.covariance = np.eye(self.p)
        self.beta = np.ones(self.p) * np.sqrt(r2 / self.p)

    @abstractmethod
    def errors(self, rng):
        """Return n independent errors with mean zero and variance one."""

    def generate(self, rng):
        X = rng.normal(size=(self.n, self.p)) #@ self.factor.T
        return {"X": X, "y": X @ self.beta + self.errors(rng),
                "beta_true": self.beta, "covariance": self.covariance}


class NormalDGP(RegressionDGP):
    def errors(self, rng):
        return rng.normal(size=self.n)


'''class LaplaceDGP(RegressionDGP):
    def errors(self, rng):
        return rng.laplace(scale=1 / np.sqrt(2), size=self.n)'''


# DGP_CLASSES = {"normal": NormalDGP, "laplace": LaplaceDGP}
