import Stack
def andquery(firstlist:list, secondlist:list):
    i = 0
    j = 0
    result = []
    if len(firstlist)!=0 and len(secondlist)!=0:
        while (i != len(firstlist) - 1 and j != len(secondlist) - 1):
            if firstlist[i] == secondlist[j]:
                result.append(firstlist[i])
                i,j=i+1,j+1
            elif firstlist[i] < secondlist[j]:
                i = i + 1
            elif firstlist[i] > secondlist[j]:
                j = j + 1
    else:
        return []
    return result
def orquery(firstlist:list, secondlist:list):
    i = 0
    j = 0
    result = []
    while (i != len(firstlist) - 1 and j != len(secondlist) - 1):
        if firstlist[i] < secondlist[j]:
            result.append(firstlist[i])
            i=i+1
        elif firstlist[i] > secondlist[j]:
            result.append(secondlist[j])
            j = j + 1
        elif firstlist[i] == secondlist[j]:
            result.append(firstlist[i])
            i, j = i + 1, j + 1
    if i == len(firstlist) - 1 and j!=len(secondlist)-1:
        for item in range(j,len(secondlist)):
            result.append(secondlist[item])
    elif i != len(firstlist) - 1 and j == len(secondlist) - 1:
        for item in range(i,len(firstlist)):
            result.append(firstlist[item])
    return result

# 返回not之后的list
def notquery(firstlist:list,jsondict:dict):
    result = [item for item in jsondict.keys() if item not in firstlist]
    return result
def adb(querystr: list, worddict: dict, qustr: dict,jsondict:dict):
    mergenum=0
    resultlist = []
    # 只含有 and 查询
    strlen=dict()
    if 'or' not in querystr and 'not' not in querystr:
        querystr = [item for item in querystr if item != '(' and item != ')']
        for item in querystr:
            if item !="and":
                if (item not in worddict.keys()):
                    return []
                strlen[item]=qustr[item]
        sortdic = sorted(strlen.items(), key=lambda item: item[1])
        resultlist=worddict[sortdic[0][0]]
        for i in range(1, len(sortdic)):
            if len(resultlist) == 0:
                return resultlist
            resultlist = andquery(resultlist, worddict[sortdic[i][0]])
        return resultlist
    # 只含有or查询
    elif 'and' not in querystr and 'not' not in querystr:
        querystr = [item for item in querystr if item != '(' and item != ')']
        for item in querystr:
            if item !="or":
                if item in worddict.keys():
                    strlen[item] = qustr[item]
                
        sortdic = sorted(strlen.items(), key=lambda item : item[1], reverse=True)
        resultlist = worddict[sortdic[0][0]]
        for i in range(1, len(sortdic)):
            resultlist = orquery(resultlist, worddict[sortdic[i][0]])
        return resultlist
    # 只含有 not
    elif 'and' not in querystr and 'or' not in querystr:
        querystr = [item for item in querystr if item != '(' and item != ')']
        return notquery(querystr[-1],jsondict)
    # 混合查询
    else:
        querystack = Stack()
        operstack = Stack()
        i = 0
        while i!=len(querystr):
            if querystr[i] == '(':
                operstack.push(querystr[i])
            elif querystr[i] == ')':
                while (operstack.top() != '('):
                    oper=operstack.pop()
                    if oper == 'or':
                        firstlist = querystack.pop()
                        secondlist = querystack.pop()
                        querystack.push(orquery(firstlist, secondlist))
                    elif oper == 'and':
                        firstlist = querystack.pop()
                        secondlist = querystack.pop()
                        querystack.push(andquery(firstlist, secondlist))
                    elif oper == 'not':
                        firstlist = querystack.pop()
                        querystack.push(notquery(firstlist,jsondict))
                operstack.pop()
            elif querystr[i] == 'and':
                oper = operstack.top()
                if (oper == 'and' or oper == 'or'):
                    operstack.pop()
                    firstlist = querystack.pop()
                    secondlist = querystack.pop()
                    if oper == 'and':
                        querystack.push(andquery(firstlist, secondlist))
                    elif oper=='or':
                        querystack.push(orquery(firstlist, secondlist))
                elif oper == 'not':
                    operstack.pop()
                    firstlist = querystack.pop()
                    querystack.push(notquery(firstlist,jsondict))
                operstack.push(querystr[i])
            elif querystr[i] == 'or':
                oper=operstack.top()
                if (oper == 'and' or oper == 'or'):
                    operstack.pop()
                    firstlist = querystack.pop()
                    secondlist = querystack.pop()
                    if oper == 'and':
                        querystack.push(andquery(firstlist, secondlist))
                    elif oper=='or':
                        querystack.push(orquery(firstlist, secondlist))
                elif oper == 'not':
                    operstack.pop()
                    firstlist = querystack.pop()
                    querystack.push(notquery(firstlist,jsondict))
                operstack.push(querystr[i])
            elif querystr[i] == 'not':
                operstack.push(querystr[i])
            else:
                if querystr[i] in worddict.keys():
                    querystack.push(worddict[querystr[i]])
                else:
                    querystack.push([]) 
            i = i + 1
        while not operstack.isEmpty() :
            oper=operstack.pop()
            if oper == 'and':
                firstlist = querystack.pop()
                secondlist = querystack.pop()
                querystack.push(andquery(firstlist, secondlist))
            elif oper == 'or':
                firstlist = querystack.pop()
                secondlist = querystack.pop()
                querystack.push(orquery(firstlist, secondlist))
            elif oper == 'not':
                firstlist = querystack.pop()
                querystack.push(notquery(firstlist,jsondict))
        return querystack.pop()