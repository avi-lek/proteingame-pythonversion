# translation page
import random
from Bio.Seq import Seq
import streamlit as st
import pandas as pd
from streamlit_ace import st_ace
from execute import *
from st_pages import hide_pages
from code_editor import code_editor

hide_pages(["Python Transcription", "Python Translation"])



st.title("RNA to Amino Acids")

# RNA input and expected AA user output

if 'aa' not in st.session_state:
    st.session_state['aa'] = rna_to_aa_super_secret(st.session_state.mrna, "123456789")
num_codons = int(len(st.session_state.mrna) / 3)

# for codon chart in pre_code later
if 'curly1' not in st.session_state:
    st.session_state['curly1'] = "{"

if 'curly2' not in st.session_state:
    st.session_state['curly2'] = "}"


# pre-existing code for user 
translate_pre_code = f"""# your mRNA sequence:
mrna = "{st.session_state.mrna}"

# number of codons (groups of 3) in the mRNA sequence:
num_codons = int(len(mrna) / 3)

# here's a Python dictionary that contains all codons and their corresponding amino acids:
codon_table = {st.session_state.curly1}
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
    'UAA': '*', 'UAG': '*', 'UGA': '*',
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
{st.session_state.curly2}

# amino acid sequence: (this should be empty at the start. it'll be complete once you translate each codon below!)
aa = "{st.session_state.aa}"

# iterate through every codon in the mRNA sequence:
for i in range(num_codons):
    # translate each codon into its corresponding AA:

    



    # add the translated codon to the amino acid sequence:

    





# at the end, print your amino acid sequence!
print(aa)
"""


translate_instructs = f"""Now that we've transcribed 

Once you're confident in your code, first click APPLY to save your work, and then hit Run Code!
"""


st.write(translate_instructs)



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


code = code_editor(translate_pre_code,  height = height, lang=language, theme=theme, shortcuts=shortcuts, focus=focus, buttons=editor_btns, options={"wrap": wrap})


# show response dict
if len(code['id']) != 0 and (code['type'] == "selection" or code['type'] == "submit" ):
    # Capture the text part
    user_text = code['text']
    output, matches = execute_code(user_text, st.session_state.mrna, "translation")

    # if output is error msg
    if output[0: 21] == 'Error executing code:':
        st.error(output)

    # if they didn't fuck up
    else:
        st.write("The amino acid sequence you got was " + output + ".") 

    if matches:
        st.success("Congratulations, you're all done!")
        if st.button("Return Home"):
            st.switch_page("Home.py")
        
    else:
        st.warning("Not quite. Try again")