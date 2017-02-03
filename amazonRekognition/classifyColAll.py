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
    #testPMs = ['David_Cameron']
    thres = 80
    maxNum = 100
    colId = 'PMs_google2'
    print('threshold: ', thres)
    print('maxNum: ', maxNum)
    print('collection ID: ', colId)
    # PM found, PM not found, no face found, wrong PM found
    pmRes = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for i in range(len(testPMs)):
        pm = testPMs[i]
        allfiles = [f for f in os.listdir(os.path.join(pdir, pm)) if os.path.isfile(os.path.join(pdir, pm , f)) and not f[0]=='.' and f.endswith('jpg')]
        #allfiles = [f for f in os.listdir(os.path.join(pdir, pm)) if os.path.isfile(os.path.join(pdir, pm , f)) and not f[0]=='.' and f.endswith('14626090.jpg')]
        for f in allfiles:
            ff = os.path.join(pdir, pm, f)
            #ff = '/Users/janae/data/desk.jpg'
            #print(ff)
            foundPM = False
            foundWrong = False
            foundFace = True
            with open(ff, 'rb') as source_image:
                try:
                    source_bytes = source_image.read()
                except:
                    print('error reading image')
                    continue
            try:
            #if True:
                resDet = client.index_faces(
                    CollectionId=colId,
                    Image={ 'Bytes': source_bytes },
                    ExternalImageId='test_' + ff.replace('/', '_')
                )
                #print('resDet')
                #pprint.pprint(resDet)
                #print('--------')
                for faceDet in resDet['FaceRecords']:
                    #print('--------------')
                    #pprint.pprint(faceDet)
                    #print(faceDet['Face'])
                    #print(faceDet['Face']['BoundingBox'])
                    #print(faceDet['Face']['FaceId'])

                    try:
                        res = client.search_faces(
                            CollectionId=colId,
                            FaceId = faceDet['Face']['FaceId'],
                            MaxFaces=maxNum,
                            FaceMatchThreshold = thres
                        )
                    except:
                        print("faceId: ", faceDet['Face']['FaceId'])
                        print("Unexpected error:", sys.exc_info()[0])
                        sys.exit(0)
                    #print('res')
                    #pprint.pprint(res)
                    allfound = []
                    for face in res['FaceMatches']:
                        #print(face['Face']['ExternalImageId'], face['Similarity'])
                        if not face['Face']['ExternalImageId'].startswith('test'):
                            allfound.append(face['Face']['ExternalImageId'])
                    if allfound:
                        #print('allfound: ', allfound)
                        c = Counter(allfound)
                        foundPerson = c.most_common(1)[0][0]
                        if foundPerson == pm:
                            foundPM = True
                        else:
                            foundWrong = True
                            print(ff, foundPerson)

                    # delete this image - has to be delete face, not image
                    #print('delete res')
                    response = client.delete_faces(
                        CollectionId=colId,
                        FaceIds= [faceDet['Face']['FaceId']]
                    )
                    #print(response)
            except:
                #print(ff, 'could not classify image')
                #print("Unexpected error:", sys.exc_info()[0])
                foundFace = False

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
