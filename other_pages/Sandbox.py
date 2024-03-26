import streamlit as st
from stmol import showmol
from sandbox_functions import *
from st_pages import Page, Section, show_pages, add_page_title, hide_pages

st.set_page_config(page_title="Practice", page_icon=":dna:", layout="wide")
hide_pages(["Transcription", "Identify Mutations", "Translation", "Sandbox Instructions"])
#add_page_title()
st.header("Sandbox")
if "instructions_read" not in st.session_state or st.sidebar.button("Instructions"):
    st.session_state["instructions_read"] = True
    st.switch_page("other_pages//Sandbox_instructions.py")

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)
protein_ids = {
    'Myoglobin': '1MBN',
    'Human Growth Hormone': '1HGU',
    'Glucagon': '1GCN',
    'Human Rac1 G-protein': '1MH1',
    'Beetle Antifreeze Protein': '1EZG',
    'Hemoglobin': '1a3n'
}
options = list(protein_ids.keys())
options.append("Select From PDB ID")
st.session_state["code"] = st.sidebar.selectbox("Select Protein",  options)
if st.session_state["code"] == "Select From PDB ID":
    st.session_state["code"] = st.sidebar.text_input('PDB Code')
    #MAKE SURE TO DISALLOW INCORRECT CODES
else: 
    st.session_state["code"] = protein_ids[st.session_state["code"]]
option = st.sidebar.selectbox('Select View', ('None', 'Hydrophobicity'))
if exists(f'https://files.rcsb.org/download/{st.session_state["code"].upper()}.pdb'):
    if option=="None":
        vis_chain()
    elif option == "Hydrophobicity":
        vis_hb()
