from text_highlighter import text_highlighter
import streamlit as st
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


# Example usage:


view = py3Dmol.view(width=800, height=600)
with open("pdb//dna//rna.pdb") as ifile:
        system = "".join([x for x in ifile])
view.addModelsAsFrames(system)
#view.addModel(open("pdb//dna//rna.pdb", 'r').read(),'pdb')
#view.setStyle({'model':0}, {"sphere": {'color': 'blue'}})
i=0
for line in system.split('\n'):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM":
            continue
        view.setStyle({'model': -1, 'serial': i+1}, {"sphere": {"color": 'blue', 'opacity': 1}})            
        i=i+1
i=0
with open("pdb//dna//dna.pdb") as ifile:
        system2 = "".join([x for x in ifile])
view.addModelsAsFrames(system2)
for line in system.split('\n'):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM":
            continue
        view.setStyle({'model': -1, 'serial': i+1}, {"sphere": {"color": 'red', 'opacity': 1}})            
        i=i+1
view.zoomTo()
showmol(view, height=600, width=800)