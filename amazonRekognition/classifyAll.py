#!/usr/bin/env python3
import pprint
import os
import boto3
import sys
from collections import Counter
from PIL import Image

if __name__ == '__main__':
    client = boto3.client('rekognition')
    pdir = '/Users/janae/data/elvisPMs_last100'
    testPMs = ['David_Cameron', 'Gordon_Brown', 'Tony_Blair']
    thres = 98.5
    print('threshold: ', thres)
    # PM found, PM not found, no face found, wrong PM found
    pmRes = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for i in range(len(testPMs)):
        pm = testPMs[i]
        #allfiles = [f for f in os.listdir(os.path.join(pdir, pm)) if os.path.isfile(os.path.join(pdir, pm , f)) and not f[0]=='.' and f.endswith('jpg')]
        allfiles = [f for f in os.listdir(os.path.join(pdir, pm)) if os.path.isfile(os.path.join(pdir, pm , f)) and not f[0]=='.' and f.endswith('13069907.jpg')]
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
                    print(ff, 'error reading image bytes')
                    continue
            with Image.open(ff) as im:
                imw, imh = im.size
                #print('size: ', imw, imh)
                try:
                    resDetect = client.detect_faces(
                        Image={ 'Bytes': source_bytes }
                    )
                except:
                    print(ff, 'could not detect faces')
                    foundFace = False
                    continue
                    #print(pprint.pprint(resDetect))
                for searchface in resDetect['FaceDetails']:
                    allfound = []
                    #print('BoundingBox:')
                    #print(pprint.pprint(searchface))
                    # seems they use at least one of Pitch, Roll, Yaw for image alignment
                    # giving up on this!!!
                    #bounding boxes are percentages
                    bbh = searchface['BoundingBox']['Height']
                    bbl = searchface['BoundingBox']['Left']
                    bbt = searchface['BoundingBox']['Top']
                    bbw = searchface['BoundingBox']['Width']
                    #crop needs The box is a 4-tuple defining the left, upper, right, and lower pixel coordinate
                    bbh = int(bbh * imh)
                    bbl = int(bbl * imw)
                    bbt = int(bbt * imh)
                    bbw = int(bbw * imw)
                    #print('imbox:', bbh, bbl, bbt, bbw)
                    cropFace = im.crop((bbl, bbt, bbl+bbw, bbt+bbh))
                    cropFace.save('tmp.jpg')
                    with open('tmp.jpg', 'rb') as source_image:
                        try:
                            source_bytes = source_image.read()
                        except:
                            print('error reading tmp image bytes')
                            continue
                    try:
                        resReco = client.search_faces_by_image(
                            CollectionId='PMs_google',
                            Image={ 'Bytes': source_bytes },
                            FaceMatchThreshold = thres
                        )
                    except:
                        print(ff, 'no face found in extracted face')
                        continue
                    #print(pprint.pprint(resReco))
                    for face in resReco['FaceMatches']:
                        #print(face['Face']['ExternalImageId'], face['Similarity'])
                        allfound.append(face['Face']['ExternalImageId'])
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
