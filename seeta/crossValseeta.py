#!/usr/bin/env python2

import argparse
import os
from operator import itemgetter
import re
import numpy as np
from sklearn.preprocessing import LabelEncoder, normalize
from sklearn.svm import SVC, LinearSVC
import pickle
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.neighbors import KNeighborsClassifier
import sys
import csv

fileDir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def sortFilesNum(ss):
    s = ss[0]
    filenum = os.path.splitext(os.path.basename(s))[0]
    filedir = os.path.split(os.path.dirname(s))[1]
    try:
        f = float(filenum)
    except:
        f = 0
    return filedir, float(f)

def getOtherTrain(args):
    trainLabels = list()
    featList = list()
    # find all corresponding files
    thisdir = args.otherDir
    for thisfile in os.listdir(thisdir):
        if thisfile.endswith(".seeta"):
            with open(os.path.join(thisdir, thisfile), 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    featList.append(row)
    thisEmbeddings = np.vstack(featList)
    thisLabels = [args.nameUnknown] * thisEmbeddings.shape[0]
    return thisEmbeddings, thisLabels

def getGoogleTrain(args):
    trainLabels = list()
    #trainEmbeddings = np.array(0)
    firstTrain = 0
    with open(args.peopleList) as plist:
        for pl in plist:
            thisp = pl.replace(' ', '_')
            thisp = thisp.strip()
            #print(thisp)
            thisFileNames = list()
            #thisEmbeddings = np.array()
            firstRow = 0
            # find all corresponding files
            thisdir = os.path.join(args.googleDir, thisp)
            for thisfile in os.listdir(thisdir):
                if thisfile.endswith(".seeta"):
                    with open(os.path.join(thisdir, thisfile), 'rb') as f:
                        reader = csv.reader(f)
                        for row in reader:
                            if firstRow:
                            #if thisEmbeddings.any():
                                thisEmbeddings = np.vstack((thisEmbeddings, row))
                            else:
                                thisEmbeddings = row
                                firstRow = 1
                   
            #print(thisEmbeddings.shape)
            #print(thisFileNames)
            trainLabels.extend([thisp] * thisEmbeddings.shape[0])
            if firstTrain:
                trainEmbeddings = np.vstack((trainEmbeddings, thisEmbeddings))
            else:
                trainEmbeddings = thisEmbeddings
                firstTrain = 1
    return trainEmbeddings, trainLabels

def getElvisTrain(args):
    trainLabels = list()
    firstTrain = 0
    with open(args.peopleList) as plist:
        for pl in plist:
            thisp = pl.replace(' ', '_')
            thisp = thisp.strip()
            #print(thisp)
            thisFileNames = list()
            # find all corresponding files
            thisdir = os.path.join(args.elvisDir, thisp)
            #print(thisdir)
            featList = list()
            if not os.path.exists(thisdir):
                continue
            for thisfile in os.listdir(thisdir):
                if thisfile.endswith(".seeta"):
                    with open(os.path.join(thisdir, thisfile), 'rb') as f:
                        reader = csv.reader(f)
                        for row in reader:
                            featList.append(row)
                   
            thisEmbeddings = np.vstack(featList)
            #print(thisEmbeddings.shape)
            #print(thisFileNames)
            if thisEmbeddings.ndim == 2:
                trainLabels.extend([thisp] * thisEmbeddings.shape[0])
            elif thisEmbeddings.ndim == 1:
                trainLabels.extend([thisp])
            else:
                sys.exit('wrong dim for thisEmbeddings')
            #print(len(trainLabels))
            if firstTrain:
                trainEmbeddings = np.vstack((trainEmbeddings, thisEmbeddings))
            else:
                trainEmbeddings = thisEmbeddings
                firstTrain = 1
            #print(trainEmbeddings.shape)
    return trainEmbeddings, trainLabels

def testElvis(args, le, clf, testPMs):
    # PM found, PM not found, no face found, wrong PM found
    pmRes = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    # read reps from 100 images, pre-computed
    for i in range(len(testPMs)):
        testperson = testPMs[i]
        thisdir = os.path.join(args.elvisTestDir, testperson)
        for thisfile in os.listdir(thisdir):
            if thisfile.endswith(".seeta"):
                foundPM = False
                foundOther = False
                foundWrong = False
                with open(os.path.join(thisdir, thisfile), 'rb') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        row = np.asarray(row)
                        row = row.reshape(1, -1)
                        row = normalize(row, axis=1, norm='l2')
                        #nb=clf.radius_neighbors(row);
                        #print(nb[0])
                        #print(nb[1])
                        #for n in nb[1]:
                        #    print(le.inverse_transform(n))
                        maxI = clf.predict(row).ravel()
                        person = le.inverse_transform(maxI)
                        #sys.exit()
                        confidence = 0
                        if person == testperson:
                            foundPM = True
                        elif person == args.nameUnknown:
                            foundOther = True
                        else:
                            foundWrong = True
                            print(thisfile, person)
                if foundPM:
                    pmRes[i][0] += 1
                if foundOther:
                    pmRes[i][1] += 1
                #if len(reps) == 0:
                #    pmRes[i][2] += 1
                if foundWrong:
                    pmRes[i][3] += 1
    return pmRes

def testElvisNotPm(args, le, clf ):
    pmRes = [0,0]
    thisdir = args.notPMDir

    for thisfile in os.listdir(thisdir):
        if thisfile.endswith(".seeta"):
            foundPM = False
            with open(os.path.join(thisdir, thisfile), 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    row = np.asarray(row)
                    row = row.reshape(1, -1)
                    row = normalize(row, axis=1, norm='l2')
                    #nb=clf.radius_neighbors(row);
                    maxI = clf.predict(row).ravel()
                    person = le.inverse_transform(maxI)

                    if not person == args.nameUnknown:
                        print('notPMs: ', thisfile, person)
                        foundPM = True
                if not foundPM:
                    pmRes[0] += 1
                if foundPM:
                    pmRes[1] += 1

    return pmRes


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--googleDir', type=str)
    parser.add_argument('--elvisDir', type=str)
    parser.add_argument('--elvisTestDir', type=str)
    parser.add_argument('--notPMDir', type=str)
    parser.add_argument('--peopleList', type=str, help="list of people, e.g. listPrimeMinisters.txt")
    parser.add_argument('--nameUnknown', type=str, help="'Other' class, e.g. notPM")
    parser.add_argument('--otherDir', type=str)
    parser.add_argument('--classifier', type=str, help="'radius', 'svm'")
    parser.add_argument('--saveClassifier', type=str, help="filename")

    args = parser.parse_args()

    trainEmbeddings = np.array([])
    trainLabels = []

    if args.googleDir:
        print('load google train')
        googleTrainEmbeddings, googleTrainLabels = getGoogleTrain(args)    
        trainEmbeddings = googleTrainEmbeddings
        trainLabels = googleTrainLabels 

    if args.elvisDir:
        print('load elvis train')
        elvisTrainEmbeddings, elvisTrainLabels = getElvisTrain(args)    
        trainEmbeddings = np.vstack([trainEmbeddings, elvisTrainEmbeddings]) if trainEmbeddings.size else elvisTrainEmbeddings
        trainLabels = trainLabels + elvisTrainLabels


    if args.classifier == 'radius':
        print('no lfw')
    elif args.classifier == 'svm' or args.classifier == 'linearSVC':
        print('with lfw')
        print('load other train')
        otherTrainEmbeddings, otherTrainLabels = getOtherTrain(args)    
        trainEmbeddings = np.vstack((trainEmbeddings, otherTrainEmbeddings))
        trainLabels = trainLabels + otherTrainLabels 
        
    otherLabel = args.nameUnknown
    le = LabelEncoder().fit(trainLabels + [otherLabel])

    #norm
    print('normalise')
    trainEmbeddings = normalize(trainEmbeddings, axis=1, norm='l2')

    # training
    testPMs = ['Tony_Blair', 'Gordon_Brown', 'David_Cameron']
    labelsNum = le.transform(trainLabels)
    nClasses = len(le.classes_)
    #print(nClasses)
    #clf = SVC(C=1, kernel='linear', probability=True)
    if args.classifier == 'radius':
        weights = 'uniform'
        #weights = 'distance'
        #for radius in [39]:
        #for radius in [0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89]:
        for radius in np.arange(0.6,0.8,0.2):
            print(radius, weights)
            outl = args.nameUnknown
            outl = outl.split()
            outl = le.transform(outl)
            clf = RadiusNeighborsClassifier(radius, weights=weights, outlier_label=outl)
            #clf = KNeighborsClassifier(n_neighbors=5, weights='distance')
            clf.fit(trainEmbeddings, labelsNum)
            #print('trainEmbeddings:', trainEmbeddings.shape)
            notPmRes = testElvisNotPm(args, le, clf )
            pmRes = testElvis(args, le, clf, testPMs)
            #print('PM found, PM not found, no face found, wrong PM found')
            print(pmRes)
            for i in range(len(testPMs)):
                print("%s, %1.2f, %1.2f, %d, %d" % (testPMs[i], pmRes[i][0], pmRes[i][0]/(100.0-pmRes[i][2])*100.0, 100-pmRes[i][2], pmRes[i][3]))
            print('not PMs:')
            print(notPmRes)
    elif args.classifier == 'svm' or args.classifier == 'linearSVC':
        if args.classifier == 'svm': 
            clf = SVC(C=1, kernel='linear', probability=True)
        else:
            clf = LinearSVC(penalty='l2', loss='squared_hinge', dual=True, tol=0.0001, C=1.0, multi_class='ovr', fit_intercept=True, intercept_scaling=1, class_weight=None, verbose=0, random_state=None, max_iter=1000)

        print('train svm')
        clf.fit(trainEmbeddings, labelsNum)
        print('test elvis PM')
        pmRes = testElvis(args, le, clf, testPMs)
        print('test elvis not PM')
        notPmRes = testElvisNotPm(args, le, clf )
        #print('PM found, PM not found, no face found, wrong PM found')
        print(pmRes)
        for i in range(len(testPMs)):
            print("%s, %1.2f, %1.2f, %d, %d" % (testPMs[i], pmRes[i][0], pmRes[i][0]/(100.0-pmRes[i][2])*100.0, 100-pmRes[i][2], pmRes[i][3]))
        print('not PMs:')
        # PM not found, PM found wrong
        print(notPmRes)
        if args.saveClassifier:
            fName = args.saveClassifier
            print("Saving classifier to '{}'".format(fName))
            with open(fName, 'w') as f:
                pickle.dump((le, clf), f)
