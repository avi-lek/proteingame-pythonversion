import streamlit as st
import streamlit.components.v1 as components
import ipywidgets as widgets
from ipywidgets import embed
import requests

#adapted from stmol to include residue names and reflect the color of residues
def add_hover(obj):
    js_script = """function(atom,viewer) {
                if(!atom.label) {
                    if(atom.style.cartoon.color!="black"){
                        atom.label = viewer.addLabel(atom.resn+':'+atom.resi,{position: atom, backgroundColor:"black" , fontColor:"white"});
                    } else{
                        atom.label = viewer.addLabel(atom.resn+':'+atom.resi,{position: atom, backgroundColor:"black" , fontColor:"white"});
                    }
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
def add_hover_gen(obj):
    js_script = """function(atom,viewer) {
                    atom.label = viewer.addLabel(atom.resn+':'+atom.resi + " | " + atom.elem,{position: atom, backgroundColor:"black" , fontColor:"white"});
              }"""
    obj.setHoverable({},True,js_script,
               """function(atom,viewer) {
                   if(atom.label) {
                    viewer.removeLabel(atom.label);
                    delete atom.label;
                   }
                }"""
    )


#adapted from stmol to dynamically resize viewer to container width
def showmol(mol_obj, height):
    html_code = mol_obj._make_html()
    to_remove = ' width: 640px;'
    index = html_code.find(to_remove)
    new_html = html_code[0:index]+html_code[(index+len(to_remove)):]
    components.html(new_html, height=height)


#Takes RNA sequence and returns AA sequence
def rna_to_amino_acids(rna_sequence):
    codon_table = {
        'UUU': 'F', 'UUC': 'F',
        'UUA': 'L', 'UUG': 'L', 'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
        'AUU': 'I', 'AUC': 'I', 'AUA': 'I',
        'AUG': 'M',
        'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
        'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S', 'AGU': 'S', 'AGC': 'S',
        'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'UAU': 'Y', 'UAC': 'Y',
        'UAA': 'A', 'UAG': 'H', 'UGA': 'S',
        'CAU': 'H', 'CAC': 'H',
        'CAA': 'Q', 'CAG': 'Q',
        'AAU': 'N', 'AAC': 'N',
        'AAA': 'K', 'AAG': 'K',
        'GAU': 'D', 'GAC': 'D',
        'GAA': 'E', 'GAG': 'E',
        'UGU': 'C', 'UGC': 'C',
        'UGG': 'W',
        'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'AGA': 'R', 'AGG': 'R',
        'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
    }
    amino_acids = ''
    for i in range(0, len(rna_sequence), 3):
        codon = str(rna_sequence[i:i+3])
        if codon_table.get(codon, 'X')=='*':
            return amino_acids
        else:
            amino_acid = codon_table.get(codon, 'X')  # 'X' for unknown or invalid codon
            amino_acids += amino_acid
    return amino_acids

#runs ESMFold on amino acid sequence and writes pdb to fname
def get_esm_pdb(aa_seq):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=aa_seq, verify=False)
    with open('pdb\\protein.pdb', 'wb') as f:
        f.write(response.content)


