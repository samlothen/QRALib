from QRALib.api                import simulate, compute_morris, compute_sobol
from QRALib.utils.importer     import RiskDataImporter
from QRALib.viz.sensitivity_analysis    import plot_morris, plot_sobol

# 1) Load your risks & simulate
risks = RiskDataImporter.import_risks("/Users/sam/projects/QRALib/examples/test_data_18.csv")
sim   = simulate(risks, method="smc", iterations=10000)

# 2) Compute sensitivity indices
si_morris = compute_morris(risks, N=1000, num_levels=4)
si_sobol  = compute_sobol( risks, N=1024)

# 3) Plot them
fig_morris = plot_morris(si_morris, top_n=10)
fig_sobol  = plot_sobol(si_sobol,  top_n=10)

fig_morris.show()
fig_sobol.show()
