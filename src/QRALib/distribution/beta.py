"""A model based on the beta distribution to produce probability modelling
"""
from scipy.stats import beta as beta_dist

class Beta:
    def __init__(self, alpha: float, beta: float):
        """:param  alpha = Number of "hit" samples  
        :param beta = Number of "miss" samples

        Alpha and Beta must be bigger than 0.
        """
        if alpha <= 0 or beta <= 0:
            raise AssertionError("Alpha and Beta must be greater than 0")
        self.distribution = beta_dist(alpha, beta)   

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