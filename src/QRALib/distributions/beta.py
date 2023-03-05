"""A model based on the beta distribution to produce probability modelling
"""
from scipy.stats import beta as beta_dist
import numpy as np

class Beta:
    def __init__(self, alpha: float, beta: float) -> None:
        """
        Create a beta distribution with given alpha and beta parameters.

        :param alpha: Number of "hit" samples
        :type alpha: float
        :param beta: Number of "miss" samples
        :type beta: float
        :raises ValueError: If alpha or beta is not greater than 0.
        """
        if alpha <= 0 or beta <= 0:
            raise ValueError("Alpha and Beta must be greater than 0")
        self.distribution = beta_dist(alpha, beta)

    def draw(self, n: int = 1) -> np.ndarray:
        """
        Draw random samples from the beta distribution.

        :param n: Number of samples to return
        :type n: int
        :return: Array of size n with random values from the distribution
        :rtype: numpy.ndarray
        """

        return self.distribution.rvs(size=n)

    def draw_ppf(self, percentile_sequences: np.ndarray) -> np.ndarray:
        """
        Generate samples from the beta distribution using the percent point function (PPF).

        :param percentile_sequences: Array of numbers in the range [0, 1]
        :type percentile_sequences: numpy.ndarray
        :return: Array of the same size as the input with values from the distribution PPF
        :rtype: numpy.ndarray
        """
        if not isinstance(percentile_sequences, np.ndarray) or not np.issubdtype(percentile_sequences.dtype, np.number) or not (0 <= percentile_sequences).all() or not (percentile_sequences <= 1).all():
            raise ValueError("percentile_sequences must be a numpy array of numbers in the range [0, 1]")
        return self.distribution.ppf(percentile_sequences)
    
    def mean(self) -> np.float64:
        """
        Calculate the mean value of the beta distribution.

        :return: Mean value of the distribution
        :rtype: float
        """
        return self.distribution.mean()