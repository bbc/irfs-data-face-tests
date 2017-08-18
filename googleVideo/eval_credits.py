#!/usr/bin/python

import csv
import json
import pandas as pd
import os
import re
import sys
import glob
import datetime
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz

prog = '19631207-000000-dr-who-h264lg-eastwood'

decade = '1960s'

roles = ('Crew description', 'Person name', 'Character name', 'Other description')
found = [0, 0, 0, 0]
notFound = [0, 0, 0, 0]
found_perFile = np.empty(shape=[0, 4])
pf = [0,0,0,0]
xl = pd.ExcelFile('50 x Programme Credits ground truth.xlsx')

overview = xl.parse('Sheet1')
for i in range(0, len(overview.index)):
    longTitle = overview.iloc[i,1]
    print('longTitle: ' + longTitle)
    #find date, space ddmmyyyy space
    searchObj = re.search( ' [0-9]{8} ', longTitle)
    date = searchObj.group().strip()
    date = date[4:]+date[2:4]+date[0:2]
    #name not always corresponding to excel sheet name
    #df = xl.parse(longTitle[0:31])
    #print(xl.sheet_names[i+1])
    gt = xl.parse(xl.sheet_names[i+1], keep_default_na=False)
    dtFile = glob.glob('*/*' + date + '*.json')
    if len(dtFile) != 1:
        print('WARNING, no detections found')
        continue
    print('detection file: ' + dtFile[0])
    with open(dtFile[0]) as json_data:
        dt = json.load(json_data)

    found_this = [0, 0, 0, 0]
    notFound_this = [0, 0, 0, 0]
    for roleIdx in range(0, len(roles)):
        for gtIdx, this_gt in enumerate(gt.iloc[:,roleIdx+2]):
            if not(this_gt):
                continue
            if isinstance(this_gt, (int, float)):
                this_gt = str(this_gt)
            #if isinstance(this_gt, datetime.datetime):
            #    print(this_gt)
            #    this_gt = str(this_gt)
            # trying to fix in excel
            this_gt = this_gt.upper()
            this_found = False
            for this_dt in dt['ocrResults']:
                i1 = this_dt['output'].find(this_gt)
                #i2 = fuzz.partial_ratio(this_gt, this_dt['output'])
                #if i2 >= 100 and not i1>=0:
                #    print(this_gt, this_dt['output'], i1, i2)
                #if i2 >= 100:
                if i1 >= 0:
                    #    print(this_gt, this_dt['output'], i)
                    this_found = True
                    break
            if this_found:
                found[roleIdx] += 1
                found_this[roleIdx] += 1
            else:
                notFound[roleIdx] += 1
                notFound_this[roleIdx] += 1
                #if roleIdx < 3:
                 #   print('gt not found: {}, role: {}, orientiation: {}'.format(this_gt, roles[roleIdx], gt.iloc[gtIdx,1]))
    for i in range(0,4):
        if found_this[i] + notFound_this[i] > 0:
            pf[i] = float(found_this[i]) / float(found_this[i] + notFound_this[i]) *100.
        else:
            pf[i] = np.nan
    print(pf)
    found_perFile = np.vstack((found_perFile, pf))

print(roles)
print(found)
print(notFound)
p = [0,0,0,0]
for i in range(0,4):
    p[i] = float(found[i]) / float(found[i] + notFound[i]) * 100
print(p)
    
    
#print(found_perFile)
y_pos = np.arange(len(found_perFile[:,1]))
plt.bar(y_pos, found_perFile[:,1])
plt.show()
