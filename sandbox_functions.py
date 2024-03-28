import streamlit as st
import requests
import urllib
import py3Dmol
from stmol import showmol
from model import *
import os
import Bio
from Bio.PDB.PDBIO import PDBIO
from puzzles.puzzle_help import pdb_to_fasta
from Bio.PDB import *
from streamlit_dimensions import st_dimensions
import streamlit.components.v1 as components
import ipywidgets as widgets
from ipywidgets import embed
import py3Dmol
import ipyspeck

def get_chains(system):
    chains=[]
    for line in system.split('\n'):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM":
            continue
        if split[4] not in chains and split[4].isalpha():
            chains.append(split[4])
    return chains

import datetime
def vis_chain():
    pdb_code = st.session_state["code"]
    pdb_content = fetch_pdb_content(pdb_code[0:5])
    #container_width = st_dimensions(key="main")["width"]
    container_width = 850
    view = py3Dmol.view(width=container_width, height=600)
    system = "".join([x for x in pdb_content])
    view.addModelsAsFrames(system)
    st.caption("Source: " + system.split('\n')[1][6:-1])
    
    if len(get_chains(system))<=1 and st.sidebar.toggle('ML Predicted Structure'):
        #can move setting up data table to inside if statement
        c0 = 'https://lh3.googleusercontent.com/pw/AP1GczOUMHVGZYT1uzxa3Bxxhra1VKflXnXcyNi-OsNOKAYpoPPrFvd4qOfQ6368vBhqmjchb7rHp17zCn1yO7EOzgvySHRV3imIigD1vmWtLZcJsaFE-QVDRaG5_0ZKJnoeCBrEdS5a4tpk-pIfyLvwWYs=w1920-h1080-s-no-gm'
        c1 = 'https://lh3.googleusercontent.com/pw/AP1GczO3yO0TLq7qUKOk67SEO4aqqjDuK5j5fcE6cQSjdMhsSJ3CriFuIRgvOJh5m7YK6hcSTRR1CD4egWJES7GWSojc4p4fhjEcpbI_tCJ1DwJRVngcE8C16ri4DbqshOJllNh6GURA7eDgIM2NUB1L7pA=w1920-h1080-s-no-gm'
        c2 = 'https://lh3.googleusercontent.com/pw/AP1GczMurj7BCXZtrfbcpXFRCbNVn6ha6kmcXSr7oomw-e8sCkTKj5po_ECivVUuM8neAKKy-WBNTPz_iA5E6J-UOjLIpAL0jDR3ijmi5ymCjXbqcOlxnXd-w9zNFof4dAuGPFAoo_PxOKmomEsPRdIJnsE=w1920-h1080-s-no-gm'
        c3 = 'https://lh3.googleusercontent.com/pw/AP1GczNyV81q2OeC_BH18lx58jY_QyfyZVTMNvqhIbwUz5PiBSK8BpfcrtEZ0otsPOVM_0qValZSe660DPOxKVRMo-3-mgGIFGB8o_WRFxGEv5RgKOtyVCDVW6D3I-ZSUU-cBKmF6AxTn1KO8BBxhAKVWho=w1920-h1080-s-no-gm'
        c4 = 'https://lh3.googleusercontent.com/pw/AP1GczOfulzfMogLMwWeGtOSpWksemPyiQoy_odrYu9wF2RO_XK51PBhqBA_uaHWGY75lNi9KFsWdk7USY6cj0dQ4dFO84aDqtOHJj9Mrxej62fgED20abrxWe2MsrBFCl2bbSFX6Dsuh6s0Mtz6biJD-Kw=w1920-h1080-s-no-gm'
        fasta = pdb_to_fasta(pdb_code)

        rows = [
            {"Color": c0, "Sequence": fasta, "Show": True},
            {"Color": c1, "Sequence": fasta, "Show": True},
            {"Color": c2, "Sequence": fasta, "Show": True},
            {"Color": c3, "Sequence": fasta, "Show": True},
            {"Color": c4, "Sequence": fasta, "Show": True},
        ]
        wild_path = ["pdb\\sandbox0.pdb", "pdb\\sandbox1.pdb", "pdb\\sandbox2.pdb", "pdb\\sandbox3.pdb", "pdb\\sandbox4.pdb"]
        if "num_overlays" not in st.session_state:
            st.session_state["num_overlays"] = 0
        
        if st.sidebar.button("Add Protein") and st.session_state["num_overlays"]<4:
            st.session_state["num_overlays"]=st.session_state["num_overlays"]+1

        if st.sidebar.button("Restart"):
            i = st.session_state["num_overlays"]+1
            for f in wild_path[0:(st.session_state["num_overlays"]+1)]:
                os.remove(f)
            st.session_state["num_overlays"]=0
        df = pd.DataFrame(rows[:st.session_state["num_overlays"]+1])
        color_vals = st.column_config.ImageColumn("Color")
        st.session_state["edited_df"] = st.data_editor(df, use_container_width=True, hide_index=True, column_config={"Color": color_vals})    
        for i in range(st.session_state["num_overlays"]+1):
            if bool(~os.path.isfile(wild_path[st.session_state["num_overlays"]])):
                get_esm_pdb(st.session_state["edited_df"]["Sequence"][i], ("sandbox"+str(i)))
                if i !=0:
                    sup(wild_path[0], wild_path[i])
        quick_viz()
    else:
        #st.caption("Sequence: " + pdb_to_fasta(pdb_code))
        chains=get_chains(system)
        with st.sidebar.expander("Visualization Settings"):
            st.session_state["style"]  = st.selectbox('Style',['Cartoon','Stick','Sphere']).lower()
            chain_color = []
            colors = ['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FFC0CB', '#FFA500', '#0000FF', '#800080', '#FF0000', '#008080']
            colors = colors[0:len(chains)]
            for chain, color in zip(chains, colors):
                chain_color.append(st.color_picker('Chain ' + chain + ' Color', color))
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

    add_hover_with_color(view)
    view.zoomTo()
    showmol(view, height=600, width=container_width)

def add_hover(obj,backgroundColor='black',fontColor='white'):
    js_script = """function(atom,viewer) {
                   if(!atom.label) {
                    atom.label = viewer.addLabel(atom.resn+':'+atom.resi,{position: atom, backgroundColor:"%s" , fontColor:"%s"});
                }
              }"""%(backgroundColor,fontColor)
    obj.setHoverable({},True,js_script,
               """function(atom,viewer) {
                   if(atom.label) {
                    viewer.removeLabel(atom.label);
                    delete atom.label;
                   }
                }"""
               )
def add_hover_with_color(obj):
    js_script = """function(atom,viewer) {
                   if(!atom.label) {
                    atom.label = viewer.addLabel(atom.resn+':'+atom.resi,{position: atom, backgroundColor:"black" , fontColor:atom.style.cartoon.color});
                }
              }"""
    obj.setHoverable({},True,js_script,
               """function(atom,viewer) {
                   if(atom.label) {
                    viewer.removeLabel(atom.label);
                    delete atom.label;
                   }
                }"""
    )

import pandas as pd
def quick_viz():
    
    wild_path = ["pdb\\sandbox0.pdb", "pdb\\sandbox1.pdb", "pdb\\sandbox2.pdb", "pdb\\sandbox3.pdb", "pdb\\sandbox4.pdb"]

    with st.sidebar.expander("Visualization Settings"):
        st.session_state["style"]  = st.selectbox('Style',['Cartoon','Stick','Sphere']).lower()
    colors = ['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FFC0CB', '#FFA500', '#0000FF', '#800080', '#FF0000', '#008080']
    view = py3Dmol.view(width=800, height=600)
    counter = 0
    for i in range(st.session_state["num_overlays"]+1):
        if st.session_state["edited_df"]["Show"][i]:
            view.addModel(open(wild_path[i], 'r').read(),'pdb')
            view.setStyle({'model':counter}, {st.session_state["style"]: {'color': colors[i], 'opacity': 1}})
            counter = counter+1
    view.zoomTo()
    showmol(view, height=600, width=800)

def sup(p1,p2):
    wild_code = "rand"
    mut_code = wild_code
    wild_path = p1
    mut_path = p2

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
    super_imposer.apply(mut_structure.get_atoms())
    io=PDBIO()
    io.set_structure(pdb_object=mut_structure)
    io.save(mut_path)

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

    #legend
    with st.sidebar.expander("Hydrophobicity Legend"):
        st.color_picker(label=">4", value="#ff3300", disabled=True)
        st.color_picker(label=">= 3.0", value="#ff9900", disabled=True)
        st.color_picker(label=">= 2.0", value="#ffcc00", disabled=True)
        st.color_picker(label=">= 0.0", value="#ffff00", disabled=True)
        st.color_picker(label=">= -0.9", value="#ccff00", disabled=True)
        st.color_picker(label=">= -1.9", value="#99ff00", disabled=True)
        st.color_picker(label=">= -2.9", value="#66ff00", disabled=True)
        st.color_picker(label=">= -3.9", value="#33ff00", disabled=True)

    with st.sidebar.expander("Visualization Settings"):
        st.session_state["style"]  = st.selectbox('Style',['Cartoon','Stick','Sphere']).lower()
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

amino_acid_dict = {
    'ALA': 'A',  # Alanine
    'ARG': 'R',  # Arginine
    'ASN': 'N',  # Asparagine
    'ASP': 'D',  # Aspartic Acid
    'CYS': 'C',  # Cysteine
    'GLN': 'Q',  # Glutamine
    'GLU': 'E',  # Glutamic Acid
    'GLY': 'G',  # Glycine
    'HIS': 'H',  # Histidine
    'ILE': 'I',  # Isoleucine
    'LEU': 'L',  # Leucine
    'LYS': 'K',  # Lysine
    'MET': 'M',  # Methionine
    'PHE': 'F',  # Phenylalanine
    'PRO': 'P',  # Proline
    'SER': 'S',  # Serine
    'THR': 'T',  # Threonine
    'TRP': 'W',  # Tryptophan
    'TYR': 'Y',  # Tyrosine
    'VAL': 'V'   # Valine
}
def get_aa(path):
    pdb_parser = Bio.PDBParser(QUIET=True)
    model = list(pdb_parser.get_structure("rand", path).get_models())[0]

    sequ = []
    sequence = ''


    for chain in model:
        for residue in chain:
            if residue.get_resname() in amino_acid_dict.keys():
                sequ.append(amino_acid_dict[residue.get_resname()])
                    
    sequence = " ".join(str(x) for x in sequ)
    sequence = sequence.replace(" ", "")

    return(sequence)
