import MCDMAxiom.axiom as ax
import MCDMAxiom.calculate as cal
import minkowski
import numpy as np
criteria = []
criteria = ax.readCriteria("test/YachtFeatureList.csv")

weights = []
weights = ax.readWeights("test/YachtEqualWeights.csv")
#weights = ax.readWeights("test/YachtDifferentWeights.csv")

data = []
data, dataTypes, cols = ax.readData("test/YachtDataset.csv")

recommendationList,columns =(cal.runMCDMAxiom(criteria, weights, data, dataTypes, cols))
tam_liste,cols3 = minkowski.Minkowski_Prospect(criteria,data,cols,weights)

ax.showRecommendationResults(recommendationList,columns)
minkowski.showRecommendationResults(tam_liste,cols3)
