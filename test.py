import MCDMAxiom.axiom as ax
import MCDMAxiom.calculate as cal
import minkowski
import numpy as np
criteria = []
criteria = ax.readCriteria("test/LaptopCase_Features.csv")
#criteria = ax.readCriteria("test/LaptopExample_Features.csv")

weights = []
weights = ax.readWeights("test/LaptopCase_Weights.csv")
#weights = ax.readWeights("test/LaptopCase_EqualWeights.csv")
#weights = ax.readWeights("test/LaptopExample_EqualWeights.csv")

data = []
data, dataTypes,cols= ax.readData("test/LaptopCase_Dataset.csv")
#data, dataTypes,cols= ax.readData("test/LaptopExample_Dataset.csv")

recommendationList,columns =(cal.runMCDMAxiom(criteria, weights, data, dataTypes, cols))
tam_liste,cols3 = minkowski.Minkowski_Prospect(criteria,data,cols,weights)

ax.showRecommendationResults(recommendationList,columns)
minkowski.showRecommendationResults(tam_liste,cols3)
