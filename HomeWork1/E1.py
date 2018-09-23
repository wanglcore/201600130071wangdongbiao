import os
import re
import string
import numpy as np
import time
import nltk
from nltk.corpus import stopwords
PATH = 'C:\\Users\\wangl\\Documents\\20news-18828'
PPath = 'C:\\Users\\wangl\\Documents\\dou\\'
ppppath='C:\\Users\\wangl\\Documents\\'
stoplist=stopwords.words('english')
diffwords = set()
# 获得一个文件夹下的所有子文件夹的绝对路径
def dir_list(path):
    dirlist=[]
    for root,dirname,filename in os.walk(path):
        for name in dirname:
            dirlist.append(os.path.join(root,name))
    return dirlist
# 获得一个文件夹下的所有文件的绝对路径
def file_list(dirlist):
    filelist=[]
    for dirname in dirlist:
        for root,dirs,files in os.walk(dirname):
            for subfile in files:
                filelist.append(os.path.join(root,subfile))
    return filelist
    
def splitword(filelist):
        wlist = set()
        filelist = [filename for filename in filelist if '.txt' not in filename]
        print(len(filelist))
        d=1
        for filename in filelist:
            print(d)
            d=d+1
            gf = open(PPath + filename.split('\\')[-2]+filename.split('\\')[-1]+'.txt','w')
            f = open(filename, 'r', errors='ignore')
            lines=f.readlines()
            for line in lines:
                if (line is not '\n'):
                    sentence = line.split()
                    for words in sentence:
                        lowword=words.lower()
                        if lowword.isalpha():
                            if lowword not in stoplist and len(lowword)>1:
                                #if lowword not in diffwords:
                                    diffwords.add(lowword)
                                #if lowword not in wlist:
                                    wlist.add(lowword)
                        else:
                            if lowword.find('@')==-1:
                                text = re.sub(r"[^a-zA-Z0-9]", ' ', lowword).split()
                                text =[t for t in text if not any(ch.isdigit() for ch in t) ]
                                for it in text:
                                    if len(it) > 1 and it not in stoplist :
                                            #if it not in diffwords:
                                        diffwords.add(it)
                                            #if it not in wlist:
                                        wlist.add(it)
            for i in wlist:
                gf.write(i + '\n')
            wlist.clear()
            f.close()
            gf.close()
        gf=open(ppppath+'\\data.txt','w')
        for i in diffwords:
            gf.write(i + '\n')
        gf.close()
def main():
    dirlist=dir_list(PATH)
    filelist=file_list(dirlist)
    splitword(filelist)
    #countword()
if __name__ == "__main__":
    start=time.clock()
    main()
    end = time.clock()
    print(end-start)


