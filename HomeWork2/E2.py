import os
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import math
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

# 统计每一类下的所有的单词
def splittrain(dirlist):
    tags=dict()
    tagsnum=dict()
    i=0
    for dirname in dirlist:
        dirtags={} #记录出现的的单词和出现的次数
        wordnum=0   #记录总的单词数,重复计数
        filelist=file_list(dirname)
        for file in filelist:
            with open(file,'r',encoding='utf-8',errors='ignore') as f:
                alltext=re.sub('\W+','\n',f.read()).replace('_',' ').split()
                f.close()
                for word in alltext:
                    if(not any(ch.isnumeric() for ch in word)) and len(word)>1:
                        word=PS.stem((word.lower()))
                        if word not in stops:
                            if word not in dirtags.keys():  #这个单词在本类中没有出现过
                                dirtags[word]=1
                            else:
                                dirtags[word]=dirtags[word]+1 #这个单词在本类中出现过,重复技术
                            wordnum=wordnum+1   #记录总单词数,重复计数
        tagsnum[dirname]=wordnum #该类下所有的单词数
        tags[dirname]=dirtags #该类下出现的单词和出现的次数
        print(i)
        i=i+1
    return tags,tagsnum

def splittest(dirname):
    tags=dict()
    filelist=file_list(dirname)
    i=0
    for file in filelist:
        filen={}
        with open(file,'r',encoding='utf-8',errors='ignore') as f:
            alltext = re.sub('\W+', '\n', f.read()).replace('_',' ').split()
            f.close()
            for word in alltext:
                if (not any(ch.isnumeric() for ch in word)) and len(word) > 1:
                    word = PS.stem((word.lower()))
                    if word not in stops:
                       if word not in filen.keys():
                           filen[word]=1
                       else:
                           filen[word]=filen[word]+1
        tags[file]=filen
        print(i)
        i=i+1
    return tags
def test(tags,tagsnum):
    testtags=splittest("C:\\Users\\wangl\\Downloads\\test")
    naive=dict()
    zz=0
    for file in testtags.keys():
        fp={}
        for cata in tags.keys():
            p=0.0
            for f in testtags[file].keys():
                if f not in tags[cata].keys():
                    for i in range(testtags[file][f]):
                        p=p+math.log2(1/(tagsnum[cata]+len(tags[cata])))
                else:
                    for i in range(testtags[file][f]):
                        p=p+math.log2((tags[cata][f]+1)/(tagsnum[cata]+len(tags[cata])))
            p=p+math.log2(catap[cata])
            fp[cata]=p
        naive[file]=fp
        print(zz)
        zz=zz+1
    return naive
def getcatagory(naive):
    dirlist = dir_list("C:\\Users\\wangl\\Downloads\\20news-18828\\")
    dirl = dict()
    for fi in dirlist:
        dirl[fi] = file_list(fi)
    t=0
    for file in naive.keys():
        find=False
        cata=max(naive[file].items(),key=lambda x:x[1])[0]
        filename=os.path.basename(cata)
        for dirs in dirl.keys():
            if dirs.find(filename)!=-1:
                for files in dirl[dirs]:
                    if os.path.basename(files)==os.path.basename(file):
                        t=t+1
                        find=True
                        break
            if find==True:
                break
    print("正确率:" +str(t/len(naive)))

def main():
    l=[0.0424,0.0517,0.0523,0.0522,0.0510,0.0521,0.0516,0.0526,0.0528,0.0528,0.0531,0.0526,0.0521,0.0526,0.0524,0.0530,0.0483,0.0499,0.0412,0.0334]
    i=0
    dirlist=dir_list("C:\\Users\\wangl\\Downloads\\20news\\")
    for f in dirlist:
        catap[f]=l[i]
        i=i+1
    tags,tagsnum=splittrain(dirlist)
    naive = test(tags,tagsnum)
    getcatagory(naive)

if __name__ =="__main__":
    main()