#!/usr/bin/env python3
import pprint
import os
import boto3

if __name__ == '__main__':
    client = boto3.client('rekognition')
    
    colId = 'PMs_google'
    trainDir = '/Users/janae/data/PMs'
    response = client.delete_collection( CollectionId=colId)
    response = client.create_collection( CollectionId=colId)
    #pprint.pprint(response)
    with open('listPrimeMinisters.txt') as l:
        for p in l:
            pname = p.strip()
            pname = pname.replace(' ', '_')
            print(pname)
            pdir = os.path.join(trainDir, pname)
            allfiles = [f for f in os.listdir(pdir) if os.path.isfile(os.path.join(pdir, f)) and not f[0]=='.' ]
            for f in allfiles:
                ff = os.path.join(pdir, f)
                print(ff)
                with open(ff, 'rb') as source_image:
                    try:
                        source_bytes = source_image.read()
                    except:
                        print('error reading image')
                        continue
                try:
                    response = client.index_faces(
                        CollectionId=colId,
                        Image={ 'Bytes': source_bytes },
                        ExternalImageId=pname
                    )
                except:
                    print('could not upload image')



    response = client.list_faces(
        CollectionId=colId
    )
    pprint.pprint(response)

