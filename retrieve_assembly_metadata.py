from os import mkdir, path
import argparse
from sys import argv
from multiprocessing import Pool, cpu_count
from subprocess import Popen, PIPE


def parse_args(argv):
    parser = argparse.ArgumentParser(description='Retrieve assembly metadata from NCBI database using assembly accession numbers')
    parser.add_argument('accession', nargs='*', help='all accession numbers you want to retrieve')
    parser.add_argument('-f', '--file', nargs='?', help='a file contains list of assembly accessions')
    parser.add_argument('-c', '--core', nargs='?', default=1, type=int, help='number of cores used, default value is 1')
    if len(argv) == 0:
        print('No input argument is provided.\n')
        parser.print_help()
        return None
    else:
        args = parser.parse_args(argv)
        if args.file and args.accession:
            print('You should only provide only one file containinga list of assembly accession numbers or directly provide assembly accession numbers')
            return None
        if args.file is None and ('-f' in argv or '--file' in argv):
            print('No file is provided for -f (--file) option')
            return None
        if args.accession == [] and args.file is None:
            print('You should only provide one file containinga list of assembly accession numbers or directly provide assembly accession numbers')
            return None
        if args.core > cpu_count():
            args.core = cpu_count
        return args


def fetch_data(accession):
    '''
    This function wraps following four commands (take assembly GCA_000696205.1 as an example):
        esearch -db assembly -query "GCA_000696205.1[asac]" | efetch -db assembly -format docsum -mode json 
        esearch -db assembly -query "GCA_000696205.1[asac]" | elink -target genome | efetch -db genome -format docsum -mode json
        esearch -db assembly -query "GCA_000696205.1[asac]" | elink -target bioproject | efetch -db bioproject -format docsum -mode json
        esearch -db assembly -query "GCA_000696205.1[asac]" | elink -target biosample | efetch -db biosample -format docsum -mode json
    '''
    mkdir(path.join('output', accession))
    esearch = Popen(['esearch', '-db', 'assembly', '-query', '"{}[asac]"'.format(accession)], stdout=PIPE)
    efetch_command = ['efetch', '-format', 'docsum', '-mode', 'json']
    efetch_assembly = Popen(efetch_command, stdin=esearch.stdout, stdout=PIPE)
    with open(path.join('output', accession, 'assembly.json'), 'w') as f:
        f.write(efetch_assembly.stdout.read().decode('utf-8'))
    esearch = Popen(['esearch', '-db', 'assembly', '-query', '"{}[asac]"'.format(accession)], stdout=PIPE)
    elink_genome = Popen(['elink', '-target', 'genome'], stdin=esearch.stdout, stdout=PIPE)
    efetch_genome = Popen(efetch_command, stdin=elink_genome.stdout, stdout=PIPE)
    with open(path.join('output', accession, 'genome.json'), 'w') as f:
        f.write(efetch_genome.stdout.read().decode('utf-8'))
    esearch = Popen(['esearch', '-db', 'assembly', '-query', '"{}[asac]"'.format(accession)], stdout=PIPE)
    elink_bioproject = Popen(['elink', '-target', 'bioproject'], stdin=esearch.stdout, stdout=PIPE)
    efetch_bioproject = Popen(efetch_command, stdin=elink_bioproject.stdout, stdout=PIPE)
    with open(path.join('output', accession, 'bioproject.json'), 'w') as f:
        f.write(efetch_bioproject.stdout.read().decode('utf-8'))
    esearch = Popen(['esearch', '-db', 'assembly', '-query', '"{}[asac]"'.format(accession)], stdout=PIPE)
    elink_biosample = Popen(['elink', '-target', 'biosample'], stdin=esearch.stdout, stdout=PIPE)
    efetch_biosample = Popen(efetch_command, stdin=elink_biosample.stdout, stdout=PIPE)
    with open(path.join('output', accession, 'biosample.json'), 'w') as f:
        f.write(efetch_biosample.stdout.read().decode('utf-8'))
    return 0


if __name__ == '__main__':
    args = parse_args(argv[1:])
    mkdir('output')
    if args is not None:
        if args.accession != []:
            accessions = args.accession
        else:
            accessions = []
            with open(args.file) as f:
                for line in f:
                    accessions.append(line.rstrip('\n'))
        pool = Pool(args.core)
        result = pool.map(fetch_data, accessions)
        # TODO: check the return code
