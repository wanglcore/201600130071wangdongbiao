import os
import copy
import re
import string
import math
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
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

#使用nltk库进行数据的分词等操作
def splitword(filelist):
    matrix=dict()
    wlist=dict()
    i=1
    for filename in filelist:
        f=open(filename,'r',errors='ignore')
        sentences=sent_tokenize(f.read())
        for sentence in sentences:
            words=word_tokenize(sentence)
            words=[PS.stem(word.lower()) for word in words if not any(ch.isnumeric() for ch in word) and all(ch.isalpha() for ch in word) and len(word)>1]
            words=[word for word in words if word not in stoplist]
            for wordz in words:
                if wordz not in diffwords.keys():
                    diffwords[wordz]=set([filename])
                else :
                    diffwords.get(wordz).add(filename)
                if wordz not in wlist.keys():
                    wlist[wordz]=1
                else :
                    wlist[wordz]=wlist.get(wordz)+1
        matrix[filename]=wlist
        wlist={}
        print(i)
        i=i+1
    print(len(diffwords))
    print('done')
    return matrix

def main():
    dirlist=dir_list('C:\\Users\wangl\\Downloads\\20news-18828\\')
    filelist=file_list(dirlist)
    matrix=splitword(filelist)
    mmatrix=weight.tfidf(len(filelist),diffwords,matrix)
    #mmatrix=weight.wfidf(len(filelist),diffwords,matrix)

if __name__=="__main__":
    main()
