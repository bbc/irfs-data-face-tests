#!/usr/bin/env python2
import os
import sys
import time
import json

pdir = 'celeb_notPMs'
allfiles = [f for f in os.listdir(pdir) if os.path.isfile(os.path.join(pdir, f)) and not f[0]=='.' and f.endswith('jpg.json')]
for f in allfiles:
    ff = os.path.join(pdir, f)
    print(ff)
    with open(ff) as json_data:
        res = json.load(json_data)
        #print(res)
        if 'categories' in res:
            for face in res['categories']:
                #print(face)
                if 'detail' in face:
                    detectedFaces = True
                    for celebPerson in face['detail']['celebrities']:
                        resPerson = celebPerson['name'].lower()
                        print(resPerson)
