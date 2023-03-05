# Quantitative Risk Analysis in Cybersecurity Library (QRALib)

Python implementations to perform quantitative risk analysis. The
library allows an analyst to represent risks with various statistical
distributions, simulate the risks using Monte Carlo methods, analyze the
results, and perform sensitivity analysis on the input.

## News
Following an increased intereset in quantiataive risk assessements I have decieded to continue develope this project.

I a currently refactoring and updating the original code. I will also update the documentation to better explain how to use it.

I plan to implment new features after the refactoring. I haven't decided what direction to take it. I am considering makeing it application with GUI. Feel free to open up an issue with ideas for features or ways to make this even better.

## Glossary

-   Frequency - This is the frequency a risk occurs (or probability). It
    can be both fractions such as 0.3 or 1.25 or a whole number.
-   Impact - The impact a risk can have.
-   Iteration - During a simulation, each risk is simulated several
    times (usually +10,000 times). Each iteration is a simulated year.
-   Occurrence - The number of times a risk occurs during an iteration;
    it is computed by passing the frequency from a simulation to a
    Poisson function.
-   Single Risk Impact - This is an array of impacts, one per iteration
    used to compute certain values. Single Risk Impact draws the same
    number of impact samples as there are iterations. Differs from Total
    Impact
-   Total Impact - The impact a risk had in the simulations. If a risk
    occurs during an iteration, then the number of occurrences is the
    number of impacts drawn from the distribution and summed up to
    represent the impact for that iteration. The total impact is then an
    array of all these impacts. One iteration can have 0, 1 or more
    occurrences (always a whole number).

## Layout

The library has been designed to allow for flexibility for the analyst
to use distributions, simulations, and analysis as needed.

    QRALib
    ├── Risk Portfolio
    ├── risk
    ├── analysis
    │   ├── MaRiQ
    │   ├── Sensitivity Analysis
    │   ├── Single Risk Analysis
    │   └── Tornado
    ├── distribution
    │   ├── Beta
    │   ├── Lognormal
    │   ├── PERT
    │   └── Uniform
    ├── simulation
    │   ├── Monte Carlo Simulation
    │   ├── Quasi-Monte Carlo Simulation
    │   └── Randomized Quasi-Monte Carlo Simulation
    └── utils
        └── Importer

## Risk and Risk Portfolio

## Distributions supported

-   Uniform
-   Lognormal
-   Beta
-   PERT

Recommended usage:

| Distribution           | Frequency | Impact |
|------------------------|-----------|--------|
| Uniform                | X         |        |
| Lognormal              |           | X      |
| Beta                   | X         |        |
| PERT                   | X         | X      |

Functions provided: - The setup of a class object takes 2 positional
parameters (3 for PERT). Parameters should be greater than 0 and
floats - draw(n) - returns n number of samples from the distribution
-draw_ppf(percentile_sequences) - uses the inverse CDF (PPF) to
calculate variables based on percentile values, the sequence should be a
list of values in the range \[0,1)

### Uniform

Uniform distribution should be used to represent risk frequency when
limited information is available.

The uniform distribution occurs when a random variable is equally likely
to fall between two limits A and B (continues) or equally likely to take
any integer value from A to B (discrete). The distribution is useful
when there is no information on the range and shape of the random
variable.

Uniform distribution takes two parameters 'low' and 'high', which
represents the lower and upper bound with a 90% confidence interval.
I.e., the numbers provided should cover 90% of all cases. The
distribution takes the 'low' and 'high' values and calculates a maximum
and minimum value for the uniform distribution. The 'low' value must be
smaller or equal to high'. Normally uniform distribution is used with
values in the range \[0,1\], but it can handle any values larger than 0.

Note that if the calculation of maximum and minimum values results in a
minimum being less than 0, it will be forced to 0.

### Lognormal

The lognormal distribution is skewed to one end, can not generate a zero
or negative amount, and has a tail. This makes it useful to represent
the probability of loss.

The lognormal distribution takes two parameters 'low' and 'high', which
represents the lower and upper bound with a 90% confidence interval.
I.e., the numbers provided should cover 90% of all cases. The
distribution takes the 'low' and 'high' values and calculates a maximum
and minimum value for the lognormal distribution. The 'low' value must
be smaller or equal to high'.

### Beta

This is the standard beta distribution.

The beta distribution can take on many shapes depending on the value of
alpha and beta when alpha \> 0, beta \> 0. The shapes range from
exponential, reverse exponential, right triangular, left triangular,
skew right, skew left, normal, and bathtub. The Beta distribution is
commonly used in Bayesian problems as it allows for providing a prior
and calculates the posterior.

Assuming we want to assess the probability of a major data breach. It is
possible to start with an uninformed prior where alpha = 1, beta = 1,
which gives a uniform distribution. By providing additional data from
publicly available data such as industry reports of data breaches, it is
possible to update the probability. Alpha can then be viewed as "hits"
or companies breached, whereas beta can be viewed as "misses" or
companies not breached.

### PERT

The Beta-PERT distribution(usually referred to as PERT, an acronym for
Program Evaluation Research Task) was developed by the U.S Navy in the
1950s for the Polaris Weapon Program. The PERT distribution is a
variation of the Beta distribution and is commonly used in project
management and risk analysis.

PERT uses three parameters minimum, mean, and maximum anticipated
values.

## Simulation methods

QRALib implements several simulation methods and is designed to be
extended with new ones.

Currently, three types of Monte Carlo Methods are supported:

-   Standard Monte Carlo Simulation (MCS)
-   Quasi-Monte Carlo using shuffled Sobol sequence (QMC)
-   Random Quasi-Monte Carlo using scrambled Sobol sequence (RQMC)

Each simulation method takes a list of risks as input to create the
class object. The number of iterations is provided per simulation to
allow the analyst to run multiple simulations with a different number of
iterations.

  Simulation method   Recommended number of iterations:

| Simulation method           | Recommended number of iterations |
|------------------------|-----------|
| MCS                | 100 000        |
| QMC              |   10 000        |
| RQMC                   | 10 000        |

### Monte Carlo simulation flow

This applies to all Monte Carlo based simulations.

1.  Draw numbers from a riks frequency distribution, store in r_1
2.  Use r_1 as input to a Poisson distribution and store the result in
    r_2
3.  If r_2 \< 0: Risk did not occur. If r_2 \> 0: Risk occurred r_2
    times that simulation year
4.  Sum up the number of times risks occurred during the simulations
5.  Retrieve sum(r_2) number of impacts from the risks impact
    distribution
6.  Sum the impact for each simulated year
7.  Retrieve additional impact numbers, 1 per simulation iteration to be
    used in analysis such as Annualized loss expectancy (ALE)

### Standard Monte Carlo Simulation (MCS)

Standard Monte Carlo Simulation draws random numbers from each risks
distributions, computes the various results

### Quasi-Monte Carlo using shuffled Sobol sequence (QMC)

Quasi-Monte Carlo uses a low-discrepancy sequence (LDS) instead of
random numbers. In this implementation, a Sobol sequence is used. As the
LDS is deterministic, it is shuffled to vary the order of the numbers.

### Random Quasi-Monte Carlo using scrambled Sobol sequence (RQMC)

Random Quasi-Monte Carlo uses a randomized low-discrepancy sequence
(LDS) instead of random numbers. In this implementation, a scrambled
Sobol sequence is used.

RQMC should, in theory, provide an error rate that is possible to
estimate.

### Simulation Results

The simulation returns a nested dictionary that contains a summary of
the simulation and results for each risk.

The summary states the number of iterations and the risk list used.

The results are a list of dictionaries. Each risk has: - Its ID
-frequency: A list of the frequencies from the simulation - occurrences:
the result of passing the frequency array to the Poisson distribution
(this is the number of times the risk occurred in a given simulation
year) - impact: A list of the impacts from the riks impact distribution,
it contains the impact for the sum of all occurrences
-single_risk_impact: A list of impacts, one for each simulation year.
This is used to calculate the ALE in certain analysis methods
(multiplying frequency and impact) - total: A list of the impact per
simulated year. Each entry is the sum of the number of impacts from that
simulation. The number of impacts is based on the 'occurrences'

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

## Analysis

-   MaRiQ
-   Single Risk Analysis

### MaRiQ

The MaRiQ model has been implemented as an example of analysis that can
be done. MaRiQ provides two analysis modes; Total Risks and Single Risk.

-   Total Risks plots an impact exceedance graph to visualizes the
    combined risk impact. This graph shows the probability of the total
    risk outcome exceeding certain values.
-   Single risk produces two plots and two lists:
    -   A list called "Estimated risks" that shows all risks and
        calculated mean expected loss
    -   A list called "Top 10 Risks" a sorted list of the ten risks with
        the highest computed mean expected loss
    -   A 'Heatmap' that plots he mean likelihood and mean the impact of
        the risks
    -   A boxplot called "Uncertainty" that plots the "impact" of the
        risks

Source: [The MaRiQ model: A quantitative approach to risk
management](http://uu.diva-portal.org/smash/record.jsf?pid=diva2%3A1323684&dswid=8165)

### Single Risk Analysis

The Single Risk Analysis (SRA) function helps the analyst dive into a
single risk and understand its distribution and result.

Setup the SRA by providing the simulation results dictionary from the
simulation method used.

Usage: call the object and function with the number of the risk that is
being analyzed.

The function returns: - a table with the minimum, 5th percentile, mean,
95th percentile and max value for impact and frequency. - Boxplot of the
frequency and impact - An impact exceedance curve for the total risk
impact

## Sensitivity Analysis

Sensitivity analysis can determine which input variables affect the
output the most or verify interaction effects within the model. This can
help to understand and verify the model or simplify and prioritize
factors that affect the model the least and most, respectively.

QRALib implements three different Sensitivity Analysis methods: 
- Tornado Chart 
- Method of Morris 
- Sobol's indices

### Tornado Chart

The Tornado Chart uses a One-at-a-time (OAT) Sampling method. It goes
through each risk and calculates the impact each risk has to the average
by changing between the 5th percentile value and 95th percentile value.
The result is calculated and presented in a Tornado chart with the risk
that has the highest impact on top. The left and right bars show the
positive and negative impact it has. Using this shows which risk has the
most variation in its impact.

The Tornado Chart can be used to look at the variation each risk has on
the total impact and also see the variation of each risk frequency and
single risk impact on the ALE.

### Method of Morris

The method of Morris is an OAT method developed in 1991 by Max D.
Morris. The method uses two sensitivity measures to classify the inputs
in three groups:

-   Inputs having negligible effects
-   Inputs having linear and additive effects without interactions
-   Inputs having non-linear and/or involved in interactions with other
    factors

The implementation takes the number of samples as an input (1000 is
recommended). It outputs a graph and table showing the two measures
mu_star and sigma.

-   mu_star is the measure of the influence of the input on the output.
    A larger mu_star, the more influence the input variable has on the
    output.
-   sigma is the measure of non-linear and/or involved in interaction
    effects. A large sigma would suggest that the variable is non-linear
    in its effect on the output or interacting with at least one other
    variable.

### Sobol's indices

Sobol' indices are a variance-based method that is capable of computing
sensitivity for arbitrary groups of factors. Sobol's method compute
three indices, first-order sensitivity index S_1, second-order
sensitivity index S_2, and total sensitivity index S_T. The current
implementation in QRALib does not implement second-order sensitivity
index S_2.

The first-order index (S_1) shows the effect of each input on the total.
The first-order index is sometimes called 'importance measure' or
'correlation ratio'.

The total sensitivity index (S_T) measures the contribution to the
output variance of Xi, including all variance caused by its
interactions, of any order, with any other input variables.

## Utilities

QRALib provides utilities to help with certain tasks. Currently, it
implements the tools to import data from a CSV or nested JSON.

Examples are provided in the example folder.

## Example usage

The library provides the functionality for an analyst to import,
simulate, and analyze data. The analyst has to combine the necessary
parts.

Steps: 1. Import necessary classes from the library 2. Setup parameters,
'number of iterations' is always needed - In this example,
'risk_tolerance' is added for the MaRiQ analysis 3. Import the data,
either from JSON or CSV, then generate the list of risks to simulate 4.
Run simulation 5. Run analysis 6. Run sensitivity analysis

    from QRALib.riskportfolio import RiskPortfolio as Risks
    from QRALib.simulation.mcs import MonteCarloSimulation as mcs
    from QRALib.analysis.mariq import MaRiQ as mariq
    from QRALib.analysis.sa import SensitivityAnalysis as sensitivity_analysis
    from QRALib.utils.importer import Importer as importer

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
