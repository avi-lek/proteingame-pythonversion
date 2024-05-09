import random
from Bio.Seq import Seq
import streamlit as st
import pandas as pd
from streamlit_ace import st_ace
from execute import *
from pyversion_funcs import *
from st_pages import hide_pages
from code_editor import code_editor

st.title("DNA to RNA")

# DNA input & expected RNA user output
if 'dna' not in st.session_state:
    st.session_state['dna'] = get_rand_dna()


if 'mrna' not in st.session_state:
    st.session_state['mrna'] = dna_to_rna(st.session_state.dna, "123456789")

# for codon chart in pre_code later
curly1 = "{"
curly2 = "}"

pre_code = f"""this is some pre-loaded code

the dna is {st.session_state.dna}


this is some more code
"""

#pre_code = pre_code + st.session_state.dna[0 : 4]


# code editor config variables
height = [19, 22]
language="python"
theme="default"
shortcuts="vscode"
focus=False
wrap=True
editor_btns = [{
    "name": "Run",
    "feather": "Play",
    "primary": True,
    "hasText": True,
    "showWithIcon": True,
    "commands": ["submit"],
    "style": {"bottom": "0.44rem", "right": "0.4rem"}
  }]


code = code_editor(pre_code,  height = height, lang=language, theme=theme, shortcuts=shortcuts, focus=focus, buttons=editor_btns, options={"wrap": wrap})

# show response dict
if len(code['id']) != 0 and (code['type'] == "selection" or code['type'] == "submit" ):
    # Capture the text part
    user_text = code['text']

    st.code(user_text, language='python') #Captured the code parameter.


