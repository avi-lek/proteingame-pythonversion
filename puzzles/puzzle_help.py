import streamlit as st
import py3Dmol
import urllib
import Bio.PDB.Polypeptide
from Bio.PDB import Superimposer, PDBParser
import numpy
from Bio.SeqUtils import seq1
from Bio.PDB.PDBIO import PDBIO
import os
import pandas as pd
import random
from Bio import SeqIO
from io import StringIO


def make_window(rna_seq):
    window_end = random.randrange(30, len(rna_seq), 3)
    window_start = window_end-30
    return window_start, window_end

def substitution(rna_seq):
    window_start, window_end = make_window(rna_seq)
    mut_len = random.randint(1,6)
    mut_start = random.randint(window_start+3,window_end-mut_len-3)
    mut_end = mut_start + mut_len
    window = "".join(['-' for n in range(window_start)]) + rna_seq[window_start:window_end] + "".join(['-' for n in range(len(rna_seq)-window_end)])
    #create_mutation
    mut_window = list(window)
    mut_rna = list(rna_seq)

    bases=['A', 'U', 'G', 'C']
    for n in range(mut_start, mut_end):
        if mut_window[n]!=mut_rna[n]:
            print("ALL FUCKED UP")

        c=mut_rna[n]
        while c==mut_rna[n]:
            c = random.choice(bases)

        mut_window[n]=c
        mut_rna[n]=c
    
    mut_window = "".join(mut_window)
    mut_rna = "".join(mut_rna)

    return remove_nonalpha(mut_window)[0:30], mut_rna, remove_nonalpha(window)[0:30], rna_seq, mut_start, mut_len

def remove_nonalpha(n):
    return "".join([i for i in n if i.isalpha()])
    
def insertion(rna_seq):
    window_start, window_end = make_window(rna_seq)
    mut_len = random.randint(1,6)
    mut_start = random.randint(window_start+3,window_end-mut_len-3)
    window = "".join(['-' for n in range(window_start)]) + rna_seq[window_start:window_end] + "".join(['-' for n in range(len(rna_seq)-window_end)])
    
    #create_mutation
    bases=['A', 'U', 'G', 'C']
    inserted_seq = "".join([random.choice(bases) for n in range(mut_len)])
    mut_window = window[:mut_start] + inserted_seq + window[mut_start:len(rna_seq)]  
    mut_rna = rna_seq[:mut_start] + inserted_seq + rna_seq[mut_start:] 
    return remove_nonalpha(mut_window)[0:30], mut_rna, remove_nonalpha(window)[0:30], rna_seq, mut_start, mut_len

def mutate(rna_seq):
    n = random.randint(1,3)
    mut_bool = True    
    if n==1:
        mut_window_seq, mut_seq, window_seq, rna_seq, mut_start, mut_len = insertion(rna_seq)
        mtype = "i"
    elif n==2:
        mut_window_seq, mut_seq, window_seq, rna_seq, mut_start, mut_len = deletion(rna_seq)
        mtype = 'd'
    elif n==3:
        mut_window_seq, mut_seq, window_seq, rna_seq, mut_start, mut_len = substitution(rna_seq)
        mtype = 's'

    return mut_window_seq, mut_seq, window_seq, rna_seq, mut_start, mut_len, mtype





def deletion(rna_seq):
    window_start, window_end = make_window(rna_seq)
    mut_len = random.randint(1,6)
    mut_start = random.randint(window_start+3,window_end-mut_len-3)
    window = "".join(['-' for n in range(window_start)]) + rna_seq[window_start:window_end] + "".join(['-' for n in range(len(rna_seq)-window_end)])
    mut_end = mut_start+mut_len
    #create_mutation
    mut_window = window[:mut_start] + rna_seq[mut_end:]  
    mut_rna = rna_seq[:mut_start] + rna_seq[mut_end:] 

    return remove_nonalpha(mut_window)[0:30], mut_rna, remove_nonalpha(window)[0:30], rna_seq, mut_start, mut_len
    




def amino_acids_to_rna(amino_acids):
    codon_table = {
        'A': ['GCU', 'GCC', 'GCA', 'GCG'],
        'R': ['CGU', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'],
        'N': ['AAU', 'AAC'],
        'D': ['GAU', 'GAC'],
        'C': ['UGU', 'UGC'],
        'Q': ['CAA', 'CAG'],
        'E': ['GAA', 'GAG'],
        'G': ['GGU', 'GGC', 'GGA', 'GGG'],
        'H': ['CAU', 'CAC'],
        'I': ['AUU', 'AUC', 'AUA'],
        'L': ['UUA', 'UUG', 'CUU', 'CUC', 'CUA', 'CUG'],
        'K': ['AAA', 'AAG'],
        'M': ['AUG'],
        'F': ['UUU', 'UUC'],
        'P': ['CCU', 'CCC', 'CCA', 'CCG'],
        'S': ['UCU', 'UCC', 'UCA', 'UCG', 'AGU', 'AGC'],
        'T': ['ACU', 'ACC', 'ACA', 'ACG'],
        'W': ['UGG'],
        'Y': ['UAU', 'UAC'],
        'V': ['GUU', 'GUC', 'GUA', 'GUG'],
        '*': ['UAA', 'UGA', 'UAG']  # Stop codons
    }
    rna = []
    for i in range(int(len(amino_acids))):
        rna.append(random.choice(codon_table.get(amino_acids[i], "XXX")))
    return "".join(rna)


amino_acid_dict = {
    'ALA': 'A',  # Alanine
    'ARG': 'R',  # Arginine
    'ASN': 'N',  # Asparagine
    'ASP': 'D',  # Aspartic Acid
    'CYS': 'C',  # Cysteine
    'GLN': 'Q',  # Glutamine
    'GLU': 'E',  # Glutamic Acid
    'GLY': 'G',  # Glycine
    'HIS': 'H',  # Histidine
    'ILE': 'I',  # Isoleucine
    'LEU': 'L',  # Leucine
    'LYS': 'K',  # Lysine
    'MET': 'M',  # Methionine
    'PHE': 'F',  # Phenylalanine
    'PRO': 'P',  # Proline
    'SER': 'S',  # Serine
    'THR': 'T',  # Threonine
    'TRP': 'W',  # Tryptophan
    'TYR': 'Y',  # Tyrosine
    'VAL': 'V'   # Valine
}
def pdb_to_fasta(pdb_code):
    pdb_url = f'https://files.rcsb.org/download/{pdb_code}.pdb'
    pdb_file = urllib.request.urlopen(pdb_url).read()
    pdb_parser = PDBParser(QUIET=True)
    model = list(pdb_parser.get_structure(id=pdb_code, file=StringIO(pdb_file.decode('utf-8'))).get_models())[0]

    sequ = []
    sequence = ''


    for chain in model:
        for residue in chain:
            if residue.get_resname() in amino_acid_dict.keys():
                sequ.append(amino_acid_dict[residue.get_resname()])
                    
    sequence = " ".join(str(x) for x in sequ)
    sequence = sequence.replace(" ", "")

    return(sequence)

def rna_to_amino_acids(rna_sequence):
    codon_table = {
        'UUU': 'F', 'UUC': 'F',
        'UUA': 'L', 'UUG': 'L', 'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
        'AUU': 'I', 'AUC': 'I', 'AUA': 'I',
        'AUG': 'M',
        'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
        'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S', 'AGU': 'S', 'AGC': 'S',
        'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'UAU': 'Y', 'UAC': 'Y',
        'UAA': '*', 'UAG': '*', 'UGA': '*',
        'CAU': 'H', 'CAC': 'H',
        'CAA': 'Q', 'CAG': 'Q',
        'AAU': 'N', 'AAC': 'N',
        'AAA': 'K', 'AAG': 'K',
        'GAU': 'D', 'GAC': 'D',
        'GAA': 'E', 'GAG': 'E',
        'UGU': 'C', 'UGC': 'C',
        'UGG': 'W',
        'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'AGA': 'R', 'AGG': 'R',
        'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
    }

    amino_acids = ''
    for i in range(0, len(rna_sequence), 3):
        codon = str(rna_sequence[i:i+3])
        if codon_table.get(codon, 'X')=='*':
            return amino_acids
        else:
            amino_acid = codon_table.get(codon, 'X')  # 'X' for unknown or invalid codon
            amino_acids += amino_acid

    return amino_acids