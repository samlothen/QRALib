# Quantitative Risk Analysis in Cybersecurity Library (QRACLib)

Python implementations to perform quantitative risk analysis. The library allos an analyst to represent risks with various statistical distribtuions, to simulate the risks using Monte Carlo methods, to analyze the results and preform sensitivity analysis on the input. 

## Layout
The library has been designed to allow for flexibility for the analyst to use distirbtuions, simulations and analysis as needed. 

## Distributions supported
- Uniform 
- Lognormal 
- Beta 
- PERT

Recommended usage: 

| Distribution | Frequency | Impact | 
|---|:---:|:---:|
|Uniform | X | |
|Lognormal | | X |
|Beta| X | |
|PERT| X | X |

## Simulation methods 
- Standard Monte Carlo Simulation 
- Quasi Monte Carlo using shuffled Sobol sequence 
- Random Quasi Monte Carlo using scrambled Sobol sequence 

Each simulation method takes a list of risks as input to create the class object. Number of iterations are provided per simulation to allow the analyst to run multiple simulations with diffrent number of iterations. 



### Results
The simulation returns a nested dictionary that contains a summary of the simulation and results for each risk. 

The summary states the number of iterations and the risk list used.

The results is a list of dictionaries. Each risk has:
- Its ID
- frequency: A list of the frequencies from the simulation
- occurances: the result of passing the frequency array to the poisson distribtuion (this is the number of times the risk occured in a given simulation year)
- impact: A list of the impacts from the riks impact distribtuion, it contains the impact for the sum of all occurances 
- single_risk_impact: A list of impacts, one for each simulation year. This is used to calculate the ALE in certain analysis methods (multiplying frequency and impact)
- total: A list of the impact per simulated year. Each entry is the sum of the number of impacts from that simulation. The number of impacts is based on the 'occurances'

```
simulation_result = {
            "summary":{
                "number_of_iterations": 10000,
                "risk_list": <Class Object>,
            },
            "results":{
                "id" : 'R254',
                "frequency" : [0.434, 0.123, 0.0678, 0.33],
                "occurances" : [2, 0, 1, 0],
                "impact" : [4502, 9543, 23895, 10235],
                "single_risk_impact": [8041, 7422, 98723, 3212],
                "total" : [14045 , 0, 23895, 0]
                }
        }     
```

## Analysis 
- MaRiQ
- Single Risk Analysis 

### MaRiQ 
The MaRiQ model has been implmented as an example of analysis that can be done. MaRiQ provides to analysis modes; Total Risks and Single Risk. 

- Total Risks plots a impact exceedance graph to visualizes the combined risk impact. This graph shows the probability of a the total risk outcome exceeding a certain values. 
- Single Risk produces two plots and two lists:
    - A list called "Estimated risks" that shows all risks and calculated mean expected loss
    - A list called "Top 10 Risks" a sorted list of the ten risks with the highest computed mean expected loss
    - A 'Heatmap' that plots he mean likelihood and mean impact of the risks 
    - A boxplot called "Uncertainty" that plots the "impact" of the risks 


Source: [The MaRiQ model: A quantitative approach to risk management](http://uu.diva-portal.org/smash/record.jsf?pid=diva2%3A1323684&dswid=8165)

### Single Risk Analysis 


### Sensitivity Analysis 
- Sobol's indices 
- Method of Morris 
- Tornado Chart


## Example usage 
The library provides the functionality for an analyst to import, simualte and analyse data. The analyst has to combine the neccesary parts.

Steps:
1. Import neccessary classes from the library 
2. Setup parameters, 'number of iterations' is always needed
    - In this example 'risk_tolerance' is added for the MaRiQ analysis 
3. Import the data, either from JSON or CSV, the generate the list of risks to simulate
4. Run simulation
5. Run analysis 
6. Run sensitivity analysis
``` 
from QRACLib.riskportfolio import RiskPortfolio as Risks
from QRACLib.simulation.mcs import MonteCarloSimulation as mcs
from QRACLib.analysis.mariq import MaRiQ as mariq
from QRACLib.analysis.sa import SensitivityAnalysis as sensitivity_analysis
from QRACLib.utils.importer import Importer as importer

# Setup parameters
number_of_iterations = 10000
risk_tolerance = ([0, 600000, 1000000, 1500000, 3000000], [100, 90, 50, 20, 0])

# Import data
risk_dictionary = importer.import_csv(inp_csv)
risk_list = Risks(risk_dictionary)

# Run simulation
simulation = mcs(risk_list)
risk_results = simulation.simulation(number_of_iterations)

# Run analysis 
analysis = mariq(risk_results1, tolerance)
analysis.total_risk_analysis()
analysis.single_risk_analysis()

# Run sensitivity analysis 
sa = sensitivity_analysis(risk_list)
morris = sa.impact_morris(1000)
``` 