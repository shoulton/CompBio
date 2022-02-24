import pysam
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", required=True, type=str, help="input the normal bam file location")
    parser.add_argument("-c",required=True, type=str, help="input the cancer bam file location")
    args = parser.parse_args()
#    cancer_bam = pysam.AlignmentFile(args.c)
    normal_bam = pysam.AlignmentFile(args.n)
    print(args)