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
    c0 = 'https://lh3.googleusercontent.com/pw/AP1GczMZOGDttrtnn2F1iM9z38YOE17aP5PFrSe7OnRZxlFUHIkvgXCPIBbHZPOB_gooW2J7YBJGmwToN-WeSCBSnHukoABNKSET6U4mpwV_jDyoDVKtQdDZ6Suw3etpm0XWSBM_Rc5aV8fu_51skX9cEyhmiOC3k2gyx1N3qlnx9giWBpzMsLJkc-2fvVEmlQjZ4txTVJPXmkIWew_k61s9J4jNUuH9augnQDkwbPZGNTDgUmN6NxiCii2jz_h16PaYzMwdoWjyqDO_PwhqDTUo-MU1TAz2KmYr6PjdIjdShZnz3k5sieP6ewvUZjGCXshi7dTCkNJRq7zKx3yUPjOR5p2fvwEq0EkuBWRG1liFbLpTqApYE2t42N2G-DdkYNiyESPLUgbE7shgdz2NfRobayAMNGYcX5hHjJI5ayIY6Uvhx67b6M8NmCKpJADJzPOT7krs7lwOhisiPtjkTro-dYplXGrAnKbHjZk23xyCIj_mVtWkYYAOz4reqCCZvQDeF7GghFgVUVltw9SSWf5_KCnfX8NstHMaR2GHUJ6-lX4unqZ-RzdM4U4qbBZYC_JH_OpaMApXmWKDnSTkP9k5PldlrIjCUJKE4XvzehGtHDVsA-iBexQwOrX_-F9MyTSt2H5XVfXdDc-7k0-_tt7W77YKQMWqwBiIGmtGlxgRNKaE8CtSr9RPJuFYB6pZ1JeO0R1AmUnSphLbSYYznkRBDKqFz6v8mlZvs1Ja5inWpaeIWbOXNMuu1msYm-K0gk-QT1ZO0kUBTb0nvky89sQBXKaCzDOzfpc_zP0uK5RP9GXllWzh5GT8tkV61wwpjnHkO8EC4j6IMhRUMvS8FWKStvcJ1uHQ34vnHz6RvCU82MEtM_z_t1mkXrenj7n3HTUf83ftKnH_9C3X-6uxxh0=w1920-h1080-s-no-gm?authuser=0'
    c1 = 'https://lh3.googleusercontent.com/pw/AP1GczNaryjartSJ-Wl7TuQ1z5B1bPlzCzmRXxAM_aTdm_0R5j98g8-BQyMhhsgfuXy0abvd6s3HhPaq3azQhT9i09uYLpOn9IunMCCOXuvtK4xttf8jEEVrcfsCs5B9VTSStNcubKZqvNs9O6Cpe4Yb2zNqv-EFEo3i_d6kk20AtYCaqLhZfQ-K6cWGKD7IfeZ0ZabMetDOAk5zD2kh09D7yVsDs-KSTKxSjfw900pVFyBAeIbxhHHbtUYlXOfpAuAPUzS5IVdtrpNaJVwJIsjQfvl668-q9fA34eelN8X94Ocq-9kjUnGSYaYePtbPfSqz5Z72AYUFUxfAiRGp4khxxuh3MRcoAb9PJZ63ByXi1dq1WXmEAyVsKvhmVc4V77zLZMaCqa3tC9H0NU3nP8Ir5-oa5PkB0C7usIyEClW7WROd9GGf6K1c4OO3n39Jb2pWuIaFBuVvBceLDcVXO_i00PbNS8gcqL4OwnXp37Xgw4aafcDP9yY9LsCqkWhKhNPhlx1zFhT0c9kuU0Z1cIM_lH4WXVPO4wxF3aDxsC6qFM_nP0NZY72FKzmdOq_mUI8qf_eQHkCrvWayeiSYyMpuCz6LS9NCuNhk8jUuyDRdHXruyJo770PDSS0aALpPfLQ664yczmjOQUswzgQMwtZlefj51x1v1NAuRk0XUoOFEpVnMqFrFJ-mmG8OED3LRiicG66Dcso3VrkBhdwFoZfeQ1aSIh5GQPwgnEMh_7e2DGB-jYOIZ3y1itMVhjc7628ePReVL3_zVKO98ZIX5ZoqGfKn_yyDvOD6ozsoj9QWLN-Bco9rFloETuoLcCD_FgXEUryAYvrOcclPZx016c0V0oSC7znXURK6pyPMvgMtcem0lCKp8_T5ykQgIGpYacxXmD0eqPWmOotwFB4xYP4=w1920-h1080-s-no-gm?authuser=0'
    c2 = 'https://lh3.googleusercontent.com/pw/AP1GczMyN4c5kDyPDoiaCnFEW61C3EUZm_5A_oy3fgGnb9ow6pBQsuUq88lYhjH4GJhiUzeXmUkDNXwvrc4whHrreUhN7YVoJ9XfRn5BOIal3mjcXEN6_bP4I8KU7VPRqdfvkqSwVidi_5IrUu5z7qYW3kfkRtsO7SbM3H2J5w1xqXTOSLwr7DDYsG4nEpj5SI7IF14f899IKSiTtRIOuBI4F_lFbdgOGeM5-YMvbuPPNwOuhPku0NTOl-9WRgIeQZlg79um0sm6givpcs7bdFdPPsJbTnt6Oy7m2JgskvxvNhx93UyxbWYl_rRyMUSvmvBfOT1wLY47E14Iibhhc4vd_dgGFUufIUSdymlEtOu0NXbhFW-Xx44AHjb648UtV_GljkHy2OPUua3ysYrxhkroQAHL5AzxTT6huburaKdP4xHVVcHG_yndP8KGUK3bNB7xiErdA_qfgM-gaTWl1xj9ECJJIU_SBHIDLmvV2Ft1ytJg-Y7-AqirLsr7UJF7AiD5SJeg1PcJKrH4OlT0IICL2e1wBsLiNUY3M4UWefQkPJbTP802WdvvLfOA7ThadoZzth2EGQcTvmUDbNVub16kLyrUktxfVQER2RDYogPXqRN8vcwGdtyu3uASQIP8SQrmkTtrrYuqhLVTvdnegjiDuT6bGv3olWkAlWwROSXRRq3EqjGXG5pEd0PiZ2N5q--EXl5ZsS2335qccpKC9SzXaRLuEFgjM__ZE9E0wgY75ChdGa2u7CPKNA5eQyOT1K-vdG7bh85hqmNEPJl6oz9EMlbIB7xwHyQWFNupr_Tk1zASlhfJSQh3vRPEN4kW6LFBmN4RVa01fsbpQIK9_Co81tLBYTWAQ5zQ3MKjg_s0O9u7AEV6NA5_HEVBHxGjG9aQj8gmkc42JEkumFkrRBw=w1920-h1080-s-no-gm?authuser=0'
    c3 = 'https://lh3.googleusercontent.com/pw/AP1GczMQwRk9-H7BHL4oBwdeFDkId6iqyoLVCDNFcKUFrT9a3oyl9kcVf0h4bcbK5fJAS9eL7cOPyS1zaISEOpVqOIhaeyafje1dYlrtFmC39dPZnN7cyeexZTkJKBjf0FcPn1FyPXTQ_iMX56WOC5F43mkIFbos9tQmj6DVIUBZ-82QDVyQw-3s1sVEFaKNmM404NJ002vULF_4uueiDyaB1tWd6Jv4GSjtJSEZqz1-nZUIwGnzeHSGB_06xFXigJ28JfaSTU2tNlcau4McsxqIYBn41RRuAuZ0M19wsSCcCw-8Dhs9WppDb3p1IFwb3gBp84vInMOfFgKSqmPrhY8wcvyJqnDPFnly1QHT9CZKD93wCpnYWSc0C__GEoamRjNx-9S0tp-U_qL9I5wAcn8V8YUrUyKy78qA8qDA1wnKUXrOEaegYf2cCOqOeU0GdC5q010vUxEriADG01zXUV0EbsZNQEFzAbTgxrOCjJnI_8RHqo1Cf1v7wKmXURcBcZr4h78v1-0UEZUA9_9IgQ-8sCIP39UkYPGMf0PMUHxbVVtre3UiNLRLtQVqQuByX1KvzozDxME1hen1EgvftnF8TcR6DP8y_-vKnQ8kJSfRq8yuKl894ONvaDXCD5cHQvcyL9vVBZzZsRhG_Nk1YVOfTAb9NOx7JhspZLsc2Oj-99ZF1XUbcUskQI5IYiSxPVl1w54cjG-7mrwTFThXHo4m1CLx6gbQRFHuyUTRVvErZnWMfQoV1o0KSg94v5mPFy_u4yBUpg4OwYlg8n_9oJAOZ-Sp8XpcjhozRT9BQ9egb865lSA0DLNg8HMbcL879hJhIUlfJnPjK41voBXn1n_VtjdS51fCsePjVghSplcMOlgXsN4BTjouMIDxLNku6Qgwywtz4TcRwI0vnhIiR_8=w1920-h1080-s-no-gm?authuser=0'
    c4 = 'https://lh3.googleusercontent.com/pw/AP1GczMFwcCnpjHpGFAgZhQx69RklP_tlWkU3D_uoe84XVykxCr7zJboni3TbGpsrG4H4R6_lmZV2EbrUkK6uUXeO4XtMEULpIGTlAwbzJw17SAfkmrXnbKsZS5SnL9lJKvb0Twr3kn-ZwykLNo_a6iCSY2fIJuQQHNwV4Hbmxn6hMPYyYTFJiJPZ1uaKgfM6E__v7i1Jwsky6g0urGsfnufeEZdtzOOYs0bQCW5H-j0ZZCxudTfvEc-XhHf5m9I7eUw9tOKPKTDmPhUFqakLR3i-d9vppb5tIOxIt-u02JB6dJpGAipeV-e5PpbG1oqwHzATuJlBn4EamX4tCRkwAqWSgyJzke3tbY9P2ZqZCyMiRRSHuocl3j698k8IZkJ-kLR1BY6aZU0dBUJjDat8FXKfWbYv9CVRnp3Nv-vF1oWLk-s3rgYtGGN-7wKQNafNDndz4-jSSrqupB7fW2O7GDsKEqKebBo_V-fG6HzV_cgAocLNsSRsA7ypXLDAzcYjV66fh3eZbYXbi4vAGX4o1gItHzTiVzwUbXb01uS4tjPiODqEmTRRrsslJPvMd3q3PQQQknJwuMMFQqNCn9P74Xmi5pfpZ6DsEaBz6xa-nkVUqEbWE0AemQ3YjPsNGMs5zWzUnylIoAmud-tStlHE09dCKamvukMHRZe-WI-YDFf2wPdz_tAIO58USt4-_pLEf9DdM-XiAPx20GMiACUIDz6neQW8j1plpGbGyHVUyA1mSAnH1ucgNrEjpr2O9OutIgIqeg5vDk1SAQb9mfpSzIKaGfkPQy59sRi3ZGaWTRbjMJvVQ1NwomZoLtwRntpRWGJ5q4ymCflos3SEC8JZ-xRMj_8pPu0jUhFY6ucsAL2z2GoNy7MUfqCGzMBBnf6e_PbNNDz21Y0kSFK6h5utYM=w1920-h1080-s-no-gm?authuser=0'
    rows = [
       {"Color": c0, "Sequence": pdb_to_fasta(pdb_code), "Show": True},
       {"Color": c1, "Sequence": pdb_to_fasta(pdb_code), "Show": True},
       {"Color": c2, "Sequence": pdb_to_fasta(pdb_code), "Show": True},
       {"Color": c3, "Sequence": pdb_to_fasta(pdb_code), "Show": True},
       {"Color": c4, "Sequence": pdb_to_fasta(pdb_code), "Show": True},
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
