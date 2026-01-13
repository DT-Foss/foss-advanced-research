# Causal Knowledge Graph (Bayesian Networks)

> **Status:** Reference Implementation (Simulation Only)
> **Formalism:** Judea Pearl's do-calculus / Directed Acyclic Graphs (DAG)

## Overview
This module moves beyond correlation to model **Causality**. It constructs a **Bayesian Belief Network** to predict the downstream probability of a cyber breach based on upstream root causes (e.g., Unpatched CVEs). This allows for counterfactual reasoning ("What if we patched the server?").

## Scientific Core
The joint probability distribution is factorized over the DAG:

$$
P(X_1, ..., X_n) = \prod_{i=1}^{n} P(X_i | Parents(X_i))
$$

Interventions are modeled using the **do-operator**:

$$
P(Y | do(X=x)) \neq P(Y | X=x)
$$

## Visualization
The [causal_dag.png](./causal_dag.png) flow diagram illustrates how probabilities propagate through the attack chain, identifying `Privilege_Escalation` as the critical chokepoint.

## Usage
```bash
python causal_inference.py
```
