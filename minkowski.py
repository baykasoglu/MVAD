import math
import numpy as np
import pandas as pd
import MCDMAxiom.calculate as cal
from MCDMAxiom.weightCalculate import create_normalized_IListM, normalize_weights
####################################################
###        Create Minkowski Prospect List        ###
####################################################
def createMinkowskiList(f_list,cols3,f_list2,dec_list,dec_list2 ):
    # Seçmek istediğin sütun indeksleri
    sutunlar1 = [len(f_list[0])-1]  # matris1'in 1. ve 3. sütunlarını seç
    sutunlar2 = [len(dec_list[0])-2,len(dec_list[0])-1]  # matris2'nin sadece 2. sütununu seç


    f_list = np.array(f_list)
    f_list2 = np.array(f_list2)
    dec_list = np.array(dec_list)
    dec_list2 = np.array(dec_list2)
    # Seçili sütunları al
    yeni_matris1 = f_list[:, sutunlar1]  # matris1'den seçili sütunlar
    yeni_matris2 = f_list2[:,:]  # matris2'den seçili sütunlar
    # Yeni matrisi oluştur (yatay birleştirme)
    sonuc = np.hstack((yeni_matris2, yeni_matris1))

    yeni_sutun = [0]
    matris_guncel = np.insert(sonuc, len(sonuc[0]), yeni_sutun, axis=1)

    declined_matris1 =dec_list[:,sutunlar2]
    declined_matris2 =dec_list2[:,:]

    declined_sonuc = np.hstack((declined_matris2, declined_matris1))
    declined_sonuc_matris_guncel = np.insert(declined_sonuc, len(declined_sonuc[0])-1, yeni_sutun, axis=1)
    cols3.append('CDA_Value')

    tam_liste = np.vstack((matris_guncel, declined_sonuc_matris_guncel))
    return tam_liste,cols3


####################################################
###               PROSPECT THEORY                ###
####################################################
def value_function(x, alpha=0.88, beta=0.88, lambd=2.25):
    """
    Computes the Value Function from Prospect Theory.

    Parameters:
        x (float): The outcome value (positive for gains, negative for losses).
        alpha (float): Sensitivity parameter for gains (0 < alpha <= 1, default 0.88).
        beta (float): Sensitivity parameter for losses (0 < beta <= 1, default 0.88).
        lambd (float): Loss aversion coefficient (lambda > 1, default 2.25).

    Returns:
        float: The subjective value of the outcome.
    """
    if x >= 0:
        return x ** alpha  # Gains
    else:
        return -lambd * (-x) ** beta  # Loss
    es

####################################################
###             MINKOWSKI - PROSPECT             ###
####################################################
def Minkowski_Prospect(criteria,data,cols,weights):
    colums=[]
    declined_list=[]
    # Alternatifler IValue'lara göre gruplanıyor.
    # I valuesu olmayanlar Elenen listeye ekleniyor.
    grouped, unique_values, declined_list = grouping_function(criteria,data)

    # Once IValuesu olan Alternatiflerin uzaklıkları her grup için kendi içinde hesaplanıyor.
    # CA degerlerini bulmak için
    # runMinkowski(criteria,grouped_data,cols) fonksiyonu uzaklıkları hesaplıyor
    # ve cıkan degeri prospect valueya gönderiyor.
    # daha sonra prospect value functiondan geçmiş distance'lar normalize oluyor
    # Min-max normalization fuction kullanılıyor
    # Son olarak her bir alternatif için kriterlerine ait normalize olan değerler toplanıyor
    # Alternatifler bu toplam değere göre rank ediliyor.
    final_list = []
    final_list2 = []
    for i in range(0, len(unique_values)):
        grouped_data = grouped[unique_values[i]]
        distanced_grouped_data,cols2 = runMinkowski(criteria,grouped_data,cols)
        columns = cols2[:]
        normalized_data2 = min_max_normalize(distanced_grouped_data,len(cols))
        # minkowskiyi normalize etme denemesi
        # weighted_normalized_data2 = applyWeight(normalized_data2, weights[0])
        sum,cols3,modified_data = rank_by_CA(normalized_data2,cols2,grouped_data)
        final_list.append(sum)
        final_list2.append(modified_data)

    serialized_final_list=[]
    serialized_final_list2=[]
    for row in range(0, len(final_list)):
        for col in range(0, len(final_list[row])):
            serialized_final_list.append(final_list[row][col])
            serialized_final_list2.append(final_list2[row][col])

    # Sonra IValuesu olmayan aslında elenmiş Alternatiflerin uzaklıkları hesaplanıyor.
    # CDA degerlerini bulmak için
    dataTypes = readDataType(declined_list,len(declined_list[0]))
    declinedIvalue , colums = cal.runMCDMAxiom(criteria, weights,declined_list,dataTypes,cols,1)

    # declinedIvalue listesinde 0 degerleri icin CA inf degerleri icin CDA diger degerler icin de I value hesaplanıyor
    # uzaklık hesaplamada değişiklik yok sadece Prospect value function kısmına negatif deger olarak gönderiliyor.
    daList = runMinkowski(criteria, declined_list, cols, declinedIvalue,1)
    normalized_dataDeclined =  min_max_normalize(daList[0],len(cols))
    # minkowskiyi normalize etme denemesi
    # weighted_normalized_dataDeclined = applyWeight(normalized_dataDeclined, weights[0])

    sumDeclined,cols4,modified_dataDeclined = rank_by_CA(normalized_dataDeclined,columns,declined_list)

    tamliste,cols3 = createMinkowskiList(serialized_final_list,cols3,serialized_final_list2,sumDeclined,modified_dataDeclined )
    return tamliste,cols3

def applyWeight(liste,weights):
    weigthedListe =[]
    weigthedList = []
    arr = np.array(liste)
    newarr= arr[:,1:17]
    float_new_arr = newarr.astype(float)
    norm_weights = normalize_weights(weights)
    for i in range(0, len(float_new_arr)):
        weigthedListe =[]
        weigthedListe = create_normalized_IListM(float_new_arr[i],norm_weights,weigthedListe)
        weigthedListe.insert(0,liste[i][0])
        weigthedListe.append(liste[i][-1])
        weigthedList.append(weigthedListe)

    return weigthedList

####################################################
###                SHOW RESULTS                  ###
####################################################
def showRecommendationResults(results,colnames):

    pd.set_option("display.max_rows", None)
    dfItem = pd.DataFrame.from_records(results)
    dfItem.head()
    if (len(dfItem)) == 0 :
        print('Sorry.  No alternative was found matching your criteria..' )
    else :
        dfItem.columns = colnames
        print(str(len(dfItem)) +' suggestions are listed below based on I Value, CA Value and CDA Value:')
        print(dfItem)

####################################################
###           MIN - MAX  NORMALIZATION           ###
####################################################
def min_max_normalize(dataList,col_length):
    normalized_dataList2 = []
    for col in range(1,col_length):
        normalized_dataList = []
        for row in range(0,len(dataList)):
           normalized_dataList.append(dataList[row][0])
    normalized_dataList2.append(normalized_dataList)

    for col in range(1,col_length):
        normalized_dataList = []
        for row in range(0,len(dataList)):
           mins = min([sat[col] for sat in dataList])
           maxs = max([sat[col] for sat in dataList])
           curr_value = dataList[row][col]
           if maxs[0]!=mins[0]:
              normalized_value = (curr_value[0] - mins[0]) / (maxs[0] - mins[0])
           else:
              normalized_value = 1

           normalized_dataList.append(round(normalized_value,2))
        normalized_dataList2.append(normalized_dataList)
        transposed = [[normalized_dataList2[j][i] for j in range(len(normalized_dataList2))] for i in range(len(normalized_dataList2[0]))]

    for row in range(0,len(dataList)):
        transposed[row].append(dataList[row][col_length])
    return transposed

####################################################
###               RANKING FUNCTION               ###
####################################################
def rank_by_CA(normalizedList,cols,systemdata):
    normalizedList2=[]
    original_list=[]
    sumCA = 0
    for row in range(0,len(normalizedList)):
        sumCA = 0
        for col in range(1,len(normalizedList[row])-1):
            sumCA += normalizedList[row][col]
            original_list.append(systemdata[row][col])
        normalizedList2.append(round(sumCA,2))
        original_list.append(round(sumCA,2))

    cols.append("CA_Value")
    normalizedList = [row + [normalizedList2[i]] for i, row in enumerate(normalizedList)]
    ranked_array = sorted(normalizedList, key=lambda x: x[len(normalizedList[0])-1], reverse=True)

    # Matris 1'in ID sırası
    id_sira = {row[0]: i for i, row in enumerate(ranked_array)}

    # Matris 2'yi, Matris 1'in ID sırasına göre sıralama
    matris2_sirali = sorted(systemdata, key=lambda row: id_sira[row[0]])

    return ranked_array,cols,matris2_sirali

####################################################
###         DATATYPE EXTRACTION FUNCTION         ###
####################################################
def readDataType(dataList, col_length):
    dataList2= np.array(dataList).tolist()
    dataTypes=[]
    dataTypeList=[]
    for row in range(0,len(dataList2)):
        for col in range(0,col_length):
            if col == 0:
                dataTypes.append('ID')
            else:
                if  '+-' in dataList2[row][col]:
                    dataTypes.append('FUZZY')
                elif '(' in dataList2[row][col]:
                    dataTypes.append('FUZZY')
                elif '-' in dataList2[row][col]:
                    dataTypes.append('CINTERVAL')
                elif ('Yes' in dataList2[row][col] or 'No' in dataList2[row][col]):
                    dataTypes.append('BOOLEAN')
                else:
                    dataTypes.append('CSINGLETON')
        dataTypeList.append(dataTypes)
        dataTypes = []
    return dataTypeList

####################################################
###              GROUPING FUNCTION               ###
####################################################
def grouping_function(designData, systemData):
    acceptedList =[]
    declinedList = []
    col_length = len(designData)+1
    for i in range(0, len(systemData)):
        if len(systemData[i]) > col_length:
            acceptedList.append(systemData[i])
        else:
            declinedList.append(systemData[i])

    np_data = np.array(acceptedList)
    unique_values = np.unique(np_data[:, col_length])

    # Group rows based on Information Content values
    grouped = {val: np_data[np.where(np_data[:, col_length] == val)] for val in unique_values}
    return grouped, unique_values, declinedList


####################################################
###              A L G O R I T H M               ###
####################################################
def runMinkowski(designData, systemData, cols,IValueList =0, disadv = 0):
    ITotalList = []
    col_length = len(designData)+1
    dataTypes= readDataType(systemData, col_length)
    flag = 0
    CA_value = []
    I_value = []
    if(disadv==1):
        col_length = col_length-1

    for i in range(0, len(systemData)):
        if len(systemData[i]) > col_length:

            IList =[]
            IList2 = []
            IList.append(systemData[i][0])
            IList2.append(systemData[i][0])
            ITotal = []
            for j in range(0, len(designData)):
                if(type(designData[j]) is list):
                    design_Req = designData[j][3]
                    system_Req = dataTypes[i][j+1]
                    design_criteria_type = designData[j][4]

                    if(disadv==1):
                        if(IValueList[i][j] == 0):
                            flag = 0
                        elif(math.isinf(IValueList[i][j])):
                            flag = 1
                        else:
                            flag = 2
                            I_value = [IValueList[i][j]]
                            IList.append(I_value)
                            continue


                    if (design_Req == 'CSINGLETON') and (system_Req  == 'CSINGLETON'): # 1
                        CA_value = minkowski_SS(designData[j][1], systemData[i][j+1], flag)

                    elif (design_Req == 'CSINGLETON') and (system_Req  == 'CINTERVAL'): # 2
                        CA_value = minkowski_SI(designData[j][1], systemData[i][j+1], flag)

                    elif (design_Req == 'CSINGLETON') and (system_Req  == 'FUZZY'): # 3
                        CA_value = minkowski_SF(designData[j][1], systemData[i][j+1], flag)

                    elif (design_Req == 'CINTERVAL') and (system_Req  == 'CSINGLETON'): # 4
                        CA_value = minkowski_IS(designData[j][1],float(systemData[i][j+1]), design_criteria_type, flag)

                    elif (design_Req == 'CINTERVAL') and (system_Req  == 'CINTERVAL'): # 5
                        CA_value = minkowski_II(designData[j][1], systemData[i][j+1],design_criteria_type, flag)

                    elif (design_Req == 'CINTERVAL') and (system_Req  == 'FUZZY'): # 6
                        CA_value = minkowski_IF(designData[j][1], systemData[i][j+1],design_criteria_type, flag)

                    elif (design_Req == 'FUZZY') and (system_Req  == 'CSINGLETON'): # 7
                        CA_value = minkowski_FS(designData[j][1], systemData[i][j+1], design_criteria_type,designData[j][2], flag)

                    elif (design_Req == 'FUZZY') and (system_Req  == 'CINTERVAL'): # 8
                        CA_value = minkowski_FI(designData[j][1], systemData[i][j+1], design_criteria_type,designData[j][2], flag)

                    elif (design_Req == 'FUZZY') and (system_Req  == 'FUZZY'): # 9
                        CA_value = minkowski_FF(int(designData[j][1]), systemData[i][j+1], design_criteria_type,designData[j][2], flag )

                    elif design_Req == 'BOOLEAN': #Boolean
                        CA_value = calculate_Bool(designData[j][1], systemData[i][j+1], j+2, flag)

                    else:
                        CA_value = [0,0]

                    if CA_value.__contains__(math.inf):
                        IList.append(CA_value)
                        break
                    else :
                        if flag==1:
                            CA_value[0]=-CA_value[0]

                        CA_value[0] = value_function(CA_value[0])
                        IList.append(CA_value)

            if(disadv==0):
                IList.append(systemData[i][len(systemData[i])-1])
            else:
                IList.append(float('nan'))

            if(len(IList)>0):
                if(not(ITotal.__contains__(math.inf))):
                    ITotalList.append(IList)

    columns=cols
    columns=[x + '' for x in columns]
    columns.append('IValue')

    return ITotalList,columns


####################################################
###          F U Z Z Y    D E S I G N            ###
####################################################
# design fuzzy (c, m, d) için design_criteria_type = BENEFIT iken (c, m, d) ---> (c, m, m) ye döner
# design fuzzy (c, m, d) için design_criteria_type = COST iken (c, m, d) ---> (m, m, d) ye döner

###  FUZZY DESIGN - CRISP SINGULAR SYSTEM
def minkowski_FS(num1, num2,  design_criteria_type ,deviation, flag, p=2):
    CAo =[]
    a = float(num2)
    b_M = float(num1)

    if(design_criteria_type=='BENEFIT'):
        if (')' in str(deviation) ):
            deviation = float(deviation.strip("()"))
            b_L = b_M - (b_M * float(deviation))
            b_U = b_M
        else:
            b_L = b_M - float(deviation)
            b_U = b_M
    elif(design_criteria_type=='COST'):
        if (')' in str(deviation) ):
            deviation = float(deviation.strip("()"))
            b_L = b_M
            b_U = b_M + (b_M * float(deviation))
        else:
            b_L = b_M
            b_U = b_M + float(deviation)
    else:
        if (')' in str(deviation) ):
            deviation = float(deviation.strip("()"))
            b_L = b_M - (b_M * float(deviation))
            b_U = b_M + (b_M * float(deviation))
        else:
            b_L = b_M - float(deviation)
            b_U = b_M + float(deviation)

    distance = ((abs(a - b_L) ** p + abs(a - b_M) ** p + abs(a - b_U) ** p) / 3) ** (1 / p)
    CAo.append(round(distance,2))
    return CAo


###  FUZZY DESIGN - CRISP INTERVAL SYSTEM
def minkowski_FI(num1, num2, design_criteria_type, deviation, flag, p=2):
    CAo =[]
    b_M = float(num1)
    if(design_criteria_type=='BENEFIT'):
        if (')' in str(deviation) ):
            deviation = float(deviation.strip("()"))
            b_L = b_M - (b_M * float(deviation))
            b_U = b_M
        else:
            b_L = b_M - float(deviation)
            b_U = b_M
    elif(design_criteria_type=='COST'):
        if (')' in str(deviation) ):
            deviation = float(deviation.strip("()"))
            b_L = b_M
            b_U = b_M + (b_M * float(deviation))
        else:
            b_L = b_M
            b_U = b_M + float(deviation)
    else:
        if (')' in str(deviation) ):
            deviation = float(deviation.strip("()"))
            b_L = b_M - (b_M * float(deviation))
            b_U = b_M + (b_M * float(deviation))
        else:
            b_L = b_M - float(deviation)
            b_U = b_M + float(deviation)

    dataItemRanges=num2.split("-")
    a = float(dataItemRanges[0])
    b = float(dataItemRanges[1])

    CI = (a + b)/2
    CF = (b_L + b_M + b_U)/3
    lamda = 1
    # Compute individual distance components
    d1 = abs(a - b_L) ** p  # Lower bounds
    d2 = abs(CI - CF) ** p  # Midpoints
    d3 = abs(b - b_U) ** p  # Upper bounds

    # Compute final distance
    distance = ( (d1 + (lamda*d2) + d3)/3 ) ** (1 / p)

    CAo.append(round(distance,2))
    return CAo

###  FUZZY DESIGN - FUZZY SYSTEM
def minkowski_FF(num1, num2, design_criteria_type, deviation, flag, p=2):
    CAo =[]
    num1 = float(num1)
    a_M = float(num1)
    if(design_criteria_type=='BENEFIT'):
        if (')' in str(deviation) ):
            deviation = float(deviation.strip("()"))
            a_L = a_M - (a_M * float(deviation))
            a_U = a_M
        else:
            a_L = a_M - float(deviation)
            a_U = a_M
    elif(design_criteria_type=='COST'):
        if (')' in str(deviation) ):
            deviation = float(deviation.strip("()"))
            a_L = a_M
            a_U = a_M + (a_M * float(deviation))
        else:
            a_L = a_M
            a_U = a_M + float(deviation)
    else:
        if (')' in str(deviation) ):
            deviation = float(deviation.strip("()"))
            a_L = a_M - (a_M * float(deviation))
            a_U = a_M + (a_M * float(deviation))
        else:
            a_L = a_M - float(deviation)
            a_U = a_M + float(deviation)

    if (')' in num2 ):
        num2 = num2.strip(")")
        dataItemRanges=num2.split("(")
        b_M = float(dataItemRanges[0])
        dev_rate_system = float(dataItemRanges[1])
        b_L = b_M -(b_M * dev_rate_system)
        b_U= b_M +(b_M * dev_rate_system)
    elif ('+-' in num2):
        dataItemRanges=num2.split("+-")
        b_M = float(dataItemRanges[0])
        dev_system = float(dataItemRanges[1])
        b_L = b_M - dev_system
        b_U = b_M + dev_system
    CI = (a_L + a_M + a_U)/3
    CF = (b_L + b_M + b_U)/3
    lamda = 1
    # Compute individual distance components
    d1 = abs(a_L - b_L) ** p  # Lower bounds
    d2 = abs(CI - CF) ** p  # Midpoints
    d3 = abs(a_U - b_U) ** p  # Upper bounds

    # Compute final distance
    distance = ( (d1 + (lamda*d2) + d3)/3 ) ** (1 / p)

    CAo.append(round(distance,2))
    return CAo


####################################################
###       I N T E R V A L    D E S I G N         ###
####################################################
# design interval (a, b) için design_criteria_type = BENEFIT iken (a, b) ---> singular (a) ye döner
# design interval (a, b) için design_criteria_type = COST iken (a, b) ---> singular (b) ye döner

###  CRISP INTERVAL DESIGN - CRISP SINGULAR SYSTEM
def minkowski_IS(num1, num2,design_criteria_type, flag, p=2):
    CAo =[]
    dataItemRanges = num1.split("-")
    a = float(dataItemRanges[0])
    b = float(dataItemRanges[1])

    if(design_criteria_type == 'BENEFIT'):
        distance = minkowski_SS(a, num2,flag)
        CAo.append(round(distance[0],2))
    elif(design_criteria_type == 'COST'):
        distance = minkowski_SS(b, num2,flag)
        CAo.append(round(distance[0],2))
    else:
        num2 = float(num2)
        distance = ((abs(num2 - a) ** p + abs(num2 - b) ** p) / 2) ** (1 / p)
        CAo.append(round(distance,2))

    return CAo

###  CRISP INTERVAL DESIGN - CRISP INTERVAL SYSTEM
def minkowski_II(num1, num2,design_criteria_type, flag, p=2):
    CAo =[]
    dataItemRanges=num1.split("-")
    a_L = float(dataItemRanges[0])
    a_U = float(dataItemRanges[1])

    dataItemRanges2=num2.split("-")
    b_L = float(dataItemRanges2[0])
    b_U = float(dataItemRanges2[1])

    if(design_criteria_type == 'BENEFIT'):
        distance = minkowski_SI(a_L, num2,flag)
        CAo.append(round(distance[0],2))
    elif(design_criteria_type == 'COST'):
        distance = minkowski_SI(a_U, num2,flag)
        CAo.append(round(distance[0],2))
    else:
        distance = ((abs(a_L - b_L) ** p + abs(a_U - b_U) ** p) / 2) ** (1 / p)
        CAo.append(round(distance,2))

    return CAo

###  CRISP INTERVAL DESIGN - FUZZY SYSTEM
def minkowski_IF(num1, num2, design_criteria_type,flag, p=2):
    CAo =[]
    dataItemRanges=num1.split("-")
    a = float(dataItemRanges[0])
    b = float(dataItemRanges[1])

    if(design_criteria_type=='BENEFIT'):
        distance= minkowski_SF(a,num2,flag)
    elif(design_criteria_type=='COST'):
        distance= minkowski_SF(b,num2,flag)
    else:
        if (')' in num2 ):
            num2 = num2.strip(")")
            fuz_num=num2.split("(")
        elif ('+-' in num2):
            fuz_num=num2.split("+-")

        distance = minkowski_FI(fuz_num[0],num1,design_criteria_type,fuz_num[1],flag)

    CAo.append(round(distance[0],2))
    return CAo



####################################################
###        S I N G U L A R   D E S I G N         ###
####################################################

###  CRISP SINGULAR DESIGN - CRISP SINGULAR SYSTEM
def minkowski_SS(a, b, flag, p=2):
    CAo =[]
    distance = abs(float(b)-float(a))
    CAo.append(round(distance,2))
    return CAo

###  CRISP SINGULAR DESIGN - CRISP INTERVAL SYSTEM
def minkowski_SI(a, b, flag, p=2):
    CAo =[]
    a = float(a)
    dataItemRanges=b.split("-")
    b_L = float(dataItemRanges[0])
    b_U = float(dataItemRanges[1])
    distance = ((abs(a - b_L) ** p + abs(a - b_U) ** p) / 2) ** (1 / p)
    CAo.append(round(distance,2))
    return CAo

###  CRISP SINGULAR DESIGN - FUZZY SYSTEM
def minkowski_SF(num1, num2, flag, p=2):
    num1=float(num1)
    CAo =[]
    if (')' in num2 ):
        b = num2.strip(")")
        dataItemRanges=b.split("(")
        b_M = float(dataItemRanges[0])
        dev_rate_system = float(dataItemRanges[1])
        b_L = b_M -(b_M * dev_rate_system)
        b_U= b_M +(b_M * dev_rate_system)
    elif ('+-' in num2):
        dataItemRanges=num2.split("+-")
        b_M = float(dataItemRanges[0])
        dev_system = float(dataItemRanges[1])
        b_L = b_M - dev_system
        b_U = b_M + dev_system

    distance = ((abs(num1 - b_L) ** p + abs(num1 - b_M) ** p + abs(num1 - b_U) ** p) / 3) ** (1 / p)
    CAo.append(round(distance,2))
    return CAo

###  BOOLEAN DESIGN - BOOLEAN SYSTEM
def calculate_Bool(subitem, dataItem, row, flag):
    CAo =[]
    distance = math.inf
    if  subitem == "Both":
        distance = 0
    elif  (subitem == "Yes") and ("Yes" in dataItem):
        distance = 0
    elif  (subitem == "No") and ("No" in dataItem):
        distance = 0
    elif  (subitem == "Yes") and ("No" in dataItem):
        distance = 1
    elif  (subitem == "No") and ("Yes" in dataItem):
        distance = 1
    else:
        raise ValueError('Values for Booleans can only be : Yes, No or Both ! Features file row '+ str(row)+' column 3' )

    CAo.append(round(distance,2))
    return CAo
