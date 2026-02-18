import math
import statistics
from MCDMAxiom.weightCalculate import create_hierachized_weight_string, create_normalized_IList, normalize_weights

####################################################
###              A L G O R I T H M               ###
####################################################
def runMCDMAxiom(designData, weights, systemData, dataTypes, cols, disadv =0):
    sortedList = []
    ITotalList = []
    normalized_w_list = []
    IDeclinedList=[]
    TotalIDeclinedList =[]

    # normalizing weights
    for i in range(0, len(weights)):
        norm_weights = normalize_weights(weights[i])
        normalized_w_list.append(norm_weights)

    # weights are calculated hierarchically
    # and constructed in a string compatible with IList
    if len(normalized_w_list)>1:
        W2 = create_hierachized_weight_string(normalized_w_list)
    else:
        W2 = normalized_w_list[0]

    for i in range(0, len(systemData)):
        IList =[]
        NormalizedIList = []
        ITotal = []
        for j in range(0, len(designData)):
            if(type(designData[j]) is list):
                design_Req = designData[j][3]
                system_Req = dataTypes[i][j+1]
                design_criteria_type = designData[j][4]


                if (design_Req == 'CSINGLETON') and (system_Req  == 'CSINGLETON'): # 1
                    I_value = calculate_1(designData[j][1], systemData[i][j+1], design_criteria_type)

                elif (design_Req == 'CSINGLETON') and (system_Req  == 'CINTERVAL'): # 2
                    I_value = calculate_2(designData[j][1], systemData[i][j+1], design_criteria_type)

                elif (design_Req == 'CSINGLETON') and (system_Req  == 'FUZZY'): # 3
                    I_value = calculate_3(designData[j][1], systemData[i][j+1], design_criteria_type)

                elif (design_Req == 'CINTERVAL') and (system_Req  == 'CSINGLETON'): # 4
                    I_value = calculate_4(designData[j][1], float(systemData[i][j+1]), design_criteria_type)

                elif (design_Req == 'CINTERVAL') and (system_Req  == 'CINTERVAL'): # 5
                    I_value = calculate_5(designData[j][1], systemData[i][j+1], design_criteria_type)

                elif (design_Req == 'CINTERVAL') and (system_Req  == 'FUZZY'): # 6
                    I_value = calculate_6(designData[j][1], systemData[i][j+1], design_criteria_type)

                elif (design_Req == 'FUZZY') and (system_Req  == 'CSINGLETON'): # 7
                    I_value = calculate_7(designData[j][1], systemData[i][j+1], design_criteria_type, designData[j][2])

                elif (design_Req == 'FUZZY') and (system_Req  == 'CINTERVAL'): # 8
                    I_value = calculate_8(designData[j][1], systemData[i][j+1], design_criteria_type, designData[j][2])

                elif (design_Req == 'FUZZY') and (system_Req  == 'FUZZY'): # 9
                    I_value = calculate_9(int(designData[j][1]), systemData[i][j+1], design_criteria_type, designData[j][2] )

                elif design_Req == 'BOOLEAN': #Boolean
                    I_value = calculate_Bool(designData[j][1], systemData[i][j+1], j+2)

                else:
                    I_value= [0,0]

                if I_value.__contains__(math.inf) and disadv==0:
                    IList.append(I_value)
                    break
                else :
                    IList.append(I_value)

        if(len(IList)>0):
            ITotal.append(sum(row[0] for row in IList))
            ITotal.append(sum(row[1] for row in IList))
            # If there is no inf value here, IList[i][0] will be calculated for each element of IList
            if(not(ITotal.__contains__(math.inf))):

                # Applying Equation 16.15 in the article (Baykasoglu & Subulan)
                NormalizedIList = create_normalized_IList(IList, W2, NormalizedIList)
                # normalized list holds separate I values ​​for each of the criteria
                # While preparing ITotalList, normalized I values ​​are summed up and added to the list together with dataID.
                val=([systemData[i][0],[round(sum(row[0] for row in NormalizedIList),9),sum(row[1] for row in NormalizedIList)]])
                val[1][0]= val[1][0]
                ITotalList.append(val)
            else:
                ilk_elemanlar = [row[0] for row in IList]
                TotalIDeclinedList.append(ilk_elemanlar)

    if(disadv==1):
        return TotalIDeclinedList, cols
    # The list is sorted from smallest to largest according to the I value.
    sortedList = sorted(ITotalList, key=lambda x: x[1])
    # print(sortedList)
    # IDs are taken from the list, sorted by I value
    sortedIDList = [el[:1] for el in sortedList]

    # The list is organized structurally
    sortedIDList2=[]
    for element in sortedIDList:
       sortedIDList2.append(element[0])

    columns =[]
    filtered_List=[]
    for rowH in range(0, len(systemData)):
        for rowS in range(0, len(sortedList)):
            if sortedList[rowS][0]==systemData[rowH][0]:
                row1=systemData[rowH]
                filtered_List.append(row1)
                filtered_List[len(filtered_List)-1].append(sortedList[rowS][1][0])

    columns=cols
    columns=[x + '' for x in columns]
    columns.append('IValue')
    return filtered_List,columns

####################################################
###                F O R M U L A S               ###
####################################################
# BOOLEAN CRITERIA
def calculate_Bool(subitem, dataItem, row):
    Io =[]
    I = math.inf
    if  subitem == "Both":
        I = 0
    elif  (subitem == "Yes") and ("Yes" in dataItem):
        I = 0
    elif  (subitem == "No") and ("No" in dataItem):
        I = 0
    elif  (subitem == "Yes") and ("No" in dataItem):
        I = math.inf
    elif  (subitem == "No") and ("Yes" in dataItem):
        I = math.inf
    else:
        raise ValueError('Values for Booleans can only be : Yes, No or Both ! Features file row '+ str(row)+' column 3' )

    Io.append(I)
    Io.append(I)
    return Io

####################################################
# DESIGN CRISP SINGLETON  -  SYSTEM CRISP SINGLETON
def calculate_1(designValue, systemValue, design_criteria_type):
    Io =[]
    designValue = float(designValue)
    systemValue = float(systemValue)

    # TARGET
    if ( design_criteria_type == 'TARGET'):
        if(systemValue != designValue):
            I = math.inf
        else:
            I = 0
    # COST
    elif( design_criteria_type == 'COST'):
        if(systemValue > designValue):
            I = math.inf
        else:
            I = 0
    # BENEFIT
    elif ( design_criteria_type == 'BENEFIT'):
        if(systemValue >= designValue):
            I = 0
        else:
            I = math.inf


    Io.append(I)
    Io.append(0)
    return Io

####################################################
# DESIGN CRISP SINGLETON  -  SYSTEM CRISP INTERVAL
def calculate_2(designValue, systemValue, design_criteria_type):
    Io =[]
    dataItemRanges = systemValue.split("-")
    designValue = float(designValue)
    sL = float(dataItemRanges[0])
    sU = float(dataItemRanges[1])
    # TARGET
    if ( design_criteria_type == 'TARGET'):
        if(sL > designValue or designValue > sU):
            I = math.inf
        elif (sL <= designValue <= sU):
            I = math.log2(sU - sL)
    # COST
    elif( design_criteria_type == 'COST'):
        if(sL > designValue):
            I = math.inf
        elif (sL < designValue < sU):
            I = math.log2((sU - sL)/ (designValue - sL))
        elif (sL == designValue):
            I = math.log2(sU - sL)
        elif (designValue >= sU):
            I = 0

    # BENEFIT
    elif ( design_criteria_type == 'BENEFIT'):
        if(designValue <= sL):
            I = 0
        elif (sL < designValue < sU):
            I = math.log2((sU - sL)/ (sU - designValue))
        elif (sU == designValue):
            I = math.log2(sU - sL)
        elif (designValue > sU):
            I = 0

    Io.append(I)
    Io.append(0)
    return Io

####################################################
# DESIGN CRISP SINGLETON  -  SYSTEM FUZZY
def calculate_3(designValue, systemValue, design_criteria_type):
    Io =[]
    I = 0
    designValue = float(designValue)
    if (')' in systemValue ):
        systemValue = systemValue.strip(")")
        dataItemRanges=systemValue.split("(")
        sM = float(dataItemRanges[0])
        dev_rate_system = float(dataItemRanges[1])
        sL = sM-(sM * dev_rate_system)
        sU = sM+(sM * dev_rate_system)
    elif ('+-' in systemValue):
        dataItemRanges=systemValue.split("+-")
        sM = float(dataItemRanges[0])
        dev_system = float(dataItemRanges[1])
        sL = sM - dev_system
        sU = sM + dev_system

    # TARGET
    if ( design_criteria_type == 'TARGET'):
        if (designValue <= sL or designValue >= sU):
            I = math.inf
        elif (sL < designValue <= sM):
            I = math.log2(((sU - sL) * (sM - sL))/(2 * (designValue - sL)))
        elif (sM < designValue < sU):
            I = math.log2(((sU - sL) * (sU - sM))/(2 * (sU - designValue)))
    # COST
    elif( design_criteria_type == 'COST'):
        if (designValue <= sL):
            I = math.inf
        elif (sL < designValue <= sM):
            I = math.log2(((sU - sL) * (sM - sL))/(pow((designValue - sL), 2)))
        elif (sM < designValue < sU):
            commonRange = ((sM - sL)/2) + (((pow((sU - sM),2))-(pow((sU - designValue),2)))/(2 * (sU - sM)))
            I = math.log2(((sU - sL))/(2 * (commonRange)))
        elif(designValue > sU):
            I = 0

    # BENEFIT
    elif ( design_criteria_type == 'BENEFIT'):
        if (designValue <= sL):
            I = math.inf
        elif (sL < designValue <= sM):
            commonRange = ((sU - sM)/2) + (((sM - sL)/2)-((pow((designValue - sL), 2))/(2 * (sM - sL))))
            I = math.log2((sU - sL)/(2 * commonRange))
        elif (sM <= designValue < sU):
            I = math.log2(((sU - sL) * (sU - sM))/(pow((sU - designValue), 2)))
        elif (designValue > sU):
            I = math.inf

    Io.append(I)
    Io.append(0)
    return Io


####################################################
# DESIGN CRISP INTERVAL  -  SYSTEM CRISP SINGLETON
def calculate_4(designValue, systemValue,  design_criteria_type):
    Io =[]
    dataItemRanges=designValue.split("-")
    dL = int(dataItemRanges[0])
    dU = int(dataItemRanges[1])

    # TARGET
    if ( design_criteria_type == 'TARGET'):
        if(systemValue < dL) or (systemValue > dU):
            Io.append(math.inf)
        else:
            Io.append(0)
    # COST
    elif( design_criteria_type == 'COST'):
        if(systemValue > dU):
            Io.append(math.inf)
        else:
            Io.append(0)
    # BENEFIT
    elif ( design_criteria_type == 'BENEFIT'):
        if(systemValue < dL):
            Io.append(math.inf)
        else:
            Io.append(0)

    Io.append(0)
    return Io


####################################################
# DESIGN CRISP INTERVAL  -  SYSTEM CRISP INTERVAL
def calculate_5(designValue, systemValue,  design_criteria_type):
    Io =[]
    dataItemRanges = designValue.split("-")
    dL = float(dataItemRanges[0])
    dU = float(dataItemRanges[1])

    dataItemRanges2 = systemValue.split("-")
    sL = float(dataItemRanges2[0])
    sU = float(dataItemRanges2[1])

    # TARGET
    if ( design_criteria_type == 'TARGET'):
        if (dL > sU or dU < sL):
            I = math.inf
        elif (dL <= sL and dU >= sU):
            I = 0
        elif (dL == sU or dU == sL):
            I = math.log2(sU - sL)
        elif (sL < dL < sU):
            I = math.log2((sU - sL)/(sU - dL))
        elif (dL < sL < dU):
            I = math.log2((sU - sL)/(dU - sL))
        elif (sL < dL and sU > dU):
            I = math.log2((sU - sL)/(dU - dL))

    # COST
    elif( design_criteria_type == 'COST'):
        if (dU < sL):
            I = math.inf
        elif (dU == sL):
            I = math.log2(sU - sL)
        elif (sL < dU < sU):
            I = math.log2((sU - sL)/(dU - sL))
        elif (dU >= sU):
            I = 0
    # BENEFIT
    elif ( design_criteria_type == 'BENEFIT'):
        if (dL > sU):
            I = math.inf
        elif (dL == sU):
            I = math.log2(sU - sL)
        elif (sL < dL < sU):
            I = math.log2((sU - sL) / (sU - dL))
        elif (dL <= sL):
            I = 0

    Io.append(I)
    Io.append(0)
    return Io

####################################################
# DESIGN CRISP INTERVAL  -  SYSTEM FUZZY
def calculate_6(designValue, systemValue, design_criteria_type):
    Io =[]
    I = 0
    dataItemRanges = designValue.split("-")
    dL = float(dataItemRanges[0])
    dU = float(dataItemRanges[1])
    dM = dU - ((dU - dL)/2)

    if (')' in systemValue ):
        systemValue = systemValue.strip(")")
        dataItemRanges=systemValue.split("(")
        sM = float(dataItemRanges[0])
        dev_rate_system = float(dataItemRanges[1])
        sL = sM-(sM * dev_rate_system)
        sU = sM+(sM * dev_rate_system)
    elif ('+-' in systemValue):
        dataItemRanges=systemValue.split("+-")
        sM = float(dataItemRanges[0])
        dev_system = float(dataItemRanges[1])
        sL = sM - dev_system
        sU = sM + dev_system

    # TARGET
    if ( design_criteria_type == 'TARGET'):
        if (dL >= sU or dU <= sL):
            I = math.inf
        elif (sM < dL < sU < dU):
            I = math.log2(((sU - sL) * (sU - sM))/(pow((sU - dL),2)))
        elif (dL < sL < dU < sM):
            I = math.log2(((sU - sL) * (sM - sL))/(pow((dU - sL),2)))
        elif (sL < dL < sM < sU < dU):
            I = math.log2(((sU - sL) * (sM - sL))/((sU - sL) * (sM - sL) - (pow((dL - sL),2))))
        elif (dL < sL < sM < dU < sU):
            I = math.log2(((sU - sL) * (sU - sM))/((sU - sL) * (sU - sM) - (pow((sU - dU),2))))
        elif (sL < dL < sM < dU < sU and sM == dM ):
            I = math.log2(((sU - sL) * (sU - sM) * (sM - sL))/(((sU - sL) * (sU - sM) * (sM - sL)) - ((pow((dL - sL),2)) * (sU - sM)) - ((pow((sU - dU),2)) * (sM - sL))))
        elif (sM < dL and sU > dU):
            I = math.log2(((sU - sL) * (sU - sM))/(((2 * sU) - dU - dL) * (dU - dL)))
        elif (sL < dL and sM > dU):
            I = math.log2(((sU - sL) * (sM - sL))/((dL + dU - (2 * sL)) * (dU - dL)))
        elif (dL <= sL and dU >= sU):
            I = 0
    # COST
    elif( design_criteria_type == 'COST'):
        if (dU <= sL):
            I = math.inf
        elif (sL < dU <= sM):
            I = math.log2(((sU - sL) * (sM - sL))/(pow((dU - sL),2)))
        elif (sM < dU < sU):
            I = math.log2(((sU - sL) * (sU - sM))/(((sU - sL) * (sU - sM)) - (pow((sU -dU),2))))
        elif (dU >= sU):
            I = 0
    # BENEFIT
    elif ( design_criteria_type == 'BENEFIT'):
        if (sU <= dL):
            I = math.inf
        elif (sM <= dL < sU):
            I = math.log2(((sU - sL) * (sU - sM))/(pow((sU - dL),2)))
        elif (sL < dL < sM):
            I = math.log2(((sU - sL) * (sM - sL))/(((sU - sL) * (sM - sL))-(pow((dL - sL),2))))
        elif (dL <= sL):
            I = 0

    Io.append(I)
    Io.append(0)
    return Io

####################################################
# DESIGN FUZZY  -  SYSTEM CRISP SINGLETON
def calculate_7(designValue, systemValue, design_criteria_type, deviation):
    Io =[]
    I = 0
    s = float(systemValue)
    if (')' in str(deviation) ):
        deviation = float(deviation.strip("()"))
        dM = float(designValue)
        dL = dM - (dM * deviation)
        dU = dM + (dM * deviation)
    else:
        deviation = float(deviation)
        dM = float(designValue)
        dL = dM - deviation
        dU = dM + deviation

    # TARGET
    if ( design_criteria_type == 'TARGET'):
        if (s <= dL or s >= dU):
            I = math.inf
        elif (dL < s < dM):
            I = math.log2((dM - dL)/(s - dL))
        elif (dM < s < dU):
            I = math.log2((dU - dM)/(dU - s))
        elif (s == dM):
            I = 0

    # COST
    elif( design_criteria_type == 'COST'):
        if (s >= dU):
            I = math.inf
        elif (dM < s < dU):
            I = math.log2((dU - dM)/(dU - s))
        elif (s <= dM):
            I = 0

    # BENEFIT
    elif ( design_criteria_type == 'BENEFIT'):
        if (s <= dL):
            I = math.inf
        elif (dL < s < dM):
            I = math.log2((dM - dL)/(s - dL))
        elif (s >= dM):
            I = 0

    Io.append(I)
    Io.append(0)
    return Io

####################################################
# DESIGN FUZZY  -  SYSTEM INTERVAL
def calculate_8(designValue, systemValue, design_criteria_type, deviation):
    Io =[]
    I = 0
    dataItemRanges=systemValue.split("-")
    sL = float(dataItemRanges[0])
    sU = float(dataItemRanges[1])

    if (')' in str(deviation) ):
        deviation = float(deviation.strip("()"))
        dM = float(designValue)
        dL = dM - (dM * deviation)
        dU = dM + (dM * deviation)
    else:
        deviation = float(deviation)
        dM = float(designValue)
        dL = dM - deviation
        dU = dM + deviation

    # TARGET
    if ( design_criteria_type == 'TARGET'):
        if (dL >= sU or dU <= sL):
            I = math.inf
        elif (sL < dL < sU < dM):
            I = math.log2((2 * (sU - sL) * (dM - dL)) / pow((sU - dL),2))
        elif (sL < dL < dM < sU < dU):
            I = math.log2((2 * (sU - sL) * (dU - dM)) / ((dU - dL)*(dU - dM) * pow((dU - sU),2)))
        elif (dM < sL < dU < sU):
            I = math.log2((2 * (sU - sL) * (dU - dM)) / pow((dU - sL),2))
        elif (dL < sL < dM < dU < sU):
            I = math.log2((2 * (sU - sL) * (dM - dL))/((dU - dL) * (dM - dL) - pow((sL - dL),2)))
        elif (sL <= dL and dU <= sU):
            I = math.log2((2 * (sU - sL))/(dU - dL))
        elif (dL < sL < dM < sU < dU ):
            I = math.log2(((sU - sL) * (dM - dL) * (dU - dM))/(((dU - dL) * (dM - dL) * (dU - dM))-(pow((sL - dL),2) * (dU - dM))-(pow((dU - sU),2) * (dM - dL))))
        elif (dL < dM < sL < sU < dU):
            I = math.log2((2 * (dU - dM))/((2 * dU)- sU - sL))
        elif (dL < sL < sU < dM < dU):
            I = math.log2 ((2 * (dM - dL))/(sL + sU - (2 * dL)))

    # COST
    elif( design_criteria_type == 'COST'):
        if (dU <= sL):
            I = math.inf
        elif (sL < dM < sU < dU):
            I = math.log2((2 * (sU - sL) * (dU - dM)) / ((2 * (dM - sL) * (dU - dM)) + (((2 * dU) - sU - dM) * (sU - dM))))
        elif (dM < sL < dU < sU):
            I = math.log2((2 * (sU - sL) * (dU - dM)) / pow((dU - sL),2))
        elif (sL < dM < dU <= sU):
            I = math.log2((2 * (sU - sL)) / (dM - (2 * sL) + dU))
        elif (dM < sL < sU < dU):
            I = math.log2((2 * (dU - dM)) / ((2 * dU) - sU - sL))
        elif (sU <= dM):
            I = 0

    # BENEFIT
    elif ( design_criteria_type == 'BENEFIT'):
        if (dL >= sU):
            I = math.inf
        elif (sL < dL < sU < dM):
            I = math.log2((2 * (sU - sL) * (dM - dL))/(pow((sU - dL),2)))
        elif (dL < sL < dM < sU):
            I = math.log2((2 * (dM - dL) * (sU - sL))/(((sL - (2 * dL) + dM) * (dM - sL)) + (2 * (dM - dL) * (sU - dM))))
        elif (sL <= dL and dM < sU):
            I = math.log2((2 * (sU - sL)) / ((2 * sU) - dM - dL))
        elif (dL < sL < sU < dM):
            I = math.log2 ((2 * (dM - dL))/(sL + sU - (2 * dL)))
        elif (dM <= sL):
            I = 0

    Io.append(I)
    Io.append(0)
    return Io


####################################################
# DESIGN FUZZY  -  SYSTEM FUZZY
def calculate_9(designValue, systemValue,  design_criteria_type, deviation):
    Io =[]
    I = 0
    A = 0
    B = 0
    C = 0
    h_alfa = 0
    h_beta = 0
    alfa = 0
    beta = 0

    if (')' in str(deviation) ):
        deviation = float(deviation.strip("()"))
        dM = float(designValue)
        dL = dM - (dM * deviation)
        dU = dM + (dM * deviation)
    else:
        deviation = float(deviation)
        dM = float(designValue)
        dL = dM - deviation
        dU = dM + deviation

    if (')' in systemValue ):
        systemValue = systemValue.strip(")")
        dataItemRanges=systemValue.split("(")
        sM = float(dataItemRanges[0])
        dev_rate_system = float(dataItemRanges[1])
        sL = sM-(sM * dev_rate_system)
        sU = sM+(sM * dev_rate_system)
    elif ('+-' in systemValue):
        dataItemRanges=systemValue.split("+-")
        sM = float(dataItemRanges[0])
        dev_system = float(dataItemRanges[1])
        sL = sM - dev_system
        sU = sM + dev_system

    # TARGET
    if ( design_criteria_type == 'TARGET'):
        if (dL >= sU or dU <= sL):
            I = math.inf
        elif (sL < dL < sU < dU):
            I = math.log2((((sU - sL)*(sU - sM))+((sU - sL)+(dM - dL)))/math.pow((sU - dL),2))
        elif (sL < dL < dU < sU) and (sM == dM):
            I = math.log2((sU - sL)/(dU - dL))
        elif (dL < sL < dU < sU):
            I = math.log2((((sU - sL)*(dU - dM))+((sU - sL)*(sM - sL)))/(math.pow((dU - sL),2)))
        elif (dL < sL < dM < sM < sU < dU):
            alfa = (((sM * dU) - (dM * sL))/(sM - sL - dM + dU))
            h_alfa = ((dU - alfa)/(dU - dM))
            beta = (((sM * dU) - (dM * sU)) / (sM - sU - dM + dU))
            h_beta = ((dU - beta)/ (dU - dM))
            A = ((alfa - sL) * h_alfa)/2
            B = ((h_alfa + h_beta)*(beta - alfa))/2
            C = ((sU - beta) * h_beta)/2
            I = math.log2((sU - sL)/(2 * (A + B + C)))

        elif (dL < sL < sM < dM < sU < dU):
            alfa = (((dM * sU)-(sM * dL))/(dM - dL - sM + sU))
            h_alfa = (sU - alfa)/(sU - sM)
            beta = (((sM * dL)-(dM * sL))/(sM - sL - dM + dL))
            h_beta = (sL - beta)/(sL - sM)
            A = ((beta - sL)* h_beta) / 2
            B = ((h_beta + h_alfa) * (alfa - beta))/2
            C = ((sU - alfa)* h_alfa)/2
            I = math.log2((sU - sL)/(2*(A + B + C)))

        elif (sL < dL < sM < dM < dU < sU):
            alfa = (((dM * sU)-(sM * dL))/(dM - dL - sM + sU))
            h_alfa = (dL - alfa)/ (dL - dM)
            beta = (((sM * dU) - (dM * sU)) / (sM - sU - dM + dU))
            h_beta = ((dU - beta)/(dU - dM))
            A = ((alfa - dL) * h_alfa)/2
            B = ((h_alfa + h_beta)*(beta - alfa))/2
            C = ((dU - beta) * h_beta)/2
            I = math.log2((sU - sL)/(2 * ( A + B + C )))

        elif (sL < dL < dM < sM < dU < sU):
            alfa = ((dM * sL) - (dU * sM))/(dM - dU - sM + sL)
            h_alfa = (alfa - dU)/(dM - dU)
            beta = ((sM * dL)-(dM * dL))/(sM - sL - dM + dL)
            h_beta = (beta - dL)/(dM - dL)
            A = ((beta - sL)* h_beta)/2
            B = ((h_beta + h_alfa)*(alfa - beta))/2
            C = ((dU - alfa) * h_alfa)/2
            I = math.log2((sU - sL)/(2*(A + B + C)))

        elif (dL < sL and dM == sM and sU <= dU):
            I = 0

        Io.append(I)
        Io.append(0)

    # COST
    elif( design_criteria_type == 'COST'):
        if (dU <= sL):
            I = math.inf
        elif(dL < sL < dU < sU):
            I = math.log2((((sU - sL)*(dU - dM))+((sU - sL)*(sM - sL)))/(math.pow((dU - sL),2)))
        elif(sL < dL < dU < sU and sM == dM) :
            I = math.log2((2*(sU - sL))/(sU - sL + dU - dL))
        elif(dL < sL < dM < sM < sU < dU):
            alfa = (((sM * dU) - (dM * sL))/(sM - sL - dM + dU))
            h_alfa = ((dU - alfa)/(dU - dM))
            beta = (((sM * dU) - (dM * sU)) / (sM - sU - dM + dU))
            h_beta = ((dU - beta)/(dU - dM))
            A = ((alfa - sL)* h_alfa)/2
            B = ((h_alfa + h_beta) * (beta - alfa))/2
            C = ((sU - beta) * h_beta)/2
            I = math.log2((sU - sL)/(2*(A + B + C)))

        elif(sL < dL < sM < dM < dU < sU):
            alfa = ((sM * dU) - (dM - sU))/(sM - sU - dM + dU)
            h_alfa = (dU - alfa)/ (dU - dM)
            A = (sM - sL)/2
            B = ((alfa - sM)*(h_alfa + 1))/2
            C = (h_alfa *(dU - alfa))/2
            I = math.log2((sU - sL)/(2*(A + B + C)))

        elif(sL < dL < dM < sM < dU < sU):
            alfa = ((dM * sL) - (dU * sM))/(dM - dU - sM + sL)
            h_alfa = (alfa - sL) / (sM - sL)
            A = ((dU - sL) * h_alfa)/2
            I = math.log2((sU - sL)/(2*A))

        elif( sU <= dU and sM <= dM):
            I = 0

        Io.append(I)
        Io.append(0)

    # BENEFIT
    elif ( design_criteria_type == 'BENEFIT'):
        if (dL >= sU):
            I = math.inf
        elif (sL < dL < sU < dU):
            I = math.log2(((sU - sL) * (sU - sM) + (sU - sL) * (dM - dL))/math.pow((sU - dL),2))
        elif (sL < dL < dU < sU) and (sM == dM):
            I = math.log2((2*(sU-sL))/(sU - sL + dU - dL))
        elif (dL < sL < sM < dM < sU < dU):
            alfa = ((dM * sU) - (sM * dL))/ (dM - dL -sM + sU)
            h_alfa = (sU - alfa) / (sU - sM)
            beta = ((sM * dL) - (dM * sL))/(sM - sL - dM + dL)
            h_beta = (sL - beta) / (sL - sM)
            A = ((beta - sL) * h_beta)/ 2
            B = ((h_beta + h_alfa) * (alfa - beta))/2
            C = ((sU - alfa)* h_alfa) / 2
            I = math.log2((sU - sL)/(2 * (A + B + C)))
        elif (sL < dL < sM < dM < dU < sU):
            alfa = ((dM * sU) - (sM * dL))/ (dM - dL -sM + sU)
            h_alfa = (dL - alfa) / (dL - dM)
            A = ((sU - dL) * h_alfa) / 2
            I = math.log2((sU - sL)/ (2 * A))
        elif (sL < dL < dM < sM < dU < sU):
            alfa = ((sM * dU) - (dM * sU)) / (sM - sU - dM + dU)
            h_alfa = (dU - alfa)/(dU - dM)
            beta = ((sM * dL)-(dM * sL)) / (sM - sL - dM + dL)
            h_beta = (beta - dL) / (dM - dL)
            A = ((beta - dL) * h_beta) / 2
            B = ((h_beta + 1)*(sM - beta))/2
            C = (sU - sM)/2
            I = math.log2((sU - sL)/(2 * (A + B + C)))
        elif (dL <= sL) and (dM <= sM):
            I = 0


    Io.append(I)
    Io.append(0)
    return Io
