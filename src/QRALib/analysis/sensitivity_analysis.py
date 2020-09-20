import numpy as np
from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.analyze import morris 
from SALib.sample.morris import sample as morris_sample
import plotly.graph_objects as go

class SensitivityAnalysis:

    def __init__(self, risk_list):

        self.names = []
        for risk in risk_list.listing():
            self.names.append(risk.uniq_id+"_frequency") 
            self.names.append(risk.uniq_id+"_impact") 
        
        self.num_vars = len(self.names)

        dists = np.repeat("unif", self.num_vars)
        self.dists = dists.tolist()

        bounds = np.repeat(np.array([0, 0.9999])[None, :], self.num_vars, axis=0)
        self.bounds = bounds.tolist()

        self.problem = {
            "num_vars": self.num_vars, 
            "names": self.names, 
            "dists": self.dists,
            "bounds": self.bounds
        }  
        self.equation = []

        for risk in risk_list.listing():
            self.equation.append(risk.get_frequency_ppf)
            self.equation.append(risk.get_impact_ppf)

    def morris(self, number_of_samples: int):
        param_values = morris_sample(self.problem, N=number_of_samples, num_levels=4, optimal_trajectories=None)
        Y = np.empty([param_values.shape[0]])
        total_outcome = []

        for i in range(0,len(self.equation),2):
            total_outcome.append((self.equation[i](param_values[:,i])*self.equation[i+1](param_values[:,i+1])))

        Y = np.sum(total_outcome, axis=0)

        Si = morris.analyze(self.problem, param_values, Y, conf_level=0.95, print_to_console=False, num_levels=4, num_resamples=100)
        
        names_sorted = self._sort_Si(Si, 'names', 'mu_star')[::-1]
        mu_star_sorted = np.round(self._sort_Si(Si, 'mu_star', 'mu_star')[::-1], 4)
        mu_star_conf_sorted = np.round(self._sort_Si(Si, 'mu_star_conf', 'mu_star')[::-1], 4)
        sigma_sorted = np.round(self._sort_Si(Si, 'mu_star_conf', 'mu_star')[::-1], 4)

        headers_list=['Parameter', 'mu_star', 'mu_star_conf', 'sigma']

        fig = go.Figure(data=[go.Table(header=dict(values=headers_list,align='left'),
                 cells=dict(values=[names_sorted, mu_star_sorted, mu_star_conf_sorted, sigma_sorted],align='left'))
                     ])
        fig.update_layout(title={
                        'text': "Sensitivity Analysis Morris Method - Sorted after mu_star"},
                        autosize=False,
                        width=750,
                        height=350,
                        margin=dict(
                            l=10,
                            r=10,
                            b=10,
                            t=100,
                            pad=4
                        ))
        fig.show()

        #self._horizontal_bar_plot(Si, {}, sortby='mu_star', unit=r"ALE")

        #return Si

    
    def sobol(self, number_of_samples: int):
        param_values = saltelli.sample(self.problem, number_of_samples, calc_second_order=False)
        Y = np.empty([param_values.shape[0]])
        total_outcome = []

        for i in range(0,len(self.equation),2):
            total_outcome.append((self.equation[i](param_values[:,i])*self.equation[i+1](param_values[:,i+1])))

        Y = np.sum(total_outcome, axis=0)

        Si = sobol.analyze(self.problem, Y, calc_second_order=False,print_to_console=False)
        Si["names"] = self.problem["names"]

        headers_list=['Parameter', 'S1', 'S1_conf', 'ST', 'ST_conf']

        names_sorted = self._sort_Si(Si, 'names', 'S1')[::-1]
        S1_sorted = np.round(self._sort_Si(Si, 'S1', 'S1')[::-1], 4)
        S1_conf_sorted = np.round(self._sort_Si(Si, 'S1_conf', 'S1')[::-1], 4)
        ST_sorted = np.round(self._sort_Si(Si, 'ST', 'S1')[::-1], 4)
        ST_conf_sorted = np.round(self._sort_Si(Si, 'ST_conf', 'S1')[::-1], 4)

        fig = go.Figure(data=[go.Table(header=dict(values=headers_list,align='left'),
                 cells=dict(values=[names_sorted, S1_sorted, S1_conf_sorted, ST_sorted, ST_conf_sorted],align='left'))
                     ])
        fig.update_layout(title={
                        'text': "Sobols' Idicies for ALE - Sorted after S1"},
                        autosize=False,
                        width=750,
                        height=350,
                        margin=dict(
                            l=10,
                            r=10,
                            b=10,
                            t=100,
                            pad=4
                        ))
        fig.show()



        #return Si


    def _horizontal_bar_plot(self, Si, param_dict, sortby='mu_star', unit=''):


        assert sortby in ['mu_star', 'mu_star_conf', 'sigma', 'mu']

        # Sort all the plotted elements by mu_star (or optionally another
        # metric)
        names_sorted = self._sort_Si(Si, 'names', sortby)
        mu_star_sorted = self._sort_Si(Si, 'mu_star', sortby)
        mu_star_conf_sorted = self._sort_Si(Si, 'mu_star_conf', sortby)

        # Plot horizontal barchart
        y_pos = np.arange(len(mu_star_sorted))
        plot_names = names_sorted

        #ax.set_ylim(min(y_pos)-1, max(y_pos)+1)
        fig = go.Figure(go.Bar(
            x=mu_star_conf_sorted,
            y=y_pos,
            text=plot_names,
            orientation='h'))

        fig.show()

    
    def _sort_Si(self, Si, key, sortby='mu_star'):
        return np.array([Si[key][x] for x in np.argsort(Si[sortby])])
