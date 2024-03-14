from stmol import showmol
import streamlit as st
import py3Dmol
import urllib
import Bio.PDB.Polypeptide
from Bio.PDB import Superimposer, PDBParser
import numpy
from Bio.SeqUtils import seq1
from Bio.PDB.PDBIO import PDBIO
from model import*
import os
import pandas as pd
from rna2aa import *
import random


def mutate(rna_seq):
    n = random.randint(1,3)
    if n==1:
        mut_window_seq, mut_seq, window_seq, rna_seq = insertion(rna_seq)
    elif n==2:
        mut_window_seq, mut_seq, window_seq, rna_seq = deletion(rna_seq)
    elif n==3:
        mut_window_seq, mut_seq, window_seq, rna_seq = substitution(rna_seq)
    return mut_window_seq, mut_seq, window_seq, rna_seq



def insertion(rna_seq):
    mut_len = random.randint(1,9)
    mut_start = random.randint(0,len(rna_seq)-mut_len)
    
    m = True
    while m:
        try:
            window_start_index = random.randint(mut_start-30+mut_len, mut_start)
            m=False
        except:
            m=True

    window_seq = rna_seq[window_start_index:(window_start_index+30)]

    bases=['A', 'U', 'G', 'C']
    mut_seq = rna_seq
    added_seq = []
    for n in range(mut_len):
        added_seq.append(random.choice(bases))
    mut_seq=mut_seq[0:mut_start]+"".join(added_seq)+mut_seq[mut_start:len(mut_seq)]
    mut_window_seq = mut_seq[window_start_index:(window_start_index+30)]
    return mut_window_seq, mut_seq, window_seq, rna_seq

def deletion(rna_seq):
    mut_len = random.randint(1,9)
    mut_start = random.randint(0,len(rna_seq)-mut_len)
    
    m = True
    while m:
        try:
            window_start_index = random.randint(mut_start-30+mut_len, mut_start)
            m=False
        except:
            m=True

    window_seq = rna_seq[window_start_index:(window_start_index+30)]

    mut_seq = rna_seq
    mut_seq=mut_seq[0:mut_start]+mut_seq[(mut_start+mut_len):len(mut_seq)]
    mut_window_seq = mut_seq[window_start_index:(window_start_index+30)]
    return mut_window_seq, mut_seq, window_seq, rna_seq


def substitution(rna_seq):
    mut_len = random.randint(1,9)
    mut_start = random.randint(0,len(rna_seq)-mut_len)
    
    m = True
    while m:
        try:
            window_start_index = random.randint(mut_start-30+mut_len, mut_start)
            m=False
        except:
            m=True

    window_seq = rna_seq[window_start_index:(window_start_index+30)]

    bases=['A', 'U', 'G', 'C']
    mut_seq = rna_seq
    added_seq = []
    for n in range(mut_len):
        added_seq.append(random.choice(bases))
    #change later to not substitute in identical bases
    mut_seq=mut_seq[0:mut_start]+"".join(added_seq)+mut_seq[(mut_start+mut_len):len(mut_seq)]
    mut_window_seq = mut_seq[window_start_index:(window_start_index+30)]
    return mut_window_seq, mut_seq, window_seq, rna_seq


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