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
from puzzle_help import *

def vis_overlay():
    wild_code = "1ans_1"
    mut_code = wild_code
    wild_path = "C:\\Users\Avi.Lekkelapudi25\\ProteinGame\\wild.pdb"
    mut_path = "C:\\Users\Avi.Lekkelapudi25\\ProteinGame\\a.pdb"

    og_structure = Bio.PDB.PDBParser(QUIET=True).get_structure(wild_code, wild_path)
    mut_structure = Bio.PDB.PDBParser(QUIET=True).get_structure(mut_code, mut_path)

    og_atoms = []
    mut_atoms = []  

    #OG protein 
    for og_model in og_structure:
        for og_chain in og_model:
            for og_residue in og_chain:

                if og_residue.get_resname() != "HOH":
                    #CA = alpha carbon
                    og_atoms.append(og_residue['CA'])
                    
    #mutated protein
    for mut_model in mut_structure:
        for mut_chain in mut_model:
            for mut_residue in mut_chain:

                if mut_residue.get_resname() != "HOH":
                    #CA = alpha carbon
                    mut_atoms.append(mut_residue['CA'])


    shortest_length = min(len(og_atoms), len(mut_atoms))

    super_imposer = Bio.PDB.Superimposer()
    super_imposer.set_atoms(og_atoms[0 : shortest_length], mut_atoms[0 : shortest_length])
    #super_imposer.apply(mut_structure.get_atoms())
    io=PDBIO()
    io.set_structure(pdb_object=mut_structure)
    io.save(mut_path)

    with open(wild_path) as ifile:
        wild_system = "".join([x for x in ifile])

    with open(mut_path) as ifile:
        mut_system = "".join([x for x in ifile])

    view = py3Dmol.view(width=800, height=600)
    with st.sidebar.expander("Visualization Settings"):
        wcolor = st.color_picker('Wildtype Protein Color', '#00f900')
        wopacity = st.slider("Wildtype Protein Opacity", min_value=0.0,max_value=1.0, value=0.5)
        mcolor = st.color_picker('Mutated Protein Color', '#F90000')
        mopacity = st.slider("Mutated Protein Opacity", min_value=0.0,max_value=1.0, value=1.0)
        st.session_state["style"]  = st.selectbox('style',['cartoon','stick','sphere'])

    view.addModel(open(wild_path, 'r').read(),'pdb')
    view.addModel(open(mut_path, 'r').read(), 'pdb')

    #style
    view.setStyle({'model':0}, {st.session_state["style"]: {'color': wcolor, 'opacity': wopacity}})
    view.setStyle({'model':1}, {st.session_state["style"]: {'color': mcolor, 'opacity': mopacity}})

    view.zoomTo()
    showmol(view, height=600, width=800)


def practice():
    
    #wildtype RNA/protein
    protein_code = "1pef"
    if "w_aa" not in st.session_state:
        st.session_state["w_aa"] = "EQLLKALEFLLKELLEKL"
        st.session_state["w_rna"] = amino_acids_to_rna(st.session_state["w_aa"])
        mut_window_seq, mut_seq, window_seq, rna_seq = mutate(st.session_state["w_rna"])
        st.session_state["mut_window"] = mut_window_seq
        st.session_state["mut_seq"] = mut_seq    
    

    w_aa = st.session_state["w_aa"]
    rna = st.session_state["mut_window"]
    m_aa = rna_to_amino_acids(rna)
    #check if a.pdb exists, if not load in
    wild_path = "C:\\Users\\Avi.Lekkelapudi25\\ProteinGame\\pdb\\a.pdb"
    #if st.sidebar.button("Refold Protein") or bool(~os.path.isfile(wild_path)):
        #get_esm_pdb(m_aa)
    vis_overlay()
    rna = st.text_input('Input RNA', rna)
    m_aa = rna_to_amino_acids(rna)

    rna_dict = {" ":"RNA"}
    m_aa_dict = {" ":"Amino Acids-M"}
    w_aa_dict = {" ":"Amino Acids-W"}
    for i in range(10):
        try:
            rna_dict[str(i+1)]=rna[i*3:(i*3+3)]
        except:
            rna_dict[str(i+1)]=''
    
        try:
            m_aa_dict[str(i+1)]=m_aa[i]
        except:
            m_aa_dict[str(i+1)] =''

        try:
            w_aa_dict[str(i+1)]=w_aa[i]
        except:
            w_aa_dict[str(i+1)]=''


    df = pd.DataFrame(
    [
       rna_dict,
       m_aa_dict,
       w_aa_dict
    ]
    )
    st.dataframe(df, use_container_width=True, hide_index=True)
    if list(m_aa_dict.values())[1:] == list(w_aa_dict.values())[1:] :
        st.success("Success")
