#!/usr/bin/env python
__author__ = 'Sergei F. Kliver'
import argparse

from collections import OrderedDict

from MACE.Parsers.VCF import CollectionVCF
from MACE.Parsers.CCF import RecordCCF, MetadataCCF, HeaderCCF, CollectionCCF

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input_vcf", action="store", dest="input", required=True,
                    help="Input  vcf file.")
parser.add_argument("-o", "--output_prefix", action="store", dest="output_prefix", required=True,
                    help="Prefix of output files.")

args = parser.parse_args()

mutations = CollectionVCF(from_file=True, in_file=args.input)

homo_list = []
chains_dict = OrderedDict()
for chromosome in mutations.scaffold_list:
    for record in mutations.records[chromosome]:
        if record.is_homozygous():
            homo_list.append(record)
        else:
            if homo_list:
                if chromosome not in chains_dict:
                    chains_dict[chromosome] = [RecordCCF(collection_vcf=CollectionVCF(records_dict=dict([(chromosome, homo_list)]), from_file=False),
                                                     from_records=True)]
                else:
                    chains_dict[chromosome].append(RecordCCF(collection_vcf=CollectionVCF(records_dict=dict([(chromosome, homo_list)]), from_file=False),
                                                     from_records=True))
                homo_list = []
            else:
                continue

chains = CollectionCCF(records_dict=chains_dict, metadata=MetadataCCF(mutations.samples,
                                                                      vcf_metadata=mutations.metadata,
                                                                      vcf_header=mutations.header),
                       header=HeaderCCF("CHAIN_ID\tCHROM\tSTART\tEND\tDESCRIPTION".split("\t")))
chains.write("%s.ccf" % args.output_prefix)
chains.write_gff("%s.gff" % args.output_prefix)
chains.statistics("%s_chains_size_distribution.svg" % args.output_prefix)
homo_mutations = chains.extract_vcf()
homo_mutations.write("%s.vcf" % args.output_prefix)