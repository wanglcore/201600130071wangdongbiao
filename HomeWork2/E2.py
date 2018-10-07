import os
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import math
import random
stops = stopwords.words('english')
stops.append("'s")
PS = PorterStemmer()
catap=dict()

#获取每一类的文件夹名
def dir_list(path):
    dirlist=[]
    for root,dirname,filename in os.walk(path):
        for name in dirname:
            dirlist.append(os.path.join(root,name))
    return dirlist
#获取每一类下的所有文件
def file_list(dirname):
    filelist = []
    for root,dirs,filename in os.walk(dirname):
        for file in filename:
            filelist.append(os.path.join(root,file))
    return filelist


def getfile_list(dirlist):
    filedic=dict()
    for dirname in dirlist:
        filedic[dirname] = file_list(dirname)
    return filedic

def splitdataset(filedic,dirlist,splitscale):
    # classnum = dict()
    trainset = dict()
    testset = dict()
    num=0
    for dirname in filedic.keys():
        #在该类下产生  该类下文档数/scale 个不重复的随机数
        #randomlist = random.sample(range(0, len(filedic[dirname])), int(len(filedic[dirname]) *splitscale))
        randomlist = random.sample(range(0, len(filedic[dirname])), int(len(filedic[dirname]) *splitscale[dirname]))
        
        tmp = []
        #经产生的随机数作为测试文档的下标
        for i in randomlist:
            tmp.append(filedic[dirname][i])
        testset[dirname] = tmp
        tmp = []
        #将其余文档作为训练文档
        for i in list(set(range(0, len(filedic[dirname]))) - set(randomlist)):
            tmp.append(filedic[dirname][i])
            num=num+1
        trainset[dirname] = tmp
    #计算每一类下训练文档占该类总文档数的比例
    for dirs in trainset.keys():
        catap[dirs] = len(trainset[dirs]) / num
    #返回训练集和测试集
    return trainset, testset
    
# 统计每一类下的所有的单词
def splittrain(trainset):
    tags=dict()
    tagsnum=dict()
    i=0
    for dirname in trainset.keys():
        dirtags={} #记录出现的的单词和出现的次数
        wordnum=0   #记录总的单词数,重复计数
        filelist=trainset[dirname]
        for file in filelist:
            with open(file,'r',encoding='utf-8',errors='ignore') as f:
                alltext=re.sub('\W+','\n',f.read()).replace('_',' ').split()
                f.close()
                for word in alltext:
                    if(not any(ch.isnumeric() for ch in word)) and len(word)>1:
                        word=PS.stem((word.lower()))
                        if word not in stops:
                            #多项式模型
                            if word not in dirtags.keys():  #这个单词在本类中没有出现过
                                dirtags[word]=1
                            else:
                                dirtags[word] = dirtags[word] + 1  #这个单词在本类中出现过,重复技术
                            #伯努利模型
                            # if word not in dirtags.keys():
                            #     dirtags[word]=1
                            wordnum=wordnum+1   #记录总单词数,重复计数
        tagsnum[dirname]=wordnum #该类下所有的单词数
        tags[dirname]=dirtags #该类下出现的单词和出现的次数
        print(i)
        i=i+1
    #返回训练集下每一类中的出现的单词和相应的出现次数和每一类下的所有的单词数(重复计数)
    return tags,tagsnum  
#统计测试集下的每一个文档中的单词,使用和训练集相同的分词方法
def splittest(testset):
    tags = dict()
    for dirname in testset.keys():
        filelist=testset[dirname]
        i=0
        for file in filelist:
            filen={}
            with open(file,'r',encoding='utf-8',errors='ignore') as f:
                alltext = re.sub('\W+', '\n', f.read()).replace('_',' ').split()
                f.close()
                for word in alltext:
                    if (not any(ch.isnumeric() for ch in word)) and len(word) > 1:
                        word = PS.stem((word.lower()))
                        #多项式模型
                        if word not in stops:
                            if word not in filen.keys():
                                filen[word]=1
                            else:
                                filen[word] = filen[word] + 1
                        #伯努利模型
                        # if word not in stops:
                        #     if word not in filen.keys():
                        #         filen[word]=1
            tags[file]=filen
            print(i)
            i = i + 1
    #返回测试集中每一篇文档中出现的单词
    return tags
def classfication(tags, tagsnum, testset):
    #测试集
    testtags=splittest(testset)
    naive=dict()
    #对于测试集中的每一篇文档中的每一个词,计算他在训练集中的各类上出现的概率,出现多次的单词重复计算
    for file in testtags.keys():
        fp = {}
        for cata in tags.keys():
            p=0.0
            for f in testtags[file].keys():
                if f not in tags[cata].keys():
                    #多项式模型
                    for i in range(testtags[file][f]):
                        p=p+math.log2(1/(tagsnum[cata]+len(tags[cata])))
                    #伯努利模型
                    # p=p+math.log2(1/(tagsnum[cata]+2))
                else:
                    #多项式模型
                    for i in range(testtags[file][f]):
                        p = p + math.log2((tags[cata][f] + 1) / (tagsnum[cata] + len(tags[cata])))
                    #伯努利模型
                    # p=p+math.log2((tags[cata][f]+1)/(tagsnum[cata]+2))
            p=p+math.log2(catap[cata])
            fp[cata]=p
        naive[file] = fp
    #返回每一个文档出现在每一类下的概率
    return naive
def getcatagory(naive,testset):
    t = 0
    z=0
    for file in naive.keys():
        cata=max(naive[file].items(),key=lambda x:x[1])[0]
        if file in testset[cata]:
            print(str(z) + "   " + file + "  True")
            t = t + 1
        else:
            print(str(z) + "   " + file + "   false")
        z=z+1
    print("true" + str(t))
    print("zong"+str(z))
    print("正确率:" +str(t/len(naive)))

def main():
    dirlist = dir_list("C:\\Users\\wangl\\Downloads\\20news-18828\\")
    #设置不同的划分比例
    #scale=0.1
    #scale=0.2
    scale=dict()
    for dirs in dirlist:
        scale[dirs]=random.random()
    filedic=getfile_list(dirlist)
    trainset,testset=splitdataset(filedic,dirlist,scale)
    tags,tagsnum=splittrain(trainset)
    naive = classfication(tags,tagsnum,testset)
    getcatagory(naive,testset)

if __name__ =="__main__":
    main()