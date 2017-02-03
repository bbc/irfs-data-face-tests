#!/usr/bin/env python3

from watson_developer_cloud import VisualRecognitionV3 as vr
import json
import os
import sys

try:
    devKey = os.environ['IBM_DEV_KEY']
except:
    exit("IBM_DEV_KEY environment variable needs to be set")

instance = vr(api_key=devKey, version='2017-01-24')

elvisTestDir='/Users/janae/data/elvisPMs_last100'
#testPMs = ['Tony_Blair', 'Gordon_Brown', 'David_Cameron']
testPMs = ['David_Cameron']
# PM found, PM not found, no face found, wrong PM found
pmRes = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
nameUnknown = 'unknown'

for i in range(len(testPMs)):
    testperson = testPMs[i]
    print(os.path.join(elvisTestDir, testperson))
    allImg = [os.path.join(elvisTestDir, testperson, f) for f in os.listdir(os.path.join(elvisTestDir, testperson)) if os.path.isfile(os.path.join(elvisTestDir, testperson, f)) and f.endswith(".jpg")]
    for imgFile in allImg:
        print(imgFile)
        with open(imgFile, 'rb') as f:
            foundPM = False
            foundOther = False
            foundWrong = False
            foundFace = False
            try:
                res = instance.detect_faces(images_file=f)
                if 'faces' in res['images'][0]:
                    foundFace = True
                    for thisface in res['images'][0]['faces']:
                        #print(thisface)
                        if 'identity' in thisface:
                            foundName = thisface['identity']['name']
                            if foundName.replace(' ', '_') == testperson:
                                foundPM = True
                            else:
                                #foundWrong = True
                                print(foundName)
                else:
                    print('no face found')

            except:
                print("Unexpected error:", sys.exc_info())

            if foundPM:
                pmRes[i][0] += 1
            if foundOther:
                pmRes[i][1] += 1
            if not foundFace:
                pmRes[i][2] += 1
            if foundWrong:
                pmRes[i][3] += 1
            break
        
print(pmRes)   
# PM found, PM not found, no face found, wrong PM found
for i in range(len(testPMs)):
            print("%s, %1.2f, %1.2f, %d, %d" % (testPMs[i], pmRes[i][0], pmRes[i][0]/(100.0-pmRes[i][2])*100.0, 100-pmRes[i][2], pmRes[i][3]))
