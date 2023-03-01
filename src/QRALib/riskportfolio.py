from QRALib.distributions.lognormal import Lognormal
from QRALib.distributions.pert import PERT
from QRALib.distributions.uniform import Uniform 
from QRALib.distributions.beta import Beta
from QRALib.risk import Risk


class RiskPortfolio:
    """Risk Model"""

    def __init__(self, risk_dict) -> None:
        """
        Initialize a RiskPortfolio object from a dictionary of risks
        
        Parameters:
        ----------
        risk_dict : dict
            A dictionary containing a list of risks, where each risk is represented as a dictionary with keys 'ID', 'name', 
            'frequency', and 'impact'.
        """
        self.risk_ids = []
        self.instances = []

        for risk in risk_dict["Risks"]:
            #uniq_id, name, frequency_dist, frequency_model, impact_dist, impact_model = self._from_dict(risk)
            #self.instances.append(Risk(uniq_id, name, frequency_dist, frequency_model, impact_dist, impact_model))
            self.instances.append(Risk(*self._from_dict(risk)))
    
    def listing(self):
        """
        Return a list of all Risk objects in the portfolio.
        
        Returns:
        -------
        list
            A list of all Risk objects in the portfolio.
        """
        return self.instances
    
    def risk_id_list(self):
        """
        Return a list of all risk IDs in the portfolio.
        
        Returns:
        -------
        list
            A list of all risk IDs in the portfolio.
        """
        return self.risk_ids

    def search(self, term):
        """
        NOT IMPLMENTED YET
        Search for a risk in the portfolio based on a search term.
        
        Parameters:
        ----------
        term : str
            A search term to match against the risk ID or name.
        """
        pass

    def lookup(self, risk_no):
        """
        Get the details of a specific risk in the portfolio by its index.
        
        Parameters:
        ----------
        risk_no : int
            The index of the risk to lookup.
            
        Returns:
        -------
        dict
            A dictionary containing details of the risk, including its ID, name, frequency distribution, frequency 
            parameters, impact distribution, and impact parameters.
        """
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

    def _from_dict(self, risk_dict)-> object:
        """Create a probability distribution object based on the given distribution name.

        Parameters:
        -----------
        risk_dict : dict
            A dictionary containing the parameters of the risk event, including its
            frequency and impact distribution parameters.
        distribution : str
            A string specifying the distribution name to be used (e.g., "Beta", "Lognormal").
        attribute : str
            A string specifying which attribute of the risk (i.e., "frequency" or "impact")
            to apply the distribution to.

        Returns:
        --------
        object
            An object representing the probability distribution of the risk's frequency
            or impact (e.g., a Beta object, Lognormal object).

        Raises:
        -------
        AssertionError:
            If the input distribution name is not recognized.
        """
        uniq_id = risk_dict['ID']
        self.risk_ids.append(uniq_id)
        name = risk_dict['name']
    
        frequency_dist = risk_dict['frequency']['distribution']
        frequency_model = self._setup_dist(risk_dict, frequency_dist, 'frequency')
        impact_dist = risk_dict['impact']['distribution']
        impact_model = self._setup_dist(risk_dict, impact_dist, 'impact')

        return uniq_id, name, frequency_dist, frequency_model, impact_dist, impact_model
    
    @staticmethod 
    def _setup_dist(risk_dict, distribution: str, attribute: str) -> object:
        """Create a probability distribution object based on the given distribution name.

        Parameters:
        -----------
        risk_dict : dict
            A dictionary containing the parameters of the risk event, including its
            frequency and impact distribution parameters.
        distribution : str
            A string specifying the distribution name to be used (e.g., "Beta", "Lognormal").
        attribute : str
            A string specifying which attribute of the risk (i.e., "frequency" or "impact")
            to apply the distribution to.

        Returns:
        --------
        object
            An object representing the probability distribution of the risk's frequency
            or impact (e.g., a Beta object, Lognormal object).

        Raises:
        -------
        AssertionError:
            If the input distribution name is not recognized.
        """
        if distribution == "Beta":
            model = Beta(risk_dict[attribute]['parameters']['alpha'], risk_dict[attribute]['parameters']['beta'])
        elif distribution == "Uniform":
            model = Uniform(risk_dict[attribute]['parameters']['low'], risk_dict[attribute]['parameters']['high'])
        elif distribution == "Lognormal":
            model = Lognormal(risk_dict[attribute]['parameters']['mu'], risk_dict[attribute]['parameters']['sigma'])
        elif distribution == "PERT":
            minimum = risk_dict[attribute]['parameters']['low']
            mean = risk_dict[attribute]['parameters']['mid']
            maximum = risk_dict[attribute]['parameters']['high']
            model = PERT(minimum, mean, maximum)
        else:
            raise AssertionError("Unknown Distribution, val:", attribute)
        
        return model
        