import sys
import os
import glob
import configparser
from pathlib import Path
from ruffus import *
from cgatcore import pipeline as P

# load options from the config file
PARAMS = P.get_parameters(
    ["pipeline.yml"])

scriptsdir = os.path.dirname(os.path.abspath(__file__)) + "/scripts"
rscriptsdir = os.path.dirname(os.path.abspath(__file__)) + "/R"

PARAMS["scriptsdir"] = scriptsdir
PARAMS["rscriptsdir"] = rscriptsdir

######################################################################
######################################################################
######################################################################
# Run geomxngspipeline
######################################################################
######################################################################
######################################################################

@follows(mkdir("dcc.dir"))
@transform("*L001*R1.fastq.gz", regex("(\S+)_L00[0-9]_R[0-9].fastq.gz"), r"dcc.dir/\1.dcc")
def runGeomx(infile, outfile):
    '''
    '''
    job_memory = PARAMS["geomx_memory"]
    job_threads = PARAMS["geomx_threads"]

    options = PARAMS["geomx_options"]
    outdir = os.path.abspath(os.path.dirname(outfile))
    if not options:
        options=""

    # running each fastq separately so create a
    # temp directory to store results
    tmpdir = P.get_temp_dir(".")

    # collate all files associated with the fastq R1
    sample_name = infile.split("_")[0]
    infiles = " ".join([os.path.abspath(x) for x in glob.glob(sample_name + "*")])

    ini = glob.glob("*.ini")[0]

    # build a new config file per fastq set
    # set threads as 1 to avoid console interaction
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(ini)
    config["Processing_v2"]["threads"] = "1"
    aoi, value = sample_name, config["AOI_List"][sample_name]
    config["AOI_List"] = {sample_name: value}

    # write out AOI config file
    with open(os.path.join(tmpdir, "config.ini"), "w") as configfile:
        config.write(configfile) 

    # build geomx statement
    statement = '''cd %(tmpdir)s; ln -s %(infiles)s .; cd ../;
                   geomxngspipeline
                   --in=%(tmpdir)s
                   --out=%(tmpdir)s
                   --ini=%(tmpdir)s/config.ini
                   --check-illumina-naming=false
                   %(options)s;
                   rm -rf %(tmpdir)s/config.ini;
                   rm -rf %(tmpdir)s/*.fastq.gz;
                   mv %(tmpdir)s/summary.txt dcc.dir/%(sample_name)s_summary.txt;
                   mv %(tmpdir)s/* dcc.dir;
                   rm -rf %(tmpdir)s
                '''
    P.run(statement)

######################################################################
######################################################################
######################################################################
# Merge summary.txt files across .ini files
######################################################################
######################################################################
######################################################################

@follows(runGeomx, mkdir("summary.dir"))
@merge(glob.glob("dcc.dir/*summary.txt"), "summary.dir/summary.txt")
def mergeSummaries(infiles, outfile):
    '''
    merge summary files across AOIs
    '''
    infiles = " ".join(infiles)
    statement = '''cat %(infiles)s > %(outfile)s'''
    P.run(statement)


######################################################################
######################################################################
######################################################################
# Merge dcc files
######################################################################
######################################################################
######################################################################

@follows(mkdir("NanoStringGeoMxSet.dir"))
@merge([runGeomx,
        PARAMS["annotation_file"],
        PARAMS["pkc_file"]],
        "NanoStringGeoMxSet.dir/geomx_set.Rds")
def buildNanoStringGeoMxSet(infiles, outfile):
    '''
    merge dcc files, annotations and pkc files
    into NanoStringGeoMxSet
    '''
    annotations = PARAMS["annotation_file"]
    pkc_file = PARAMS["pkc_file"]

    statement = '''Rscript %(rscriptsdir)s/dcc2geomxset.R
                   --annotation-file=%(annotations)s
                   --pkc-file=%(pkc_file)s 
                   --dcc-dir=dcc.dir
                   --output-file=%(outfile)s
    '''
    P.run(statement)

# ---------------------------------------------------
# Generic pipeline tasks
@follows(mergeSummaries, buildNanoStringGeoMxSet)
def full():
    pass


def main(argv=None):
    if argv is None:
        argv = sys.argv
    P.main(argv)


if __name__ == "__main__":
    sys.exit(P.main(sys.argv))    
