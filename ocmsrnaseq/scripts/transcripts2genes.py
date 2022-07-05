'''
transcripts2genes.py
====================================================

:Author: Nick Ilott
:Tags: Python

Purpose
-------

Build a tsv file that maps ensembl transcripts to ensembl genes from ensembl fasta file. This is
for use with kallisto outputs to be imported using tximport.

Usage
-----

.. Example use case

Example::

   python transcripts2genes.py

Type::

   python transcripts2genes.py --help

for command line help.

Command line options
--------------------

'''

import sys
import cgatcore.experiment as E
import cgat.FastaIterator as FastaIterator

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

    args.stdout.write("TXNAME\tGENEID\n")
    for fasta in FastaIterator.iterate(args.stdin):
        title = fasta.title.split(" ")
        transcript = title[0]
        gene = [x.replace("gene:", "") for x in title if "gene:" in x][0]
        args.stdout.write("\t".join([transcript, gene]) + "\n")

    # write footer and output benchmark information.
    E.stop()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
