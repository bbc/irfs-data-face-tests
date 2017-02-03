#!/usr/bin/env python3
import pprint
import os
import boto3

if __name__ == '__main__':
    client = boto3.client('rekognition')
    response = client.list_faces(
        CollectionId='PMs_google2'
    )
    for face in response['Faces']:
        if face['ExternalImageId'].startswith('test'):
            print(face['FaceId'] )
            print(face['ExternalImageId'])
            response = client.delete_faces( CollectionId='PMs_google2', FaceIds=[ face['FaceId'] ])
            print(response)

