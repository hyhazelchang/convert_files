#!/usr/bin/python3

# convert_fastq_to_fasta.py

# Hsin-Ying Chang <hyhazelchang@gmail.com>
# v1 2023/06/18

# Usage: python3 /home/xinchang/pyscript_xin/convert_fastq_to_fasta.py --in_dir=/scratch/xinchang/cyano22/cyano22.03/nanopore_reads/ --out_dir=/scratch/xinchang/cyano22/cyano22.03/nanopore_reads/test/ --verbose=1


import argparse
import os
import glob

def main():
    parser = argparse.ArgumentParser(
        description=("Convert fastq to fasta."),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--in_dir",
                        default=None,
                        type=str,
                        help="Path to fastq file. Please provide absolute path.")
    parser.add_argument("--out_dir",
                        default=None,
                        type=str,
                        help="Output file. Please provide absolute path.")
    parser.add_argument("--verbose",
                        default=0,
                        type=int)
                        

    args = parser.parse_args()
    in_dir = args.in_dir
    out_dir = args.out_dir
    verbose = args.verbose

    # Make output directory
    if not os.path.exists(out_dir):
        os.system("mkdir -p " + out_dir)

    # Open the file
    seqfiles = glob.glob(os.path.join(in_dir, "*.fastq"))

    # Parse sequences
    for file in seqfiles:
        filename = os.path.basename(file).split(".")[0]
        seqs = [line.rstrip("\n") for line in open(file)]
        count_in = 0
        count_out = 0
        seqs_out = []
        for i in range(0, len(seqs), 4):
            if "@" in seqs[i]:
                id, seq = seqs[i].lstrip("@"), seqs[i+1]
                count_in += 1
            else:
                print("error parsing " + seq[i])
            seqs_out.append([id, seq])
            count_out += 1

        # Write into output
        output = out_dir + filename + ".fasta"
        out = open(output, "w")
        for seq in seqs_out:
            out.write(">" + seq[0] + "\n" + seq[1] + "\n")
        out.close()

        # verbose
        if verbose:
            print("file_id = " + filename + ", count_in = " + str(count_in) + ", count_out = " + str(count_out))

if __name__ == "__main__":
    main()