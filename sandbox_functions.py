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

    #set up overlay interface
    c0 = 'https://lh3.googleusercontent.com/pw/AP1GczNUryCWmTffrqoVj4-CbFrt4NPxP22C3Kbef1bVla6Ur9xXejbK71_-keZgHPtmErznwXs3-TgJ2jUeaVunDhMzjXmHWQsJvDyq0vsWgUK0vpFrtJf_8Tb9OBH0ZEj3OwfQUW1XjiQGTjyJbNr9DRegWTps3PEbSncMtiMiI2MqAt_idm_GM-M7vL0DlQS_1c6eGd6cMFfjSXQvW-nJymJ90HuimUXnoA78eSerR_UCAiGI5CKWsO1szXQC8PTSBPivANImiAU0u4VqpuuzymX8gzbgR8tlY97Z_gSsiEZdkv5C5vXXAs_L3rEXkCPv3ARjiSxQXw7vXwRIhG9vPRF_NlSXZIHHp1Cbu7xkfxt6_UUBThKs_uQmRYKn8PHS88rRkgFInhmejNrpAU6M5aNmosDlpmE3qBQ7DGMYo-TkeWF7P5zCvMBom3g189P00sKjmUZ6-UdZAu9QjYwufXl4Rf4lMgxAFe5z7McsiJR84JPRF-aQleovGpL8MV7kJu2W1izliUovhjXYXQxNZGXAqwhv8Eemzw-XxJD0gxxMDYHNwfREOXYOGaAlRGt-u84sWg2usCoDJg67XaCv6px7Qfs5hcOmlHdFU5PH6BnnxSbfsrzBBzGXBHKBqlIFYT4CszFMyQDgmCVqQLyfo8MY3khwFo31miJ_8outbD8hR2aWk1Ud7Ic2A9PvLMYe1Xm419t16aMbLssYPF4nV45Ly8QvOD7Fx9d85Gt-rqrLqEzHEUM2bEqT9XZAbhU8cO8ut8W-_IPllsjb42MuqRGg1eJfyoSe9uiv4aBrZa0TWJF7eZUWOHsNuv70KDU-2C6AVqSmvgd_XhWrbi4znMrpyHVMrgdEmBkqy74l9g--u-FY3ZOLPteIWRJwpmmpkhxOBZl3fkAgolk7B74=w1920-h1080-s-no-gm?authuser=0'
    c1 = 'https://lh3.googleusercontent.com/pw/AP1GczOxTJfgXUeDLvGDVtggDCOFHhsXF26GPxh4loom2198yCEgOSRHmvVoWvViVvceVMIEBzafSyFr7FP1Pjc2HPk6SAaay0maGR5hC4ZZasueo5Ar4wszc8DoYEuFr0pB2Cnm_TnbP0rocUSRNocirKx2vD37heq-zHSaSZghYWkJTbRFrIgfXatPmycqjukxbjmorEvCg-802y1jRQg4-EZczZEfPBIChziJrolpj7E9vuOXAxrBo2xMthX5qo99fcmLhpW2PMdsORM9BR2iqSl_rX7KU_JZZpULtdQ3dit-O_zLwdurF9fQ-4fnbqUCAr9vEKut6RBxAsJcj7uZTz_KuPGk6j-a4X53_L2RFu85uh0NPAqNdX8Z9ZXIQGJ6Ex0Bmoqw_sNfdTY40wPNQ0780v2EevgUFq1lG5d8YC1JvkA276kO7hq8ltY1VAWysvODzWiS6TrT96i_6jqX2MOnNpEOsQh9HYKTj_36-PsltjqOOoD2TFBbOz0vj1xwVnA8Uj3L8AwxQWzK8grNSQj_JFZqIIJP2WvNP-nnCqySRJb3I4lz6CS3EjIpI8MLjAF7arY7FtPEJX48oilxrgQNTBAqR8JWNQJfa9-VIUO4ZGdWLiAPRdHcZBuWYiZa1B7152lhmAX8jQElNDHYWFzl8ZMnsv-7cGwIZgZkK7zIAd69ZrZbCO-p2aL4H8knKFgk3ryjJ9LqHGZZAmiCO-Nu0ZWclFTQFE7rfF48aTnvAsr7hJxPDDGNHd6aUR7D-EztR255slEJQ3U1NSG58xGPnqAmerkX_TOGcjdXyw1rvwt1nPydxy8sCH325ko7mIlajnWd-E-1wt__p-f9g4bSwgjDz7t0u0RsRr7jOrkAsPODTdgjFM9UC-w6MV0xPvlw3ncdXazMj3dKgoc=w1920-h1080-s-no-gm?authuser=0'
    c2 = 'https://lh3.googleusercontent.com/pw/AP1GczNS6rXVQ0T9FtpqD2VFH1SLdlTdVAk-rgfu2trOqyl8E8v9z0mDrQkVEwMZ_fjOfH_mpPLXSjY_48r0kygv_IOLNQTbiVnvXqTtnpfT0wYk8LWh_65Lm7j6lSJXkABigPt6wrqHiwreKyo_nhsapBT5P3dkpggmmjx2SwJgKayE8yv2_2SmdBEafglQesXreU-Mj8J-3yQx_G0N0OmRt89ZzMTWYmqYHTaLsBIHudYJFwg9rnvfrehJI5OESXFxYZokQojPqUP3T6zMwWtjuGs5Me5JB-cBAKd6kbftaGC38CH0cpymB6zJkFjYmOL098YA0pcu-laj_quqFcgYdrwvX5sTXpzIgg6ipSgLAoWOHeEbmWm4OXUkUt4XbSdsFyrVddKp-rPwSUx3JKAbUREQ3oaWWohc6yesYzz2IWGlqeOB9lzYQD9yw9gg0_VpvlDdMOsS5_jKXP1b_89iBd5qdE3NU9Psi2_El0WVPoCjpenuEcWDYDTTgHuLjDq-fLYhftjdPuq01NYKiTu_D6ht3n4KCVHqIIdfwTX6tKIdd0tp6p9LZ8HHE4k73rfn_XnjOLF2dHcX3dKr4kSw97sQFBLzfwLFzdsrYAJ2bt4v9xUaZ4hns1QA7dyfC6VxV-lIJdpC1GMRJrln3IrtJr_h_8GFSvUXgR-96nJCBOqRYYDyAvm22jfiA8cUjrLyukHlmwlqlPQNorQgCISyphru_flsnES75Eoij1mqZK2XWdKBnxvcbD0ZwM13GFSQka-bQ_PVMrNn5lqTAQm7gPgMHXLWyUisQUwcxPkk4PS4bO1Au3mcAZZ5ERjE1DsJHmS-yQTY_SmwHu6T1rMNEMLlX4M3JDtw7gCWC3S28Sl7e5Sw2KMeMCoI9WFp7lhh83PSwSNQWhURXw0lU6c=w1920-h1080-s-no-gm?authuser=0'
    c3 = 'https://lh3.googleusercontent.com/pw/AP1GczPpMWv1Rw88sSSNcl8WGbuDcQY2o7eUavH4PaBt0-tabSGvsOxM3A5avZZxNiKhA7Z6vFv_dUGqys3uTwjmch-8UJRqhFYjPoL8twMrZNnlouSfebrGoKvjxbXcCvHvbQJiaojifCNmAY3dNMJsvGqMP4GDICcDN0vI_LxeSVY7GJgxRo-BRHMMCcEqmXsT1fYPCwAf5hSh-L1_G5REcwmt39tIaAKZlBbvcl3j8-PfwG6uRRzTzWLJJa6xzC4IpBhdxy6llmbUF0KiwZmymYTEOyC9yIikf58hIrjZGenzHOuqkaWrRM14eo94aTv4_ptAIHoNUAk9HugBnWvwfBr2QAJd4BE6yT91qTQqk_32rk6OVvYhhxgcnv3AGCc7C3tHvrw_Z6rowU3ziz-_e9_FSxaUGYv4Q0PDvb7YjPdFhHLmVek-ClbjN6X46-JWenom6ftXG318P2BbpKaTbQpaW5HnSf914x3cdqYZMhiafsCfnOin1ZqcnHQ0OIU5XTpSiSAp6bXIlQkP1k8TuBt7_pfq1wrdP9bZ-BPDV_-xA1nmGkBf0vuw4AOYV3LlPIQxyNFU0HYBcnFVXB2gg38hc8CXs-Xg7VL1YSpbR1-abebUFaLbhEYFl6_lghMjQ_qkl5YEyu1Jn2YUtm5p6Nk4VgUolzDWqFd73PwQaLjkEOzhmJAjXs9HSWYa6N4LVu9gDGT5Yva9GBMYzA3yYVtylR_QnrKAjyNBB_LFYDXW0pfyVFzpGCbsslPhfamaSU0QvEt7r9dd6Gaz6qM_Q7QbgPWFJPnITORvZlxReVX0CvGm8aiNlSMOiKG2isbhiPXjCd3okNtnRMQGuy1KZ2CHHHUkOtF7OEfGcZrFyhxOA-wc1q5UiplEo1gs93xSoyGhdNl_iSBZIW1wzGA=w1920-h1080-s-no-gm?authuser=0'
    c4 = 'https://lh3.googleusercontent.com/pw/AP1GczM_ov502BEy_fnLQoib4XhizIDlhQYfcnUZVdgUA7YTvbFMj2-B963LBV_TU6JNIwzEHcnALw8u5o-D63mkdPPR7IoQMAqoSPmaL0bOj7AuwmW9MOnyXLhefGYBUsEKxuNIjXCgp2StG5pqkCxoIAAOjhpjTZja38wpstQ8sVP1MievWKmJ3WWudFfqQZwYvwZwgBt6_0vTfzVmKzOeVhrS1EZMlZpOxpe058a1BQfp0yeoMULqfcSik6xkmqCVcHwqjVGD2GjcNmbOc5DlXPmP5IGu2jhICEKSCmhEnx2SpoKQykMrh94MHLoeiZf4rOWLXzJN5u6imQF_sDKM0artk1NK-QhsdcJwZpqiAP0kbtkcTQZ_ddBx3Ksl_BoVuHqk5b0DjTgwBNynzWHfpwJ4n2O8DL__Ub34daDjcMkn33nGUvZFhjXgdqkSXUmJSOif9NHqzVcWjApU74onx-vgntiqe96s6CEKKujBC56braB3ETBCPhBvQBMjFDdEhjvijxq0qD-0XvBSyqAhATRQ_IhKGVSC7Rs2P3dun46nqPe_lY5Nh38SE1MH94V4-xA3ifyIH7LcizXnEmXrN8q0G1_BjNnjUJ82LOtyz29iBqLn5jWd9hjNqTr8KJQ_re3livxBtBKXqUi1YuJjQfVRDAqCU7rKHhaDTPt837xhNVofoUlsGM0XUzChcn2_STz3gK5XkrHoC2AToPMESnQAsoYyp5dVkA6hHBYD65eb8H3OOus9KwXUiX1A0Z8fIH8RXWqPste1xTzadrVmHfTG8_5c98PjdR2_7v8Bv6xOOjQ21JYXdz_ST9aI7_zTGI8ltuOlQL2D5J0ZNzJgzmGriYF6VHqHVN07JFPLUi2e-WRsrGMFsQ2zMlwl2EeNiHpg7gZjVf16yVvHdT8=w1920-h1080-s-no-gm?authuser=0'
    rows = [
       {"Color": c0, "Sequence": pdb_to_fasta(pdb_code), "Keep": True},
       {"Color": c1, "Sequence": pdb_to_fasta(pdb_code), "Keep": True},
       {"Color": c2, "Sequence": pdb_to_fasta(pdb_code), "Keep": True},
       {"Color": c3, "Sequence": pdb_to_fasta(pdb_code), "Keep": True},
       {"Color": c4, "Sequence": pdb_to_fasta(pdb_code), "Keep": True},
    ]
    

    if len(get_chains(system))<=1 and st.sidebar.toggle('ML Predicted Structure'):
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
        st.session_state["edited_df"] = st.data_editor(df, use_container_width=True, column_config={"Color": color_vals})    
        for i in range(st.session_state["num_overlays"]+1):
            if bool(~os.path.isfile(wild_path[st.session_state["num_overlays"]])):
                get_esm_pdb(st.session_state["edited_df"]["Sequence"][i], ("sandbox"+str(i)))
                if i !=0:
                    sup(wild_path[0], wild_path[i])
        quick_viz()
    else:
        chains=get_chains(system)
        with st.sidebar.expander("Visualization Settings"):
            st.session_state["style"]  = st.selectbox('style',['cartoon','stick','sphere'])
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


    view.zoomTo()
    showmol(view, height=600, width=800)
import pandas as pd
def quick_viz():
    
    wild_path = ["pdb\\sandbox0.pdb", "pdb\\sandbox1.pdb", "pdb\\sandbox2.pdb", "pdb\\sandbox3.pdb", "pdb\\sandbox4.pdb"]

    with st.sidebar.expander("Visualization Settings"):
        st.session_state["style"]  = st.selectbox('style',['cartoon','stick','sphere'])
    colors = ['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#FFC0CB', '#FFA500', '#0000FF', '#800080', '#FF0000', '#008080']
    view = py3Dmol.view(width=800, height=600)
    counter = 0
    for i in range(st.session_state["num_overlays"]+1):
        if st.session_state["edited_df"]["Keep"][i]:
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
