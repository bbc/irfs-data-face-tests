#!/usr/bin/env python2
import cognitive_face as CF
import os

try:
    devKey = os.environ['MICROSOFT_DEV_KEY']
except:
    exit("MICROSOFT_DEV_KEY environment variable needs to be set")

CF.Key.set(devKey)

filename = '/Users/janae/data/elvisPMs_last100/David_Cameron/13069907.jpg'
filename2 = '/Users/janae/data/PMs/David_Cameron/0.jpg'
#filename2 = '/Users/janae/data/PMs_aligned_manCleanTGD/David_Cameron/0.png'

result = CF.face.detect(filename)
result2 = CF.face.detect(filename2)
for face in result:
    print face['faceId']
    for face2 in result2:
        print face2['faceId']
        v = CF.face.verify(face['faceId'], face2['faceId'])
        print(v)

