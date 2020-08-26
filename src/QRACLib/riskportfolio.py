from QRACLib.distribution.lognormal import Lognormal
from QRACLib.distribution.pert import PERT
from QRACLib.distribution.uniform import Uniform
from QRACLib.distribution.beta import Beta
from QRACLib.risk import Risk as Risk

class RiskPortfolio:
    """Risk Model"""

    def __init__(self, risk_dict):
        self.risk_ids = []
        self.instances = []

        for risk in risk_dict["Risks"]:
            uniq_id, name, frequency_dist, frequency_model, impact_dist, impact_model = self._from_dict(risk)
            
            self.instances.append(Risk(uniq_id, name, frequency_dist, frequency_model, impact_dist, impact_model))
    
    def listing(self):
        return self.instances
    
    def risk_id_list(self):
        return self.risk_ids

    def search(self, term):
        pass

    def lookup(self, risk_no):
        risk = {
            "id" : self.instances[risk_no].uniq_id,
            "name" : self.instances[risk_no].name,
            "frequency_distribution" : self.instances[risk_no].frequency_group,
            "frequency_parameters" : self.instances[risk_no].frequency_model.__dict__,
            "impact_distribution" : self.instances[risk_no].impact_group,
            "impact_parameters" : self.instances[risk_no].impact_model.__dict__
        }
        del risk["frequency_parameters"]["distribution"]
        del risk["impact_parameters"]["distribution"]
        return risk

    def _from_dict(self, risk_dict):
        """Take a Dicitionary object and create a risk"""
        uniq_id = risk_dict['ID']
        self.risk_ids.append(uniq_id)
        name = risk_dict['name']
    
        frequency_dist = risk_dict['frequency']['distribution']
        frequency_model = self._setup_dist(risk_dict, frequency_dist, 'frequency')
        impact_dist = risk_dict['impact']['distribution']
        impact_model = self._setup_dist(risk_dict, impact_dist, 'impact')

        return uniq_id, name, frequency_dist, frequency_model, impact_dist, impact_model
    
    @staticmethod 
    def _setup_dist(risk_dict, distribution: str, attribute: str):
        if distribution == "Beta":
            model = Beta(risk_dict[attribute]['parameters']['alpha'], risk_dict['frequency']['parameters']['beta'])
        elif distribution == "Uniform":
            model = Uniform(risk_dict[attribute]['parameters']['low'], risk_dict['frequency']['parameters']['high'])
        elif distribution == "Lognormal":
            model = Lognormal(risk_dict[attribute]['parameters']['low'], risk_dict['impact']['parameters']['high'])
        elif distribution == "PERT":
            minimum = risk_dict[attribute]['parameters']['low']
            mean = risk_dict[attribute]['parameters']['mean']
            maximum = risk_dict[attribute]['parameters']['high']
            model = PERT(minimum, mean, maximum)
        
        else:
            raise AssertionError("Unknown Distribution, val:", attribute)
        
        return model
        