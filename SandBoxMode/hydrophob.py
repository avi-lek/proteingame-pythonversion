from stmol import showmol
import streamlit as st
import py3Dmol
import urllib
from io import StringIO

#pdb_code
pdb_url = f'https://files.rcsb.org/download/2jmy.pdb'
pdb_file = urllib.request.urlopen(pdb_url).read().decode("utf-8")

system = "".join([x for x in pdb_file])

#visualization
view = py3Dmol.view()
view.addModelsAsFrames(system)
view.setStyle({'model': -1}, {"cartoon": {'color': 'spectrum'}})
showmol(view, height = 500,width=800)

