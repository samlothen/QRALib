"""Single Risk Analysis tool to explore individual risks. 
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statistics import mean

class SingleRiskAnalysis:

    def __init__(self, simulation_result):
        self.simulation_dict = simulation_result["results"]
        self.num_iter = simulation_result["summary"]["number_of_iterations"]
    
    def single_risk_analysis(self, risk_no):

        tbl_headers = ["Attribute", "Min", "5%", "Mean", "95%", "Max"]
        attribute = ["Frequency","Impact"]
        min_val =[round(min(self.simulation_dict[risk_no]["frequency"]), 2),round(min(self.simulation_dict[risk_no]["single_risk_impact"]), 2)]
        percentile_5th = [round(np.percentile(self.simulation_dict[risk_no]["frequency"], 5), 2),round(np.percentile(self.simulation_dict[risk_no]["single_risk_impact"], 5), 2)]
        mean_val = [round(mean(self.simulation_dict[risk_no]["frequency"]),  2),round(mean(self.simulation_dict[risk_no]["single_risk_impact"]), 2)]
        percentile_95th = [round(np.percentile(self.simulation_dict[risk_no]["frequency"], 95), 2),round(np.percentile(self.simulation_dict[risk_no]["single_risk_impact"], 95), 2)]
        max_val = [round(max(self.simulation_dict[risk_no]["frequency"]), 2), round(max(self.simulation_dict[risk_no]["single_risk_impact"]), 2)]


        sorted_array = np.sort(self.simulation_dict[risk_no]["total"])
        max_outcome = np.percentile(sorted_array, 99)
        points = np.arange(0, max_outcome+1, max_outcome/100)
        counter = np.zeros(shape=(len(points),1))


        for i in range(0,len(points)):
            counter[i] = sum(comp >= points[i] for comp in self.simulation_dict[risk_no]["total"])
        
        y1 = counter/self.num_iter
        y1_flat = [y for x in y1 for y in x]



        uncertainty_fig = make_subplots(
            rows=3, 
            cols=2,
            specs=[
                [{"type": "scatter", "rowspan": 2}, {"type": "box"}],
                [None, {"type": "box"}],
                [{"type": "table", "colspan": 2}, None]],
           subplot_titles=("Impact exceedance curve", "Frequency", "Impact", "Statistics"))

        uncertainty_fig.add_trace(go.Box(
                x=(self.simulation_dict[risk_no]["frequency"]),
                name='',
                boxpoints=False,
                boxmean='sd',
                showlegend=False),
                row=1, col=2)


        uncertainty_fig.add_trace(go.Box(
                x=self.simulation_dict[risk_no]["single_risk_impact"],
                name='',
                boxpoints=False,
                boxmean='sd',
                showlegend=False),
                row=2, col=2)


        
        uncertainty_fig.add_trace(
            go.Scatter(
                x=points,y=y1_flat,
                name='',
                marker=dict(color="crimson"), showlegend=False),row=1, col=1)
        
        uncertainty_fig.add_trace(
            go.Table(columnwidth = [50,50,50,50,50,50],header=dict(values=tbl_headers,align='left'),
                cells=dict(values=[attribute, min_val, percentile_5th, mean_val, percentile_95th, max_val],
                align='left')), row=3, col=1)

        risk_id_string = self.simulation_dict[risk_no]["id"]
        title = f"Analysis Risk {risk_id_string}"
        
        uncertainty_fig.update_xaxes(title_text="Impact", row=1, col=1)
        uncertainty_fig.update_yaxes(title_text="Impact exceedance probability",tickformat=".2%", row=1, col=1)

        uncertainty_fig.update_xaxes(tickformat=".2%", row=1, col=2)


        uncertainty_fig.update_layout(title={
                                'text': title},
                                autosize=False,
                                width=1000,
                                height=750,
                                margin=dict(
                                    l=50,
                                    r=50,
                                    b=50,
                                    t=100,
                                    pad=4
                                ))
        uncertainty_fig.show()
