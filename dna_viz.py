import streamlit as st
import py3Dmol
import stmol
import math

# Function to generate PDB file
def generate_pdb(sequence_length):
    #helix_radius = 10.0  # Radius of the helix
    helix_radius = 10.0
    #helix_rise_per_basepair = 3.4  # Distance between consecutive base pairs along the helix axis
    helix_rise_per_basepair = 10
    atom_counter = 1  # Counter for atom serial numbers
    residue_counter = 1  # Counter for residue numbers
    res_per_swirl = 10
    with open("pdb/strand1.pdb", 'w') as pdb_file:
        # Header information
        pdb_file.write("HEADER    Double Helix DNA\n")
        
        # Generate coordinates for each base pair
        for i in range(sequence_length):
            # Calculate angle for each base pair
            angle = 2 * math.pi * (i / res_per_swirl)
            
            # Calculate coordinates for strand 1
            z1 = helix_radius * math.cos(angle) 
            y1 = helix_radius * math.sin(angle) 
            x1 = i * helix_rise_per_basepair 
            # Write atom lines for strand 1
            pdb_file.write(f"ATOM  {atom_counter:5}  CA   DA A{residue_counter:4}    {x1:8.3f}{y1:8.3f}{z1:8.3f}  1.00  0.00           P\n")


            atom_counter += 1

            residue_counter += 1

        # Write termination information
        pdb_file.write("TER\n")
        pdb_file.write("END\n")
    atom_counter = 1  # Counter for atom serial numbers
    residue_counter = 1  # Counter for residue numbers
    with open("pdb/strand2.pdb", 'w') as pdb_file:
        # Header information
        pdb_file.write("HEADER    Double Helix DNA\n")
        
        # Generate coordinates for each base pair
        for i in range(sequence_length):
            # Calculate angle for each base pair
            angle = 2 * math.pi * (i / res_per_swirl)
            
            # Calculate coordinates for strand 1
            z2 = helix_radius * math.cos(angle + math.pi)
            y2 = helix_radius * math.sin(angle + math.pi)
            x2 = i * helix_rise_per_basepair
            # Write atom lines for strand 1
            pdb_file.write(f"ATOM  {atom_counter:5}  CA   DA A{residue_counter:4}    {x2:8.3f}{y2:8.3f}{z2:8.3f}  1.00  0.00           P\n")
            atom_counter += 1
            residue_counter += 1

        # Write termination information
        pdb_file.write("TER\n")
        pdb_file.write("END\n")

def viz_single_strand(seq):
    color_dict = {"A":"Red", "U":"Blue", "G":'Yellow', "C":"Green", "T":"Purple", "a":"Red", "u":"Blue", "g":'Yellow', "c":"Green", "t":"Purple"}
    generate_pdb(len(seq))

    with open("pdb/strand1.pdb") as ifile:
        system1 = "".join([x for x in ifile])
    view = py3Dmol.view(height=200, width=700)
    theme_dict = {"light":"dark", "dark":"light"}
    theme = theme_dict[st.session_state.themes["current_theme"]]
    view.setBackgroundColor(st.session_state.themes[theme]["theme.secondaryBackgroundColor"])
    view.addModelsAsFrames(system1)
    i=0 
    for line in system1.split('\n'):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM":
            continue
        view.setStyle({'model': 0, 'serial': i+1}, {"sphere": {'color': color_dict.get(seq[i], "black"), 'scale':2.5}})
        i += 1
    view.zoomTo()
    stmol.showmol(view, height=200, width=700)

def viz_double_strand(seq1, seq2):
    color_dict = {"A":"Red", "U":"Blue", "G":'Yellow', "C":"Green", "T":"Purple", "a":"Red", "u":"Blue", "g":'Yellow', "c":"Green", "t":"Purple"}
    generate_pdb(len(seq1))

    with open("pdb\strand1.pdb") as ifile:
        system1 = "".join([x for x in ifile])

    with open("pdb\strand2.pdb") as ifile2:
        system2 = "".join([x for x in ifile2])

    view = py3Dmol.view(height=200, width=700)
    theme_dict = {"light":"dark", "dark":"light"}
    theme = theme_dict[st.session_state.themes["current_theme"]]
    view.setBackgroundColor(st.session_state.themes[theme]["theme.secondaryBackgroundColor"])
    view.addModelsAsFrames(system1)
    view.addModelsAsFrames(system2)
    i=0 
    for line in system1.split('\n'):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM":
            continue
        view.setStyle({'model': 0, 'serial': i+1}, {"sphere": {'color': color_dict.get(seq1[i], "black"), 'scale':2.5, 'opacity':0.8}})
        i += 1
    
    i=0 
    for line in system1.split('\n'):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM" or i>=len(seq2):
            continue
        view.setStyle({'model': 1, 'serial': i+1}, {"sphere": {'color': color_dict.get(seq2[i], "black"), 'scale':2.5}})
        i += 1
    view.zoomTo()
    stmol.showmol(view, height=200, width=700)


def viz_dna():
    with open("pdb\\strand1.pdb") as ifile:
        system1 = "".join([x for x in ifile])

    with open("pdb\\strand2.pdb") as ifile2:
        system2 = "".join([x for x in ifile2])
    view = py3Dmol.view(height=800, width=800)
    view.addModelsAsFrames(system1)
    view.addModelsAsFrames(system2)
    i=0 
    for line in system1.split('\n'):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM":
            continue
        if i%2==0:
            view.setStyle({'model': 0, 'serial': i+1}, {"sphere": {'color': "blue", 'scale':2.5}})
        else:
            view.setStyle({'model': 0, 'serial': i+1}, {"sphere": {'color': "red", 'scale':2.5}})
        i += 1
    
    i=0
    for line in system2.split('\n'):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM":
            continue
        if i%2==0:
            view.setStyle({'model': 1, 'serial': i+1}, {"sphere": {'color': "purple", 'scale':2.5}})
        else:
            view.setStyle({'model': 1, 'serial': i+1}, {"sphere": {'color': "yellow", 'scale':2.5}})
        i += 1

    view.zoomTo()
    stmol.showmol(view, height=800, width=800)


