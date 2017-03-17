#!/usr/bin/env python2
import cognitive_face as CF
import os
import sys
import time


try:
    devKey = os.environ['MICROSOFT_DEV_KEY']
except:
    exit("MICROSOFT_DEV_KEY environment variable needs to be set")

time.sleep(3.1)
CF.Key.set(devKey)
#CF.person_group.train('pms2')
#sys.exit(0)


pdir = '/Users/janae/data/elvisPMs_last100'
testPMs = ['David_Cameron', 'Gordon_Brown', 'Tony_Blair']
# PM found, PM not found, no face found, wrong PM found
pmRes = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
for i in range(len(testPMs)):
    pm = testPMs[i]
    allfiles = [f for f in os.listdir(os.path.join(pdir, pm)) if os.path.isfile(os.path.join(pdir, pm , f)) and not f[0]=='.' and f.endswith('jpg')]
    for f in allfiles:
        ff = os.path.join(pdir, pm, f)
        print(ff)
        foundPM = False
        foundWrong = False
        detectedFaces = []
        try:
            time.sleep(3.1)
            detectedFaces = CF.face.detect(ff)
            for face in detectedFaces:
                time.sleep(3.1)
                res = CF.face.identify([face['faceId']], 'pms2')
                for a in res:
                    for b in a['candidates']:
                        time.sleep(3.1)
                        resPerson = CF.person.get('pms2',b['personId'])
                        resPerson = resPerson['name']
                        print(resPerson)
                        if resPerson.replace(' ', '_') == pm:
                            foundPM = True
                        else:
                            foundWrong = True
        except:
            print "Unexpected error:", sys.exc_info()[0]
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
