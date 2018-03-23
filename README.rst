A Python Script to be used by Lab Technologists at MSKCC
=======================

A Utility script written in Python intended for use by Lab Technologists at Memorial Sloan Kettering Hospital.
The software helps in validating a CSV against a predefined format and outputs a formatted file if any errors exist.

A SampleSheet file is a plain text, CSV, meta-data file, that represents samples to be sequenced through an Illumina sequencer.  This file is a required input file for sample data generation. 

The first line in the SampleSheet file is always a header, which represents field names for various meta-data. Records for each sequenced sample follow as rows below the header line (the order of meta-data fields for a given sample are always in the same order as the header). 

For instance, “Lane” field defines physical location where sample is sequenced, and can have only two values ‘1’ or ‘2’. If sample (SampleID header field) is considered as a pivot, for each sample meta-data line in “Lane 1”, there has to be a matching sample meta-data line from “Lane 2”. The ordering of columns is also strictly enforced.

SampleSheets generated manually by lab techologists can contain errors. A common error is when a sample is listed in “Lane 1”, but is missing in “Lane 2”. A second common error is incorrect ordering of columns in the SampleSheet. 

The lab technologists can use this script to check the CSV file for above mentioned errors, if any such errors exist the script alters the file and outputs a error free file. The below command can be used to run the script.


``>>./script.py -f <csv-file-name>``
