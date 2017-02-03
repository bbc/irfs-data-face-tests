#!/usr/bin/env python3
import pprint
import os
import boto3

if __name__ == '__main__':
    client = boto3.client('rekognition')

    trainDir = '/Users/janae/data/PMs2'
    response = client.delete_collection( CollectionId='PMs_google2')
    response = client.create_collection( CollectionId='PMs_google2')
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
                        CollectionId='PMs_google2',
                        Image={ 'Bytes': source_bytes },
                        ExternalImageId=pname
                    )
                except:
                    print('could not upload image')



    response = client.list_faces(
        CollectionId='PMs_google2'
    )
    pprint.pprint(response)

