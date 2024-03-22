import streamlit as st
from stmol import showmol
from sandbox_functions import *
from st_pages import Page, Section, show_pages, add_page_title, hide_pages
add_page_title()

hide_pages(["Transcription", "Identify Mutations", "Translation", "Sandbox Instructions"])
if st.sidebar.button("Go To Sandbox"):
    st.switch_page("pages//Sandbox.py")


st.markdown("**Sandbox Mode**")
st.markdown('''In this mode, you can experiment with a protein of your choice and visualize its basic structure and characteristics. You can also try changing its amino acid sequence and observing the resulting structure.''')

st.markdown('''Instructions for use:  
We’ve already preloaded some basic proteins, including myoglobin (1MBN), Human Growth Hormone (1HGU), and glucagon (1GCN). But, you can also personalize the proteins you look at by clicking on the dropdown menu under “PDB Code” and selecting “Select From PDB ID.” From there, find a PDB ID from protein databases like Uniprot and RCSB. ''')

st.markdown('''Afterwards, you’ll see a prediction of the structure of the protein. Study its structure by zooming in and out of the protein and rotating around it. An example structure is shown below.''')

st.image("screenshots//base_1.jpg")

st.markdown('''In the left sidebar menu, you can also change the color of the protein (“Pick A Color” in the “Visualization Settings” menu), highlight the hydrophobicity of each area (“Hydrophobicity” in “Select View”), and choose between different visualization styles, including cartoon, stick, and sphere styles (“Style” in the “Visualization Settings” menu). For the hydrophobicity setting, a key is provided in the sidebar that explains the color gradient. A few illustrations of the “stick” style and hydrophobicity visualizations are provided below.''')

st.image("screenshots//stick_hydrophobicity_2.jpg")
st.image("screenshots//hydrophobicity_legend_3.jpg")

st.markdown('''You can also test out the effects of mutations on a protein’s structure by turning on “ML Predicted Structure.” Add, delete or insert amino acids in the original protein’s sequence to see the structure of the new, mutated protein compared with the original.''')

st.image("screenshots//ml_predicted_structure_4.jpg")
