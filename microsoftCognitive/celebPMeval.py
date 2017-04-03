#!/usr/bin/env python2
import os
import sys
import time
import json

pdir = 'celebPMs'
testPMs = ['David_Cameron', 'Gordon_Brown', 'Tony_Blair']
# PM found, PM not found, no face found, wrong PM found
pmRes = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
for i in range(len(testPMs)):
    pm = testPMs[i]
    #print(pm)
    allfiles = [f for f in os.listdir(os.path.join(pdir, pm)) if os.path.isfile(os.path.join(pdir, pm , f)) and not f[0]=='.' and f.endswith('jpg.json')]
    for f in allfiles:
        ff = os.path.join(pdir, pm, f)
        foundPM = False
        foundWrong = False
        detectedFaces = False
        with open(ff) as json_data:
            res = json.load(json_data)
            #print(res)
            print(ff)
            if 'categories' in res:
                for face in res['categories']:
                    #print(face)
                    if 'detail' in face:
                        detectedFaces = True
                        for celebPerson in face['detail']['celebrities']:
                            resPerson = celebPerson['name'].lower()
                            if resPerson.replace(' ', '_') == pm.lower():
                                foundPM = True
                            else:
                                foundWrong = True
                                print(resPerson)
        if foundPM:
            pmRes[i][0] += 1
        if not detectedFaces:
            pmRes[i][2] += 1
        if foundWrong:
            pmRes[i][3] += 1
        #sys.exit(1)
print(pmRes)
for i in range(len(testPMs)):
            print("%s, %1.2f, %1.2f, %d, %d" % (testPMs[i], pmRes[i][0], pmRes[i][0]/(100.0-pmRes[i][2])*100.0, 100-pmRes[i][2], pmRes[i][3]))
