#!/usr/bin/python

from Bio import Phylo, AlignIO
from Bio.Align import MultipleSeqAlignment


def build_msa(node, sequence_msa_map):
    key = str(node.__hash__())
    file_name = key + '.msa'
    file_handle = open(file_name, 'w')
    terminals = node.get_terminals()
    alignments = [sequence_msa_map[terminal.name] for terminal in
            terminals]
    alignments = MultipleSeqAlignment(alignments)
    AlignIO.write(alignments, file_handle, 'stockholm')
    return file_name

def treewalker(root, sequence_msa_map):
    msa_file_name = build_msa(root, sequence_msa_map)
    for clade in root.clades:
        treewalker(clade, sequence_msa_map)
    return

def main():
    tree_file = "sample_tree.ml"
    msa_file = "sample_alignment.msa"
    new_sequence_file = "new_sequence.fasta"
    
    # Note: the name of the tree leaf nodes is going to be the 
    # same as the id of each msa entry

    tree = Phylo.read(tree_file, "newick")
    msa = AlignIO.read(msa_file, "fasta")
    
    sequence_msa_map = {}
    for entry in msa:
        sequence_msa_map[entry.id] = entry

    print tree
    
    treewalker(tree.root, sequence_msa_map)
    
if __name__ == '__main__':
    main()
