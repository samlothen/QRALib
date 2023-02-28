"""A model based on the uniform distribution define by a 90% confidence interval
"""
from scipy.stats import uniform
import numpy as np

class Uniform:
    def __init__(self, low_bound: float, up_bound: float) -> None:
        """
        :param low_bound: Lower bound estimate
        :type low_bound: float
        :param up_bound: Upper bound estimate
        :type up_bound: float
    
        The range low_bound -> up_bound should represent the 90% confidence interval
        that the probability of the event occuring will fall in that range.
    
        These values are then fit to a uniform distribution so that they fall at the 5% and
        95% cumulative probability points.
        """
        if low_bound >= up_bound:
            raise ValueError("up_bound must exceed low_bound")
        self.low_bound = low_bound
        self.up_bound = up_bound
        self._parameters()

    def _parameters(self) -> None:
        """
        Calculate the parameters of the uniform distribution.

        :param low_bound: Lower bound estimate
        :type low_bound: float
        :param up_bound: Upper bound estimate
        :type up_bound: float
        """
        confidence_interval = 0.9
        factor = (1.0 - confidence_interval) / 2
        min_val = (confidence_interval + factor) * self.low_bound - factor * self.up_bound
        if min_val < 0:
            min_val = 0
        max_val = (confidence_interval + factor) * self.up_bound - factor * self.low_bound
        self.loc = min_val
        self.scale = max_val - min_val
        self.distribution = uniform(self.loc, self.scale)

    def draw(self, n: int = 1) -> np.ndarray:
        """
        Generate random samples from the uniform distribution.

        :param n: Number of samples to return
        :type n: int
        :return: Array of size n with random values from distribution
        :rtype: numpy.ndarray
        """
        return self.distribution.rvs(size=n)

    def draw_ppf(self, percentile_sequences: np.ndarray) -> np.ndarray:
        """
        Generate samples from the uniform distribution using the percent point function (PPF).

        :param percentile_sequences: Array of numbers in the range [0, 1)
        :type percentile_sequences: numpy.ndarray
        :return: Array of the same size as the input with values from the distribution PPF
        :rtype: numpy.ndarray
        """
        if not isinstance(percentile_sequences, np.ndarray) or not np.issubdtype(percentile_sequences.dtype, np.number) or not (0 <= percentile_sequences).all() or not (percentile_sequences < 1).all():
            raise ValueError("percentile_sequences must be a numpy array of numbers in the range [0, 1)")
        return self.distribution.ppf(percentile_sequences)

    def mean(self) -> np.float64:
        """
        Calculate the mean value of the uniform distribution.

        :return: Mean value of the distribution
        :rtype: numpy.float64
        """
        return self.distribution.mean()
