# MVAD User Manual

**MVAD** (Multi-Variable Axiomatic Design) is a Python project for multi-criteria decision-making (MCDM) using the weighted hierarchical **Axiomatic Design** methodology plus a **Minkowski distance** layer with **Prospect Theory**. The **`MCDMAxiom`** modules and tooling are developed by Adil Baykasoglu and Filiz Senyuzluler.

---

## Table of contents

1. [Introduction](#introduction)
2. [Repository layout](#repository-layout)
3. [Installation](#installation)
4. [How it works](#how-it-works)
5. [Input file formats](#input-file-formats)
6. [Usage](#usage)
7. [Outputs](#outputs)
8. [Worked example (yacht dataset)](#worked-example-yacht-dataset)
9. [Troubleshooting](#troubleshooting)
10. [References](#references)

---

## Introduction

Two complementary evaluation paths are available:

1. **MCDMAxiom (Axiomatic Design)** — Hierarchical weights and **Information Content** (I-value) per alternative; lower I-value means a better fit to stated design ranges and types.
2. **Minkowski–Prospect** — Distances between alternatives and ideal points, combined with Prospect Theory value functions; **CA_Value** (higher is better) ranks acceptable options.

Typical uses include recommendation systems, product or asset selection, and any setting where alternatives are scored on many criteria at once.

---

## Repository layout

```
MVAD/
├── MCDMAxiom/                 # Core package (import as MCDMAxiom)
│   ├── __init__.py
│   ├── axiom.py               # CSV readers, result display
│   ├── calculate.py           # Axiomatic Design I-value pipeline
│   └── weightCalculate.py     # Weight hierarchy and normalization
├── minkowski.py               # Minkowski–Prospect integration
├── prospect.py                # Prospect Theory value functions
├── test.py                    # Demo script (uses test/ yacht sample)
├── test/                      # Sample CSV bundle (marine / yacht scenario)
│   ├── YachtFeatureList.csv
│   ├── YachtEqualWeights.csv
│   ├── YachtDifferentWeights.csv
│   └── YachtDataset.csv
├── lib/                       # Static front-end libraries (optional)
│   ├── tom-select/
│   └── vis-9.0.4/ / vis-9.1.2/
├── requirements.txt
├── setup.py                   # setuptools metadata (egg name differs from folder; see below)
├── build/ / axiomlib.egg-info/  # Generated if you build/install; safe to regenerate
└── README.md                  # This manual
```

**Notes:**

- **`MCDMAxiom`** is the Python package directory you import (`import MCDMAxiom.axiom as ax`). Root-level **`minkowski.py`** / **`prospect.py`** complete the Prospect pipeline.
- **`test/`** currently ships **one end-to-end scenario**: the yacht listing sample (features, weights, alternatives).
- **`lib/`** contains vendored CSS/JS (**vis-network**, **tom-select**). Nothing in **`MCDMAxiom`** imports these; keep them if you attach a browser UI elsewhere.
- **`setup.py`** is named **`axiomlib`** in setuptools metadata while the editable source tree exposes **`MCDMAxiom`**. Prefer running from the project root with dependencies from **`requirements.txt`** unless you align the package name in **`setup.py`** with your install layout.
- **`build/`** and **`axiomlib.egg-info/`** are build outputs; they can be omitted from version control or regenerated.

---

## Installation

**Prerequisites:** Python 3.7+, **pip**.

```bash
pip install -r requirements.txt
```

Pinned versions (see **`requirements.txt`**): **numpy**, **pandas**, **scipy**, **sympy**.

**Verify imports** (run from the **MVAD** project root so **`MCDMAxiom`** is on the path):

```python
import MCDMAxiom.axiom as ax
import MCDMAxiom.calculate as cal
import minkowski
```

---

## How it works

| Piece | Role |
|--------|------|
| **`readCriteria()`** | Loads the feature / design-requirement matrix from CSV. |
| **`readWeights()`** | Loads weights and optional parent–child hierarchy. |
| **`readData()`** | Loads alternatives and infers cell types (singleton, interval, fuzzy, boolean). |
| **`runMCDMAxiom()`** | Computes normalized I-values and returns ranked rows + **`IValue`**. |
| **`Minkowski_Prospect()`** | Runs the Minkowski–Prospect ranking ( **`CA_Value`** ). |
| **`showRecommendationResults()`** | Pretty-prints tabular results (axiom and minkowski modules). |

Weights are normalized; hierarchical weights combine levels as described in the cited literature.

---

## Input file formats

### 1. Features / criteria CSV

**Columns (in order):** `feature_name`, `value`, `fuzziness`, `design_req`, `criteria_type`

| `design_req` | Meaning |
|----------------|---------|
| `CSINGLETON` | Single crisp target |
| `CINTERVAL` | Interval, e.g. `"1000-7500"` |
| `FUZZY` | Fuzzy target; set `fuzziness` (use `-` if not fuzzy) |
| `BOOLEAN` | `Yes`, `No`, or `Both` |

| `criteria_type` | Meaning |
|-----------------|--------|
| `BENEFIT` | Larger attribute values are better |
| `COST` | Smaller is better |
| `TARGET` | Match target / interval as specified by pairing rules in code |

### 2. Weights CSV

**Columns:** `feature_name`, `hierarchy`, `parent`, `weight`

- Top level: `hierarchy` `0`, `parent` `-` (or as your convention allows).
- Sub-criteria: higher `hierarchy`, `parent` set to the parent feature name.
- Weights are relative (e.g. 1–5); the library normalizes them.

### 3. Dataset CSV

- First column: **`ListingID`** (unique id per alternative).
- Remaining columns: one per criterion, **same names and order** as in the features file.

**Cell conventions (aligned with readers in `axiom.py` / `calculate.py`):**

- Numbers: `8`, `12.5`
- Intervals: `"10-20"`
- Fuzzy: `"12+-1"`, forms with parentheses, etc.
- Boolean: `Yes` / `No`

---

## Usage

### Axiomatic Design only

```python
import MCDMAxiom.axiom as ax
import MCDMAxiom.calculate as cal

criteria = ax.readCriteria("test/YachtFeatureList.csv")
weights = ax.readWeights("test/YachtEqualWeights.csv")
data, data_types, cols = ax.readData("test/YachtDataset.csv")

recommendation_list, columns = cal.runMCDMAxiom(
    criteria, weights, data, data_types, cols
)
ax.showRecommendationResults(recommendation_list, columns)
```

### Minkowski–Prospect only

```python
import MCDMAxiom.axiom as ax
import minkowski

criteria = ax.readCriteria("test/YachtFeatureList.csv")
weights = ax.readWeights("test/YachtEqualWeights.csv")
data, data_types, cols = ax.readData("test/YachtDataset.csv")

tam_liste, cols3 = minkowski.Minkowski_Prospect(criteria, data, cols, weights)
minkowski.showRecommendationResults(tam_liste, cols3)
```

### Both methods

```python
import MCDMAxiom.axiom as ax
import MCDMAxiom.calculate as cal
import minkowski

criteria = ax.readCriteria("test/YachtFeatureList.csv")
weights = ax.readWeights("test/YachtDifferentWeights.csv")
data, data_types, cols = ax.readData("test/YachtDataset.csv")

rec, columns = cal.runMCDMAxiom(criteria, weights, data, data_types, cols)
tam_liste, cols3 = minkowski.Minkowski_Prospect(criteria, data, cols, weights)

print("=== Axiomatic Design (I-value) ===")
ax.showRecommendationResults(rec, columns)
print("\n=== Minkowski–Prospect (CA_Value) ===")
minkowski.showRecommendationResults(tam_liste, cols3)
```

Run the bundled demo:

```bash
python test.py
```

([`test.py`](test.py) must point at CSV paths that exist under [`test/`](test/).)

---

## Outputs

### Axiomatic Design

Output rows include original columns plus **`IValue`**.

- Prefer **small** **`IValue`**: very small ≈ excellent fit.
- **`IValue`** = infinity means hard failure on a gated criterion (row may be dropped from the accepted list depending on internals).

Sorting is by **`IValue`** ascending.

### Minkowski–Prospect

Adds **advantage/disadvantage** style columns (**`CA_Value`**, **`CDA_Value`** where applicable).

- **`CA_Value`**: higher is better among feasible alternatives.
- Use together with axiomatic ranks for sensitivity checks.

---

## Worked example (yacht dataset)

The **`test/`** bundle models **motor yacht listing** selection: budgets, hull vintage, cabins, sanitary capacity, hull geometry, tankage, machinery, documented maintenance, and installed equipment (**Radar**, **Jenerator** [filename spelling], **GPS**).

### Criterion overview

| Criterion | Typical role | Notes |
|-----------|----------------|--------|
| **Price** | `CINTERVAL`, `COST` | Prefer lower price inside bracket. |
| **Year** | `CINTERVAL`, `TARGET` | Model years of interest; outside range penalized strongly. |
| **Cabins**, **WC**, **Length**, **Deepness**, **Width**, **Weight**, **WaterTank**, **FuelTank**, **MotorPower** | Mostly benefit / fuzzy / intervals | Matches listings with singletons, intervals, or fuzzy cells. |
| **MotorHour** | `COST` | Prefer lower engine hours at the design singleton. |
| **MaintenanceRecord** | `BOOLEAN` | Design file can require **`Yes`** for full service logs. |
| **Radar**, **Jenerator**, **GPS** | `BOOLEAN` | **`Both`** relaxes equip requirements; tighten to **`Yes`** if mandatory. |

### Files

| File | Purpose |
|------|---------|
| [`test/YachtFeatureList.csv`](test/YachtFeatureList.csv) | Design requirements and criterion types |
| [`test/YachtEqualWeights.csv`](test/YachtEqualWeights.csv) | Flat hierarchy, uniform emphasis |
| [`test/YachtDifferentWeights.csv`](test/YachtDifferentWeights.csv) | Stronger emphasis on e.g. price and length |
| [`test/YachtDataset.csv`](test/YachtDataset.csv) | **`A001`…** listing rows |

Tight **`Year`** or boolean filters can shrink the feasible set (many infinite I-values). Widen intervals or relax **`BOOLEAN`** targets to expose more listings.

---

## Troubleshooting

| Symptom | What to check |
|---------|----------------|
| **`FileNotFoundError`** | Run from project root or pass absolute paths; confirm **`test/*.csv`** names. |
| Column / order mismatch | Feature names and order must match between criteria, weights (by feature list), and dataset columns after **`ListingID`**. |
| Wrong inferred type | Intervals need `-` in strings; fuzzy uses `+-` / parentheses; booleans exactly **`Yes`** / **`No`**. |
| Empty or tiny result set | Severe **`TARGET`** / **`BOOLEAN`** rules remove rows; soften design file. |
| **`ModuleNotFoundError: MCDMAxiom`** | CWD / `PYTHONPATH` should include project root containing **`MCDMAxiom/`**. |
| setuptools vs folder name | Editable **`pip install -e .`** may need **`setup.py`** updated to **`packages=find_packages()`** naming **`MCDMAxiom`**; until then use **`requirements.txt`** + root on path. |

**Practices:** keep ListingIDs unique; prototype on a small CSV; compare axiomatic ranks with Minkowski–Prospect for robustness.

---

## References

### Academic

1. Baykasoglu, A., Felekoglu, B., Unal, C. (2022). Perceived usability evaluation of learning management systems via axiomatic design with a real life application. *Kybernetes*. DOI: 10.1108/K-07-2022-1024  
2. Subulan, K. & Baykasoğlu, A. (2021). An Improved Extension of Weighted Hierarchical Fuzzy Axiomatic Design. *Sustainable Production and Logistics*, Ch. 16, 321–357. DOI: 10.1201/9781003005018-16-17  


### Methodological

- Suh, N. P. (2001). *Axiomatic Design: Advances and Applications*. Oxford University Press.  
- Kahneman, D. & Tversky, A. (1979). Prospect Theory: An Analysis of Decision under Risk. *Econometrica*, 47(2), 263–291.

---

**Version:** 1.0  
**Last updated:** April 2026  

For questions, verify dependencies, CSV layout, and the [`test/`](test/) yacht sample paths in this README.
