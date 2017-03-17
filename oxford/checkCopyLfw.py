#!/usr/bin/python

import os
from sys import exit
import argparse
import re
from os.path import splitext, basename
import shutil

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-l', '--lfwList', type=str, 
        help="List of names, typically Labelled Faces in the Wild, Firstname_Lastname, can be ls of directories.",
    )
    parser.add_argument(
        '-s', '--searchList', type=str, 
        help="List of names, typically a set of politicians, Firstname Lastname.",
    )
    parser.add_argument(
        '-r', '--sourceDir', type=str, 
        help="Directory to take non-duplicated names from, typically LFW aligned.",
    )
    parser.add_argument(
        '-d', '--destinationDir', type=str, 
        help="Directory to copy non-duplicated name images to, e.g. unknown_person.",
    )

    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    if args.destinationDir:
        if not os.path.exists(args.destinationDir):
            print('creating output directory: ' + args.destinationDir)
            os.makedirs(args.destinationDir)

    with open(args.lfwList) as lfw:
        with open(args.searchList) as pol:
            allPol = pol.readlines()
            for l in lfw:
                l = l.strip()
                ln = l.split('_')
                use = 1
                for p in allPol:
                    p = p.strip()
                    pn = p.split()
                    if all(px in ln for px in pn):
                        print("not used: " + l + "(lfw) - " + p + "(list politicians)")
                        use = 0
                if use and args.sourceDir and args.destinationDir:
                    src = os.path.join(args.sourceDir, l)
                    try:
                        src_files = os.listdir(src)
                    except:
                        print('directory not found: ', src)
                        continue
                    for file_name in src_files:
                       full_file_name = os.path.join(src, file_name)
                       if (os.path.isfile(full_file_name)):
                           shutil.copy(full_file_name, args.destinationDir)
                           #print("copy: " + full_file_name + " to " + args.destinationDir)

