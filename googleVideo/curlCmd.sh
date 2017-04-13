curl -s -k -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer <TOKEN>' \
    'https://videointelligence.googleapis.com/v1beta1/videos:annotate' \
    -d @annotate-video-request.json
