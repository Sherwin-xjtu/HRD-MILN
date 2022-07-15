# -*-coding:utf-8-*-
from __future__ import division

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

testFile = 'H:/DATA/CNV/NA10851/NA10851.mapped.ILLUMINA.bwa.CEU.exome.20130415.tsv'
tp_reader = pd.read_csv(testFile, low_memory=False,sep='\t')
x = tp_reader['pos']
y = tp_reader['depth']
plt.plot(x,y)
plt.show()