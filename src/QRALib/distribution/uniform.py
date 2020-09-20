"""A model based on the uniform distribution define by a 90% confidence interval
"""
from scipy.stats import uniform

class Uniform:
    def __init__(self, low_bound, up_bound):
        """:param  low_bound = Low bound estimate
        :param up_bound = Upper bound estimate

        The range low_bound -> up_bound should represent the 90% confidence interval
        that the probability of the event occuring will fall in that range.

        These values are then fit to a uniform distribution so that they fall at the 5% and
        95% cumulative probability points.
        """
        self.low_bound = low_bound
        self.up_bound = up_bound
        self._parameters(low_bound, up_bound)
        
   
    def _parameters(self, low_bound, up_bound):
        if low_bound >= up_bound:
            raise AssertionError("Upper bound must exceed lower bound")

        confidence_interval = (0.9)
        factor = ((1.00 - confidence_interval)/2)
        min_val = ((confidence_interval + factor) * low_bound - factor * up_bound)/confidence_interval
        if min_val < 0:
            min_val = 0

        max_val = ((confidence_interval + factor) * up_bound - factor * low_bound)/confidence_interval
        
        self.loc = min_val
        self.scale = max_val - min_val

        self.distribution = uniform(self.loc, self.scale)

    def draw(self, n=1):
        """:param  n = Number of samples to return
        :return: array of size n with random values from distribtuion 
        :rtype: numpy.ndarray
        """
        return self.distribution.rvs(size=n)

    def draw_ppf(self, percentile_sequences):
        """:param  percentile_sequences = list of numbers in range [0,1]
        :return: array of same size as inpu with values from the distribtuions
        percent point function. 
        :rtype: numpy.ndarray
        """
        return self.distribution.ppf(percentile_sequences)
    
    def mean(self):
        """:return: mean value of the distribution
        :rtype: numpy.float64
        """
        return self.distribution.mean()