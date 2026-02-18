from itertools import groupby
import pandas as pd
from operator import itemgetter

def readCriteria(path):
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
    dataTList=[]
    feature=[]
    for row in range(0,len(data_list_cop)):
        for col in range(0,len(data_list_cop.columns)):
            col_name= data_list_cop.columns[col]
            feature.append(data_list_cop[col_name][row])
        dataList.append(feature)
        feature=[]
    columns = data_list_cop.columns
    dataTList= readDataType(data_list_cop)
    return dataList,dataTList,columns

def readDataType(dataList):
    dataTypes=[]
    dataTypeList=[]
    for row in range(0,len(dataList)):
        for col in range(0,len(dataList.columns)):
            if col == 0:
                dataTypes.append('ID')
            else:
                col_name= dataList.columns[col]
                if type(dataList[col_name][row]) is str and '+-' in dataList[col_name][row]:
                    dataTypes.append('FUZZY')
                elif type(dataList[col_name][row]) is str and '(' in dataList[col_name][row]:
                    dataTypes.append('FUZZY')
                elif type(dataList[col_name][row]) is str and '-' in dataList[col_name][row]:
                    dataTypes.append('CINTERVAL')
                elif type(dataList[col_name][row]) is str and ('Yes' in dataList[col_name][row] or 'No' in dataList[col_name][row]):
                    dataTypes.append('BOOLEAN')
                else:
                    dataTypes.append('CSINGLETON')
        dataTypeList.append(dataTypes)
        dataTypes = []
    return dataTypeList

def showRecommendationResults(results,colnames):
    pd.set_option("display.max_rows", None)
    dfItem = pd.DataFrame.from_records(results)
    dfItem.head()
    if (len(dfItem)) == 0 :
        print('Sorry.  No house was found matching your criteria..' )
    else :
        dfItem.columns = colnames
        print('Listed ' + str(len(dfItem)) +' suggestions are the top picks that fit your criteria:')
        print( dfItem.sort_values('IValue'))
####################################################
