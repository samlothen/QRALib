"""A impact model based on the Beta-PERT distribution to produce impact modelling
"""
from scipy.stats import beta as beta_dist

class PERT:
    def __init__(self, minimum: float, mid: float, maximum: float):
        """:param  minimum = Low bound estimate
        :param mid = Most likely estimate
        :param maximum = Upper bound estimate
        The range minimum -> maximum should represent the 90% confidence interval
        that the loss will fall in that range.
        """
        self.min = minimum
        self.mid = mid
        self.max = maximum
        self._parameters(minimum, mid, maximum)

    def _parameters(self, minimum, mid, maximum):
        """:param frequency = Mean rate per interval"""
        if minimum >= maximum:
            raise AssertionError("Min frequency must exceed max frequency. Min:", minimum, "Max:", maximum)
        if not minimum <= mid <= maximum:
            raise AssertionError("Mean should be between min and max frequencies. Min:", minimum, "Mean:",mid, "Max:", maximum)
        self.alpha = (1 + (4 * (mid - minimum) / (maximum - minimum) ) )
        self.beta = (1 + (4 * (maximum - mid) / (maximum - minimum) ) )
        self.location = minimum
        self.scale = maximum - minimum
        
        self.distribution = beta_dist(self.alpha, self.beta, loc=self.location, scale=self.scale)
        

    def draw(self, n=1):
        return self.distribution.rvs(size=n)

    def draw_ppf(self, low_discrepancy_sequences):
        return self.distribution.ppf(low_discrepancy_sequences)
    
    def mean(self):
        return self.distribution.mean()
