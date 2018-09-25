import math
import numpy as np
#   N 为文件总数
#   diffwords 为文件中含有的总词数 是一个字典
#   matrix 为各个文件中的每个单词出现的次数 是一个字典

#权重计算
def tfidf(N,diffwords,matrix):
    difflist=diffwords.keys()
    ma=np.zeros((N,len(difflist)))
    j=0
    for file in matrix.keys():
        lists=matrix[file]
        filist=lists.keys()
        i=0
        for words in difflist:
            if words in filist:
                ma[j][i]=lists[words]*math.log10(N/diffwords[words])
            i=i+1
        j=j+1
    np.savetxt('C:\\Users\wangl\\Downloads\\data.txt',ma)
#tf的亚尺度尺度变换方法
def wfidf(N,diffwords,matrix):
    difflist=diffwords.keys()
    ma = np.zeros((N, len(difflist)))
    j=0
    
    for file in matrix.keys():
        lists = matrix[file]
        i=0
        
        filelist=lists.keys()
        for words in difflist:
            if words in filelist():
                ma[words] = (1 + math.log10(lists[words])) * math.log10(N / diffwords[words])
            i = i + 1
        j = j + 1
    np.savetxt('C:\\Users\wangl\\Downloads\\data.txt',ma)        