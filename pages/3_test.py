import py3Dmol
import streamlit as st
from stmol import showmol
import pandas as pd
from Bio.PDB import Superimposer, PDBParser
from Bio.SeqUtils import seq1
import random
from practice_functions import *
#pdb to AA sequence
def sequence_from_pdb(code, file):
    parser = PDBParser()
    struc = parser.get_structure(code, file)

    #iterate over residues and extract sequence
    sequence = ''
    for model in struc:
        for chain in model:
            for residue in chain:
                if residue.get_id()[0] == ' ':
                    #Check if residue is a standard amino acid
                    if residue.get_resname() in {'ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLN', 'GLU', 'GLY', 'HIS', 'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL'}:
                        sequence += seq1(residue.get_resname())
    return sequence

#AA to RNA
def aa_to_rna(amino_acids):
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

#pulling PDBs
og_code = '3i40'
mut_code = og_code
og_path = "pdb//mut.pdb"
mut_path = 'pdb//wild.pdb'

#PDB to AA
og_sequence = sequence_from_pdb(og_code, og_path)
og_sequence = og_sequence[0:10]
mut_sequence = sequence_from_pdb(mut_code, mut_path)
mut_sequence = mut_sequence[0:10]

#AA to RNA
og_rna = aa_to_rna(og_sequence)
mut_rna = aa_to_rna(mut_sequence)
import time
def practice_dogma():
    if "w_change_aa" not in st.session_state:
        st.session_state["w_change_aa"]=""
    if "m_change_aa" not in st.session_state:
        st.session_state["m_change_aa"]=""
    st.session_state["puzzle_info"]['m_rna']

    wild_dict = {
        "":["Wild-Type DNA", "Wild-Type mRNA", "Wild-Type Amino Acids"]                   
    }

    rna_text = st.text_input("mRNA Sequence", max_chars=30)
    if rna_text.isalpha() and is_rna(rna_text.upper()):
        mrna = rna_text
    else:
        st.warning('Only RNA Bases are permitted: A, C, U, G', icon="⚠️")
    st.text_input("A")
    for i in range(10):
        dna_codon = rna_to_DNA(st.session_state['w_rna'][i*3:(i*3+3)])
        rna_codon = (rna_codon+'                              ')[i*3:(i*3+3)]
        aa = '                              '[i]
        #rna_codon = st.session_state['w_rna'][i*3:(i*3+3)]
        #dna_codon = rna_to_DNA(rna_codon)
        #aa = rna_to_amino_acids(rna_codon)
        wild_dict[str(i+1)] = [dna_codon, rna_codon, aa]
    df = pd.DataFrame(wild_dict)


    
    
    
    
    
og_rna_dict = {" ":"Original RNA"}
mut_rna_dict = {" ":"Mutated RNA"}
og_aa_dict = {" ":"Original AA"}
mut_aa_dict = {" ":"Mutated AA"}


for i in range(10):
    try:
        og_rna_dict[str(i+1)] = og_rna[i*3:(i*3+3)]
    except:
        og_rna_dict[str(i+1)] = ''
    
    try:
        mut_rna_dict[str(i+1)] = mut_rna[i*3:(i*3+3)]
    except:
        mut_rna_dict[str(i+1)] = ''

    try:
        og_aa_dict[str(i+1)] = ""
    except:
        og_aa_dict[str(i+1)] = ''
    
    try:
        mut_aa_dict[str(i+1)] = ""
    except:
        mut_aa_dict[str(i+1)] = ''



og_df = pd.DataFrame(
    [
        og_rna_dict,
        og_aa_dict
        
    ]
)


mut_df = pd.DataFrame(
[
    mut_rna_dict,
    mut_aa_dict
]
)

#add in protein visualization
view = py3Dmol.view(width=600, height=400)
view.addModel(open(og_path, 'r').read(), 'pdb')
view.addModel(open(mut_path, 'r').read(), 'pdb')

with st.sidebar.expander("Visualization Settings"):
    view.setStyle({'model':0}, {'cartoon': {'color':'purple'}})
    view.setStyle({'model':1}, {'cartoon': {'color':'yellow'}})

with st.sidebar.expander("Codon Chart"):
    st.image('codon_wheel.png')

st.table(og_df)
og_aa = st.text_input("Original AA Sequence", "")

st.table(mut_df)


mut_aa = st.text_input("Mutated AA Sequence", "")

if len(og_aa) > 10 or len(mut_aa) > 10:
    #some condition or pop up that says it's too long
    st.write("IT'S TOO LONG BRO")

if st.button("Check Answers") and len(og_aa) == 10 and len(mut_aa) == 10:
    for i in range(10):
        og_aa_dict[str(i+1)] = og_aa[i]
        mut_aa_dict[str(i+1)] = mut_aa[i]


view.zoomTo()
showmol(view, height=500, width=700)
