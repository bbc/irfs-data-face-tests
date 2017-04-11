#!/usr/bin/env python2

import argparse
import os
from operator import itemgetter
import re
import numpy as np
from sklearn.preprocessing import LabelEncoder, normalize
from sklearn.svm import SVC, LinearSVC
import pickle
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.neighbors import KNeighborsClassifier
import sys
import csv

t=sys.argv[1]
print(t)
f='mpSvm.pkl'
(le,clf) = pickle.load(open(f, 'rb'))
with open(t, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        row = np.asarray(row)
        row = row.reshape(1, -1)
        row = normalize(row, axis=1, norm='l2')
        maxI = clf.predict(row).ravel()
        person = le.inverse_transform(maxI)
        print(person)

