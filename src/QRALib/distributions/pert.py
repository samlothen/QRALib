from scipy.stats import beta as beta_dist
import numpy as np
from typing import Optional

class PERT:
    """
    A model based on the Beta-PERT distribution for impact modelling.

    The Beta-PERT distribution is a three-point estimation technique commonly used in project management
    to model uncertain variables with a known minimum, most likely, and maximum value.

    :param minimum: The minimum value in the range.
    :type minimum: float
    :param mid: The most likely value in the range.
    :type mid: float
    :param maximum: The maximum value in the range.
    :type maximum: float
    """

    def __init__(self, minimum: float, mid: float, maximum: float) -> None:
        if minimum >= maximum:
            raise AssertionError("Min frequency must exceed max frequency. Min:", minimum, "Max:", maximum)
        if not minimum <= mid <= maximum:
            raise AssertionError("Mean should be between min and max frequencies. Min:", minimum, "Mean:",mid, "Max:", maximum)

        self.min = minimum
        self.mid = mid
        self.max = maximum
        self._parameters()

    def _parameters(self) -> None:
        """
        Calculate the parameters of the Beta-PERT distribution.
        """

        self.alpha = (1 + (4 * (self.mid - self.min) / (self.max - self.min) ) )
        self.beta = (1 + (4 * (self.max - self.mid) / (self.max - self.min) ) )
        self.location = self.min
        self.scale = self.max - self.min

        self.distribution = beta_dist(self.alpha, self.beta, loc=self.location, scale=self.scale)

    def draw(self, n: int = 1) -> np.ndarray:
        """
        Generate random samples from the Beta-PERT distribution.

        :param n: The number of samples to generate.
        :type n: int
        :return: Array of size n with random values from the distribution.
        :rtype: numpy.ndarray
        """

        return self.distribution.rvs(size=n)

    def draw_ppf(self, percentile_sequences: np.ndarray) -> np.ndarray:
        """
        Generate samples from the Beta-PERT distribution using the percent point function (PPF).

        :param percentile_sequences: Array of numbers in the range [0, 1)
        :type percentile_sequences: numpy.ndarray
        :return: Array of the same size as the input with values from the distribution PPF
        :rtype: numpy.ndarray
        """
        if not isinstance(percentile_sequences, np.ndarray) or not np.issubdtype(percentile_sequences.dtype, np.number) or not (0 <= percentile_sequences).all() or not (percentile_sequences <= 1).all():
            raise ValueError("percentile_sequences must be a numpy array of numbers in the range [0, 1)")
        return self.distribution.ppf(percentile_sequences)

    def mean(self, round_to: Optional[int] = None) -> np.float64:
        """
        Calculate the mean value of the Beta-PERT distribution.

        :param round_to: Number of decimal places to round the mean value to.
        :type round_to: int or None
        :return: Mean value of the distribution.
        :rtype: numpy.float64
        """
        mean = self.distribution.mean()
        if round_to is not None:
            mean = round(mean, round_to)
        return mean
