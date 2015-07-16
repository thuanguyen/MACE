#!/usr/bin/env python
__author__ = 'Sergei F. Kliver'
import os
import argparse

from MACE.General.File import split_filename, make_list_of_path_to_files
from MACE.Parsers.VCF import CollectionVCF

def vcf_filter(filename):
    return True if filename[-4:] == ".vcf" else False

parser = argparse.ArgumentParser()

parser.add_argument("-o", "--output", action="store", dest="output", required=True,
                    help="Output file with number of variants in vcf file(files)")
parser.add_argument("-a", "--write_header", action="store_true", dest="write_header",
                    help="Write header in output file. Default: false")
parser.add_argument("-i", "--input_vcf", action="store", dest="input_vcf", type=lambda s: s.split(","),
                    help="Comma-separated list of vcf files or directories containing them",  required=True)
parser.add_argument("-w", "--write_dir_path", action="store_true", dest="write_dir_path",
                    help="write directory name(if directory is source of vcf files) in output file. Default: false")
parser.add_argument("-e", "--write_ext", action="store_true", dest="write_ext",
                    help="write extensions of vcf files in output file. Default: false")
args = parser.parse_args()

files_list = make_list_of_path_to_files(args.input_vcf, vcf_filter)

with open(args.output, "w") as out_fd:
    if args.write_header:
        out_fd.write("#file/sample\tnumber_of_variants\n")
    for filename in files_list:
        directory, prefix, extension = split_filename(filename)
        variants = CollectionVCF(from_file=True, in_file=filename)
        number_of_variants = len(variants)
        if args.write_dir_path and args.write_ext:
            name = filename
        elif args.write_dir_path:
            name = (directory + prefix) if directory else prefix
        elif args.write_ext:
            name = prefix + extension
        else:
            name = prefix

        out_fd.write("%s\t%i\n" % (name, number_of_variants))


