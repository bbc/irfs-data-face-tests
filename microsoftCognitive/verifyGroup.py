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

trainDir = '/Users/janae/data/PMs'

# delete for clean start
CF.person_group.delete('pms')
#only do once
if not CF.person_group.lists():
    CF.person_group.create('pms')
    with open('listPrimeMinisters.txt') as f:
        for person in f:
            person = person.strip()
            print(person)
            # will recreate same name with different ID, only do once
            CF.person.create('pms', person)
else:
    print('pm group already exists, doing nothing')

time.sleep(60)
persons = CF.person.lists('pms')
for p in persons:
    pname = (p['name'])
    print(pname)
    pname = pname.replace(' ', '_')
    pdir = os.path.join(trainDir, pname)
    allfiles = [f for f in os.listdir(pdir) if os.path.isfile(os.path.join(pdir, f))]
    for f in allfiles:
        ff = os.path.join(pdir, f)
        print(ff)
        try:
            CF.person.add_face(ff, 'pms', p['personId'])
        except:
            # no face or more than one face ignored
            # it would be possible to do face detect first
            #   and then take largest face
            print "Unexpected error:", sys.exc_info()[0]
        time.sleep(4)

#testPMs = ['David_Cameron', 'Gordon_Brown', 'Tony_Blair']
#result = CF.face.detect(filename)
#result2 = CF.face.detect(filename2)
#for face in result:
#    print face['faceId']
#    for face2 in result2:
#        print face2['faceId']
#        v = CF.face.verify(face['faceId'], face2['faceId'])
#        print(v)

