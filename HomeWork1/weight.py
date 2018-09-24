import math

#   N 为文件总数
#   diffwords 为文件中含有的总词数 是一个字典
#   matrix 为各个文件中的每个单词出现的次数 是一个字典

#权重计算
def tfidf(N,diffwords,matrix):
    mmatrix={}
    for file in matrix.keys():
        lists=matrix.get(file)
        ma={}
        for words in diffwords.keys():
            if words in lists.keys():
                ma[words]=lists.get(words)*math.log10(N/len(diffwords.get(words)))
            else:
                ma[words]=0.0
        mmatrix[file]=ma
    return mmatrix

#tf的亚尺度尺度变换方法
def wfidf(N,diffwords,matrix):
    mmatrix={}
    for file in matrix.keys():
        lists=matrix.get(file)
        ma={}
        for words in diffwords.keys():
            if words in lists.keys():
                ma[words]=(1+math.log10(lists.get(words)))*math.log10(N/len(diffwords.get(words)))
            else:
                ma[words]=0.0
        mmatrix[file]=ma
    return mmatrix