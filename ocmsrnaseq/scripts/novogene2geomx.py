# rename novogene files to work with geomx pipeline
# they are expected for each sample to have an L001_R1
# file pattern which is used to find the rest of the samples
# associated with that sample

import glob
import collections
import natsort
import os


# get a sample mapping - assumes all fastq files are . and end with .fq.gz
infiles = glob.glob("*.fq.gz")

sample_map = collections.defaultdict(list)
for f in infiles:
    sample = f.split("_")
    sample, lane, read = sample[0], sample[-2], sample[-1]
    
    # re label various aspects of
    # the file names
    lane = lane.replace("L", "L00")
    read = "R" + read.replace("fq", "fastq")
    
    sample_map[sample].append([f, lane, read])


# Keep a log of file mappings for output
mapping = open("file_map.txt", "w")
for sample, associated_data in sample_map.items():

    # find the lowest number and replace with L001
    sorted_lanes = natsort.natsorted([x[1] for x in associated_data])
    lowest = sorted_lanes[0]
    for dat in associated_data:
        if dat[1] == lowest:
            new_lane = dat[1].replace(dat[1], "L001")
        else:
            new_lane = dat[1]
        new_fname = "_".join([sample, new_lane, dat[2]])

        mapping.write(dat[0] + "\t" + new_fname + "\n")

        os.symlink(os.path.abspath(dat[0]), os.path.abspath(new_fname))
                
