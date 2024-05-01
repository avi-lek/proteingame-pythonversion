import random
from Bio.Seq import Seq
import streamlit as st
import pandas as pd
from streamlit_ace import st_ace
from execute import *
from pyversion_funcs import *
from st_pages import hide_pages

hide_pages(["Sandbox", "Mutations Practice", "Python Transcription", "Python Translation", "Transcription", "Identify Mutations", "Translation", "Sandbox Instructions"])

st.title("DNA to RNA")

# DNA input & expected RNA user output
dna = get_rand_dna()
mrna = dna_to_rna(dna, "123456789")

# for codon chart in pre_code later
curly1 = "{"
curly2 = "}"

# pre code for user
transcribe_pre_code = f"""
# your DNA sequence:
dna_sequence = "{dna}"

# DNA sequence length:
dna_length = len(dna_sequence)

# your RNA output (this is empty for now... it'll be complete once you transcribe the DNA below!)
rna_sequence = ""

# transcribe the DNA into RNA by iterating through every nucleotide:
for nucleotide in dna_sequence:
    # how do you transcribe each individual nucleotide?



# at the end, print your RNA sequence!
print(rna_sequence)

"""

# instructions
transcribe_instructs = f"""In actuality, mutations in proteins can be much larger than just a couple nucleotides, requiring scientists to study significantly longer sequences of DNA. 
Here, we are looking at an DNA sequence that is {len(dna)} nucleotides long. When transcribing larger sequences like these, it's useful to use a Python instead of by hand.
Writing your own Python script, iterate through the DNA sequence and transcribe it into an mRNA sequence.

Once you're confident in your code, first click APPLY to save your work, and then hit Run Code!
"""
st.write(transcribe_instructs)


# make user text editor
code = st_ace(value = transcribe_pre_code, language = 'python', height = 800)

# if user tries to run it
if st.button("Run Code"):
    output, matches = execute_code(code, dna, "transcription")

    # if output is error msg
    if output[0: 21] == 'Error executing code:':
        st.error(output)

    # if they didn't fuck up
    else:
        st.write("The amino acid sequence you got was " + output + ".") 

    if matches:
        st.success("Congratulations, your code works! Once you're ready, click Next to go to the translation portion of the exercise.")
        if st.button("Next"):
            st.switch_page("other_pages//CodeTranslation.py")

    else:
        st.warning("Not quite. Try again")


