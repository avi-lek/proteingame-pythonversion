import streamlit as st
import pandas as pd
from streamlit_ace import st_ace
#from streamlit-extras import st.switch_page
import contextlib
import io
import sys
from Bio.Seq import Seq
from pyversion_funcs import *
from py_version_utils import *
from st_pages import hide_pages

hide_pages(["Python Transcription", "Python Translation"])
init_sidebar()

# welcome user to page
st.title("Python Version")
intro_msg = """Welcome to the Python version! This aspect of our website will integrate Python programming with the central dogma of biology.

In actuality, the DNA sequences bioinformaticians and data analysts deal with can be thousands of nucleotides long, making it unfeasible to transcribe DNA or translate mRNA by hand. Especially when dealing with larger datasets, it makes a lot more sense to use programming tools like Python to analyze our data. 

No experience with Python? No worries! The first section of this exercise will introduce you to a couple key Python concepts you'll need to know. In the second section, you'll transcribe a DNA sequence into mRNA using Python.  

Whenever you are ready, click Start Exercise to begin!
"""
st.write(intro_msg)

# if they click start exercise
if st.button("Start Exercise"):
    st.switch_page("other_pages//PythonIntro.py")