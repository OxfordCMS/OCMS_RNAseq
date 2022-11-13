###################################################
###################################################
# dcc2geomxset: combine outputs from 
# geomx pipeline, annotations and .pkc files into
# R object as input into shiny geomx
###################################################
###################################################

suppressPackageStartupMessages(library("GeomxTools"))
suppressPackageStartupMessages(library("optparse"))
suppressPackageStartupMessages(library("futile.logger"))

# make options list
option_list <- list(
               make_option(c("--annotation-file"), default=NA, type="character",
                           help="Annotation file [default %default]"),
               make_option(c("--pkc-file"), default="NA", type="character",
                           help=".pkc file [default %default]"),
               make_option(c("--dcc-dir"), default="NA",
                           help="Directory where .dcc files [default %default]"),
               make_option(c("--output-file"), default="NA",
                           help="Output filename [default %default]")
)

# suppress warning messages
options(warn=-1)

###########################
# get command line options
###########################
opt <- parse_args(OptionParser(option_list=option_list))

dcc_dir <- opt$`dcc-dir`
annotation_file <- opt$`annotation-file`
pkc_file <- opt$`pkc-file`
outfile <- opt$`output-file`


# automatically list files in each directory for use
flog.info("Reading in .dcc files")
DCCFiles <- dir(normalizePath(dcc_dir), pattern = ".dcc$",
                full.names = TRUE, recursive = TRUE)

flog.info(paste0("Read in ", length(DCCFiles), " .dcc files"))

# need to write annotations out as .xlsx and read back in :(
flog.info(paste0("Reading in annotation file: ", annotation_file))
annotation <- read.csv(annotation_file, sep="\t", header=TRUE, stringsAsFactors=FALSE)
# annotation$Sample_ID <- rownames(annotation)
outxlsx <- gsub(".txt", ".xlsx", annotation_file)
xlsx::write.xlsx(annotation, file = outxlsx, col.names = TRUE, row.names = FALSE)

# read in pkc files for now
#PKCFiles <- unzip(zipfile = pkc_file)

flog.info("building NanoStringGeoMxSet")
geomx_dat <- readNanoStringGeoMxSet(dccFiles=DCCFiles,
                                    pkcFiles=pkc_file,
                                    phenoDataFile=outxlsx,
                                    phenoDataSheet="Sheet1",
                                    phenoDataDccColName="Sample_ID")
flog.info("Done...")

# write out the R object
flog.info("Writing GeoMx .Rds data")
saveRDS(geomx_dat, file=outfile)