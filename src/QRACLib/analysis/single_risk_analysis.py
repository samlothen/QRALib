"""Single Risk Analysis tool to explore individual risks. 
"""

import numpy as np
import plotly.express as px
from tabulate import tabulate


class SingleRiskAnalysis:

    def __init__(self, simulation_result):
        self.simulation_dict = simulation_result["results"]
        self.num_iter = simulation_result["summary"]["number_of_iterations"]
    
    def single_risk_analysis(self, risk_no):
        # Table 
        tbl_headers = ["Attribute", "Min", "5%", "Mean", "95%", "Max"]
        frequency_stats = ["Frequency", min(self.simulation_dict[risk_no]["frequency"]), np.percentile(self.simulation_dict[risk_no]["frequency"], 5),np.percentile(self.simulation_dict[risk_no]["frequency"], 50), np.percentile(self.simulation_dict[risk_no]["frequency"], 95) ,max(self.simulation_dict[risk_no]["frequency"]) ]
        impact_stats = ["Impact", min(self.simulation_dict[risk_no]["single_risk_impact"]), np.percentile(self.simulation_dict[risk_no]["single_risk_impact"], 5),np.percentile(self.simulation_dict[risk_no]["single_risk_impact"], 50), np.percentile(self.simulation_dict[risk_no]["single_risk_impact"], 95) ,max(self.simulation_dict[risk_no]["single_risk_impact"]) ]
        print("Risk ID: ", self.simulation_dict[risk_no]["id"])
        print(tabulate([frequency_stats, impact_stats], headers=tbl_headers))

        # Uncertainty - box plot 
        uncertainty_frequency_fig = px.box(x=(self.simulation_dict[risk_no]["frequency"])*100)
        uncertainty_frequency_fig.show()
        uncertainty_impact_fig = px.box(x=self.simulation_dict[risk_no]["single_risk_impact"])
        uncertainty_impact_fig.show()

        # Total risk 
        sorted_array = np.sort(self.simulation_dict[risk_no]["total"])
        max_outcome = np.amax(sorted_array)
        points = np.arange(0, max_outcome+1, max_outcome/100)
        counter = np.zeros(shape=(len(points),1))


        for i in range(0,len(points)):
            counter[i] = sum(comp >= points[i] for comp in self.simulation_dict[risk_no]["total"])

        y1 = 100*(counter/self.num_iter)
        y1_flat = [y for x in y1 for y in x]
        
        fig = px.line(x=points, y=y1_flat)
        fig.show()
