#!/usr/bin/env python2
from __future__ import print_function
import os
import sys
import time
import requests
import cv2
import operator
import numpy as np
import json

try:
    _key = os.environ['MICROSOFT_VISION_KEY']
except:
    exit("MICROSOFT_VISION_KEY environment variable needs to be set")

#_url = 'https://api.projectoxford.ai/vision/v1/analyses'
_url = 'https://westus.api.cognitive.microsoft.com/vision/v1.0/analyze'
_maxNumRetries = 10

def processRequest( json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429: 

            print( "Message: %s" % ( response.json()['error']['message'] ) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print(response.json())
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()['error']['message'] ) )

        break
        
    return result

    
# Computer Vision parameters
# params = { 'visualFeatures' : 'Color,Categories'} 
params = { 'details' : 'Celebrities'} 

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/octet-stream'

ajson = None


pdir = '/Users/janae/data/elvisAll/elvis_notPM'
resDir = 'celeb_notPMs'
# PM found, PM not found, no face found, wrong PM found
pmRes = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
allfiles = [f for f in os.listdir(pdir) if os.path.isfile(os.path.join(pdir, f)) and not f[0]=='.' and f.endswith('jpg')]
for f in allfiles:
    ff = os.path.join(pdir, f)
    print(ff)
    resFile = os.path.join(resDir, f + '.json')
    foundPM = False
    foundWrong = False
    detectedFaces = []
    result = {}
    try:
        time.sleep(3.1)
        with open( ff, 'rb' ) as fr:
            data = fr.read()
        result = processRequest( ajson, data, headers, params )
    except:
        print("Unexpected error:", sys.exc_info()[0])
    with open(resFile, 'w') as outfile:
        json.dump(result, outfile)
