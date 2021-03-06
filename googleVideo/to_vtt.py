#!/usr/bin/env python

import csv
import json

def to_ts(nanoseconds):
    seconds = nanoseconds / 1000000.0
    if (seconds % 60) < 10:
        remaining_seconds = '0%05.3f' % (seconds % 60)
    else:
        remaining_seconds = '%05.3f' % (seconds % 60)
    minutes = seconds / 60
    remaining_minutes = '%02d' % (minutes % 60)
    hours = '%02d' % (minutes / 60)
    return '%s:%s:%s' % (hours,remaining_minutes,remaining_seconds)

with open("londonNews1_label.json", "rb") as f:
    rd = json.load(f)

cues = {}
timestamps = []
one_frame = 1. / 25.

for anRes in rd['response']['annotationResults']:
    #print(json.dumps(anRes, indent=2, sort_keys=True))
    for labRes in anRes['labelAnnotations']:
        label = labRes['description']
        for labTime in labRes['locations']:
            begins = labTime['segment']['startTimeOffset']
            begins = to_ts(float(begins))
            ends = labTime['segment']['endTimeOffset']
            ends = to_ts(float(ends))
            interval = "%s --> %s" % (begins, ends)
            if interval not in cues:
                cues[interval] = []
                timestamps.append(interval)
            cues[interval].append({'label': label})

print "WEBVTT FILE"

for i in timestamps:
    print ""
    print i
    print json.dumps(cues[i])
