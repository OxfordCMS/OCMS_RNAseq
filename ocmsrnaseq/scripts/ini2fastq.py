
######################################################
######################################################
# Take an geomx DSP ini file and rename fastq files
# from Novogene according to DSP naming convention
######################################################
######################################################

# TODO: Make this into a proper script: Modularise functions for
# the different bits and create script with named arguments

import sys
import glob
import configparser
import collections
import natsort
import os

# usage -> python ini2fastq.py config.ini 

# positional arguments and globs for files
fastqs = glob.glob("*.fq.gz")

ini_file = sys.argv[1] 

# load ini file
ini = configparser.ConfigParser()
ini.read(ini_file)

# create map of samples
sample_map = {}
for sample in ini["AOI_List"]:
    dat = sample.split("-")
    sample = "-".join([dat[0].upper(), dat[1].upper(), dat[2].upper(), dat[3].upper()])
    well = dat[-1].upper()
    sample_map[well] = sample

# create new filenames for fastq files
sample_map2 = collections.defaultdict(list)
for f in fastqs:
    well = f.split("_")[0]
    sample_name = sample_map[well]
    new_name = f.replace(well, sample_name)
    
    sample = f.split("_")
    sample, lane, read = sample[0], sample[-2], sample[-1]
    
    # re label various aspects of
    # the file names
    lane = lane.replace("L", "L00")
    read = "R" + read.replace("fq", "fastq")
    
    sample_map2[sample].append([f, new_name, lane, read])


# Keep a log of file mappings for output
mapping = open("file_map.txt", "w")
for sample, associated_data in sample_map2.items():

    # find the lowest number and replace with L001
    # this is for compatibility with the geomx pipeline
    sorted_lanes = natsort.natsorted([x[2] for x in associated_data])
    lowest = sorted_lanes[0]
    for dat in associated_data:
        if dat[2] == lowest:
            new_lane = dat[2].replace(dat[2], "L001")
        else:
            new_lane = dat[2]
        new_fname = "_".join([dat[1].split("_")[0], new_lane, dat[3].replace(".fastq.gz", "_001.fastq.gz")])

        mapping.write(dat[0] + "\t" + new_fname + "\n")

        # create symlinks to files
        os.symlink(os.path.abspath(dat[0]), os.path.abspath(new_fname))
                



