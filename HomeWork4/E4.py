import json
import re
import string
from nltk.corpus import stopwords
import math
from nltk.stem import PorterStemmer
import Stack
from query import adb
stops = stopwords.words('english')
PS = PorterStemmer()
stops.append("'s")
jsondict = dict()
doccid = dict()
b = 0.02
k = 10
def gettext():
    index=0
    with open("C:\\Users\\wangl\\Documents\\tweets.txt") as f:
        for lines in f:
            jsonstr = json.loads(lines)
            jsondict[index] = jsonstr["text"]
            doccid[index]=jsonstr["tweetId"]
            index = index + 1
    f.close()
    return jsondict
#返回倒排索引表,词出现的文档数,以及文档长度
def getinvertedindex(jsondict: dict):
    worddict = dict()  #倒排索引表
    worddictnum=dict() #单词在每一个文档中出现的次数
    pairnum = dict() # 单词出现的文档数
    doclength = dict() #文档的长度,key:
    for text in jsondict.keys():
        textlist = jsondict[text].split()
        for item in textlist:
            if (item.find('http') == -1):
                item = re.sub("\W+", "", item).split()
                for it in item:
                    if it.encode('UTF-8').isalpha():
                        it = PS.stem(it.lower())
                        if it not in stops:
                            if it not in worddict.keys():#该单词没有出现过
                                worddict[it] = [text]
                                pairnum[it]=1
                            else:
                                if text not in worddict[it]: #该单词在该文档中第一次出现
                                    worddict[it].append(text)
                                    pairnum[it] = pairnum[it] + 1
                            if it not in worddictnum.keys(): #该单词没有出现过
                                worddictnum[it] = [{text:1}] 
                            else:
                                find = False
                                for zit in worddictnum[it]: 
                                    if text in zit.keys(): #这个词在该文档中出现过
                                        zit[text] = zit[text] + 1 #出现次数加1
                                        find = True
                                        break
                                if not find: #在该文档中第一次出现
                                    worddictnum[it].append({text: 1})
                            if text not in doclength.keys(): #计算该文档的长度
                                doclength[text] = 1
                            else:
                                doclength[text] = doclength[text] + 1
    return worddict,worddictnum, pairnum, doclength
# compute pivoted length
def conpute_pivotedlength(worddictnum: dict, pairnum: dict, doclength: dict, querydict: dict, result: list):
    #计算文档的平均长度
    avdl = 0
    for key, value in doclength.items():
        avdl += value
    avdl /= len(doclength)
    fqd = dict()
    #对于每一篇文档,计算f(q,d)
    for doc in result:
        sum = 0
        # 求q∩d中的单词的和
        for item in querydict.keys():
            if item in worddictnum.keys():
                for dic in worddictnum[item]:
                    if doc in dic.keys():
                        sum = sum + querydict[item] * math.log(1 + math.log(1 + dic[doc])) / (1 - b - b * doclength[doc] / avdl) * math.log((len(doclength) + 1) / pairnum[item])
                        break
        fqd[doc]=sum
    return fqd

def compute_BM25(worddictnum: dict, pairnum: dict, doclength: dict, querydict: dict, result: list):
    #计算平均文档长度
    avdl = 0
    for key, value in doclength.items():
        avdl += value
    avdl /= len(doclength)
    fqd = dict()
    for doc in result:
        sum = 0
        for item in querydict.keys():
            if item in worddictnum.keys():
                for dic in worddictnum[item]:
                    if doc in dic.keys():
                        sum = sum + querydict[item] * ((k + 1) * dic[doc]) / (dic[doc] + k*(1 - b - b * doclength[doc] / avdl)) * math.log((len(doclength)+1)/pairnum[item])
        fqd[doc] = sum
    return fqd

def main():
    jsondict = gettext()
    [worddict, worddictnum, pairnum, doclength] = getinvertedindex(jsondict)
    number = 171
    with open("PIVOTqures.txt", 'w', encoding='utf-8') as PIVOTqures_out:
        with open("BM25Dqures.txt", 'w', encoding='utf-8') as BM25Dqures_out:
            with open('querys.txt', 'r', errors	='ignore') as f:
                for line in f:
                    qu = line.split()
                    resu=dict()
                    for item in qu:
                        if (item == '(' or item == ')'):
                            resu.append(item)
                        if (item.find('http') == -1):
                            item = re.sub("\W+", "", item).split()
                            for it in item:
                                if it.encode('UTF-8').isalpha():
                                    it = PS.stem(it.lower())
                                    if (it not in stops):
                                            if it not in resu.keys():
                                                resu[it] = 1
                                            else:
                                                resu[it] = resu[it] + 1
                    result = adb(resu.keys(), worddict, pairnum, jsondict)                     
                    BM25D = compute_BM25(worddictnum, pairnum, doclength, resu, result)
                    sorted_BM25D = sorted(BM25D.items(), key=lambda kv: kv[1])
                    sorted_BM25D.reverse()
                    for i in sorted_BM25D:
                        BM25Dqures_out.write(str(number)+" " +"Q0"+" "+ str(doccid[i[0]]) + " " + str(i[1]) + "\n")
                    PIVOT = conpute_pivotedlength(worddictnum, pairnum, doclength, resu, result)
                    sorted_PIVOT = sorted(PIVOT.items(), key=lambda kv: kv[1])
                    sorted_PIVOT.reverse()
                    for i in sorted_PIVOT:
                        PIVOTqures_out.write(str(number)+" " +"Q0"+" "+ str(doccid[i[0]]) + " " + str(i[1]) + "\n")
                    number += 1
    f.close()
if __name__ == "__main__":
    main()