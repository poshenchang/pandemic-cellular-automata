# Pandemic Cellular Automata Simulation

> [!WARNING]
> TODO:
>   * Mathematical formulation:
>       * Virus transmission rate as a function of neighboring cells.
>       * Antibody decay or reinforcement over time.
>   * Algorithm design:
>       * Cellular state update rules.
>       * Stochastic transitions.

## Introduction

<!-- Importance of simulating disease dynamics during pandemics. -->

<!-- Brief description of PCA and the SEIR model. -->

## Focus and Features

* Probabilistic Automata
* Interaction within neighborhoods
* Effectiveness of control measures (e.g. quaratine strategies)
* Heterogeneous populations: variation of attributes for individuals (e.g. vulnerability, degree of contact)
* Integration of virus and antibody values per cell.


## Objectives

* Exploring the impact of diverse attributes on disease dynamics.
* Testing hybrid control measures (e.g., selective quarantine + vaccination).


## SEIR Model

$n_S, n_E, n_I, n_R$ denotes the population of susceptible, exposed, infected, and removed respectively. 

* $S\to E$: $p_e(n_E + n_I)$. 
* $E\to I$: $p_i$.
* $I\to R$: $p_r$. 

## Evaluation and Validation

* Benchmarks against real-world data (e.g., COVID-19 spread curves)
* Comparisons with existing PCA models

## Implementation

Python 3.12.7

Each cell is treated as a target, and has two attributes: amount of virus `virus_val`, and amount of antibodies `antibody_val`.

The rate of change of the amount of virus depends on the amount of virus of neighboring cells (including the cell itself), and the amount of antibody of the cell itself. 

## Impact and Contributions

* Potential policy implications
* Open-source release for researchers and policymakers.

## Refrences

###  [Computational Model on COVID-19 Pandemic Using Probabilistic Cellular Automata](https://link.springer.com/article/10.1007/s42979-021-00619-3)

Uses a probabilistic cellular automata (PCA) model on a two-dimensional lattice, provides an epidemiological framework with five subpopulations: susceptible, exposed, infected, quarantined, and recovered. The model captures disease spread by analyzing interactions within neighborhoods, simulating scenarios such as infection rates and quarantining strategies. Helps understanding the dynamics of COVID-19 and the effectiveness of control measures. 

