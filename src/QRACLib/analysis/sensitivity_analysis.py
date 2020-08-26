import numpy as np
from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.analyze import morris 
from SALib.sample.morris import sample as morris_sample
from tabulate import tabulate

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

        Si = morris.analyze(self.problem, param_values, Y, conf_level=0.95, print_to_console=True, num_levels=4, num_resamples=100)


        self._horizontal_bar_plot(Si, {}, sortby='mu_star', unit=r"ALE")

        return Si

    
    def sobol(self, number_of_samples: int):
        param_values = saltelli.sample(self.problem, number_of_samples, calc_second_order=False)
        Y = np.empty([param_values.shape[0]])
        total_outcome = []

        for i in range(0,len(self.equation),2):
            total_outcome.append((self.equation[i](param_values[:,i])*self.equation[i+1](param_values[:,i+1])))

        Y = np.sum(total_outcome, axis=0)

        Si = sobol.analyze(self.problem, Y, calc_second_order=False,print_to_console=False)
        
        headers_list=['Parameter', 'S1', 'S1_conf', 'ST', 'ST_Conf']
        tabs = []
        for i in range(len(self.problem["names"])):
            tabs.append([self.problem["names"][i],round(Si["S1"][i], 4), round(Si["S1_conf"][i], 4), round(Si["ST"][i], 4), round(Si["ST_conf"][i], 4)])
        print(tabulate(tabs,headers=headers_list))

        return Si


    def _horizontal_bar_plot(self, Si, param_dict, sortby='mu_star', unit=''):

        import plotly.graph_objects as go
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
