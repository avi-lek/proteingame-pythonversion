import streamlit as st
import requests
import urllib
import py3Dmol
from stmol import showmol
from model import *
import os
def vis_reg():
    pdb_code = st.session_state["code"]
    pdb_content = fetch_pdb_content(pdb_code)
    view = py3Dmol.view(width=800, height=600)
    system = "".join([x for x in pdb_content])
    if len(get_chains(system))<=1 or True:
        if st.sidebar.toggle('ML Predicted Structure'):
            wild_path = "C:\\Users\\Avi.Lekkelapudi25\\ProteinGame\\a.pdb"
            aa_seq = st.text_input("Amino Acid Sequence", "EQLLKALEFLLKELLEKL")
            if st.sidebar.button("Refold Protein") or bool(~os.path.isfile(wild_path)):
                get_esm_pdb(aa_seq)
            with open("a.pdb") as ifile:
                system = "".join([x for x in ifile])
    view.addModelsAsFrames(system)
    i = 0
    with st.sidebar.expander("Visualization Settings"):
        st.session_state["style"]  = st.selectbox('Style',['cartoon','stick','sphere'])
        color = st.color_picker('Pick A Color', '#00f900')
        if st.session_state["style"] != 'sphere':
            surface = st.checkbox("Generate Surface")
            if surface :
                opacity = st.slider("Surface Opacity", min_value=0.0,max_value=1.0, value=0.5)

    for line in system.split('\n'):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM":
            continue
        view.setStyle({'model': 0, 'serial': i+1}, {st.session_state["style"]: {'color': color}})
        i += 1
    if st.session_state["style"] != 'sphere' and surface:
        view.addSurface(py3Dmol.VDW, {"opacity": opacity, "color":color})

    view.zoomTo()
    showmol(view, height=600, width=800)

def get_chains(system):
    chains=[]
    for line in system.split('\n'):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM":
            continue
        if split[4] not in chains and split[4].isalpha():
            chains.append(split[4])
    return chains
def vis_chain():
    pdb_code = st.session_state["code"]
    pdb_content = fetch_pdb_content(pdb_code)
    view = py3Dmol.view(width=800, height=600)
    system = "".join([x for x in pdb_content])
    view.addModelsAsFrames(system)

    chains=get_chains(system)
    with st.sidebar.expander("Visualization Settings"):
        st.session_state["style"]  = st.selectbox('style',['cartoon','stick','sphere'])
        chain_color = []
        for chain in chains:
            chain_color.append(st.color_picker('Chain ' + chain + ' Color', '#00f900'))
        i = 0
        if st.session_state["style"] != 'sphere':
            surface = st.checkbox("Generate Surface")
            if surface :
                opacity = st.slider("Surface Opacity", min_value=0.0,max_value=1.0, value=0.5)
        for line in system.split('\n'):
            split = line.split()
            if len(split) == 0 or split[0] != "ATOM":
                continue

            if split[4].isalpha():
                color = chain_color[chains.index(split[4])]
            else:
                color = "black"
            view.setStyle({'model': -1, 'serial': i+1}, {st.session_state["style"]: {'color': color}})
            i += 1
        if st.session_state["style"] != 'sphere' and surface:
            view.addSurface(py3Dmol.VDW, {"opacity": opacity, 'color':'#808080'})


    view.zoomTo()
    showmol(view, height=600, width=800)




def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok

# Hydrophobicity values for amino acids
hydrophobicity_values = {
    'ILE': 4.5, 'VAL': 4.2, 'LEU': 3.8, 'PHE': 2.8, 'CYS': 2.5,
    'MET': 1.9, 'ALA': 1.8, 'GLY': -0.4, 'THR': -0.7, 'SER': -0.8, 'TRP': -0.9,
    'TYR': -1.3, 'PRO': -1.6, 'HIS': -3.2, 'GLU': -3.5, 'GLN': -3.5, 'ASP': -3.5,
    'ASN': -3.5, 'LYS': -3.9, 'ARG': -4.5
}
# Function to fetch PDB content
def fetch_pdb_content(pdb_code):
    pdb_url = f'https://files.rcsb.org/download/{pdb_code.upper()}.pdb'
    pdb_content = urllib.request.urlopen(pdb_url).read().decode("utf-8")
    return pdb_content

# Function to get color based on hydrophobicity
def get_color(resname):
    hydrophobicity = hydrophobicity_values.get(resname, 0)
    if hydrophobicity >= 4.0:
        return '#ff3300'
    elif hydrophobicity >= 3.0:
        return '#ff9900'
    elif hydrophobicity >= 2.0:
        return '#ffcc00'
    elif hydrophobicity >= 0.0:
        return '#ffff00'
    elif hydrophobicity >= -0.9:
        return '#ccff00'
    elif hydrophobicity >= -1.9:
        return '#99ff00'
    elif hydrophobicity >= -2.9:
        return '#66ff00'
    elif hydrophobicity >= -3.9:
        return '#33ff00'
    else:
        return 'black'
    
# Function to calculate hydrophobicity of a residue
def calculate_hydrophobicity(resname, hydrophobicity_values):
    return hydrophobicity_values.get(resname, 0)
    
def vis_hb():
    pdb_code = st.session_state["code"]
    pdb_content = fetch_pdb_content(pdb_code)

    # Create Py3Dmol view
    view = py3Dmol.view(width=800, height=600)

    # Add protein structure to the view
    system = "".join([x for x in pdb_content])
    view.addModelsAsFrames(system)

    with st.sidebar.expander("Visualization Settings"):
        st.session_state["style"]  = st.selectbox('style',['cartoon','stick','sphere'])
        if st.session_state["style"] != 'sphere':
            surface = st.checkbox("Generate Surface")
            if surface :
                opacity = st.slider("Surface Opacity", min_value=0.0,max_value=1.0, value=0.5)
    # Color each amino acid based on hydrophobicity
    i = 0

    for line in system.split('\n'):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM":
            continue
        color = get_color(split[3])
        idx = int(split[1])
        view.setStyle({'model': -1, 'serial': i+1}, {st.session_state["style"]: {'color': color}})
        i += 1

    if st.session_state["style"] != 'sphere' and surface:
        view.addSurface(py3Dmol.VDW, {"opacity": opacity, 'color':'#808080'})
    # Zoom to protein and show view
    view.zoomTo()
    showmol(view, height=600, width=800)