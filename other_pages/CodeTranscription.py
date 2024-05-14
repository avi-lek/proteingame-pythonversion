import random
from Bio.Seq import Seq
import streamlit as st
import pandas as pd
from streamlit_ace import st_ace
from pyversion_funcs import *
from st_pages import hide_pages
from code_editor import code_editor
from execute import *

hide_pages(["Python Transcription", "Python Translation"])

st.title("DNA to RNA")

# DNA input & expected RNA user output
if 'dna' not in st.session_state:
    st.session_state['dna'] = get_rand_dna()

if 'mrna' not in st.session_state:
    st.session_state['mrna'] = dna_to_rna(st.session_state.dna, "123456789")

# for codon chart in pre_code later
curly1 = "{"
curly2 = "}"

# pre code for user
transcribe_pre_code = f"""# your DNA sequence:
dna_sequence = "{st.session_state.dna}"

# DNA sequence length:
dna_length = len(dna_sequence)

# your RNA output (this is empty for now... it'll be complete once you transcribe the DNA below!)
rna_sequence = "{st.session_state.mrna}"

# transcribe the DNA into RNA by iterating through every nucleotide:
for i in range(dna_length)
    # how do you transcribe each individual nucleotide?


# at the end, print your RNA sequence!
print(rna_sequence)

"""


# instructions
transcribe_instructs = f"""In actuality, mutations in proteins can be much larger than just a couple nucleotides, requiring scientists to study significantly longer sequences of DNA. 
Here, we are looking at an DNA sequence that is {len(st.session_state.dna)} nucleotides long! When transcribing larger sequences like these, using Python is a lot more efficient than doing it by hand.  
Writing your own Python script, iterate through the DNA sequence and transcribe it into an mRNA sequence.

Once you're confident in your code, first click Run in the bottom right corner of the text editor window. 
"""
st.write(transcribe_instructs)


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


code = code_editor(transcribe_pre_code,  height = height, lang=language, theme=theme, shortcuts=shortcuts, focus=focus, buttons=editor_btns, options={"wrap": wrap})

# show response dict
if len(code['id']) != 0 and (code['type'] == "selection" or code['type'] == "submit" ):
    # Capture the text part
    user_text = code['text']
    output, matches = execute_code(user_text, st.session_state.dna, "transription")

    # if output is error msg
    if output[0: 21] == 'Error executing code:':
        st.error(output)

    # if their code compiles
    else:
        st.write("The mRNA sequence you got was: " + output + ".") 

    if matches:
        st.success("Congratulations, your code works! Once you're ready to move on to the translation portion, click Next!")

        # move on to translation
        if st.button("Next"):
            st.switch_page("other_pages//CodeTranslation.py")
        
    else:
        st.warning("Not quite. Try again.")