import streamlit as st
import requests
import urllib
import py3Dmol
import os
import Bio
from Bio.PDB.PDBIO import PDBIO
from puzzles.puzzle_help import pdb_to_fasta
from Bio.PDB import *
import py3Dmol
from utils import *
import pandas as pd

# gets PDB content
def get_pdb_content():
    if st.session_state["use_esm"]:
       get_esm_pdb(st.session_state["esm_seq"], ("sandbox_new"))
       st.write(st.session_state["esm_seq"])
       #if bool(~os.path.isfile("pdb/sandbox.pdb")): get_esm_pdb(st.session_state["esm_seq"], ("sandbox"))
       with open("pdb\\sandbox_new.pdb") as ifile:
           system = "".join([x for x in ifile])
           st.caption("Source: " + system.split('\n')[1][6:])
           return system
    else:
        pdb_url = f'https://files.rcsb.org/download/{st.session_state["code"][0:5].upper()}.pdb'
        system = urllib.request.urlopen(pdb_url).read().decode("utf-8")
        st.caption("Source: " + system.split('\n')[1][6:-1])
        return system



def vis_none():
    #Load in PDB Structure
    system = get_pdb_content()
    view = py3Dmol.view(height=600)
    #add models
    if st.session_state["style"][0]:
        view.addModelsAsFrames(system)
        view.addModelsAsFrames(system)
    if st.session_state["style"][1]:
        view.addModelsAsFrames(system)
        #get color function
        if st.session_state["ribbon_color"]=='None':
            st.session_state.chains=get_chains(system)
            colors = ['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FFC0CB', '#FFA500', '#0000FF', '#800080', '#FF0000', '#008080']
            st.session_state.chain_color = colors[0:len(st.session_state.chains)]
            color_func = ch_color
        else:
            color_func = hb_color

    i = 0
    for line in system.split('\n'):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM":
            continue
        if st.session_state["style"][0]:
            view.setStyle({'model': 0, 'serial': i+1}, {"sphere": {'color':ball_stick_color(split) , "scale":0.3}})
            view.setStyle({'model': 1, 'serial': i+1}, {'stick': {'color': ball_stick_color(split) , "scale":0.3}})
        if st.session_state["style"][1]:
            view.setStyle({'model': -1, 'serial': i+1}, {'cartoon': {'color': color_func(split), "opacity":st.session_state["ribbon_opacity"]}})
            
        i += 1
    if st.session_state["make_surface"]:
        view.addSurface(py3Dmol.VDW, {"opacity": st.session_state["VDW_opacity"], 'color':'#808080'})
    add_hover_gen(view)
    view.zoomTo()
    showmol(view, height=600)

# Function to get color based on chains
def ch_color(split):
    if split[4].isalpha():
        color = st.session_state.chain_color[st.session_state.chains.index(split[4])]
    else:
        color = "black"
    return color

# Function to get color based on element
def ball_stick_color(split):
    #new element colors
    if split[-1]=="C":
        color_elem = "#d3d3d3"
    elif split[-1]=="N":
        color_elem = "#ADD8E6"
    elif split[-1]=="O":
        color_elem = "#FF474C"
    elif split[-1]=="S":
        color_elem = "yellow"
    elif split[-1]=="H":
        color_elem = "white"
    else:
        color_elem = "black"
    return color_elem
# Function to get color based on hydrophobicity of residues
def hb_color(split):

    # Hydrophobicity values for amino acids
    hydrophobicity_values = {
        'ILE': 4.5, 'VAL': 4.2, 'LEU': 3.8, 'PHE': 2.8, 'CYS': 2.5,
        'MET': 1.9, 'ALA': 1.8, 'GLY': -0.4, 'THR': -0.7, 'SER': -0.8, 'TRP': -0.9,
        'TYR': -1.3, 'PRO': -1.6, 'HIS': -3.2, 'GLU': -3.5, 'GLN': -3.5, 'ASP': -3.5,
        'ASN': -3.5, 'LYS': -3.9, 'ARG': -4.5
    }
    hydrophobicity = hydrophobicity_values.get(split[3], 0)
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
    

def vis_esm():
    system = get_pdb_content()
    view = py3Dmol.view(height=600)
    view.addModelsAsFrames(system)
    
    #can move setting up data table to inside if statement
    c0 = 'https://lh3.googleusercontent.com/pw/AP1GczOUMHVGZYT1uzxa3Bxxhra1VKflXnXcyNi-OsNOKAYpoPPrFvd4qOfQ6368vBhqmjchb7rHp17zCn1yO7EOzgvySHRV3imIigD1vmWtLZcJsaFE-QVDRaG5_0ZKJnoeCBrEdS5a4tpk-pIfyLvwWYs=w1920-h1080-s-no-gm'
    c1 = 'https://lh3.googleusercontent.com/pw/AP1GczO3yO0TLq7qUKOk67SEO4aqqjDuK5j5fcE6cQSjdMhsSJ3CriFuIRgvOJh5m7YK6hcSTRR1CD4egWJES7GWSojc4p4fhjEcpbI_tCJ1DwJRVngcE8C16ri4DbqshOJllNh6GURA7eDgIM2NUB1L7pA=w1920-h1080-s-no-gm'
    c2 = 'https://lh3.googleusercontent.com/pw/AP1GczMurj7BCXZtrfbcpXFRCbNVn6ha6kmcXSr7oomw-e8sCkTKj5po_ECivVUuM8neAKKy-WBNTPz_iA5E6J-UOjLIpAL0jDR3ijmi5ymCjXbqcOlxnXd-w9zNFof4dAuGPFAoo_PxOKmomEsPRdIJnsE=w1920-h1080-s-no-gm'
    c3 = 'https://lh3.googleusercontent.com/pw/AP1GczNyV81q2OeC_BH18lx58jY_QyfyZVTMNvqhIbwUz5PiBSK8BpfcrtEZ0otsPOVM_0qValZSe660DPOxKVRMo-3-mgGIFGB8o_WRFxGEv5RgKOtyVCDVW6D3I-ZSUU-cBKmF6AxTn1KO8BBxhAKVWho=w1920-h1080-s-no-gm'
    c4 = 'https://lh3.googleusercontent.com/pw/AP1GczOfulzfMogLMwWeGtOSpWksemPyiQoy_odrYu9wF2RO_XK51PBhqBA_uaHWGY75lNi9KFsWdk7USY6cj0dQ4dFO84aDqtOHJj9Mrxej62fgED20abrxWe2MsrBFCl2bbSFX6Dsuh6s0Mtz6biJD-Kw=w1920-h1080-s-no-gm'
    fasta = pdb_to_fasta(st.session_state["code"])

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

def quick_viz():
    wild_path = ["pdb\\sandbox0.pdb", "pdb\\sandbox1.pdb", "pdb\\sandbox2.pdb", "pdb\\sandbox3.pdb", "pdb\\sandbox4.pdb"]
    colors = ['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FFC0CB', '#FFA500', '#0000FF', '#800080', '#FF0000', '#008080']
    view = py3Dmol.view(height=600)
    counter = 0
    for i in range(st.session_state["num_overlays"]+1):
        if st.session_state["edited_df"]["Show"][i]:
            view.addModel(open(wild_path[i], 'r').read(),'pdb')
            view.setStyle({'model':counter}, {'cartoon': {'color': colors[i], 'opacity': 1}})
            counter = counter+1
    add_hover(view)
    view.zoomTo()
    showmol(view, height=600)

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


    #shortest_length = min(len(og_atoms), len(mut_atoms))
    shortest_length = 3
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

# Function to get color based on hydrophobicity of residues
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

def get_chains(system):
    chains=[]
    for line in system.split('\n'):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM":
            continue
        if split[4] not in chains and split[4].isalpha():
            chains.append(split[4])
    return chains
