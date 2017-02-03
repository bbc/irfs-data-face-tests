#!/usr/bin/env python3

from watson_developer_cloud import VisualRecognitionV3 as vr
import json
import os

try:
    devKey = os.environ['IBM_DEV_KEY']
except:
    exit("IBM_DEV_KEY environment variable needs to be set")

instance = vr(api_key=devKey, version='2017-01-24')


imgFile='/Users/janae/data/elvisPMs_last100/Gordon_Brown/Archive.zip'
with open(imgFile, 'rb') as f:
    res = instance.detect_faces(images_file=f)
    print(res)
