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
from puzzles.puzzle_help import amino_acids_to_rna
from rna2aa import *
import random
from puzzle_help import *

def vis_overlay():
    wild_code = "1ans_1"
    mut_code = wild_code
    wild_path = "pdb\\wild.pdb"
    mut_path = "pdb\\mut.pdb"

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
    if "w_aa" not in st.session_state or "w_rna" not in st.session_state or "mut_window" not in st.session_state or "mut_seq" not in st.session_state or "mut_start" not in st.session_state or "mut_len" not in st.session_state:
        st.session_state["w_aa"] = "EQLLKALEFLLKELLEKL"
        st.session_state["w_rna"] = amino_acids_to_rna(st.session_state["w_aa"])
        mut_window_seq, mut_seq, window_seq, rna_seq,mut_start, mut_len = mutate(st.session_state["w_rna"])
        st.session_state["mut_window"] = mut_window_seq
        st.session_state["mut_seq"] = mut_seq 
        st.session_state["w_window"] = window_seq
        st.session_state["w_rna"] = rna_seq
        st.session_state["mut_start"] = mut_start
        st.session_state["mut_len"] = mut_len

    if bool(~os.path.isfile("pdb\\wild.pdb")):
        get_esm_pdb("EQLLKALEFLLKELLEKL", "wild")
        st.write("pred")
    if st.sidebar.button("Refold Protein") or bool(~os.path.isfile("pdb\\mut.pdb")):
        st.write()
        f_rna = st.session_state["mut_seq"][0:st.session_state["mut_start"]]+st.session_state["mut_window"]+st.session_state["mut_seq"][(st.session_state["mut_start"]+st.session_state["mut_len"]):]
        aa = rna_to_amino_acids(f_rna)
        get_esm_pdb(aa, "mut")
        st.write("pred")

    w_aa = st.session_state["w_aa"]
    rna = st.session_state["mut_window"]
    m_aa = rna_to_amino_acids(rna)

    vis_overlay()
    st.session_state["mut_window"] = st.text_input('Input RNA', rna)
    rna = st.session_state["mut_window"]
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
