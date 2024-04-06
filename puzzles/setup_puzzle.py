import streamlit as st
from stmol import showmol
import pandas as pd
import os
import random

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
        codon = rna_sequence[i:i+3]
        amino_acid = codon_table.get(codon, 'X')  # 'X' for unknown or invalid codon
        amino_acids += amino_acid

    return amino_acids

def puzzle():
    key_path = "C:\\Users\\Avi.Lekkelapudi25\\Downloads\\practice_problems\\key\\"
    key = random.choice(os.listdir(key_path))
    key="key_1ans.txt"
    key = open((key_path+key), "r").read().split('\n')[2:4]

    wild_rna = key[0]
    mut_rna = key[1]

    wild_aa_seq = rna_to_amino_acids(wild_rna)
    st.write("Wildtype Amino Acid Sequence: " + wild_aa_seq)
    mut_rna = st.text_input("Mutated RNA", mut_rna)
    st.write("Mutated Amino Acid Sequence: " + rna_to_amino_acids(mut_rna))
    if wild_aa_seq == rna_to_amino_acids(mut_rna):
        st.success("You win!!!")

