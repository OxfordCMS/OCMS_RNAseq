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

* pipeline_geomx
* pipeline_kallisto
* pipeline_cite-seq-count

## kallisto

Kallisto is a pseudoalignment tool that allows for quantification of RNA-seq data. 

### Input files

Fastq files from an RNA-seq experiment are input files. Further parameters are specified in the pipeline.yml file that is created by:

    ocms_rnaseq kallisto config

This allows you to specify the location of the kallisto index for the species and build of interest. Then you can run kallisto using:

    ocms_rnaseq kallisto make full -v5 -p24 


## Geomx

This pipeline is used to quantitate probes associated with spatial profiling using the Nanostring Geomx DSP platform.

### Dependencies

You need to make sure that you have all of the relevant modules for the pipeline to run. On the BMRC this looks something like:

module load Python/3.8.2-GCCcore-9.3.0
source ~/devel/venv/Python-3.8.2-GCCcore-9.3.0/${MODULE_CPU_TYPE}/bin/activate;
module load geomx/2.3.3.10;
module load R/4.2.1-foss-2020a-bare

Make sure that the R version that you load has GeomxTools installed.


### Input files

You need four input files to run the pipeline to completion:

* Fastq files (sequenced probes)
* LabWorksheet (Annotation of regions/areas of interest from the DSP)
* .pkc file (probe annotations for species of interest)
* .ini configuration file that contains information for each sample and probes used.

#### Fastq files

The fastq file names must match the sample names found in the .ini config file. For example, the DSP will name captured regions as something like DSP-12789924-B-A01. This corresponds to probes that are captured in well A01. Names of fastq files often differ from these names and may need to be changed. There is a script to rename fastq files that are compatible with the geomx pipeline in ./ocmsrnaseq/scripts/ini2fastq.py which can be run on samples derived from Novogene names. 

The name of the fastq files needs to be for example:

DSP-12789924-B-A01_L001_R1_001.fastq.gz
DSP-12789924-B-A01_L001_R2_001.fastq.gz

The sample name is derived from the portion before the first underscore. L001 corresponds to lane 1 and R1 to read 1 of a pair etc. If there are multiple lanes per sample there HAS TO BE a L001_R1_001.fastq.gz file present for a sample. This is because the pipeline picks up this sample in order to combine data. If there isn't a L001 file for a particular sample then you will need to rename one of your files so that it acts as a "dummy" file for this lane. This is taken care of in ./ocmsrnaseq/scripts/ini2fastq.py if the sequencing is from Novogene.


#### LabWorksheet

This is a .txt file that is obtained from the DSP machine. The only difference is that it does not contain the first 15 lines (i.e. machine parameters etc) so the first 15 lines need to be removed before running the pipeline:

```
tail -n+15 LabWorksheet.txt > pipeline_LabWorksheet.txt
```

Specify the name of the annotation file in the pipeline.yml before running the pipeline (parameter is annotation_file: )

#### .pkc file

The .pkc file is obtained from the Nanostring website and contains mapping between probe ids and gene annotations etc.

Specify the path to the .pkc file in the pipeline.yml before running the pipeline.

#### .ini file

The .ini file is used to produce the .dcc file outputs for each sample. The pipeline creates a new .ini for each sample so that they can all be run in parallel. This is obtained for each experiment on the DSP.

### Running the pipeline

Create a run directory and link fastq files, .ini, .pkc and Labworksheet into the working directory. Run:


```
ocms_rnaseq geomx config
```

This will produce the pipeline.yml file that you can edit to point to the relevant annotation files. To run the pipeline type for example:


```
ocms_rnaseq geomx make full -v5 -p96
```

### Output files

The counts files for each sample (.dcc files) are output into dcc.dir/ and can be used for downtream analysis. A NanostringGeoMxSet is also produced in NanoStringGeoMxSet.dir/. This is an .Rds file and so can be loaded straight into R for analysis with GeoMxTools or shiny-geomx.



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


