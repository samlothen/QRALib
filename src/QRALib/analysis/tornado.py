import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statistics import mean 


class Tornado:

    def __init__(self, risk_results):
        single_risk_impact_data, frequency_data = self._set_ale_stats(risk_results)
        total_impact_data = self._set_stats(risk_results,"total")
        
        self.tornado_parameters = {
            "single_risk_impact" : single_risk_impact_data,
            "frequency" : frequency_data,
            "total": total_impact_data
        }

    def draw_ale(self): 
        self._draw("single_risk_impact")  
        self._draw("frequency")  

    def draw_total(self): 
        self._draw("total")  

    def _set_stats(self, risk_results, attribute):
        assert attribute in ['single_risk_impact', 'frequency', 'total']
        percentile_95 = []
        percentile_5 = []
        mean_value = []
        risk_id = []
        
        for i in range(len(risk_results["results"])):
            risk_id.append(risk_results["results"][i]["id"])
            mean_value.append(mean(risk_results["results"][i][attribute]))
            percentile_95.append(
                np.percentile(risk_results["results"][i][attribute], 95))
            percentile_5.append(
                np.percentile(risk_results["results"][i][attribute], 5))


        negative_variation = []
        positive_variation = []
        mean_sum = sum(mean_value)
        for i in range(0,len(mean_value),1):
            negative_variation.append((
                sum(mean_value[:i])+percentile_5[i]+sum(mean_value[i+1:]))-mean_sum)
            positive_variation.append((
                sum(mean_value[:i])+percentile_95[i]+sum(mean_value[i+1:]))-mean_sum)

        data = self._sorter(positive_variation, negative_variation, risk_id)
        return data

    def _set_ale_stats(self, risk_results):
        
 
        single_risk_impact_percentile_95 = []
        single_risk_impact_percentile_5 = []
        single_risk_impact_mean_value = []
        
        frequency_percentile_95 = []
        frequency_percentile_5 = []
        frequency_mean_value = []

        mean_value = []
        
        risk_id = []
        
        for i in range(len(risk_results["results"])):
            risk_id.append(risk_results["results"][i]["id"])
            single_risk_impact_mean_value.append(
                mean(risk_results["results"][i]["single_risk_impact"]))
            single_risk_impact_percentile_95.append(
                np.percentile(risk_results["results"][i]["single_risk_impact"], 95))
            single_risk_impact_percentile_5.append(
                np.percentile(risk_results["results"][i]["single_risk_impact"], 5))
            frequency_mean_value.append(
                mean(risk_results["results"][i]["frequency"]))
            frequency_percentile_95.append(
                np.percentile(risk_results["results"][i]["frequency"], 95))
            frequency_percentile_5.append(
                np.percentile(risk_results["results"][i]["frequency"], 5))
            mean_value.append(
                mean(risk_results["results"][i]["single_risk_impact"]*risk_results["results"][i]["frequency"]))

        single_risk_impact_negative_variation = []
        single_risk_impact_positive_variation = []
        
        frequency_negative_variation = []
        frequency_positive_variation = []

        mean_sum = sum(mean_value)

        for i in range(0,len(mean_value),1):
            single_risk_impact_negative_variation.append(
                (sum(mean_value[:i])
                +(single_risk_impact_percentile_5[i]*frequency_mean_value[i])
                +sum(mean_value[i+1:]))
                -mean_sum)
            single_risk_impact_positive_variation.append(
                (sum(mean_value[:i])
                +(single_risk_impact_percentile_95[i]*frequency_mean_value[i])
                +sum(mean_value[i+1:]))
                -mean_sum)
            frequency_negative_variation.append(
                (sum(mean_value[:i])
                +(single_risk_impact_mean_value[i]*frequency_percentile_5[i])
                +sum(mean_value[i+1:]))
                -mean_sum)
            frequency_positive_variation.append(
                (sum(mean_value[:i])
                +(single_risk_impact_mean_value[i]*frequency_percentile_95[i])
                +sum(mean_value[i+1:]))
                -mean_sum)            
        
        single_risk_impact_data = self._sorter(single_risk_impact_positive_variation, single_risk_impact_negative_variation, risk_id)
        frequency_data = self._sorter(frequency_positive_variation, frequency_negative_variation, risk_id)

        return single_risk_impact_data, frequency_data

    def _sorter(self, positive_variation, negative_variation, risk_id):
        index = 0
        for pos_value,neg_value in zip(positive_variation, negative_variation):
            if pos_value < neg_value:
               negative_variation[index] = pos_value
               positive_variation[index] = 0
            elif neg_value > pos_value:
                positive_variation[index] = neg_value
                negative_variation[index] = 0
            elif pos_value < 0:
                positive_variation[index] = 0
            elif neg_value > 0:
                negative_variation[index] = 0
            index += 1

        absolute_difference = []
        for pos_value,neg_value in zip(positive_variation, negative_variation):
            absolute_difference.append(pos_value-neg_value)

        data = {"risk_ids": risk_id,
        "negative_variation": negative_variation,
        "positive_variation": positive_variation,
        "absolute_difference": absolute_difference}

        risk_id_sorted = np.array([data["risk_ids"][x] for x in np.argsort(data["absolute_difference"])])
        negative_variation_sorted = np.array([data["negative_variation"][x] for x in np.argsort(data["absolute_difference"])])
        positive_variation_sorted = np.array([data["positive_variation"][x] for x in np.argsort(data["absolute_difference"])])

        return_data = {
            "id" : risk_id_sorted,
            "negative_variation": negative_variation_sorted,
            "positive_variation": positive_variation_sorted
        }
        return return_data


    
    
    def _draw(self, attribute):
        assert attribute in ['single_risk_impact', 'frequency', 'total']

        fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                            shared_yaxes=True, vertical_spacing=0,horizontal_spacing = 0 )
        
        fig.append_trace(go.Bar(
            x=self.tornado_parameters[attribute]["negative_variation"],
            y=self.tornado_parameters[attribute]["id"],
            name='Negative variation',
            orientation='h',
        ), 1, 1)                
        fig.append_trace(go.Bar(
            x=self.tornado_parameters[attribute]["positive_variation"],
            y=self.tornado_parameters[attribute]["id"],
            name='Positive variation',
            orientation='h',
        ), 1, 2)
        fig.update_layout(
            title=attribute,
            legend_title="Legend ",)       

        fig.show()