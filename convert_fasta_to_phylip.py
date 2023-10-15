#!/usr/bin/python3

# convert_fasta_to_phylip.py

# Hsin-Ying Chang <hyhazelchang@gmail.com>
# v1 2023/10/14

# Usage: python3 /home/xinchang/pyscript_xin/convert_fasta_to_phylip.py --in_dir=/scratch/xinchang/cyano11/cyano11.29/macse/nt_ns/ns_TA1/ --out_dir=/scratch/xinchang/cyano11/cyano11.29/macse/nt_ns/ns_TA1_phylip/ --in_file_ext="fasta"

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
    parser.add_argument("--in_file_ext",
                        type=str,
                        default=None,
                        help="input file extension.")

    # Defining variables from input
    args = parser.parse_args()
    in_dir = args.in_dir
    out_dir = args.out_dir
    in_file_ext = args.in_file_ext

    # Create a new directory for sequences output
    if not os.path.exists(out_dir):
        os.system("mkdir -p " + out_dir)
    
    # Get the genbank files in the input directory
    seqfiles = glob.glob(in_dir + "*." + in_file_ext)

    # Parse out the sequences
    count_in = 0
    count_out = 0
    for file in seqfiles:
        filename = os.path.basename(file).split(".")[0]
        seq_dict = {}
        for record in SeqIO.parse(open(file), "fasta"):
            count_in += 1
            seq_dict[record.id] = record.seq
        ids = list(seq_dict.keys())
        num_ids = len(ids)
        seq_len = len(seq_dict[ids[0]])
        # write into output
        output = open(out_dir + filename + ".phylip", "w")
        output.write(" " + str(num_ids) + " " + str(seq_len) + "\n")
        for id in ids:
            output.write(str(id) + "  " + str(seq_dict[id]) + "\n")
            count_out += 1
        output.close()
    print("count_in = " + str(count_in) + ", " + "count_out = " + str(count_out))
        
if __name__ == '__main__':
    main()
