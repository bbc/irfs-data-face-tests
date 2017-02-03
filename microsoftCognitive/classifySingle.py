#!/usr/bin/env python2
import cognitive_face as CF
import os
import sys
import time

try:
    devKey = os.environ['MICROSOFT_DEV_KEY']
except:
    exit("MICROSOFT_DEV_KEY environment variable needs to be set")

CF.Key.set(devKey)

ff = '/Users/janae/data/elvisPMs_last100/Gordon_Brown/9242339.jpg'
print(ff)
try:
    detectedFaces = CF.face.detect(ff)
    for face in detectedFaces:
        print face
        res = CF.face.identify([face['faceId']], 'pms')
        time.sleep(4)
        for a in res:
            for b in a['candidates']:
                resPerson = CF.person.get('pms',b['personId'])
                resPerson = resPerson['name']
                print(resPerson)
except:
    print "Unexpected error:", sys.exc_info()[0]
