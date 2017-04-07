#!/usr/bin/env python2

import argparse
import os
import glob
import sys
import csv

import numpy as np
np.set_printoptions(precision=2)

from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import normalize

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--threshold', type=float, default=0.9)
    parser.add_argument('--delete', action='store_true', help='Delete the outliers.')
    parser.add_argument('--doSubDirs', action='store_true', help='Work on all direct subdirectories.')
    parser.add_argument('--duplicates', action='store_true', help='Identify duplicates rather than outliers.')
    parser.add_argument('--checkDirs', action='store_true', help='Check directories for high variance, indicating previous clean-up has not worked well.')
    parser.add_argument('directory')

    args = parser.parse_args()

    if args.duplicates and args.checkDirs:
        sys.exit("Combination of --duplicates and --checkDirs is not allowed.")

    if not os.path.isdir(args.directory):
        sys.exit("Input directory not found.")

    if args.doSubDirs:
        d = next(os.walk(args.directory))[1]
    else:
        #d = [args.directory]
        d = ['.']

    for thisdir in d:
        print("=== {} ===".format(os.path.join(args.directory, thisdir)))
        outliers = []
        duplicates = []
        featList = list()
        allfiles = os.listdir(os.path.join(args.directory, thisdir))
        allfilesFaces = list()
        for thisfile in allfiles:
            if thisfile.endswith(".seeta"):
                with open(os.path.join(args.directory, thisdir, thisfile), 'rb') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        row = np.vstack(row)
                        row = row.reshape(1, -1)
                        row = normalize(row, axis=1, norm='l2')
                        featList.append(row)
                        #multiple faces in a single image files
                        allfilesFaces.append(os.path.join(args.directory, thisdir, thisfile))
        if not featList:
            continue
        thisEmbeddings = np.vstack(featList)
        thisEmbeddings = thisEmbeddings.astype(np.float)
        if args.duplicates:
            for p1 in range(0, thisEmbeddings.shape[0]):
                for p2 in range(p1+1, thisEmbeddings.shape[0]):
                    dist = euclidean_distances(thisEmbeddings[p1].reshape(1, -1), thisEmbeddings[p2].reshape(1, -1))
                    if dist < args.threshold:
                        duplicates.append((allfilesFaces[p1], allfilesFaces[p2], dist))
            print("Found {} duplicate pairs from {} images.".format(len(duplicates), len(allfiles)))
            for p1, p2, dist in duplicates:
                print("{} - {}: {:0.4f}".format(p1, p2, dist[0][0]))
                if args.delete:
                    try:
                        os.remove(p2)
                    except OSError:
                        # might already be removed if 3 or more identials
                        print("could not remove: ", p2)
        elif args.checkDirs:
            std = np.std(thisEmbeddings, axis=0)
            #mean = np.mean(reps, axis=0)
            dists = euclidean_distances(thisEmbeddings, thisEmbeddings)
            o = np.std(dists)
            # little reduction of std in cleaned-up version after outlier removal could be a hint, 
            # but could also indicate perfect start, and would need keeping both directories
            # std < 0.2 means probably mostly images of one person, OK
            # std > 0.25 means probably images of two or more persons, not OK
            # std between 0.2 and 0.25 is a bit unclear, either a very varied face, or young to old, or multiple persons
            print(o)
        else:    
            #print(type(thisEmbeddings))
            #print(type(thisEmbeddings[0][0]))
            mean = np.mean(thisEmbeddings, axis=0)
            dists = euclidean_distances(thisEmbeddings, mean.reshape(1, -1))
            for path, dist in zip(allfilesFaces, dists):
                dist = dist.take(0)
                if dist > args.threshold:
                    outliers.append((path, dist))
            print("Found {} outlier(s) from {} images.".format(len(outliers), len(allfiles)))
            for path, dist in outliers:
                print(" + {} ({:0.2f})".format(path, dist))
                if args.delete:
                    try:
                        os.remove(path)
                    except:
                        a=3

if __name__ == '__main__':
    main()
