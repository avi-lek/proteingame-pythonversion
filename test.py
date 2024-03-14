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
quick_viz()
rna = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

rna = st.text_input('Input RNA', rna)

m_aa = rna_to_amino_acids(rna)
w_aa = 'RRRRRRRRRR'

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

