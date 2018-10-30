import json
import re
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from Stack import Stack
stops = stopwords.words('english')
PS = PorterStemmer()
stops.append("'s")
jsondict = dict()
#得到所有文件中的
def gettext():
    index=0
    with open("C:\\Users\\wangl\\Documents\\tweets.txt") as f:
        for lines in f:
            jsonstr = json.loads(lines)
            jsondict[index] = jsonstr["text"]
            index = index + 1
    f.close()
    return jsondict   
def getinvertedindex(jsondict:dict):
    worddict = dict()
    pairnum = dict()
    for text in jsondict.keys():
        #print(i)
        #i=i+1
        textlist = jsondict[text].split()
        for item in textlist:
            if (item.find('http')==-1):
                item = re.sub("\W+", "", item).split()
                for it in item:
                    if  it.encode('UTF-8').isalpha():
                        it = PS.stem(it.lower())
                        if (it not in stops):
                            if it not in worddict.keys():
                                worddict[it] = [text]
                                pairnum[it]=1
                            else:
                                if text not in worddict[it]:
                                    worddict[it].append(text)
                                    pairnum[it] = pairnum[it] + 1
    return worddict,pairnum
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
def notquery(firstlist:list):
    result = [item for item in jsondict.keys() if item not in firstlist]
    return result
def adb(querystr: list, worddict: dict, qustr: dict):
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
        return notquery(querystr[-1])
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
                        querystack.push(notquery(firstlist))
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
                    querystack.push(notquery(firstlist))
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
                    querystack.push(notquery(firstlist))
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
                querystack.push(notquery(firstlist))
        return querystack.pop()
def main():
    jsontext = gettext()
    worddict,pairnum = getinvertedindex(jsontext)
    print("have create")
    stops.remove('and')
    stops.remove('or')
    stops.remove('not')
    a = input("input:")
    while(a!="exit"):
        qu = a.split()
        resu=[]
        for item in qu:
            if (item == '(' or item == ')'):
                resu.append(item)
            if (item.find('http') == -1):
                item = re.sub("\W+", "", item).split()
                for it in item:
                    if it.encode('UTF-8').isalpha():
                        it = PS.stem(it.lower())
                        if (it not in stops):
                                resu.append(it)
        result = adb(resu, worddict,pairnum)
        num = 0
        for i in result:
            if(num<10):
                print("id:" + str(i) + "   " + jsondict[i])
                num = num + 1
        a = input("input:")
if __name__ == "__main__":
    main()