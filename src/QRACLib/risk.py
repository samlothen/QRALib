"""Container for risk event
* ID = An identifier for the scenario
* name = A descriptive name for the scenario
* frequency_model = Probability distribtuion for it occuring
* frequency_group = String for frequency model used
* impact_group = Probability distribtuion for impact
* impact_model = String for magnitude model used
"""

class Risk:
    """Risk Model"""

    def __init__(self, uniq_id, name, frequency_dist, frequency_model, impact_dist, impact_model):

        """Initialize impact and frequency paramters"""
        self.uniq_id = uniq_id
        self.name = name
        self.frequency_group = frequency_dist
        self.frequency_model = frequency_model
        self.impact_group = impact_dist
        self.impact_model = impact_model

    def get_impact(self, n):
        return self.impact_model.draw(n)

    def get_frequency(self,n):
        return self.frequency_model.draw(n)

    def get_impact_ppf(self, n):
        return self.impact_model.draw_ppf(n)

    def get_frequency_ppf(self,n):
        return self.frequency_model.draw_ppf(n)