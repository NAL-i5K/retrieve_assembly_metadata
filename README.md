# Retrieve Assembly metadata

Script for fetching assembly metadata from NCBI database, based on [EDirect](https://www.ncbi.nlm.nih.gov/books/NBK179288/).

## Depedencies
* Python 3
* EDirect

## Usage:
```
retrieve_assembly_metadata.py [-h] [-f [FILE]] [-c [CORE]] [accession [accession ...]]

Retrieve assembly metadata from NCBI database using assembly accession numbers

positional arguments:
  accession             all accession numbers you want to retrieve

optional arguments:
  -h, --help            show this help message and exit
  -f [FILE], --file [FILE]
                        a file contains list of assembly accessions
  -c [CORE], --core [CORE]
                        number of cores used, default value is 1
```
