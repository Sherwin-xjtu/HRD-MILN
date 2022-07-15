# -*-coding:utf-8-*-
from __future__ import division

import os

import pandas as pd
from fancyimpute import KNN
from sklearn import preprocessing


def mergeFiles(path):

    labelPath = 'C:/Users/Sherwin/Desktop/label.csv'
    df1 = pd.read_csv(labelPath, sep=',', low_memory=False)
    keys = df1['id']
    values = df1['label']
    labelDict = dict(zip(keys, values))
    try:
        pathDir = os.listdir(path)
        m = 0
        for allDir in pathDir:
            child = os.path.join('%s/%s' % (path, allDir))

            if os.path.isfile(child) and (".cns" in str(allDir)) and ("副本" in str(allDir)):
                id = child.split('/')[-1].split()[0]
                if m == 0:
                    tm = pd.read_csv(child, sep='\t', low_memory=False)
                    tm = tm.drop(['seg'], 1)
                    tm.insert(0,'id',id)
                    lb = labelDict[id]
                    tm['label'] = lb
                    m += 1
                else:
                    df = pd.read_csv(child, sep='\t', low_memory=False)
                    df = df.drop(['seg'], 1)
                    df.insert(0, 'id', id)
                    lb1 = labelDict[id]
                    df['label'] = lb1
                    tm = pd.concat([tm, df],ignore_index=True)
    except:
        pass

    X_t = tm.iloc[:, 1:14]
    X_t = pd.DataFrame(KNN(k=6).fit_transform(X_t))
    min_max_scaler = preprocessing.MinMaxScaler()
    X_train_minmax = min_max_scaler.fit_transform(X_t)

    dfa = pd.DataFrame(X_train_minmax,
                      columns=['chrom','num.mark','nhet', 'cnlr.median', 'mafR', 'segclust', 'cnlr.median.clust', 'mafR.clust', 'start', 'end', 'cf.em', 'tcn.em',
                               'lcn.em'])
    dfa.insert(0, 'id', tm['id'])
    dfa['label'] = tm['label']
    tm.to_csv(path + 'allFeatures.csv', index=False)
    dfa.to_csv(path+'allFeatures_s.csv',index=False)

# tpDataFile = 'C:/Users/Sherwin/Desktop/交大二HRD结果/all/S20111157FD01_S20111157FD01L01_AHVCV5DMXX_1T.cns'
# tp_reader = pd.read_csv(tpDataFile, sep='\t', low_memory=False)
# print(tp_reader['lcn.em'])
path = 'C:/Users/Sherwin/Desktop/交大二HRD结果/all/'

mergeFiles(path)
