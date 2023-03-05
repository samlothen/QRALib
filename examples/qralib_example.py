"""Example usage of QRALib"""
from QRALib.riskportfolio import RiskPortfolio  as Risks
from QRALib.simulation.smc import MonteCarloSimulation as smc
from QRALib.simulation.qmc import QuasiMonteCarlo as qmc
from QRALib.simulation.rmc import RandomQuasiMonteCarlo as rqmc
from QRALib.analysis.mariq import MaRiQ as mariq
from QRALib.analysis.sensitivity_analysis import SensitivityAnalysis as sensitivity_analysis
from QRALib.analysis.tornado import Tornado as tornado
from QRALib.utils.importer import RiskDataImporter as importer
from QRALib.analysis.single_risk_analysis import SingleRiskAnalysis as sra



number_of_iterations = 100000
#inp_json = "./example.json"
#inp_csv = "./test_data_600.csv"
inp_xlsx = "./test_data_18.xlsx"

tolerance = ([0, 600000, 1000000, 1500000, 3000000], [100, 90, 50, 20, 0])

# Import data 

#risk_dictionary = importer.import_json(inp_json)
#risk_dictionary = importer.import_csv(inp_csv)
risk_dictionary = importer.import_excel(inp_xlsx)

# Setup the risk_list
risk_list = Risks(risk_dictionary)


# Simulate 
simulation = smc(risk_list)
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
# Sobol Convergence properties of the Sobol' sequence is only valid if
# `N` is equal to `2^n`.
sa.sobol(1024)

# Single Risk Analysis
sra_ = sra(risk_results)
sra_.single_risk_analysis(1)

# Tornado 
ta = tornado(risk_results)
ta.draw_total()
ta.draw_ale()

print("DONE")
