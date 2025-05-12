from QRALib.api           import simulate, compute_tornado
from QRALib.utils.importer      import RiskDataImporter
from QRALib.viz.tornado   import plot_tornado, plot_ale_variation

# load & simulate
risks = RiskDataImporter.import_risks("/Users/sam/projects/QRALib/examples/test_data_18.csv")
sim = simulate(risks, method="smc", iterations=10000)

# single-attribute tornado
data_total = compute_tornado(sim, "total")
fig = plot_tornado(data_total, "total")
fig.show()

# two-panel ALE variation
data_impact = compute_tornado(sim, "single_risk_impact")
data_freq   = compute_tornado(sim, "frequency")
fig2 = plot_ale_variation(data_impact, data_freq)
fig2.show()
