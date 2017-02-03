#!/usr/bin/env python3
import pprint
import os
import boto3
import sys
from collections import Counter

if __name__ == '__main__':
    client = boto3.client('rekognition')
    pdir = '/Users/janae/data/elvis_notPM'
    thres = 50
    colId = 'PMs_google2'
    print('threshold: ', thres)
    print('collectionId: ', colId)
    # no PM found, no face found, wrong PM found
    pmRes = [0,0,0]
    allfiles = [f for f in os.listdir(pdir) if os.path.isfile(os.path.join(pdir, f)) and not f[0]=='.' and f.endswith('jpg')]
    for f in allfiles:
        ff = os.path.join(pdir, f)
        #ff = '/Users/janae/data/desk.jpg'
        #ff = '/Users/janae/data/elvisPMs/David_Cameron/10326689.jpg'
        #print(ff)
        foundPM = False
        foundFace = True
        allfound = []
        with open(ff, 'rb') as source_image:
            try:
                source_bytes = source_image.read()
            except:
                print('error reading image')
                continue
        try:
            # serch based on largest face only
            res = client.search_faces_by_image(
                CollectionId=colId,
                Image={ 'Bytes': source_bytes },
                FaceMatchThreshold = thres
            )
            #pprint.pprint(res)
            for face in res['FaceMatches']:
                #print(face['Face']['ExternalImageId'], face['Similarity'])
                allfound.append(face['Face']['ExternalImageId'])
        except:
            #print(ff, 'could not classify image')
            foundFace = False
        if allfound:
            print(ff)
            print(allfound)
            c = Counter(allfound)
            foundPerson = c.most_common(1)[0][0]
            foundPM = True
        # no PM found, no face found, wrong PM found
        if not foundPM:
            pmRes[0] += 1
        if foundPM:
            pmRes[2] += 1
        if not foundFace:
            pmRes[1] += 1

print("no PM found, no face found, PM found wrong")
print(pmRes)
