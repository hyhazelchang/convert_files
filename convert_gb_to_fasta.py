#!/usr/bin/python3

# convert_gb_to_fasta.py

# Hsin-Ying Chang <hyhazelchang@gmail.com>
# v1 2023/09/22

# Usage: python3 /home/xinchang/pyscript_xin/convert_gb_to_fasta.py --in_dir=/scratch/xinchang/cyano11/cyano11.24/source_data/gb/ --out_dir=/scratch/xinchang/cyano11/cyano11.24/source_data/fasta/ --table=/scratch/xinchang/cyano11/cyano11.24/list/download.list --in_file_ext="gbff" --index_in=3 --index_out=0 --opt="VERSION"

import argparse
import os
import glob
from Bio import SeqIO

def main():
    parser = argparse.ArgumentParser(
            description=("Parse the sequences from gb"),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--in_dir",
                        type=str,
                        default=None,
                        help="The directory of input files.")
    parser.add_argument("--out_dir",
                        type=str,
                        default=None,
                        help="The directory of output file.")
    parser.add_argument("--table",
                        type=str,
                        default=None,
                        help="The table for renaming.")
    parser.add_argument("--in_file_ext",
                        type=str,
                        default=None,
                        help="input file extension.")
    parser.add_argument("--index_in",
                        type=int,
                        default=None)
    parser.add_argument("--index_out",
                        type=int,
                        default=None)
    parser.add_argument("--opt",
                        type=str,
                        default="LOCUS")

    # Defining variables from input
    args = parser.parse_args()
    in_dir = args.in_dir
    out_dir = args.out_dir
    table = args.table
    in_file_ext = args.in_file_ext
    index_in = args.index_in
    index_out = args.index_out
    opt = args.opt

    # Create a new directory for sequences output
    if not os.path.exists(out_dir):
        os.system("mkdir -p " + out_dir)
    
    # Find table for renaming
    tb_file = [line.rstrip("\n").split("\t") for line in open(table)]

    # Get the genbank files in the input directory
    input = glob.glob(os.path.join(in_dir, "*." + in_file_ext))

    # Find the files from table
    for line in tb_file:
        file = in_dir + str(line[index_in]) + "." + in_file_ext
        # Count the sequence number
        seqs_out = []
        if file in input:
            for record in SeqIO.parse(open(file), "genbank"):
                # Extract the ids and sequences out to the new file
                if opt == "LOCUS":
                    seqs_out.append(">" + str(record.name + "\n" + record.seq))
                elif opt == "DEFINITION":
                    seqs_out.append(">" + str(record.description + "\n" + record.seq))
                elif opt == "VERSION":
                    seqs_out.append(">" + str(record.id + "\n" + record.seq))
            # write into output
            out = open(out_dir + str(line[index_out]) + ".fasta", "w")
            out.write(("\n").join(seqs_out))
            out.close()
        else:
            print("There is no file: " + str(line[index_in]) + "." + in_file_ext + "!")

if __name__ == '__main__':
    main()