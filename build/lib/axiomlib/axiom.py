import pandas as pd
from calculate import runAxiom
from itertools import groupby
from operator import itemgetter

def readFeatures(path):
    feature_list_cop = pd.read_csv(path)
    ar1=[]
    feature=[]
    for row in range(0,len(feature_list_cop)):
        for col in range(0,len(feature_list_cop.columns)):
            col_name= feature_list_cop.columns[col]
            feature.append(feature_list_cop[col_name][row])
        ar1.append(feature)
        feature=[]
    return ar1


def readWeights(path):
    weight_list_cop = pd.read_csv(path)
    feature=[]
    features =[]

    for row in range(0,len(weight_list_cop)):
        for col in range(0,len(weight_list_cop.columns)):
            col_name= weight_list_cop.columns[col]
            feature.append(weight_list_cop[col_name][row])
        features.append(feature)
        feature=[]

    grouped_by_y1 = [list(g) for _, g in groupby(features, key=itemgetter(2))]

    weights=[]
    sub=[]
    for row in range(0,len(grouped_by_y1)):
        for r2 in range(0,len(grouped_by_y1[row])): 
            sub.append(grouped_by_y1[row][r2][3])         
        weights.append(sub)
        sub=[]
    return weights

def readData(path):
    data_list_cop=[]
    dataList=[]
    data_list_cop = pd.read_csv(path)

    feature=[]
    for row in range(0,len(data_list_cop)):
        for col in range(0,len(data_list_cop.columns)):
            col_name= data_list_cop.columns[col]
            feature.append(data_list_cop[col_name][row])
        dataList.append(feature)
        feature=[]
    columns = data_list_cop.columns   
    return dataList, columns

def showResult(results,colnames):
    dfItem = pd.DataFrame.from_records(results)
    dfItem.columns = colnames
    
    if (len(dfItem)) == 0 :
        print('Sorry.  No house was found matching your criteria..' )
    else :  
        print('Listed ' + str(len(dfItem)) +' suggestions are the top picks that fit your criteria:')
        print(dfItem)



features = []
features = readFeatures("axiomlib/feature_list.csv")

weights = []
weights = readWeights("axiomlib/weightList.csv")

data = []
data, cols= readData("axiomlib/house_dataset.csv")

bestList,columns =(runAxiom(features, weights, data, cols))
showResult(bestList,columns)


####################################################   