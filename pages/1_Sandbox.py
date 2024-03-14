import streamlit as st
from stmol import showmol
from sandbox_functions import *

st.set_page_config(page_title="Protein Game", page_icon=":dna:", layout="wide")
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)
st.title("Sandbox")

st.session_state["code"] = st.sidebar.text_input('PDB Code', '3i40')
option = st.sidebar.selectbox('Select View', ('None', "Chain", 'Hydrophobicity'))
if exists(f'https://files.rcsb.org/download/{st.session_state["code"].upper()}.pdb'):
    if option=="None":
        vis_reg()
    elif option == "Chain":
        vis_chain()
    elif option == "Hydrophobicity":
        vis_hb()

