from Bio.Seq import Seq
import streamlit as st
import pandas as pd
from streamlit_ace import st_ace
from pyversion_funcs import *
from st_pages import hide_pages
from code_editor import code_editor
from execute import *
from py_version_sidebar_utils import *

hide_pages(["Python Transcription", "Python Translation"])

st.title("DNA to RNA")

init_sidebar()

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

# your RNA output (this is empty for now... it'll be complete once you transcribe the DNA below!)
rna_sequence = "{st.session_state.mrna}"

# transcribe the DNA into RNA by going through through every nucleotide:
for nucleotide in dna_sequence:
    # if the DNA base is A, then the RNA base is U
    if nucleotide == "A":
        rna_sequence += "U"

    # what about the other bases? 


# at the end, print your RNA sequence!
print(rna_sequence)"""


# instructions
transcribe_instructs = f"""Think back to when you first looked at central dogma in biology and had to transcribe a small portion of a DNA sequence by hand. 
Here, we are looking at an DNA sequence that is {len(st.session_state.dna)} nucleotides long.  When transcribing larger sequences like these, using Python is a lot more efficient.   

Instructions below the text editing box will guide you through everything!


Once you're confident in your code, hover over the bottom right corner of the text editor window and click Run.  
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


code = code_editor(transcribe_pre_code,  height = height, lang=language, theme=theme, shortcuts=shortcuts, focus=focus, buttons=editor_btns, options={"wrap": wrap, "showLineNumbers": True})

transcription_guide = f"""You might not have any Python experience, but that’s totally ok! Here’s a runthrough of what’s going on here and what you need to do. 

There are 3 parts to this Python script:

1. In line 2, we’ve stored the DNA sequence you’re transcribing today into a ***Python string***. Think of it as one long word with each letter representing one nucleotide in the sequence. 

2. Right under that in line 5, we’ve stored the RNA sequence in another string. You’ll notice that it’s empty right now, but that’s because we’ll add each nucleotide one by one when we transcribe. 

3. Finally, let’s do the actual transcription. In line 8, we’ve initiated a ***for loop***. A for loop is essentially a function in Python that in this case, individually goes through all {len(st.session_state.dna)} nucleotides in the DNA sequence. 

Inside the ***for loop***, we can check what each base in the DNA is and attach the corresponding base to the RNA sequence. That’s pretty easy with ***if statements***. If statements check to see if something is true, and in this scenario, we want to check what each nucleotide is.  

On line 9, the ***if statement*** we’ve already written is checking if the base is A. If it is, it’ll add the corresponding base, U, to the RNA sequence. But A isn’t the only possible nucleotide in the DNA. Your job will be to finish the ***for loop*** by writing ***if statements*** for the other 3 bases! 

"""

st.markdown(transcription_guide)

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