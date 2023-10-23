'''
gtf2genes.py
==============

:Author: Nick Ilott
:Tags: Python

Purpose
-------

Build a tsv file that maps ensembl transcripts to ensembl genes from ensembl gtf file. This is
for use with kallisto outputs to be imported using tximport.

Usage
-----

.. Example use case

Example::

   python gtf2gene_names.py

Type::

   python gtf2gene_names.py --help

for command line help.

Command line options
--------------------

'''

import sys
import cgatcore.experiment as E
import cgat.GTF as GTF

def main(argv=None):
    """script main.
    parses command line options in sys.argv, unless *argv* is given.
    """

    if argv is None:
        argv = sys.argv

    # setup command line parser
    parser = E.ArgumentParser(description=__doc__)

    parser.add_argument("-t", "--test", dest="test", type=str,
                        help="supply help")

    # add common options (-h/--help, ...) and parse command line
    (args) = E.start(parser, argv=argv)

    args.stdout.write("gene_id\tgene_name\n")
    gene_ids = []
    for gtf in GTF.iterator(args.stdin):
        gene_id = gtf.gene_id
        try:
            gene_name = gtf.gene_name
        except KeyError:
             #print("could not find gene name in dict for %s" % gtf.gene_id)
             gene_name = ""
        if gene_id in gene_ids:
            continue
        else:
            gene_ids.append(gene_id)
            args.stdout.write("\t".join([gene_id, gene_name]) + "\n")

    # write footer and output benchmark information.
    E.stop()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
