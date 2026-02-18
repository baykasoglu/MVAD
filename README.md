# MCDMAxiom Library
Python 3 library for solving multi-criteria decision-making (MCDM) problems using Weighted Hierarchical Axiomatic Design Method .    
The library is developed by Adil Baykasoglu and Filiz Senyuzluler Ozcelik .     
The details of the study can be found in article 'MCDMAxiom - The library for appliying Axiomatic Design Methodology on Recommendation Systems'  written by Adil Baykasoglu and Filiz Senyuzluler  Ozcelik (2023). *link will come here soon*     
___

# Installation and compilation
The library is available on the Python Package Index (PyPI) and can be installed using the command:
pip install MCDMAxiom
___

# Available Methods
The library contains the following methods:

* **readCriteria(filepath)** :   
    This method takes the path of the criteria list file in .csv format as paramater.  
    > readCriteria(text type)   
    The method returns result in 'list' type.   

    The criteria list file (.csv) format should meet the following rules:
    - the column names should be *"criterion_name"*, *"axiom_req"*, *"value"* and *"dev_rate"* in this order
    - *"criterion_name"* column includes the names of the criteria. All criteria names in the problem should be written in rows.
    - *"axiom_req"* column states the axiom requirement. The user should use one of following the numbers below based on the axiom requirement.   
        - *exactly*: Exact values         
        - *interval*: Interval values    (lower value of range - upper value of range)     
        - *fuzzy*: Fuzzy values       (number)   
        - *boolean*: Boolean values     (Yes / No / Both)   
        - When the user doesn't want to mention any data for a given criterion, the *"axiom_req"* column should include "-" sign.   
    - *"value"* column is for defining the values of the given criterion in either exact, interval, fuzzy or boolean format. 
       When the user doesn't want to mention any data for a given criterion, the *"value"* column should include "-" sign.   
       - if the *"axiom_req"* is given as *exactly*, the value should be a number   
       - if the *"axiom_req"* is given as *interval*, the value should be an interval as : lower value of range - upper value of range    
       - if the *"axiom_req"* is given as *fuzzy*, the value should be a number   
       - if the *"axiom_req"* is given as *boolean*, the value should be one of the following texts : Yes, No or Both(both means system accepts both yes and no valued criteria)   
   
    - *"dev_rate"* column is for defining deviation rate for Fuzzy Values expressed as a percentage in decimal format.    
       The deviation rate value for other value types should be "0" (zero).    
       When the user doesn't want to mention any data for a given criteria, the *"dev_rate"* column should include "-" sign.   
   
* **readWeights(filepath)** :   
    This method takes the path of the weight list file in .csv format as paramater.    
    > readWeights(text type)    
    The method returns result in 'list' type.    
    
    The weight list file (.csv) format should meet the following rules:    
    - the column names should be *"criterion_name"*, *"hierarchy"*, *"parent"* and *"weight"* in the same order  
    - if the criteria has an hierarchy, then the hierarchy level 0 criteria will be for grouping purpose which are not mentioned in the criteria file.
    - if the criteria has no hierarchy, then all the criteria will be at hierarchy level 0 and they will be the overall criteria in the criteria file.
    - all criteria given under *"criterion_name"* column in *"criteria list file"* should be listed in this file. 
    - the hierarchy level should be written under *"hierarchy"* column starting from "0"     
    - if the criterion is in level "0", it means the criterion has no parent node, which should be represented with "-" sign under *"parent"* column.    
    - if level of the criterion is bigger than "0", the name of the parent criterion should be written under *"parent"* column.    
    - the weight (importance level) should be written under *"weight"* column as a number between (1 and 5).    
    
* **readData(filepath)** :    
    This method takes the path of the data list file in .csv format as paramater.     
    > readData(text type)    
    The method returns result in 'list' type.    
    
    The data list file (.csv) format should meet the following rules:    
    - the column names should be *"listingID"* and the names of the criteria given under *"criterion_name"* column in *"criteria list file"* in the same order    
    - each listing ID given under *"listingID"* column should be unique.    
    - any data value which is an interval should be represented as : lower value of range - upper value of range     
    - any data value which is a Boolean type should be "Yes" or "No"    
    
* **runMCDMAxiom(criteria, weights, data, cols** :    
    This method takes the criteria, weights, data, cols of list datatype as paramaters.     
    > runMCDMAxiom(list type, list type, list type, list type)    
    The method returns result in 'list' type.    
    
* **showRecommendationResults(list, column_index)** :    
    This method takes the recommended list by the axiom method and columns index as paramaters.    
    > showRecommendationResults(list type, index type)    
    The method print results on terminal.    
        
___

# Usage Example

```python
    import MCDMAxiom.axiom as ax

    criteria = []
    criteria = ax.readCriteria("test/criteria_list.csv")

    weights = []
    weights = ax.readWeights("test/weightList_noHierarchy.csv")

    data = []
    data, cols= ax.readData("test/house_dataset.csv")

    recommendationList,columns =(ax.runMCDMAxiom(criteria, weights, data, cols))
    ax.showRecommendationResults(recommendationList,columns)
```

The "criteria_list.csv" given in the example above:

|  criterion_name | axiom_req  |    value   | dev_rate |
| --------------- | ---------- | ---------- | -------- |
|        netsize  |  interval  |    50-135  |    0     |
|       brutsize  |  interval  |     0-175  |    0     |
|     roomnumber  |   exactly  |      2     |    0     |
|          price  |  interval  |  1000-7500 |    0     |
|            age  |   fuzzy    |     10     |   0.5    |
|    totalfloors  |       -    |      -     |    -     |
|         insite  |   boolean  |    Both    |    0     |   



The "weight_list.csv" with a hierarchy given in the example above:

|  criterion_name  | hierarchy  |   parent  | weight |
| ---------------- | ---------- | --------- | ------ |
|            size  |         0  |        -  |      1 |
|           price  |         0  |        -  |      1 |
|        building  |         0  |        -  |      1 |
|         netsize  |         1  |     size  |      2 |
|        brutsize  |         1  |     size  |      3 |
|      roomnumber  |         1  |     size  |      2 |
|    monthlyprice  |         1  |    price  |      1 |
|             age  |         1  | building  |      2 |
|     totalfloors  |         1  | building  |      4 |
|          insite  |         1  | building  |      2 |
   

The "weight_list_noHierarcy.csv" with a hierarchy given in the example above:

|  criterion_name  | hierarchy  |   parent  | weight |
| ---------------- | ---------- | --------- | ------ |
|         netsize  |         0  |     -     |      2 |
|        brutsize  |         0  |     -     |      3 |
|      roomnumber  |         0  |     -     |      2 |
|    monthlyprice  |         0  |     -     |      1 |
|             age  |         0  |     -     |      2 |
|     totalfloors  |         0  |     -     |      4 |
|          insite  |         0  |     -     |      2 |

    
The "data_list.csv" given in the example above:

|   listingID  |  netsize | brütsize | roomnumber | price |   age  | totalfloors | insite |
| ------------ | -------- | -------- | ---------- | ----- | ------ | ----------- | ------ |
|   LP0001002  |     100  |     120  |      2+1   | 1500  |   0-15 |           3 |   Yes  |
|   LP0001003  |     110  |     145  |      2+1   | 2000  |     7  |           3 |    No  |
|   LP0001004  |     130  | 100-150  |      4+1   | 2500  |     5  |           9 |   Yes  |
|   LP0001005  |     100  |     150  |      2+1   | 2000  |    11  |           3 |   Yes  |
|   LP0001006  |     140  |     180  |      3+1   | 1000  |    20  |           4 |    No  |
    

The output of this example using "weight_list.csv" file:
```bash
   listingID   netsize  brütsize  roomnumber   price   age   totalfloors  insite    IValue
2  LP0001005       100       150         2+1    2000    11             3     Yes  0.000001
0  LP0001002       100       120         2+1    1500  0-15             3     Yes  0.309499
1  LP0001003       110       145         2+1    2000     7             3      No  1.023530

```

The output of this example using "weight_list_noHierarcy.csv" file:
```bash
   listingID   netsize  brütsize  roomnumber   price   age   totalfloors  insite    IValue
2  LP0001005       100       150         2+1    2000    11             3     Yes  0.000115
0  LP0001002       100       120         2+1    1500  0-15             3     Yes  0.457551
1  LP0001003       110       145         2+1    2000     7             3      No  1.035502

```


# References
* Baykasoglu, A., Felekoglu, B., Unal, C. (2022). Perceived usability evaluation of learning management systems via axiomatic design with a real life application, Kybernetes, Article in press, DOI: 10.1108/K-07-2022-1024
* Subulan, K. and Baykasoğlu A. (2021) An Improved Extension of Weighted Hierarchical Fuzzy Axiomatic Design. Sustainable Production and Logistics. Chapter 16 - Sustainable Route Selection Problem in Intermodal Transportation Networks. 321-357. 10.1201/9781003005018-16-17.

