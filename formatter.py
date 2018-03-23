#!/usr/bin/env python

import csv
from collections import defaultdict
from collections import Counter
import os
import argparse

columns = defaultdict(list)
defaultHeader = ['FCID', 'Lane', 'SampleID', 'SampleRef', 'Index',
                 'Description', 'Control', 'Recipe', 'Operator', 'SampleProject']


def columnOrderChecker(args):
    inputFile = args.input
    columnsDiffer = False

    with open(inputFile, 'r') as infile:
        reader = csv.DictReader(infile)
        if defaultHeader != reader.fieldnames:
            columnsDiffer = True
            print "Columns order differ"
        else:
            print "Columns order perfect"

    with open(inputFile, 'r') as infile, open('formatted.csv', 'a') as outfile:
        writer = csv.DictWriter(
            outfile, extrasaction='ignore', fieldnames=defaultHeader)
        writer.writeheader()
        for row in csv.DictReader(infile):
            writer.writerow(row)

    if columnsDiffer == True:
        print "Columns order changed"


def missingSamplesFinder(inputFile):
    with open(inputFile, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            for (key, value) in row.items():
                columns[key].append(value)

    sampleIDs = columns['SampleID']
    sampleOccurenceCount = Counter(sampleIDs)
    incompleteSamples = []
    incr = 0

    for sampleID in sampleOccurenceCount:
        if sampleOccurenceCount[sampleID] == 1:
            incompleteSamples.append(sampleID)
            incr = incr + 1

    if incompleteSamples:
        print "Incomplete samples exist"
        missingSamplesAppender(inputFile, incompleteSamples)
    else:
        print "No incomplete samples found"


def missingSamplesAppender(inputFile, incompleteSamples):
    missingRows = []

    for sampleID in incompleteSamples:
        with open(inputFile, 'r') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                for (key, value) in row.items():
                    if row[key] == sampleID:
                        if row['Lane'] == '1':
                            missingRows.append([row['FCID'], '2', row['SampleID'], row['SampleRef'], row['Index'],
                                                row['Description'], row['Control'], row['Recipe'], row['Operator'], row['SampleProject']])
                        elif row['Lane'] == '2':
                            missingRows.append([row['FCID'], '1', row['SampleID'], row['SampleRef'], row['Index'],
                                                row['Description'], row['Control'], row['Recipe'], row['Operator'], row['SampleProject']])

    inFile = open(inputFile, 'ab')

    with inFile:
        writer = csv.writer(inFile)
        print "Apending missing samples..."
        writer.writerows(missingRows)
        print "Formatted file created"


def main():
    parser = argparse.ArgumentParser(
        description='Formats the CSV file as required')
    parser.add_argument("-f", help="Input file to be formatted",
                        dest="input", type=str, required=True)
    parser.set_defaults(func=columnOrderChecker)
    args = parser.parse_args()
    args.func(args)
    missingSamplesFinder('formatted.csv')


if __name__ == '__main__':
    main()
