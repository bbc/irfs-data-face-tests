#!/usr/bin/env python3
import pprint

import boto3

# Set this to whatever percentage of 'similarity'
# you'd want
SIMILARITY_THRESHOLD = 75.0

if __name__ == '__main__':
    client = boto3.client('rekognition')

    # Our source image: http://i.imgur.com/OK8aDRq.jpg
    with open('/Users/janae/data/elvisPMs_last100/Gordon_Brown/9242386.jpg', 'rb') as source_image:
        source_bytes = source_image.read()

    # Our target image: http://i.imgur.com/Xchqm1r.jpg
    with open('/Users/janae/data/elvisPMs_last100/Gordon_Brown/8892637.jpg', 'rb') as target_image:
        target_bytes = target_image.read()

    response = client.compare_faces(
                   SourceImage={ 'Bytes': source_bytes },
                   TargetImage={ 'Bytes': target_bytes },
                   SimilarityThreshold=SIMILARITY_THRESHOLD
    )

    pprint.pprint(response)
