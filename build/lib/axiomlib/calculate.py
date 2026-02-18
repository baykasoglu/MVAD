import math
import statistics
from weightCalculate import create_hierachized_weight_string, create_normalized_IList, normalize_weights

def runAxiom(userList, weights, data, cols):
    sortedList = []
    ITotalList = []
    normalized_w_list = [] 
    
    # weightler normalize ediliyor
    for i in range(0, len(weights)):  
        norm_weights = normalize_weights(weights[i])
        normalized_w_list.append(norm_weights)

    # weightler hiyeraşik olarak hesaplanıyor ve IList ile uyumlu string hale getiriliyor
    W2 = create_hierachized_weight_string(normalized_w_list)

    for i in range(0, len(data)):
        IList =[]
        NormalizedIList = []
        ITotal = []
        for j in range(0, len(userList)):
            if(type(userList[j]) is list):
                
                if userList[j][1] == 0: #Exactly
                    I_value = calculate_Exactly(userList[j][2], data[i][j+1], IList)
                elif userList[j][1] == 1: #Interval
                    I_value = calculate_Interval(userList[j][2], data[i][j+1],IList)
                elif userList[j][1] == 2: #Around 
                    I_value = calculate_Around(userList[j][2], data[i][j+1],IList , userList[j][0])
                elif userList[j][1] == 3: #Boolean
                    I_value = calculate_Bool(userList[j][2], data[i][j+1])
                else:
                    I_value= 0  

                if I_value.__contains__(math.inf):
                    IList.append(I_value)
                    break
                else :
                    IList.append(I_value)

        if(len(IList)>0):
            ITotal.append(sum(row[0] for row in IList))
            ITotal.append(sum(row[1] for row in IList))
            # burada inf value yoksa IList 'in her elemanı icin IList[i][0] bulucaz
            if(not(ITotal.__contains__(math.inf))):

                # makaledeki 16.15 denklemi uygulanıyor
                NormalizedIList = create_normalized_IList(IList, W2, NormalizedIList)
                # normalized list 10 kriterin her biri için ayrı ayrı I değerini tutuyor
                # ITotalList hazırlanırken normalize edilmis I değerleri toplanıp, dataID ile birlikte listeye ekleniyor.
                ITotalList.append([data[i][0],[sum(row[0] for row in NormalizedIList),sum(row[1] for row in NormalizedIList)]])
                
    # liste I değerine gore küçükten büyüğe sıralanıyor.
    sortedList = sorted(ITotalList, key=lambda x: x[1])
    #print(sortedList)
    # listeden ID ler alınıyor, I değerine göre sıralanmıs sekilde
    sortedIDList = [el[:1] for el in sortedList]
    
    # liste yapısal olarak düzenleniyor
    sortedIDList2=[]
    for element in sortedIDList:
       sortedIDList2.append(element[0])

    columns =[]
    filtered_List=[]
    for rowH in range(0, len(data)):
        for rowS in range(0, len(sortedList)):
            if sortedList[rowS][0]==data[rowH][0]:
                row1=data[rowH]
                filtered_List.append(row1)
                filtered_List[len(filtered_List)-1].append(sortedList[rowS][1][0])

    columns=cols
    columns=[x + '' for x in columns]
    columns.append('IValue')
    return filtered_List,columns


def calculate_Bool(subitem, dataItem):
    Io =[]
    I = math.inf
    if  subitem == "Both":
        I = 0
    elif  (subitem == "Yes") and ("Yes" in dataItem):
        I = 0
    elif  (subitem == "No") and ("No" in dataItem):
        I = 0
    
    Io.append(I)
    Io.append(I)
    return Io
   

# same calculation for all criteria 
# result is 0 if it fits, 1 otherwise
def calculate_Exactly(subitem, dataItem, Ilist):
    Io =[]
    roomnumber= dataItem.split("+")
    if int(subitem) == int(roomnumber[0]) :
        I = 0
    else:
        I = (math.inf) 

    Io.append(I)
    Io.append(I) 
    return Io 


def calculate_Interval(subitem, dataItem, Ilist):
    Io =[]
    INo = 0
    IPo = 0
        
    # kullanıcı interval verdi, sistem aralıgı da interval ise I hesaplamak icin denklemi yazmalıyız
    if(type(dataItem) is str):
        dataItemRanges=dataItem.split("-")
        if(len(dataItemRanges)>1):
            srL = int(dataItemRanges[0])
            srU = int(dataItemRanges[1])
            limits= subitem.split("-")
            drL = int(limits[0])
            drU = int(limits[1])

            if srU <= drL or drU <= srL :
                I = (math.inf)
            elif drL <= srL and srU <= drU : 
                I = 0
            elif drL < srU and drL > srL : 
                I = math.log2((srU - srL)/(srU - drL)) 
            elif srL < drU and srL > drL :
                I = math.log2((srU - srL)/(drU - srL))   
            elif drL < srU and (1 < srL < drL) or  srU <= drL :
                I = math.log2(1 / (statistics.median([drL,drU])-statistics.median([srL, srU])))      
            elif srL < drU and (1 < drL < srL) or  drU <= srL :
                I = math.log2(1 / (statistics.median([srL,srU])-statistics.median([drL, drU])))       
            elif drL < srU and (srL < drL <= 1) or srU <= drL :
                I = math.log2(statistics.median([drL, drU]) - statistics.median([srL, srU]))
            elif srL < drU and (drL < srL <= 1) or drU <= srL :
                I = math.log2(statistics.median([srL, srU]) - statistics.median([drL, drU]))
            
            if(I<0):
                INo = INo + (I * -1)
                print("Negative")
            else :
                IPo = IPo + I
                
            Io.append(IPo)
            Io.append(INo)
            return Io    
        else:
            limits= subitem.split("-")
            drL = int(limits[0])
            drU = int(limits[1])
            if drL <= int(dataItemRanges[0]) and drU >= int(dataItemRanges[0]):
                Io.append(0)
                Io.append(0)
            else:
                Io.append(math.inf)
                Io.append(math.inf)
        
            return Io   
    # kullanıcı interval verdi, sistem aralıgı crisp
    else:
        limits= subitem.split("-")
        drL = int(limits[0])
        drU = int(limits[1])
        if drL <= int(dataItem) and drU >= int(dataItem):
            Io.append(0)
            Io.append(0)
        else:
            Io.append(math.inf)
            Io.append(math.inf)
    
        return Io 

def calculate_Around(subitem, dataItem, Ilis, criteria):
    # kullanıcı fuzzy verdi, sistem aralıgı da interval ise formulu uygulayacagız. 
    # iki dogru arasında kalan alanın, system range ile olarn kesisimini bulup orantılayacagız
    # bir üçgen , iki doğru olmuş oldu 
    Io =[]
    INo = 0
    IPo = 0

    drM = int(subitem)
    drL = drM-(drM * 0.4)
    drU = drM+(drM * 0.4)
    if(type(dataItem) is list):

        srM = statistics.median([int(dataItem[0]),int(dataItem[1])])
        srL = int(dataItem[0])
        srU = int(dataItem[1])
        if srU <= drL or drU <= srL:
            I = (math.inf)
        elif drL <= srL and srU <= drU :
            I = 0
        elif drL < srU and drL > srL:
            I = math.log2(((srU -srL) * (srU -srM) + (srU - srL) * (drM - drL))/(math.pow(srU - drL,2)))
        elif srL < drU and srL > drL:
            I = math.log2(((srU-srL) * (drU - drM) + (srU - srL) * (srM - srL))/(math.pow(drU -srL,2)))    
        elif srL < drU and drL < srL or drU <= srL:
            I = math.log2(1 - ((srM - drM - drU + srL + ((math.pow(drU - srL, 2))/(srM - srL - drM + drU)))/(2 * (srU - drL))))
        elif drL < srU and srL < drL or srU <= drL:
            I = math.log2(1 - ((drM - srM + drL - srU + ((math.pow(srU - drL, 2))/(drM - drL - srM + srU)))/(2 * (drU - srL))))
        
        if(I<0):
            INo = INo + (I * -1)
            print("Negative")
        else :
            IPo = IPo + I
        
        Io.append(IPo)
        Io.append(INo)
        return Io
            

    # kullanıcı fuzzy verdi, sistem aralıgı crisp
    # bir üçgen (design Aralıgı) , bir doğru olmuş oldu (system aralıgı)
    # I = log2(system  range / common range )
    # log2( 1 x dogrunun tam yuksekliği yani 1  /  1 x dogrunun kesisen yuksekligi )
    else:
        if criteria == "price" and dataItem <= drM:
            I = 0 
        elif dataItem == drM:
            I = 0
        elif dataItem >= drU or dataItem <= drL:
            I = (math.inf)
        elif dataItem > drM and dataItem < drU:
        # (subitem,1) ve (drU,0) dan gecen dogrunun egimi ile (dataitem,y2) ve (drU,0) den gecen dogrunun egimi eşit
        # m1 = (0-y1)/ (drU - subitem)
        # m2 = (0-y2)/ (drU - dataitem)
        # y1/y2 = ((drU - subitem)/(drU - dataitem)) 
        # y1/y2 oranı 1 ise tam orta noktadayım I = 0 olmalı yani log2 almalıyız
        # y1/y2 oranı azaldıkca I artmalı yani log2 almalıyız
        # I = log2(1/y2)
            I = math.log2((drU - drM)/(drU - dataItem))    
        elif dataItem < drM and dataItem > drL:
        # (subitem,y1) ve (drL,0) dan gecen dogrunun egimi ile (dataitem,y2) ve (drL,0) den gecen dogrunun egimi eşit
            I = math.log2((drL - drM)/(drL - dataItem))        
        
        if(I < 0):
            INo = INo + I
            print("Negative")
        else :
            IPo = IPo + I
        
        Io.append(IPo)
        Io.append(INo)
        return Io