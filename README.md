# Pandemic Cellular Automata Simulation

> [!WARNING]
> TODO:
>   * References, including PCA and viral propagation
>   * Real world data regarding pandemic (e.g. COVID-19)
>   * 1-minute video
>       * Introduction
>       * Importance
>       * Matehmatical model
>       * Demo/Data visualization
>       * Data fitting

## Introduction

* Importance of simulating disease dynamics during pandemics.
* Brief description of PCA and the SEIR model.

## Program Installation and Usage

Prerequisites include *Python v.3.12.7* and *Numpy v.2.1.1*.

1. Clone the repository
2. `cd` into the directory

```bash
cd pandemic-cellular-automata
```
3. Type the following command to display the help message (to see what options are available)

```bash
python cellsim.py -h
```
4. Run program with desired options
```bash
python cellsim.py [options]
```

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

Each cell is treated as a target, and has two attributes: amount of virus `virus_val`, and amount of antibodies `antibody_val`.

The rate of change of the amount of virus depends on the amount of virus of neighboring cells (including the cell itself), and the amount of antibody of the cell itself. 

For the following discussion, let $V_i$ and $A_i$ denote the value of virus and antibody of cell $i$.

### Linear Model

The virus count in a cell depends on the virus concentration in neighboring cells:

$$
\frac{dV_i}{dt} = \alpha\sum_j k_{ij}V_j - \beta V_iA_i
$$

* $k_ij$ denotes the transmission rate from cell $j$ to cell $i$, and $\alpha$ denotes the replication rate of the virus
* $\mu$ denotes the rate of antibodies eliminating the virus

$$
\frac{dA_i}{dt} = \gamma V_i - \delta A_i
$$

* $\gamma$ denotes the rate of growth of antibodies stimulated by virus
* $\delta$ denotes the natural decay rate of antibodies

### Saturation Model

In saturation model, we introduce the saturation parameter $s$, which represents the capacity of the immune system to produce antibodies.

$$
\frac{dA_i}{dt} = \frac{\gamma V_i}{1 + sV_i} - \delta A_i
$$

### Heterogeneous Population and Fluctuation

To simulate variation in attributes of individual cells, when each cell is initialized, the parameters $\alpha, \beta, \gamma, \delta$ are sampled from log-normal distributions. 

To simulate randomness in virus and antibody production, for each step, the rate of changes $dV/dt$ and $dA/dt$ are scaled by random factors, which are sampled from a log-normal distribution with median $1$. 

## Results

![sample_image](./images/point25var_0.png)

*Sample image generated with default parameters and seed 0*

![sample_animation](./images/point25var_0.gif)

*Sample heatmap animation generated with default parameters and seed 0*

## Impact and Contributions

* Potential policy implications
* Open-source release for researchers and policymakers.

## Refrences

*  [Computational Model on COVID-19 Pandemic Using Probabilistic Cellular Automata](https://link.springer.com/article/10.1007/s42979-021-00619-3)

Uses a probabilistic cellular automata (PCA) model on a two-dimensional lattice, provides an epidemiological framework with five subpopulations: susceptible, exposed, infected, quarantined, and recovered. The model captures disease spread by analyzing interactions within neighborhoods, simulating scenarios such as infection rates and quarantining strategies. Helps understanding the dynamics of COVID-19 and the effectiveness of control measures. 

* [Cellular automata in the light of COVID-19](https://link.springer.com/article/10.1140/epjs/s11734-022-00619-1#Tab3)

Currently, the world has been facing the brunt of a pandemic due to a disease called COVID-19 for the last 2 years. To study the spread of such infectious diseases it is important to not only understand their temporal evolution but also the spatial evolution. In this work, the spread of this disease has been studied with a cellular automata (CA) model to find the temporal and the spatial behavior of it. Here, we have proposed a neighborhood criteria which will help us to measure the social confinement at the time of the disease spread. The two main parameters of our model are (i) disease transmission probability (q) which helps us to measure the infectivity of a disease and (ii) exponent (n) which helps us to measure the degree of the social confinement. Here, we have studied various spatial growths of the disease by simulating this CA model. Finally we have tried to fit our model with the COVID-19 data of India for various waves and have attempted to match our model predictions with regards to each wave to see how the different parameters vary with respect to infectivity and restrictions in social interaction.

* [COVID-19 India data source](covid19india.org)

* [地區年齡性別統計表-嚴重特殊傳染性肺炎](https://data.gov.tw/dataset/120711)
