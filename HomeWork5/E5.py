from __future__ import print_function

import copy
import json
import math
import os
import re
import string

import sklearn.mixture
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn import cluster, datasets
import sklearn.cluster
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.metrics import v_measure_score
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
stoplist = stopwords.words('english')
PS = PorterStemmer()


def read_json(file_path: str):
    content_json = dict()
    cluster_json=dict()
    index = 0
    with open(file_path, 'r', errors='ignore') as f:
        for line in f:
            txt = json.loads(line)
            content_json[index] = txt["text"]
            cluster_json[index] = txt["cluster"]
            index += 1
    f.close()
    return content_json, cluster_json
    
def handle_text(content_json: dict, cluster_json: dict):
    text = list(content_json.values())
    vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(text)
    word = vectorizer.get_feature_names()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(x)
    return tfidf.toarray()

def KMeans_e(tfidf,cluster_list):
    kmeans = cluster.KMeans(n_clusters=101).fit(tfidf)
    # result=normalized_mutual_info_score(kmeans.labels_,cluster_list )
    result=v_measure_score(kmeans.labels_,cluster_list )
    print("the K-Means cluster algorithm result is: ",result)

def Affinity(tfidf, cluster_list):
    affinity = cluster.AffinityPropagation(preference=10).fit(tfidf)
    labels = affinity.labels_
    # result = normalized_mutual_info_score(labels, cluster_list)
    result=v_measure_score(labels,cluster_list )

    print("the Affinity propagation cluster algorithm result is:",result)
    

def meanshift(tfidf, cluster_list):
    meanshif = cluster.MeanShift(bandwidth=0.4,bin_seeding=2).fit(tfidf)
    # result = normalized_mutual_info_score(meanshif.labels_, cluster_list)
    result=v_measure_score(meanshif.labels_,cluster_list )

    print("the Mean-shift cluster algorithm result is:",result)

def spectral(tfidf, cluster_list):
    spectra = cluster.SpectralClustering(101).fit(tfidf)
    # result = normalized_mutual_info_score(spectra.labels_, cluster_list)
    result=v_measure_score(spectra.labels_,cluster_list )

    print("the Spectral clustering cluster algorithm result is: ",result)
    
def Ward(tfidf, cluster_list):
    ward = cluster.AgglomerativeClustering(101, linkage='ward').fit((tfidf))
    # result = normalized_mutual_info_score(ward.labels_, cluster_list)
    result=v_measure_score(ward.labels_,cluster_list )

    print("the Ward hierarchical clustering cluster algorithm result is: ",result)

def Agg(tfidf, cluster_list):
    agg = cluster.AgglomerativeClustering(n_clusters=89, linkage='average').fit_predict(tfidf)
    # result = normalized_mutual_info_score(agg, cluster_list)
    result=v_measure_score(agg,cluster_list )

    print("the Aggiomerative clustering cluster algorithm result is: ",result)

def dbscan(tfidf, cluster_list):
    scan = cluster.DBSCAN(eps=0.5,min_samples=1).fit(tfidf)
    # result = normalized_mutual_info_score(scan.labels_, cluster_list)
    result=v_measure_score(scan.labels_,cluster_list )

    print("the DBSCAN cluster algorithm result is: ",result)

def gaussian_maxtures(tfidf, cluster_list):
    gaussian = sklearn.mixture.GaussianMixture(n_components=20).fit(tfidf)
    labels=gaussian.predict(tfidf)
    # result = normalized_mutual_info_score(labels, cluster_list)
    result=v_measure_score(labels,cluster_list )

    print("the Gaussian mixtures cluster algorithm result is: ",result)

def main():
    file_path = "Homework5Tweets.txt"
    content_json, cluster_json = read_json(file_path)
    tfidf=handle_text(content_json,cluster_json)
    cluster_list = list(cluster_json.values())
    KMeans_e(tfidf, cluster_list)
    Affinity(tfidf, cluster_list)
    meanshift(tfidf, cluster_list)
    spectral(tfidf, cluster_list)
    Ward(tfidf, cluster_list)
    Agg(tfidf, cluster_list)
    dbscan(tfidf, cluster_list)
    gaussian_maxtures(tfidf, cluster_list)
    
if __name__ == "__main__":
    main()
