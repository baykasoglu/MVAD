# MVAD User Manual
This project is coded for solving multi-criteria decision-making (MCDM) problems using Weighted Multi Variable Hierarchical Axiomatic Design Method .    
This project and the MCDMAxiom library is developed by Adil Baykasoglu and Filiz Senyuzluler Ozcelik .     
     
___
## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Project Overview](#project-overview)
4. [Input File Formats](#input-file-formats)
5. [Usage Guide](#usage-guide)
6. [Output Explanation](#output-explanation)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)
9. [References](#references)

---

## Introduction

**MVAD** (Multi-Variable Axiomatic Design) is a Python library for solving multi-criteria decision-making (MCDM) problems using two complementary methodologies:

1. **Axiomatic Design Methodology (MCDMAxiom)**: A weighted hierarchical approach for evaluating alternatives based on Information Content (I-Value)
2. **Minkowski Distance with Prospect Theory**: An advanced distance-based method that combines Minkowski distance calculations with Prospect Theory value functions

This library is particularly useful for recommendation systems, product selection, and decision support applications where multiple criteria need to be evaluated simultaneously.

---

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Step 1: Install Dependencies

Install all required packages using the provided requirements file:

```bash
pip install -r requirements.txt
```

This will install:
- numpy==1.24.3
- pandas==2.0.3
- scipy==1.11.4
- sympy==1.12

### Step 2: Verify Installation

You can verify the installation by running a simple import test:

```python
import MCDMAxiom.axiom as ax
import MCDMAxiom.calculate as cal
import minkowski
import numpy as np
import pandas as pd
```

If no errors occur, the installation is successful.

---

## Project Overview

### Project Structure

```
MVAD/
├── MCDMAxiom/              # Core Axiomatic Design module
│   ├── __init__.py
│   ├── axiom.py            # Data reading functions
│   ├── calculate.py        # Axiomatic Design calculations
│   └── weightCalculate.py  # Weight normalization functions
├── minkowski.py            # Minkowski-Prospect implementation
├── prospect.py             # Prospect Theory value functions
├── test.py                 # Example usage script
├── test/                   # Sample data files
│   ├── LaptopCase_Features.csv
│   ├── LaptopCase_EqualWeights.csv
│   ├── LaptopCase_Weights.csv
│   ├── LaptopCase_Dataset.csv
│   ├── LaptopExample_Features.csv
│   ├── LaptopExample_Weights.csv
│   └── LaptopCase_Dataset.csv
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

### Key Components

1. **MCDMAxiom Module**: Implements the Axiomatic Design methodology
   - `readCriteria()`: Reads criteria/features from CSV
   - `readWeights()`: Reads weight configurations from CSV
   - `readData()`: Reads dataset/alternatives from CSV
   - `runMCDMAxiom()`: Performs Axiomatic Design calculations
   - `showRecommendationResults()`: Displays results

2. **Minkowski Module**: Implements Minkowski distance with Prospect Theory
   - `Minkowski_Prospect()`: Main function combining distance and prospect calculations
   - `runMinkowski()`: Calculates Minkowski distances
   - `value_function()`: Applies Prospect Theory value function
   - Various distance calculation functions for different data types

---

## Input File Formats

### 1. Features/Criteria File (CSV)

This file defines the design requirements and criteria for evaluation.

**Required Columns (in order):**
- `feature_name`: Name of the criterion
- `value`: The target value for the criterion
- `fuzziness`: Deviation rate for fuzzy values (use `-` for non-fuzzy)
- `design_req`: Design requirement type
- `criteria_type`: Type of criterion (BENEFIT, COST, or TARGET)

**Design Requirement Types:**
- `CSINGLETON`: Exact/crisp single value (e.g., `12`, `8`)
- `CINTERVAL`: Interval range (e.g., `"10-20"`, `"1000-7500"`)
- `FUZZY`: Fuzzy value with uncertainty (e.g., `4` with fuzziness `1`)
- `BOOLEAN`: Boolean values (`Yes`, `No`, or `Both`)

**Criteria Types:**
- `BENEFIT`: Higher values are better (e.g., RAM, Screen Size)
- `COST`: Lower values are better (e.g., Price, Weight)
- `TARGET`: Specific target value is desired (e.g., Status, Battery)

**Example:**
```csv
feature_name,value,fuzziness,design_req,criteria_type
RAM,8,-,CSINGLETON,BENEFIT
Price,"10000-45000",-,CINTERVAL,COST
Status,4,1,FUZZY,TARGET
Guarantee,Both,-,BOOLEAN,BENEFIT
```

**Notes:**
- Use `-` in `fuzziness` column for non-fuzzy values
- Interval values must be in quotes: `"10-20"`
- Boolean values: `Yes`, `No`, or `Both` (accepts both)

### 2. Weights File (CSV)

This file defines the importance weights for each criterion, optionally with hierarchy.

**Required Columns (in order):**
- `feature_name`: Name of the criterion (must match Features file)
- `hierarchy`: Hierarchy level (0 = top level, 1+ = sub-levels)
- `parent`: Parent criterion name (use `"-"` for level 0)
- `weight`: Importance weight (1-5 scale, where 5 is most important)

**Example (No Hierarchy):**
```csv
feature_name,hierarchy,parent,weight
RAM,0,"-",5
Price,0,"-",5
Status,0,"-",3
Guarantee,0,"-",2
```

**Example (With Hierarchy):**
```csv
feature_name,hierarchy,parent,weight
Performance,0,"-",5
Price,0,"-",5
RAM,1,Performance,4
CPU,1,Performance,5
MonthlyPrice,1,Price,5
```

**Notes:**
- All criteria in Features file must be listed
- Hierarchy level 0 = no parent (use `"-"` for parent)
- Weights are automatically normalized
- Hierarchical weights are calculated as: H1 × H2

### 3. Dataset File (CSV)

This file contains the alternatives/options to be evaluated.

**Required Columns:**
- `ListingID`: Unique identifier for each alternative
- One column for each criterion in the Features file (in the same order)

**Data Format Rules:**
- **CSINGLETON**: Single number (e.g., `8`, `12.5`)
- **CINTERVAL**: Range format `"lower-upper"` (e.g., `"10-20"`, `"1000-7500"`)
- **FUZZY**: 
  - With deviation: `"12+-1"` or `"10(0.25)"`
  - Single value: `5.0`
- **BOOLEAN**: `Yes` or `No`

**Example:**
```csv
ListingID,RAM,Price,Status,Guarantee
L000001,8.0,13000,2-3.5,Yes
L000002,16.0,17450,5.0+-1,Yes
L000003,8.0,32900,2.0,No
```

**Notes:**
- ListingID must be unique
- Column order should match Features file
- Interval values can be written as ranges: `"10-20"`
- Fuzzy values can use `+-` or `()` notation

---

## Usage Guide

### Basic Workflow

1. **Prepare Input Files**: Create your Features, Weights, and Dataset CSV files
2. **Import Modules**: Import required modules
3. **Read Input Data**: Load your CSV files
4. **Run Analysis**: Execute either MCDMAxiom or Minkowski-Prospect method
5. **Display Results**: View and interpret the results

### Method 1: Axiomatic Design (MCDMAxiom)

This method calculates Information Content (I-Value) for each alternative.

```python
import MCDMAxiom.axiom as ax
import MCDMAxiom.calculate as cal

# Step 1: Read input files
criteria = ax.readCriteria("test/LaptopCase_Features.csv")
weights = ax.readWeights("test/LaptopCase_Weights.csv")
data, dataTypes, cols = ax.readData("test/LaptopCase_Dataset.csv")

# Step 2: Run Axiomatic Design calculation
recommendationList, columns = cal.runMCDMAxiom(criteria, weights, data, dataTypes, cols)

# Step 3: Display results
ax.showRecommendationResults(recommendationList, columns)
```

### Method 2: Minkowski-Prospect

This method combines Minkowski distance with Prospect Theory.

```python
import MCDMAxiom.axiom as ax
import minkowski

# Step 1: Read input files
criteria = ax.readCriteria("test/LaptopCase_Features.csv")
weights = ax.readWeights("test/LaptopCase_Weights.csv")
data, dataTypes, cols = ax.readData("test/LaptopCase_Dataset.csv")

# Step 2: Run Minkowski-Prospect calculation
tam_liste, cols3 = minkowski.Minkowski_Prospect(criteria, data, cols, weights)

# Step 3: Display results
minkowski.showRecommendationResults(tam_liste, cols3)
```

### Combined Usage

You can run both methods and compare results:

```python
import MCDMAxiom.axiom as ax
import MCDMAxiom.calculate as cal
import minkowski

# Read input files
criteria = ax.readCriteria("test/LaptopCase_Features.csv")
weights = ax.readWeights("test/LaptopCase_Weights.csv")
data, dataTypes, cols = ax.readData("test/LaptopCase_Dataset.csv")

# Run Axiomatic Design
recommendationList, columns = cal.runMCDMAxiom(criteria, weights, data, dataTypes, cols)

# Run Minkowski-Prospect
tam_liste, cols3 = minkowski.Minkowski_Prospect(criteria, data, cols, weights)

# Display both results
print("=== Axiomatic Design Results ===")
ax.showRecommendationResults(recommendationList, columns)

print("\n=== Minkowski-Prospect Results ===")
minkowski.showRecommendationResults(tam_liste, cols3)
```

---

## Output Explanation

### Axiomatic Design Output

The output includes:
- **ListingID**: Unique identifier for each alternative
- **All criterion columns**: Original data values
- **IValue**: Information Content value (lower is better)

**Interpretation:**
- **IValue = 0.000001 or very small**: Perfect or near-perfect match
- **IValue < 1**: Good match
- **IValue > 1**: Poor match
- **IValue = inf**: Does not meet requirements (excluded from results)

Results are sorted by IValue (ascending), so the best matches appear first.

### Minkowski-Prospect Output

The output includes:
- **ListingID**: Unique identifier for each alternative
- **All criterion columns**: Original data values
- **CA_Value**: Cumulative Advantage value (higher is better)
- **CDA_Value**: Cumulative Disadvantage value (for declined alternatives)

**Interpretation:**
- **CA_Value**: Higher values indicate better alternatives
- Alternatives are grouped by I-Value and ranked within groups
- Results are sorted by CA_Value (descending) for accepted alternatives
- CDA_Value is shown for alternatives that don't meet minimum requirements

**Key Differences:**
- **Axiomatic Design**: Focuses on Information Content (lower I-Value = better)
- **Minkowski-Prospect**: Uses distance-based approach with Prospect Theory (higher CA-Value = better)

---

## Examples

### Example 1: Laptop Selection

This example evaluates laptops based on multiple criteria.

**Features File (LaptopCase_Features.csv):**
```csv
feature_name,value,fuzziness,design_req,criteria_type
RAM,8,-,CSINGLETON,BENEFIT
Price,"10000-45000",-,CINTERVAL,COST
Status,4,1,FUZZY,TARGET
Battery,"60-100",-,CINTERVAL,BENEFIT
```

**Weights File (LaptopCase_Weights.csv):**
```csv
feature_name,hierarchy,parent,weight
RAM,0,"-",5
Price,0,"-",5
Status,0,"-",3
Battery,0,"-",2
```

**Dataset File (LaptopCase_Dataset.csv):**
```csv
ListingID,RAM,Price,Status,Battery
L000001,8.0,13000,2-3.5,90
L000002,16.0,17450,5.0+-1,90
L000003,8.0,32900,2.0,80
```

**Code:**
```python
import MCDMAxiom.axiom as ax
import MCDMAxiom.calculate as cal
import minkowski

criteria = ax.readCriteria("test/LaptopCase_Features.csv")
weights = ax.readWeights("test/LaptopCase_Weights.csv")
data, dataTypes, cols = ax.readData("test/LaptopCase_Dataset.csv")

# Axiomatic Design
recommendationList, columns = cal.runMCDMAxiom(criteria, weights, data, dataTypes, cols)
ax.showRecommendationResults(recommendationList, columns)

# Minkowski-Prospect
tam_liste, cols3 = minkowski.Minkowski_Prospect(criteria, data, cols, weights)
minkowski.showRecommendationResults(tam_liste, cols3)
```

### Example 2: House Selection

**Features File:**
```csv
feature_name,value,fuzziness,design_req,criteria_type
netsize,"50-135",-,CINTERVAL,BENEFIT
brutsize,"0-175",-,CINTERVAL,BENEFIT
roomnumber,2,-,CSINGLETON,BENEFIT
price,"1000-7500",-,CINTERVAL,COST
age,10,0.5,FUZZY,COST
insite,Both,-,BOOLEAN,BENEFIT
```

**Weights File (with hierarchy):**
```csv
feature_name,hierarchy,parent,weight
size,0,"-",1
price,0,"-",1
netsize,1,size,2
brutsize,1,size,3
roomnumber,1,size,2
monthlyprice,1,price,1
age,1,building,2
insite,1,building,2
```

---

## Troubleshooting

### Common Issues

#### 1. File Not Found Error
**Error:** `FileNotFoundError: [Errno 2] No such file or directory`

**Solution:**
- Check that file paths are correct
- Use relative paths from your script location
- Ensure CSV files exist in the specified directory

#### 2. Column Mismatch Error
**Error:** Columns don't match between files

**Solution:**
- Ensure Features file column names match Dataset file columns (except ListingID)
- Verify column order matches between files
- Check for typos in column names

#### 3. Data Type Detection Issues
**Error:** Incorrect data type detection

**Solution:**
- For intervals, use format: `"10-20"` (with quotes in CSV)
- For fuzzy values, use: `"12+-1"` or `"10(0.25)"`
- For boolean, use exactly: `Yes` or `No`
- Ensure numeric values don't have quotes

#### 4. Empty Results
**Error:** No alternatives found matching criteria

**Solution:**
- Check that alternatives meet at least some requirements
- Verify criteria values are reasonable
- Check for data type mismatches
- Some alternatives may have IValue = inf (infinite), which are excluded

#### 5. Import Errors
**Error:** `ModuleNotFoundError: No module named 'MCDMAxiom'`

**Solution:**
- Ensure you're running from the project root directory
- Check that MCDMAxiom folder exists
- Verify Python path includes the project directory

#### 6. Weight Normalization Warnings
**Error:** Weights not summing correctly

**Solution:**
- Weights are automatically normalized, so exact sums don't matter
- Use values 1-5 for relative importance
- Higher numbers = more important

### Best Practices

1. **File Organization:**
   - Keep all CSV files in a `test/` or `data/` folder
   - Use descriptive file names
   - Maintain consistent column ordering

2. **Data Quality:**
   - Ensure ListingIDs are unique
   - Check for missing values
   - Validate data types match design requirements

3. **Performance:**
   - For large datasets (>1000 alternatives), consider filtering first
   - Both methods can handle moderate-sized datasets efficiently

4. **Result Interpretation:**
   - Compare both methods for validation
   - Lower I-Value (Axiomatic) = Better
   - Higher CA-Value (Minkowski-Prospect) = Better
   - Consider top 5-10 recommendations

---

## References

### Academic References

1. Baykasoglu, A., Felekoglu, B., Unal, C. (2022). Perceived usability evaluation of learning management systems via axiomatic design with a real life application, Kybernetes, Article in press, DOI: 10.1108/K-07-2022-1024

2. Subulan, K. and Baykasoğlu A. (2021) An Improved Extension of Weighted Hierarchical Fuzzy Axiomatic Design. Sustainable Production and Logistics. Chapter 16 - Sustainable Route Selection Problem in Intermodal Transportation Networks. 321-357. 10.1201/9781003005018-16-17.

3. Baykasoglu, A., & Senyuzluler Ozcelik, F. (2023). MCDMAxiom - The library for applying Axiomatic Design Methodology on Recommendation Systems. *[Article link to be added]*

### Methodology References

- **Axiomatic Design**: Suh, N. P. (2001). Axiomatic Design: Advances and Applications. Oxford University Press.
- **Prospect Theory**: Kahneman, D., & Tversky, A. (1979). Prospect Theory: An Analysis of Decision under Risk. Econometrica, 47(2), 263-291.
- **Minkowski Distance**: Standard distance metric in multi-dimensional space

---

## Support and Contact

For issues, questions, or contributions:
- Check the README.md for additional information
- Review example files in the `test/` directory
- Ensure all dependencies are correctly installed

---

**Version:** 1.0  
**Last Updated:** 2024  
**License:** [Check project license file]

