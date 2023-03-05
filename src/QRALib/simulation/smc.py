"""Simulate risk portfolio using Monte Carlo Simulations.
The simulator takes a list of risks when setting up. 
The simulation takes the number of interations as input.
Output is a nested dictionary. The dictionary has two primary keys 'summary' and 
'results' that contain the information about the simulation and the results.
"""

import numpy as np
from numpy.random import poisson as poisson
import multiprocessing
from joblib import Parallel, delayed

class MonteCarloSimulation:

    def __init__(self, risk_list):
        """:param  risk_list = list of the risks to simulate
        """
        self.risk_list = risk_list
        self.num_cores = multiprocessing.cpu_count()

    def simulation(self, num_of_iter=10000):
        """:param  num_of_iter = number of simulation iterations, default 10 000
        :return: nested dictionary with a 'summary' and 'results' as keys
        :rtype: dictionary  
        """

        self.num_of_iter = num_of_iter
        risk_outcome = Parallel(n_jobs=self.num_cores)(delayed(self._simulation)(risk) for risk in self.risk_list.listing())
        simulation_result = {
            "summary":{
                "number_of_iterations": num_of_iter,
                "risk_list": self.risk_list,
            },
            "results": risk_outcome
        }
        return simulation_result
        
    def _simulation(self, risk):
        r_1 = risk.get_frequency(self.num_of_iter)
        r_2 = poisson(r_1)
        impact = risk.get_impact(np.sum(r_2))
        sr_impact = risk.get_impact(self.num_of_iter)
        last = 0
        outcome = []

        outcome = [np.sum(impact[last:last+i]) for i in np.nditer(r_2)]
            
        risk_outcome = {
            "id" : risk.uniq_id,
            "frequency" : r_1,
            "occurances" : r_2,
            "impact" : impact,
            "single_risk_impact" : sr_impact,
            "total" : outcome
        }
        
        return risk_outcome