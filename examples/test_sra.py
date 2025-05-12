from QRALib.api                 import simulate, compute_single_risk
from QRALib.utils.importer      import RiskDataImporter
from QRALib.viz.single_risk_analysis     import plot_single_risk

# load & simulate
risks = RiskDataImporter.import_risks("/Users/sam/projects/QRALib/examples/test_data_18.csv")
sim   = simulate(risks, method="smc", iterations=10000)

# compute & plot for one risk
out = compute_single_risk(sim, risk_id=risks[0].uniq_id, num_bins=200)
fig = plot_single_risk(out["stats"], out["exceedance"])
fig.show()
