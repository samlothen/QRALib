# minimal_qralib_test.py
# Minimal example to verify QRALib works with your existing files
from QRALib.risk.portfolio import RiskPortfolio
from QRALib.utils.importer import RiskDataImporter
from QRALib.pipeline import QRAPipeline
from QRALib.api import run_full_qra

# Replace with your actual file paths
data_file = "./test_data_18.csv"

# 1. Import risks and build a portfolio
risks = RiskDataImporter.import_risks(data_file)
portfolio = RiskPortfolio(risks)
print("Loaded risk IDs:", portfolio.ids())

# 2. Run a simulation step-by-step
pipeline = QRAPipeline(data_file, method="smc", iterations=10000)
results = pipeline.run_simulation()
print("Simulation summary:", results["summary"])

# 3. Use the one-line API for full analysis and single-risk output
full_results = run_full_qra(
    data_file,
    method="smc",
    iterations=5000,
    single_risk_idx=0
)
print("Full pipeline output keys:", full_results.keys())
