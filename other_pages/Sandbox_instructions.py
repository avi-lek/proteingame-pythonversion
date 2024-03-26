import streamlit as st
from stmol import showmol
from sandbox_functions import *
from st_pages import Page, Section, show_pages, add_page_title, hide_pages
add_page_title()

hide_pages(["Transcription", "Identify Mutations", "Translation", "Sandbox Instructions"])
if st.sidebar.button("Go To Sandbox"):
    st.switch_page("other_pages//Sandbox.py")


st.markdown('''In this mode, you can experiment with a protein of your choice and visualize its basic structure and characteristics. You can also try changing its amino acid sequence and observing the resulting structure.''')

st.image("screenshots//SandboxDiagram.png")
st.markdown('''
            1. Click here to change the protein you are viewing. Several proteins are preset, but you can select any protein in the RCSB PDB through the PDB ID.
            2. Click here to select what attributes are highlighted. “None” highlights by chain and “Hydrophobicity” highlights amino acids by the Kyte-Doolittle scale.
            3. Click here to view the impact of amino-acid mutations here, predicted by Meta’s ESMFold. This option is unavailable for multi-chain proteins.
            4. Click here to  view the impact of amino-acid mutations, predicted by Meta’s ESMFold. This option is unavailable for multi-chain proteins.
            5. Click here to  change the color of chains. If visualizing multiple chains, more than one color boxes will appear.
            6. Click here to generate a Van Der Waals surface for the protein. This is not available if style is set to sphere.
''')
st.markdown("**To go to sandbox, click the 'Go To Sandbox' button in the sidebar.**")
