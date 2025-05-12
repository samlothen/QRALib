from QRALib.api            import simulate
from QRALib.api            import analyze_mariq
from QRALib.viz.mariq      import plot_total_risk, plot_single_risk
from QRALib.utils.importer import RiskDataImporter
# 1) Run the sim (pass in your list of Risk objects)
#    If you only have a file, first do:
#      from QRALib.utils.importer import RiskDataImporter
risks = RiskDataImporter.import_risks("/Users/sam/projects/QRALib/examples/test_data_18.csv")
#    then:
#      sim = simulate(risks, method="mcs", iterations=10000)

sim = simulate(risks, method="smc", iterations=10000)

# 2) Analyze MaRiQ
tolerance = ([0, 600_000, 1_000_000, 1_500_000], [100, 90, 50, 20])
mariq = analyze_mariq(sim, tolerance)
# mariq is {"total": {...}, "single": {...}}

# 3a) Plot the total‐risk curve
fig_total = plot_total_risk(mariq["total"])
fig_total.show()

# 3b) Plot the single‐risk dashboard
fig_single = plot_single_risk(mariq["single"])
fig_single.show()
