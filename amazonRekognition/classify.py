#!/usr/bin/env python3
import pprint
import os
import boto3
import sys
from collections import Counter

if __name__ == '__main__':
    client = boto3.client('rekognition')
    pdir = '/Users/janae/data/elvisPMs_last100'
    testPMs = ['David_Cameron', 'Gordon_Brown', 'Tony_Blair']
    thres = 50
    colId = 'PMs_google2'
    print('threshold: ', thres)
    print('collectionId: ', colId)
    # PM found, PM not found, no face found, wrong PM found
    pmRes = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for i in range(len(testPMs)):
        pm = testPMs[i]
        allfiles = [f for f in os.listdir(os.path.join(pdir, pm)) if os.path.isfile(os.path.join(pdir, pm , f)) and not f[0]=='.' and f.endswith('jpg')]
        #allfiles = [f for f in os.listdir(os.path.join(pdir, pm)) if os.path.isfile(os.path.join(pdir, pm , f)) and not f[0]=='.' and f.endswith('13657111.jpg')]
        for f in allfiles:
            ff = os.path.join(pdir, pm, f)
            #ff = '/Users/janae/data/desk.jpg'
            #print(ff)
            foundPM = False
            foundWrong = False
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
                # TODO: do face det first!
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
            #print(allfound)
            if allfound:
                c = Counter(allfound)
                foundPerson = c.most_common(1)[0][0]
                if foundPerson == pm:
                    foundPM = True
                else:
                    foundWrong = True
                    print(ff, foundPerson)
            if foundPM:
                pmRes[i][0] += 1
            if not foundFace:
                pmRes[i][2] += 1
            if foundWrong:
                pmRes[i][3] += 1
print(pmRes)
# PM found, PM not found, no face found, wrong PM found
for i in range(len(testPMs)):
            print("%s, %1.2f, %1.2f, %d, %d" % (testPMs[i], pmRes[i][0], pmRes[i][0]/(100.0-pmRes[i][2])*100.0, 100-pmRes[i][2], pmRes[i][3]))
