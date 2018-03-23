#!/usr/bin/env python

import csv
from collections import defaultdict
from collections import Counter
import os
import argparse

columns = defaultdict(list)
defaultHeader = ['FCID', 'Lane', 'SampleID', 'SampleRef', 'Index',
                 'Description', 'Control', 'Recipe', 'Operator', 'SampleProject']
columnsDiffer = False


def columnOrderChecker(args):
    """Checks if the columns order differ."""

    inputFile = args.input
    global columnsDiffer

    # check if the column order differs from the defaultheaders (default columns)
    with open(inputFile, 'r') as infile:
        reader = csv.DictReader(infile)
        if defaultHeader != reader.fieldnames:
            columnsDiffer = True
            print "Columns order differ"
        else:
            print "Columns order perfect"

    # delete  modified.csv if already exists
    if os.path.isfile('modified.csv'):
        os.remove('modified.csv')

    # creates  new modified.csv file and modifies it's columns if required
    with open(inputFile, 'r') as infile, open('modified.csv', 'a') as outfile:
        writer = csv.DictWriter(
            outfile, extrasaction='ignore', fieldnames=defaultHeader)
        writer.writeheader()
        for row in csv.DictReader(infile):
            writer.writerow(row)

    if columnsDiffer == True:
        print "Columns order changed"


def missingSamplesFinder(inputFile):
    """Prepares a list of all samples that are missing."""

    global columnsDiffer

    # prepares a dictionary with each column name as 'key' and it's values in an array as 'value'
    with open(inputFile, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            for (key, value) in row.items():
                columns[key].append(value)

    sampleIDs = columns['SampleID']
    sampleOccurenceCount = Counter(sampleIDs)
    incompleteSamples = []
    incr = 0

    # makes a list of all the incomplete samples, a sample is considered incomplete if it's sampleID occurs only once in the file
    for sampleID in sampleOccurenceCount:
        if sampleOccurenceCount[sampleID] == 1:
            incompleteSamples.append(sampleID)
            incr = incr + 1

    if incompleteSamples:
        print "Incomplete samples exist"
        missingSamplesAppender(inputFile, incompleteSamples)
    else:
        print "No incomplete samples found"
        if columnsDiffer == False:
            print "The file is free of errors, no modifications required"
            os.remove('modified.csv')
        else:
            print "Modified file created with correct column order"


def missingSamplesAppender(inputFile, incompleteSamples):
    """Appends the missing samples to the end of CSV file."""

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
        print "Apending missing samples"
        writer.writerows(missingRows)
        print "Missing samples added"
        print "Modified file created"


def main():
    parser = argparse.ArgumentParser(
        description='Checks the samplesheet CSV file for errors and modifies it as required')
    parser.add_argument("-f", help="Input file to be modified",
                        dest="input", type=str, required=True)
    parser.set_defaults(func=columnOrderChecker)
    args = parser.parse_args()
    args.func(args)
    missingSamplesFinder('modified.csv')


if __name__ == '__main__':
    main()
