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
        c0 = 'https://lh3.googleusercontent.com/pw/AP1GczMXgqPFYsqjT33Yois55JinybhKc3ZmWUOQHKiHOJ6dZAkHYFxyPknh0bCQ2LUi1aL4Kl0fxjJ_z4ix7NfTBsRvs3kSqaSRTqWTKkCv2IcCSSXIGbvMaSLZjufz1T7KnWDxRVvx2LkuWGOaabhWHhT8AiIuS2HseQgxnxAMos_bWyGhTdRv4HoxhhkjwZJGIkvfTNtPpVtEQnRnOk3xas2RSgy405xEGUCg9rJwxHAXYXPOpVj3OxsXJuxjycUTYTx-abL156DcVwwCXcLNXZY_4STONLm4_vobMjFaog1hJ9B29xTcCWTCE6Qspy1ZpAmOYHgs5Enm7hHmA5kAPK-LK1_Iq4tOEdJCxLmMd3u8sZWt83sVI4epqpyAtHc7kbV_k4wmGnrryYuMWZ0fq-n9SmmVGxaaF9u5Isv-fzvcNJdIkuv9eoCxWhvs-x6D1YjmiQDy7ixW_QPRfWYUo-E0_q_EvmHay3zaub_N7YiiWYoIiTZxfX7wtP-ap-Qg9eyXWQBgbDl60YeD8O5P0LHqm04N41waiVgI0WM7ozjNq2DDuM4OmTGWxYBsikLwVrpAf_DUZh7qeibUpePF-BT5fzrJVnDPGnk0spMOebAB999STaY2xfRhe3sw-HmkmCFMkE_oBp8GJRpLXM4jSf4_c5KoTjdzESLeyjv5mFRtfiE63zIJaQNud1xZLa5wgncue40IL8UADLUzJ89jn3mfnCEgweEgos8lOIwI4yia3isXt8fe1FvaqiRI8sLaNDoDVCkR6DbbU7xyF1G5gvRtqorHAl-EuALfSV5TqMcojsY3ioIh0xZxL6zV5-U5uBegeYahSQVIihW2kPhTrGK80Lrf5ofr38hhHozrWPeInbrN_NpcW4RiwJtrosWyeGpSrdwlARPvt0hfVeg=w1920-h1080-s-no-gm?authuser=0'
        c1 = 'https://lh3.googleusercontent.com/pw/AP1GczPErbXtIuHffPuPIaZfdAq5pff3pucCOC23SR6Ye_FAbLhkO4_nUtg1rO9Ha7PMaz87eidypjXqIb3_1SFxPXcuwfEBZeB4HnU4FMLbcPpMEvEQ3dp7bnjAVBMdTNj--KcgIxtPBUn74hM-SBmCmWAJYGPuNSXw2JTaZ-6nzUVDVmtgCsSKmtrXm-41d_Ww2a64rCWqpc2njMbs_9E1VLSivNxlWVYk4Ap4nsvyy2PW4h5Vyej7mBnGPKbyDn6HprG-luB_h16Mwo-_LZd0XjnjVTc_MAEyVQOvDAs24z9h39qlE6YoRLoZ8lxB1RKmNFvQOgIAm9AwyNWK_qdM-rTr6eVFZZeJhbswyrbQ3ZKAFfASYnLIltW-9R-odUrGMkh36lO-0_IuAjdqwyF_Eg4BI1isfiZJ3fCtAU7FmLbb5BA6se8VNe5h1FEeLZX0u1CsTHrK-2Hey9hFQcd-HjKSX4ohNwnxX5bU29WVBELs_yweaPaUgr1wjsLf4zjTid_MXVAa7rfZIZwGC6AeqDCI6oYM4zhspvLdTycH3hiqTx0bRF3MCMev7LQg2El46ts1gvX97uGRg-aKSXx9UwP8JaAa0ndxv-u9uu1psT-k7_3aXEqh_yR2YcamCrAywJ8_1KGgVj_pB_NvAMU8iCnFOm0zAPJzfB3l7hEXy66OE-r6yHJDDzWjI8MdzzGq0daOhC66IPttQpvtQ1lwKstlfVqOnZyqzTI0pQfP8cq8wGsBepmkLnmRYJoeinQSqA_ywnMlFBISI_wW0whjRebFRSicM2uRlwEUmN6zJq7J4uPNl5hJVpI1LeiMge6CHiPNjyBbFvAplMpTmV_EjeIC_hVY59byE_WvqF2vnfZ9o14-ev21xqW6SitV38w17pUUIhDs2Wf-NyEduuw=w1920-h1080-s-no-gm?authuser=0'
        c2 = 'https://lh3.googleusercontent.com/pw/AP1GczOFA9rlWelpFMaMocOsoQZCw1BgzIE1aM18FScjv3H1O_CEQwQ3TU9EKpJIZmR9o42q79DYQ5hTe0O4b_LxABdPiyLF8AVqMlCVFKxSA-htpkzlIjcAX0U9Fc8QTc0CK4-27HYof0E44nX3jsu2LYm_MUnSvm0UekYYDdcRRCm98zfUyMPaTqrmphWwJW_8-FlLhhC-57jyw4rWhzXdzQ0IGsqQJgUCvso90PTxUt5v8A9rHT1Kg792p6_joRFe5OBnPDmJrFVNeldHI11Yg3jCz0eZv1yM8R1S9cG7qOWlt4T-Y4MqrGeNnojS2Ztf3GUPm8G1ri1jEo31Oxz1QTQ7DoOhAWcZ9ZqVQr6ihd_M-5euchgicC17wRyxiMMDBuxE7DTbKElABPG9WH450h657_isK1MKNn15myqa12PZ-htjRwNl_NfwSE_OHKSrLjfR1sYoEZai4JKektrLEKA7wP5EdTlXqOlgWzDENWO5VcEZiiqPioJYXz-O75sdY-R00w0_B3WLx7Y60OqcJsW-HQbzpaTGhSXv5I9Lcxag0k4gAXCeOXBPeyG670vmfnej90rUGy505oZUhlUUMzo8RFz9BolqKYeUWRX0dJspvEQQhObRAu5WRGTUXr9bsP8BuraNhCO-KKUyYwITXBHfjYfda0yxYPBMOMmdUfSiIGlqBnfLQsxhwAyNvo4cHn-BKwNNxyw5RCL-a6a7XsBTlTKY6uv7ghPkLBc2Y3SQiW8Qt2pYz_rTGnKpD6pc_6iskS68awjAD5-s3jyo8_bTW1Psk9jx4P641EBEFEeR5eT6xVoQ88Y6Hi1sUrz4pIctJPuoWKHqOPtaa2f38iUlIT981OfUeu3F46fUaCUOQxNn5zKApEyENYl68pIps-fTaSEAgfnG9H4-FIE=w1920-h1080-s-no-gm?authuser=0'
        c3 = 'https://lh3.googleusercontent.com/pw/AP1GczPpMQtOELzrWxA9MRNPyDhFMgPLhtdi769b7jGSZXYETKXbb_38ysoP71DIPNPhwOJahxCrh-Zpzsc8aq_dDXz71qzkKAljwP6G7LgRCjkDfgBV1BbpMWtaQpH8fl31DGSM1ifR4eG9Ndp5cO2GYUAMjuB7mQqNQQn0T3eq3zgzza-uCCq71vk_2SOXNfKA-GND9PdRpHpDFLXyh4PMaOhVaEqj1fTAjyiQ1mHNf32idkSoLRNNYBCNMySRs3hmLY04yRLmqN_XdHVOm3TFeYdIJTg9d_6iYaN_ngBQFGIw2euXjky2Am1ahIWKT1jKvsYMeuLeOSwcZqI5oI414Vkn8DKKZoYo23LiOTLwmH7Pz7mMHFfLdGMKte1hkL9BhsAD7rK0IVmUHLw37E945hE1k9pM5uKu8t0XeTC4EZMbxFVfoXhtsh7M36_EkMOWSxtu8FyPfkwGdf-BIzVJOMOOtXSDP9J9PzS-0YFW4hu_Ef2-A1tVoUok4myHpe5QvAeJtd7YaxCq7r9uwGmV7uqleEEw6uwAJB_IgpqBIKU_A6Dg3PzPgweJz8JvBpO_CYTRg6zcP5SFY1XmY_fAkqNupdTt8esAsBr-yBtgrbPVbaXCCvxriWVu43wZNJOYMJ0b8bbWs6Sj9enrf4jvP0PKIyR3YfYbPPvK-wFD1R9RXQ5YSeeJuQQGPmxqiOrrbJmibYeNh2WGasnrue2LZZ9OjzHrAKoC1XgfzAZAtYghIw-ueR96uR0181ojiSMnmQGTq_lf2fY5nVdkqWNAUmWPcRarcG1JD91xIo4r9xuSNXWctZy4i_Pcbb3J1XxKAI3FjDLjJlF-gz8SPPG5dUc4__Xz1CQ_IY7Q6xwjwPEbx-BI_5_V74xujRImU8PLPHcjYUPWjYigG1Ovkxs=w1920-h1080-s-no-gm?authuser=0'
        c4 = 'https://lh3.googleusercontent.com/pw/AP1GczOc08CWhOM9MrQGoGaR0AcYA42Yz3UKA7ymXFW4ozuJd36_NKXq_st5-QNWw34RmiE824EXWBch0SXh_fax92l_yaTtU2JjA2djJhI9TkXaBRWYJpwJknAO8ZEfa7nNQGMiajQagoH0GT3ZN3p_TveyHInVMwu8StuHBFAzpokZVsitLhG1wwnKbI5s0f3XrVi-IrBxdSUbxqtliFHBEbnBiyEpAM6oT1c3NRFHq8kxnlrQj1hUIHCHo0eGRjq0ireqEelIFPZiwhFUC-xVv2tVZOHb1CSf-hprh0TP10c91sXpjhpUl91kBVXDhxSSBmVR-zMONU3VNMGVCd_6UzGPpaailpeYOQX1vgej3ojsmvEIe4sJT_cvT_g3mREZ2EnSUQjpkmRJe438CiYVJAMdxRf4BBMFfszb8Aj9CbmijIDO8sXE3rfxhGOSPh93FKbJyx4ScdzuBjXbkwgYcxbdP5iC3POrOESOF3u2I_KdlWvA-BSardj_rpzSkIc9ICJRWeFuseQTa9wGyhMEwwnoCiPafBmbNXT3yFSh2T4992OI4TcH6SvLB3G3N6wDIaYW_Ea8lM7zpalq5-UU-4KiOmQvrl2GJ_u5l3_VjDkcAOOfwSPepmV_lFgVFkQ2g-5Ci4vLuZih7sfbMmNwlMGW4V7erf7swu5jVGn-fGFx0mEm2Jv9bMW6jlr9hAYjA60CxKGWROjMajVQSG4nOCjK9npTvPX1iFi63B7llRBIsDyo7ra_xdhPX-RVJ9INrPGU_eRE92Vum1a0q-zWHV1sEbHhqO0H2dJSBcq0JJBQUoqk-zKsoHx_4VjBMHteEI0Gy6FkR6jtP2Ws5JKt51y45-m-vWBODaanel9Ijl_t5nK1VU7Vh5ASYm4Llo_meRyla27qhN9Pd2yiyOs=w1920-h1080-s-no-gm?authuser=0'
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
        st.session_state["edited_df"] = st.data_editor(df, use_container_width=True, column_config={"Color": color_vals})    
        for i in range(st.session_state["num_overlays"]+1):
            if bool(~os.path.isfile(wild_path[st.session_state["num_overlays"]])):
                get_esm_pdb(st.session_state["edited_df"]["Sequence"][i], ("sandbox"+str(i)))
                if i !=0:
                    sup(wild_path[0], wild_path[i])
        quick_viz()
    else:
        st.caption("Sequence: " + pdb_to_fasta(pdb_code))
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

    add_hover(view)
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
