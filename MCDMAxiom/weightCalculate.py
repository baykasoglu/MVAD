def normalize_weights(wlist):
    nwlist=[]
    for item in range(0, len(wlist)):
        nwlist.append(((wlist[item]/(sum(wlist)))))
    return nwlist

def create_hierachized_weight_string(normalized_w_list):
    # weights are calculated hierarchically
    # weights[0] first row -> H1
    # from weights[1] to the list length are subrows -> H2
    # calculared as H1 * H2
    W2=[]
    W1= normalized_w_list[0]
    for i in range(1, len(normalized_w_list)):
        for j in range(0, len(normalized_w_list[i])):
            W2.append(normalized_w_list[i][j]* W1[i-1])
    return W2

def create_normalized_IList(IList, W2, NormalizedIList):
    # If there is no inf value here, IList[i][0] will be calculated for each element of IList
    # we will formulate this value with a normalized weight list (it should also become a string).
    # Applying Equation 16.15 in the article (Baykasoglu & Subulan)
    # Since there is no negative value, we do not need to do that part in the article.
    for item in range(0,len(IList)):
        if IList[item][0] >= 0 and IList[item][0] < 1:
            NormI = pow(IList[item][0],(1/W2[item]))
        elif IList[item][0] > 1:
            NormI = pow(IList[item][0],W2[item])
        elif IList[item][0] == 1:
            NormI = W2[item]
        NormalizedIList.append([NormI,0])

    return NormalizedIList

def create_normalized_IListM(IList, W2, NormalizedIList):
    # If there is no inf value here, IList[i][0] will be calculated for each element of IList
    # we will formulate this value with a normalized weight list (it should also become a string).
    # Applying Equation 16.15 in the article (Baykasoglu & Subulan)
    # Since there is no negative value, we do not need to do that part in the article.
    for item in range(0,len(IList)):
        if IList[item] >= 0 and IList[item] < 1:
            NormI = pow(IList[item],(1/W2[item]))
        elif IList[item] > 1:
            NormI = pow(IList[item],W2[item])
        elif IList[item] == 1:
            NormI = W2[item]
        NormalizedIList.append(NormI)

    return NormalizedIList
