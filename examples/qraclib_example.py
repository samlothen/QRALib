"""Example usage of QRACLib"""
from QRACLib.riskportfolio import RiskPortfolio as Risks
from QRACLib.simulation.mcs import MonteCarloSimulation as mcs
from QRACLib.simulation.qmc import QuasiMonteCarlo as qmc
from QRACLib.simulation.rqmc import RandomQuasiMonteCarlo as rqmc
from QRACLib.analysis.mariq import MaRiQ as mariq
from QRACLib.analysis.sensitivity_analysis import SensitivityAnalysis as sensitivity_analysis
from QRACLib.analysis.tornado import Tornado as tornado
from QRACLib.utils.importer import import_csv, import_json
from QRACLib.analysis.single_risk_analysis import SingleRiskAnalysis as sra



number_of_iterations = 10000
inp_json = "../example_data/example.json"
#inp_csv = "../example_datadata_test2.csv"

tolerance = ([0, 600000, 1000000, 1500000, 3000000], [100, 90, 50, 20, 0])

# Import data 

risk_dictionary = import_json(inp_json)
#risk_dictionary = import_csv(inp_csv)

# Setup the risk_list
risk_list = Risks(risk_dictionary)


# Simulate 
simulation = mcs(risk_list)
#simulation = qmc(risk_list)
#simulation = rqmc(risk_list)

risk_results = simulation.simulation(number_of_iterations)

# Analysis 
analysis = mariq(risk_results, tolerance)
analysis.total_risk_analysis()
analysis.single_risk_analysis()

# Sensitivity Analysis
sa = sensitivity_analysis(risk_list)
sa.morris(1000)
sa.sobol(1000)

# Single Risk Analysis
sra_ = sra(risk_results)
sra_.single_risk_analysis(1)

# Tornado 
ta = tornado(risk_results)
ta.draw_total()
ta.draw_ale()

print("DONE")
