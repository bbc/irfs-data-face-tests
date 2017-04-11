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

f='mpSvm.pkl'
(le,clf) = pickle.load(open(f, 'rb'))

testPMs = ['Tony_Blair', 'Gordon_Brown', 'David_Cameron']
# PM found, PM not found, no face found, wrong PM found
pmRes = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
mydir=sys.argv[1]
for i in range(len(testPMs)):
    testperson = testPMs[i]
    thisdir = os.path.join(mydir, testperson)
    if not os.path.isdir(thisdir):
        print('dir does not exist!!!')
        continue
    for thisfile in os.listdir(thisdir):
        if thisfile.endswith(".seeta"):
            foundPM = False
            foundOther = False
            foundWrong = False
            with open(os.path.join(thisdir, thisfile), 'rb') as f:
                #reader = csv.reader(f)
                reader = csv.reader(f, delimiter=' ')
                for row in reader:
                    row = np.asarray(row)
                    row = row.reshape(1, -1)
                    row = normalize(row, axis=1, norm='l2')
                    maxI = clf.predict(row).ravel()
                    person = le.inverse_transform(maxI)
                    if person == testperson:
                        foundPM = True
                    elif person == 'unknown':
                        foundOther = True
                    else:
                        foundWrong = True
                        print(thisfile, person)
                if foundPM:
                    pmRes[i][0] += 1
                if foundOther:
                    pmRes[i][1] += 1
                #if len(reps) == 0:
                #    pmRes[i][2] += 1
                if foundWrong:
                    pmRes[i][3] += 1


print(pmRes)
for i in range(len(testPMs)):
    print("%s, %1.2f, %1.2f, %d, %d" % (testPMs[i], pmRes[i][0], pmRes[i][0]/(100.0-pmRes[i][2])*100.0, 100-pmRes[i][2], pmRes[i][3]))


