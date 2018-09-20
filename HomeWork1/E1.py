import os
import re
import string
import numpy as np
import time
import nltk
import numpy as np
from nltk.corpus import stopwords
PATH = 'C:\\Users\\wangl\\Documents\\20news-18828'
stoplist=stopwords.words('english')
diffwords = set()
dirlist = []
filelist=[]
# 获得一个文件夹下的所有子文件夹的绝对路径
def dir_list():
    for root,dirname,filename in os.walk(PATH):
        for name in dirname:
            dirlist.append(os.path.join(root,name))

# 获得一个文件夹下的所有文件的绝对路径
def file_list():
    for dirname in dirlist:
        for root,dirs,files in os.walk(dirname):
            for subfile in files:
                filelist.append(os.path.join(root,subfile))

def splitword():
        for filename in filelist:
            f = open(filename, 'r', errors='ignore')
            lines=f.readlines()
            for line in lines:
                if (line is not '\n'):
                    sentence = line.split()
                    for words in sentence:
                        lowword=words.lower()
                        if lowword.isalpha():
                            if lowword not in stoplist and lowword not in diffwords:
                                diffwords.add(lowword)
                        else:
                            if lowword.find('@')==-1:
                                text = re.sub(r"[^a-zA-Z0-9]", ' ', lowword).split()
                                text =[t for t in text if not any(ch.isdigit() for ch in t) ]
                                for it in text:
                                    if len(it)>1 and it not in stoplist and it not in diffwords:
                                        diffwords.add(it)
            f.close()

def countword():
    diffwoodlist=list(diffwords)
    rows = len(filelist)
    cols = len(diffwords)
    arr=np.zeros((rows,cols),dtype=np.int8)
    for row in range(0, rows):
        f = open(filelist[row], 'r', errors='ignore')
        lines = f.readlines()
        for line in lines:
            if line is not '\n':
                sentence = line.split()
                for words in sentence:
                    lowword=words.lower()
                    if lowword.isalpha() :
                        if lowword not in stoplist:
                            #arr[row][diffwoodlist.index(lowword)]=arr[row][diffwoodlist.index(lowword)]+1
                            arr[row][diffwoodlist.index(lowword)]=1
                    else :
                        if lowword.find('@')==-1:
                            text=re.sub(r"[^a-zA-Z0-9]",' ',lowword).split()
                            text=[t for t in text if not any(ch.isdigit() for ch in t)]
                            for it in text:
                                if len(it) > 1 and it not in stoplist:
                                    #arr[row][diffwoodlist.index(it)]=arr[row][diffwoodlist.index(it)]+1

                                    arr[row][diffwoodlist.index(it)]=1
        f.close()
    print("begin save")
    np.savetxt('C:\\Users\\wangl\\Documents\\result.txt',arr)
def main():
    dir_list()
    file_list()
    splitword()
    countword()
if __name__ == "__main__":
    start=time.clock()
    main()
    end = time.clock()
    print(end-start)


