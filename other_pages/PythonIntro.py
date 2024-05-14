from Bio.Seq import Seq
import streamlit as st
import pandas as pd
from streamlit_ace import st_ace
from pyversion_funcs import *
from st_pages import hide_pages
from code_editor import code_editor
from execute import *

hide_pages(["Python Transcription", "Python Translation"])

st.title("Intro to Python")

# PART 1: FOR LOOPS...

# introduce the Python string
string_intro = """To start, in order to transcribe a DNA sequence, we need to store it somewhere first. 
We can store DNA sequences in a ***Python string***, a data type that can store words and sentences. Think of the string dna_sequence below as one long word with each base being a letter. 

Here's an example of a short DNA sequence stored in a string:
"""
st.markdown(string_intro)

# show string ex
string_code = """# DNA sequence stored in a Python string:
dna_sequence = "AUGCUAGUA"
"""
st.code(string_code, language = "python", line_numbers = True)


# introduce the for loop
for_loop_intro = """In order to transcribe this sequence though, we need to be able read through every “letter,” or nucleotide, of the sequence. 
An efficient way to go through the sequence is with ***for loops***. Here's an example!
"""
st.markdown(for_loop_intro)

# show for loop ex
for_loop_code = string_code + """
# for every nucleotide in the sequence, print it:
for nucleotide in dna_sequence:
    print(nucleotide)
"""

# config it
height = [6, 22]
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

code = code_editor(for_loop_code,  height = height, lang=language, theme=theme, shortcuts=shortcuts, focus=focus, buttons=editor_btns, options={"wrap": wrap, "showLineNumbers": True})

# more for loop explanation
for_loop_exp = """The ***for loop*** above reads through every nucleotide in the DNA sequence and print every nucleotide individually. 

Hover over the  bottom right of the code window and click Run to see!
"""
st.markdown(for_loop_exp)

# show result of for loop print
for_loop_result = """A
U
G
C
U
A
G
U
A
"""

if len(code['id']) != 0 and (code['type'] == "selection" or code['type'] == "submit" ):
    st.code(for_loop_result, language = "python", line_numbers = False)


























# if conditional instruction
if_state_msg = """
"""
st.markdown(if_state_msg)


# string concatenation instruction
string_concat_msg = """
"""
st.markdown(string_concat_msg)





if st.button("Next"):
    st.switch_page("other_pages//CodeTranscription.py")