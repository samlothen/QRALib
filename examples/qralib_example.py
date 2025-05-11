# minimal_qralib_test.py
# Minimal example to verify QRALib works with your existing files

from QRALib.risk.portfolio import RiskPortfolio
from QRALib.utils.importer import RiskDataImporter
from QRALib.api import simulate, SimulationResults
import json
# Replace with your actual file path
data_file = "./test_data_18.csv"

# 1. Import risks and build a portfolio
risks = RiskDataImporter.import_risks(data_file)
portfolio = RiskPortfolio(risks)
print("Loaded risk IDs:", portfolio.ids())

# 2. Run a simulation step-by-step via the new simulate() API
sim = simulate(data_file, method="smc", iterations=10000)
payload = sim.to_json()   # no more AttributeError
json_str = json.dumps(payload)
with open("simulation_results.json", "w") as f:
    json.dump(payload, f)
sim2 = SimulationResults.from_json(payload)
print(sim2.results.keys())  # should be the risk IDs
# You can also access the raw arrays:
# print("First risk outcomes:", sim.results[portfolio.ids()[0]]["total"])

# 3. Use the one-line API for full analysis
#full = run_full_qra(
#    data_file,
#    method="smc",
#    iterations=5000,
#    single_risk_idx=0
#)
## full is also a SimulationResults
#print("Full pipeline summary:", full.summary)
#print("Per-risk result keys for first risk:", list(full.results[portfolio.ids()[0]].keys()))
