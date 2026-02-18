def normalize_weights(wlist):
    nwlist=[]
    for item in range(0, len(wlist)):
        nwlist.append(wlist[item]/(sum(wlist)))

    return nwlist


def create_hierachized_weight_string(normalized_w_list):
    # weightler hiyeraşik olarak hesaplanıyor 
    # weights[0] ilk sıra H1
    # weights[1] den liste uzunluguna kadar olanları alt sıralar H2
    # H1 * H2 şeklinde hesaplanıyor   
    W2=[] 
    W1= normalized_w_list[0]
    for i in range(1, len(normalized_w_list)): 
        for j in range(0, len(normalized_w_list[i])): 
            W2.append(normalized_w_list[i][j]* W1[i-1])

    return W2


def create_normalized_IList(IList, W2, NormalizedIList):
    # burada inf value yoksa IList 'in her elemanı icin IList[i][0] bulucaz
    # bu değeri normalized weight list (aynı sekilde string hale gelmis olmalı) ile formülize edicez
    # makaledeki 16.15 denklemi uygulanıyor
    # negatif değer olmadığı için o kısmı yapmamız gerekmiyor.
    for item in range(0,len(IList)):
        if IList[item][0] >= 0 and IList[item][0] < 1:
            NormI = pow(IList[item][0],(1/W2[item]))
        elif IList[item][0] > 1:
            NormI = pow(IList[item][0],W2[item])
        elif IList[item][0] == 1:
            NormI = W2[item]
        NormalizedIList.append([NormI,0])

    return NormalizedIList