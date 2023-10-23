"""===========================
pipeline_kallisto.py
===========================

Overview
========

This pipeline takes raw fastq files and uses kallisto to quantify using pseudoaligment
against a reference transcriptome
 

Usage
=====

See :ref:`PipelineSettingUp` and :ref:`PipelineRunning` on general
information how to use cgat pipelines.

Configuration
-------------

The pipeline requires a configured :file:`pipeline.yml` file.

Default configuration files can be generated by executing:

   python <srcdir>/pipeline_kallisto.py config

Input files
-----------

fastq files that are in the format .fastq.1.gz and .fastq.2.gz.

Requirements
------------


Requirements:


Pipeline output
===============


Glossary
========

.. glossary::


Code
====

"""
import sys
import os
import glob
from pathlib import Path
from ruffus import *
from cgatcore import pipeline as P

# load options from the config file
PARAMS = P.get_parameters(
    ["pipeline.yml"])

#get all files within the directory to process
SEQUENCEFILES = ("*.fastq.1.gz")

SEQUENCEFILES_REGEX = regex(
    r"(\S+).(fastq.1.gz)")

scriptsdir = os.path.dirname(os.path.abspath(__file__)) + "/scripts"
PARAMS["scriptsdir"] = scriptsdir

########################################################
########################################################
########################################################
# Run kallisto
########################################################
########################################################
########################################################

@follows(mkdir("kallisto.dir"))
@transform(SEQUENCEFILES, SEQUENCEFILES_REGEX, r"kallisto.dir/\1/\1_abundance.tsv")
def runKallisto(infile, outfile):
    '''classify reads with kraken2
    '''
    # Note that at the moment I only deal with paired-end
    # reads properly
    p1 = infile
    p2 = p1.replace(".fastq.1.gz", ".fastq.2.gz")

    # bit of a hack about
    if not os.path.exists(p2):
        p2 = "--single"

    transcriptome = PARAMS.get("kallisto_transcriptome")
    nthreads = PARAMS.get("kallisto_nthreads")
    job_memory = PARAMS.get("kallisto_job_mem")
    options = PARAMS.get("kallisto_options")
    if options == None:
        options = ""
    sample_name = P.snip(p1, ".fastq.1.gz")
    statement = '''kallisto quant 
                   -i %(transcriptome)s 
                   -o kallisto.dir/%(sample_name)s 
                   -b 100
                   %(options)s 
                   %(p1)s 
                   %(p2)s;
                   mv kallisto.dir/%(sample_name)s/abundance.tsv kallisto.dir/%(sample_name)s/%(sample_name)s_abundance.tsv
                '''
    P.run(statement)

########################################################
########################################################
########################################################
# Build transcripts to genes mapping
########################################################
########################################################
########################################################

@follows(mkdir("transcripts2genes.dir"))
@files(PARAMS["kallisto_transcripts_gtf"],
       "transcripts2genes.dir/transcripts2genes.tsv")
def transcripts2genes(infile, outfile):
    '''
    convert fasta file to tsv files containing transcript2gene
    mapping
    '''
    statement = '''zcat %(infile)s | python %(scriptsdir)s/gtf2genes.py
                                     --log=transcripts2genes.dir/transcripts2genes.log
                                   | sort -k1,2
                                   | uniq
                                     > transcripts2genes.dir/transcripts2genes.tsv
                '''
    P.run(statement)

# ---------------------------------------------------
# Generic pipeline tasks
@follows(runKallisto, transcripts2genes)
def full():
    pass


def main(argv=None):
    if argv is None:
        argv = sys.argv
    P.main(argv)


if __name__ == "__main__":
    sys.exit(P.main(sys.argv))    
