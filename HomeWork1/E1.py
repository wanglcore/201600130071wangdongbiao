import os
import copy
import re
import string
import math
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import weight

stoplist=stopwords.words('english')
stoplist.append("'s")
PS=PorterStemmer()
diffwords=dict()
def dir_list(path):
    dirlist=[]
    for root,dirname,filename in os.walk(path):
       for name in dirname:
           dirlist.append(os.path.join(root,name))
    return dirlist

def file_list(dirlist):
    filelist=[]
    for dirname in dirlist:
        for root,dirs,filename in os.walk(dirname):
            for file in filename:
                filelist.append(os.path.join(root,file))
    return filelist
    
#将所有的标点符号转化为空格在进行计算
def splitword(filelist):
    matrix=dict()
    wlist=dict()
    for filename in filelist:
        f=open(filename,'r',errors='ignore')
        alltext=re.sub('\W+','\n',f.read()).replace('_',' ').split()
        f.close()
        for wordz in alltext:
           if (not any(ch.isnumeric() for ch in wordz)) and len(wordz)>1:
               wordz=PS.stem(wordz.lower())
               if wordz not in stoplist:
                   if wordz not in diffwords.keys():
                       diffwords[wordz]=1
                   else:
                        diffwords[wordz]=diffwords[wordz]+1
                   if wordz not in wlist.keys():
                       wlist[wordz]=1
                   else :
                       wlist[wordz]=wlist[wordz]+1
                   matrix[filename]=wlist
                   wlist={}
    return matrix

def main():
    dirlist=dir_list('C:\\Users\wangl\\Downloads\\20news-18828\\')
    filelist=file_list(dirlist)
    matrix=splitword(filelist)
    weight.tfidf(len(filelist),diffwords,matrix)
    #mmatrix=weight.wfidf(len(filelist),diffwords,matrix)

if __name__=="__main__":
    main()
