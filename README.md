# OCMS_RNAseq: Pipelines for processing of bulk and single-cell RNAseq data

## Overview

The pipelines in this repository are for the processing and analysis of bulk and single-cell RNAseq data. They are built using the [cgat-core](https://github.com/cgat-developers/cgat-core) workflow management system. In general, and as well as having specific tools installed as detailed in the below sections, you will need to have cgat-core installed. For example, cgat-core can be installed via pip (best within a virtualenv).

    pip install numpy==1.19.5
    pip install cgatcore

You must also make sure that you have a .cgat.yml in your home directory that specifies the cluster environment.

    cluster:
    queue_manager: <slurm|sge|pbstorque>
    parallel_environment: <pe name>
    queue: <queue_name>


and that you have drmaa in your path.

    export DRMAA_LIBRARY_PATH=/<full-path>/libdrmaa.so


## Install OCMS_RNAseq

To install OCMS_RNAseq simply clone the repsository and run setup.py:

    git clone <>
    cd OCMS_RNAseq
    python setup.py install

This will place relevant modules in your path and enable the use of the simplified command line interface (CLI).


# Pipelines

There are a variety of pipelines related to RNAseq data processing. These are

* pipeline_kallisto
* pipeline_cite-seq-count

## CITE-seq-count

CITE-seq-count is a tool that is used to de-multiplex Hash-tag-oligo (HTO) multiplexed fastq files in single-cell RNA-seq datasets. pipeline_cite-seq-count is a convenient wrapper to CITE-seq-count that enables multiple fastq files to be processed concurrently with a single command. In order to use this pipeline you will first have to configure the pipeline with various parameters that are passed to CITE-seq-count. To initialise the parameters file (pipeline.yml) run:

    ocms_rnaseq cite-seq-count config

You can then edit the pipeline.yml file with the parameters that you desire. Visit the [CITE-seq-count](https://hoohm.github.io/CITE-seq-Count/Running-the-script/) documentation for details about the parameterisation.

### Input files

The inputs to cite-seq-count are fastq files and a .csv file that specifies the hashtag sequences and names. Paired fastq files should be in the format <sample_name>.fastq.1.gz and <sample_name>.fastq.2.gz. The hashtag file is in the form:


    |sample1|tag_seq1|tag_name1|
    |sample1|tag_seq2|tag_name2|
    |sample1|tag_seq3|tag_name3|

In this example, this specification would correspond to the following fastq files:

    sample1.fastq.1.gz 
    sample1.fastq.2.gz

Where three HTOs were used i.e. 3 samples were multiplexed using hashtag oligos. The tag file is specified in the pipeline.yml. 


### Running the pipeline


Make sure you have CITE-seq-count installed:

    pip install CITE-seq-count

Assuming you are in a working directory that has all of your fastq files in you can run the pipeline by typing:

    ocms_rnaseq cite-seq-count make full -v5 -p24

where the -v5 specifies the verbosity of the logging information that is available in pipeline.log and -p24 specifies that you want to run 24 processes concurrently i.e. 24 samples processed in parallel.


