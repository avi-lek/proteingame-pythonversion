import streamlit as st 
import pandas as pd 

def rna_to_amino_acid(rna_sequence):
    # Define the RNA codon to amino acid mapping
    codon_table = {
        'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
        'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
        'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
        'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
        'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
        'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'UAU': 'Y', 'UAC': 'Y', 'UAA': 'Stop', 'UAG': 'Stop',
        'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
        'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
        'UGU': 'C', 'UGC': 'C', 'UGA': 'Stop', 'UGG': 'W',
        'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
        'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
        'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
    }

    # Ensure the length of the RNA sequence is a multiple of 3
    if len(rna_sequence) % 3 !=0:
        st.write("RNA sequence length must be a multiple of 3!")
    else:
        # Translate the RNA sequence to amino acids
        amino_acid_sequence = ''
        for i in range(0, len(rna_sequence), 3):
            codon = rna_sequence[i:i+3]
            amino_acid = codon_table.get(codon, 'X')  # 'X' represents an unknown amino acid
            if amino_acid == 'Stop':
                break
            amino_acid_sequence += amino_acid
        st.write("Amino Acid Sequence:", amino_acid_sequence)

# Example usage:
st.write("RNA To Amino Acids")
rna_sequence = st.text_input("RNA Sequence", "AUGCCGUUUGAGUCAUGCAUCAGUGAUACUGUAGACAUAGUGUGUACUGAC")
rna_to_amino_acid(rna_sequence)

