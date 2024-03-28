from stmol import showmol
import streamlit as st
import py3Dmol
import urllib
import Bio.PDB.Polypeptide
from Bio.PDB import Superimposer, PDBParser
import numpy
from Bio.SeqUtils import seq1
from Bio.PDB.PDBIO import PDBIO
from model import*
import os
import pandas as pd
from puzzles.puzzle_help import amino_acids_to_rna
from rna2aa import *
import random
from puzzles.puzzle_help import *
from get_puzzle import *
import pandas as pd
from text_highlighter import text_highlighter
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
def vis_overlay():
    if "info1" not in st.session_state:
        placeholder = st.empty()
        with placeholder.container():
            with st.form("form"):
                st.write("Below is the mutated protein (red) compared to the non-mutated protein (green). Due to a mutation in the DNA, the mRNA sequence is also shifted. Since mRNA is transcribed into amino acids, the amino acid sequence of the protein is also shifted, resulting in structural changes. To view the impacts of this mutation on amino acid sequence, transcribe the mRNA sequence in the table using the codon chart in the sidebar.")
                if st.form_submit_button("Close"):
                    st.session_state["info1"]=True
                    placeholder.empty()
    wild_code = "1ans_1"
    mut_code = wild_code
    wild_path = "pdb\\wild.pdb"
    mut_path = "pdb\\mut.pdb"

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
    super_imposer.set_atoms(og_atoms[0 : 3], mut_atoms[0 : 3])
    #super_imposer.set_atoms(og_atoms[0 : shortest_length], mut_atoms[0 : shortest_length])
    super_imposer.apply(mut_structure.get_atoms())
    io=PDBIO()
    io.set_structure(pdb_object=mut_structure)
    io.save(mut_path)

    with open(wild_path) as ifile:
        wild_system = "".join([x for x in ifile])

    with open(mut_path) as ifile:
        mut_system = "".join([x for x in ifile])



    view = py3Dmol.view(width=800, height=400)
    with st.sidebar.expander("Visualization Settings"):
        wcolor = st.color_picker('Wildtype Protein Color', '#00f900')
        wopacity = st.slider("Wildtype Protein Opacity", min_value=0.0,max_value=1.0, value=1.0)
        mcolor = st.color_picker('Mutated Protein Color', '#F90000')
        mopacity = st.slider("Mutated Protein Opacity", min_value=0.0,max_value=1.0, value=1.0)
        st.session_state["style"]  = st.selectbox('style',['cartoon','stick','sphere'])

    view.addModel(open(wild_path, 'r').read(),'pdb')
    view.addModel(open(mut_path, 'r').read(), 'pdb')

    #style
    view.setStyle({'model':0}, {st.session_state["style"]: {'color': wcolor, 'opacity': wopacity}})
    view.setStyle({'model':1}, {st.session_state["style"]: {'color': mcolor, 'opacity': mopacity}})
    add_hover_with_color(view)
    view.zoomTo()
    showmol(view, width=800, height=400)
def viz_dna(choice):
    dna = rna_to_DNA(st.session_state[choice+"_change_rna"])
    
    dna_colors = []
    rna_colors = []
    color_dict = {"A":"Red", "U":"Blue", "G":'Yellow', "C":"Green", "T":"Purple"}
    
    for i in st.session_state["puzzle_info"][choice+"_rna_window"]:
        dna_colors.append(color_dict[rna_to_DNA(i)])
        dna_colors.append(color_dict[rna_to_DNA(i)]) 
        dna_colors.append(color_dict[rna_to_DNA(i)])
        dna_colors.append(color_dict[rna_to_DNA(i)])   
    for i in st.session_state[choice+"_change_rna"]:
        rna_colors.append(color_dict[i])
        rna_colors.append(color_dict[i])
        rna_colors.append(color_dict[i])
        rna_colors.append(color_dict[i])

    with open("pdb//dna//dna.pdb") as ifile:
        system1 = "".join([x for x in ifile])
    with open("pdb//dna//rna.pdb") as ifile:
        pre_sys = [x for x in ifile][0:len(rna_colors)]
        system2 = "".join(pre_sys)
    view = py3Dmol.view(width=800, height=300)
    view.addModelsAsFrames(system1)
    view.addModelsAsFrames(system2)
    i=0 
    for line in system1.split('\n'):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM":
            continue
        if i<len(dna_colors):
            view.setStyle({'model': 0, 'serial': i+1}, {"sphere": {'color': dna_colors[i], 'opacity': 0.5}})
        i += 1
    
    i=0 
    for line in system2.split('\n'):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM":
            continue
        if i<len(rna_colors):
            view.setStyle({'model': 1, 'serial': i+1}, {"sphere": {"color": rna_colors[i], 'opacity': 1}})     
          
        i=i+1
    view.zoomTo()

    showmol(view, width=800, height=300)

def transcript_dogma():
    if "info0" not in st.session_state:
        placeholder = st.empty()
        with placeholder.container():
            with st.form("form"):
                st.write("Here is a small portion of the wild-type DNA sequence. Fill in the mRNA sequence in the text box below by transcribing the DNA sequence in the table.")
                if st.form_submit_button("Close"):
                    st.session_state["info0"]=True
                    placeholder.empty()

    with st.sidebar.expander("Nucleotide Bases Key"):
        st.color_picker(label="Cytosine (C)", value="#00FF00", disabled=True)
        st.color_picker(label="Guanine (G)", value="#FFFF00", disabled=True)
        st.color_picker(label="Adenine (A)", value="#FF0000", disabled=True)
        st.color_picker(label="Thymine (T) - DNA Only", value="#800080", disabled=True)
        st.color_picker(label="Uracil (U) - RNA Only", value="#0000FF", disabled=True)
    if "w_change_aa" not in st.session_state:
        st.session_state["w_change_aa"]=""
    if "m_change_aa" not in st.session_state:
        st.session_state["m_change_aa"]=""
    if "w_change_rna" not in st.session_state:
        st.session_state["w_change_rna"]=""
    if "m_change_rna" not in st.session_state:
        st.session_state["m_change_rna"]=""
    if "input_checks" not in st.session_state:
        st.session_state["input_checks"]=[False, False]


    wild_dict = {
        "":["Wild-Type DNA", "Wild-Type mRNA"]#, "Wild-Type Amino Acids"]                   
    }
    mut_dict = {
        "":["Mutated DNA", "Mutated mRNA"]#, "Mutated Amino Acids"]                   
    }
    place1 = st.empty()
    with place1.container():
        wrna_text = st.text_input("Wild-Type mRNA Sequence", max_chars=30, disabled=st.session_state["input_checks"][0])
        if wrna_text.isalpha() and is_rna(wrna_text.upper()):
            st.session_state["w_change_rna"] = wrna_text
        else:
            if wrna_text != '':
                st.warning('Only RNA Bases are permitted: A, C, U, G', icon="⚠️")
    for i in range(10):
        dna_codon = rna_to_DNA(st.session_state["puzzle_info"]['w_rna_window'][i*3:(i*3+3)])
        rna_codon = (st.session_state["w_change_rna"] +'                              ')[i*3:(i*3+3)]
        #aa = (st.session_state["w_change_aa"]+'          ')[i]
        wild_dict[str(i+1)] = [dna_codon, rna_codon]#, aa]
    df1 = pd.DataFrame(wild_dict)
    st.dataframe(df1, use_container_width=True, hide_index=True)
    viz_dna('w')
    if st.button("Check Transcription of Wild-Type Sequence"):
        if st.session_state["puzzle_info"]['w_rna_window'] == st.session_state["w_change_rna"]:
            st.success('Correct Transcription!', icon="✅")
            st.session_state["input_checks"][0]=True
            place1.empty()
        else:
            st.error('Incorrect Transcription', icon="🚨")
            st.write(st.session_state["puzzle_info"]['w_rna_window'])
            st.session_state["input_checks"][0]=False
            
    st.divider()

    if "info2" not in st.session_state:
        placeholder = st.empty()
        with placeholder.container():
            with st.form("form2"):
                st.write("Because of mutations in the DNA and mRNA sequences, the resulting polypeptide is also mutated, leading to structural changes in the protein.")
                st.write("To view the impacts of this mutation on the amino acid sequence, translate the mRNA sequences transcribed from before using the codon chart in the sidebar.")
                if st.form_submit_button("Close"):
                    st.session_state["info2"]=True
                    placeholder.empty()
    place2 = st.empty()
    with place2.container():
        mrna_text = st.text_input("Mutated mRNA Sequence", max_chars=30, disabled=st.session_state["input_checks"][1])
        if mrna_text.isalpha() and is_rna(mrna_text.upper()):
            st.session_state["m_change_rna"] = mrna_text
        else:
            if mrna_text != '':
                st.warning('Only RNA Bases are permitted: A, C, U, G', icon="⚠️")
    for i in range(10):
        dna_codon = rna_to_DNA(st.session_state["puzzle_info"]['m_rna_window'][i*3:(i*3+3)])
        rna_codon = (st.session_state["m_change_rna"] +'                              ')[i*3:(i*3+3)]
        #aa = '                                        '[i]
        mut_dict[str(i+1)] = [dna_codon, rna_codon]#, aa]
    df2 = pd.DataFrame(mut_dict)
    st.dataframe(df2, use_container_width=True, hide_index=True)
    viz_dna('m')
    if st.button("Check Transcription of Mutated Sequence"):
        if st.session_state["puzzle_info"]['m_rna_window'] == st.session_state["m_change_rna"]:
            st.success('Correct Transcription!', icon="✅")
            place2.empty()
            st.session_state["input_checks"][1]=True
        else:
            st.error('Incorrect Transcription', icon="🚨")
            st.write(st.session_state["puzzle_info"]['m_rna_window'])
            st.session_state["input_checks"][1]=False
    if st.session_state["input_checks"][0]==True and st.session_state["input_checks"][1]==True:
        st.switch_page("other_pages//Translation.py")


def transcription():
    # Removes Previous Puzzle Initialization
    if st.sidebar.button("New Puzzle"):
        for key in st.session_state.keys():
            del st.session_state[key]
    
    #wildtype RNA/protein
    if "puzzle_info" not in st.session_state:
        get_puzzle()

    if bool(~os.path.isfile("pdb\\wild.pdb")):
        get_esm_pdb(st.session_state["puzzle_info"]["w_aa"], "wild")
    if bool(~os.path.isfile("pdb\\mut.pdb")):
        get_esm_pdb(rna_to_amino_acids(st.session_state["puzzle_info"]["m_rna"]), "mut")
    transcript_dogma()
import re

def translation():
    if "puzzle_info" not in st.session_state:
        st.switch_page("other_pages//Practice.py")
    if bool(~os.path.isfile("pdb//wild.pdb")):
        get_esm_pdb(rna_to_amino_acids(st.session_state["puzzle_info"]['w_rna']), "wild")
    if bool(~os.path.isfile("pdb//mut.pdb")):
        get_esm_pdb(rna_to_amino_acids(st.session_state["puzzle_info"]['m_rna']), "mut")
    vis_overlay()
    
    st.divider()    
    if "trans_correct" not in st.session_state:
        st.session_state["trans_correct"] = [False, False]
    if st.sidebar.button("New Puzzle"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.switch_page("other_pages//Transcription.py")
    #Makes Popup Codon Chart
    with st.sidebar.expander("Codon Chart"):
        st.image('screenshots//codon_wheel.png')
    if "w_aa_change" not in st.session_state or "m_aa_change" not in st.session_state:
        st.session_state["w_aa_change"] = ''
        st.session_state["m_aa_change"] = ''
    
    wild_dict = {
        "":["Wild-Type DNA", "Wild-Type mRNA", "Wild-Type Amino Acids"]                   
    }
    mut_dict = {
        "":["Mutated DNA", "Mutated mRNA", "Mutated Amino Acids"]                   
    }
    place1 = st.empty()
    with place1.container():
        waa_text = st.text_input("Wild-Type Amino Acid Sequence", max_chars=10, disabled=st.session_state["trans_correct"][0])
        if waa_text.isalpha() and is_aa(waa_text.upper()):
            st.session_state["w_aa_change"] = waa_text
        else:
            if waa_text != '':
                st.warning('Only Amino Acids are permitted.', icon="⚠️")
    for i in range(10):
        dna_codon = rna_to_DNA(st.session_state["puzzle_info"]['w_rna_window'][i*3:(i*3+3)])
        rna_codon = (st.session_state["puzzle_info"]["w_rna_window"] +'                              ')[i*3:(i*3+3)]
        aa = (st.session_state["w_aa_change"]+'          ')[i]
        wild_dict[str(i+1)] = [dna_codon, rna_codon, aa]
    df1 = pd.DataFrame(wild_dict)
    st.dataframe(df1, use_container_width=True, hide_index=True)
    if st.button("Check Translation of Wild-Type Sequence"):
        window = "".join(re.findall("[a-zA-Z]+", rna_to_amino_acids(st.session_state["puzzle_info"]['w_rna_window']).replace(" ","")))
        if rna_to_amino_acids(st.session_state["w_change_rna"]) == st.session_state["w_aa_change"]:
            st.success('Correct Translation!', icon="✅")
            st.session_state["trans_correct"][0]=True
            place1.empty()
        else:
            st.write(rna_to_amino_acids(st.session_state["w_change_rna"]))
            st.error('Incorrect Translation', icon="🚨")
            st.session_state["trans_correct"][0]=False
            
    st.divider()
    place2 = st.empty()
    with place2.container():
        maa_text = st.text_input("Mutated Amino Acid Sequence", max_chars=10, disabled=st.session_state["trans_correct"][1])
        if maa_text.isalpha() and is_aa(maa_text.upper()):
            st.session_state["m_aa_change"] = maa_text
        else:
            if maa_text != '':
                st.warning('Only Amino Acids are permitted.', icon="⚠️")
    for i in range(10):
        dna_codon = rna_to_DNA(st.session_state["puzzle_info"]['m_rna_window'][i*3:(i*3+3)])
        rna_codon = (st.session_state["puzzle_info"]["m_rna_window"] +'                              ')[i*3:(i*3+3)]
        aa = (st.session_state["m_aa_change"]+'          ')[i]
        mut_dict[str(i+1)] = [dna_codon, rna_codon, aa]
    df2 = pd.DataFrame(mut_dict)
    st.dataframe(df2, use_container_width=True, hide_index=True)
    
    if st.button("Check Translation of Mutated Sequence"):
        if rna_to_amino_acids(st.session_state["m_change_rna"]) == st.session_state["m_aa_change"]:
            st.success('Correct Translation!', icon="✅")
            st.session_state["trans_correct"][0]=True
            place2.empty()
            st.session_state["trans_correct"][1]=True
        else:
            st.write(rna_to_amino_acids(st.session_state["m_change_rna"]))
            st.error('Incorrect Translation', icon="🚨")
            st.session_state["trans_correct"][0]=False
            
    if st.session_state["trans_correct"][1]==True and st.session_state["trans_correct"][1]==True:
        st.toast('Correctly Translated!')
        st.session_state["df_w"] = df1
        st.session_state["df_m"] = df2
        st.switch_page("other_pages//MutationQuiz.py")

def select_mut_type():
    st.write(st.session_state.select_mut_type)
    if st.session_state["select_mut_type_bool"]!=None:
        if st.session_state['puzzle_info']["m_type"][0].upper() == st.session_state.select_mut_type[0]:
            st.session_state["select_mut_type_bool"]=True
        else:
            st.session_state["select_mut_type_bool"]=False


def mut_quiz():
    if "puzzle_info" not in st.session_state:
        st.switch_page("other_pages//Practice.py")
    if "select_mut_type_bool" not in st.session_state:
        st.session_state["select_mut_type_bool"] = False
    st.dataframe(st.session_state["df_w"], use_container_width=True, hide_index=True)
    st.dataframe(st.session_state["df_m"], use_container_width=True, hide_index=True)
    mut_type = st.selectbox(label="What type of mutation was made?", key="select_mut_type", options=["Insertion", "Deletion", "Substitution"], on_change=select_mut_type, index=None, disabled=st.session_state["select_mut_type_bool"])
    if mut_type!=None:
        if st.session_state['puzzle_info']["m_type"].upper() == mut_type[0]:
            st.success('Correct!', icon="✅")
            if mut_type[0] == 'I':
                check_insertion()
            elif mut_type[0] == 'D':
                check_deletion()
            elif mut_type[0] == 'S':
                check_substitution()
        else:
            st.error('Incorrect', icon="🚨")
            st.write(st.session_state['puzzle_info']["m_type"][0].upper())
import time
def check_insertion():
    w_dna = "".join(st.session_state["df_w"].iloc[0].tolist()[1:])#[3:]
    m_dna = "".join(st.session_state["df_m"].iloc[0].tolist()[1:])#[3:]
    result = text_highlighter(
        text=m_dna,
        labels=[("Highlight the Inserted Bases of the Mutated DNA Sequence", "#faffc9")],
    )
    if len(result)>0:
        del_seq = m_dna[0:result[0]["start"]]+m_dna[result[0]["end"]:-1]
        if del_seq == w_dna[0:len(del_seq)]:
            st.success("Correct!")
            for key in st.session_state.keys():
                del st.session_state[key]
            st.balloons()
            time.sleep(3)
            st.switch_page("other_pages//Practice.py")
        else:
            st.error('Incorrect', icon="🚨")
            st.write("You Inputed: "+ del_seq)
            #st.write("Your Answer: "+ w_dna[0:len(del_seq)])

    
def check_deletion():
    w_dna = "".join(st.session_state["df_w"].iloc[0].tolist()[1:])#[3:]
    m_dna = "".join(st.session_state["df_m"].iloc[0].tolist()[1:])#[3:]
    result = text_highlighter(
        text=w_dna,
        labels=[("Highlight The Deleted Sequence", "#faffc9")],
    )
    if len(result)>0:
        del_seq = w_dna[0:result[0]["start"]]+w_dna[result[0]["end"]:-1]
        if del_seq == m_dna[0:len(del_seq)]:
            st.success("Correct!")
            for key in st.session_state.keys():
                del st.session_state[key]
            st.balloons()
            time.sleep(3)
            st.switch_page("other_pages//Practice.py")
        else:
            st.error('Incorrect', icon="🚨")
            st.write("You Inputed: "+ del_seq)
            #st.write("Answer: "+ m_dna)
def check_substitution():
    w_dna = "".join(st.session_state["df_w"].iloc[0].tolist()[1:])
    m_dna = "".join(st.session_state["df_m"].iloc[0].tolist()[1:])
    result = text_highlighter(
        text=w_dna,
        labels=[("Select Substituted Sequence", "#faffc9")],
    )
    insert = st.text_input("Substitued Sequence", max_chars=30)
    if len(insert)!=len(result[0]["text"]):
        st.warning("Both sequence must have equal length for substitution.")
    else:
        output = w_dna[0:result[0]["start"]]+insert+w_dna[result[0]["end"]:]
        output = "".join([n for n in output if n.isalpha()]).upper()
        if len(result)>0:
            if output == m_dna[0:30]:
                st.success("Correct!")
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.balloons()
                time.sleep(3)
                st.switch_page("other_pages//Practice.py")
            else:
                st.error('Incorrect', icon="🚨")
                st.write("You Inputed: "+ output)
                #st.write("The Answer: "+ m_dna[0:30])




def q_viz(file, color):
    with open(file) as ifile:
        system = "".join([x for x in ifile])
    view = py3Dmol.view(height=600, width=800)
    view.addModelsAsFrames(system)
    view.setStyle({'model': -1}, {"cartoon": {'color': color}})
    view.zoomTo()
    showmol(view, height=600, width=800)
def rna_to_DNA(rna):
    opp_dna = []
    for i in list(rna):
        if i=="A":
            opp_dna.append("T")
        elif i=="U":
            opp_dna.append("A")
        elif i =="C":
            opp_dna.append("G")
        elif i =="G":
            opp_dna.append("C")
    return "".join(opp_dna)
    
def is_aa(text):
    amino_acids = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
    text = list(text)
    exists = True
    for c in text:
        if c not in amino_acids:
            exists = False
    return exists
def is_rna(text):
    bases = ['A', 'C', 'U', 'G']
    text = list(text)
    exists = True
    for c in text:
        if c not in bases:
            exists = False
    return exists

