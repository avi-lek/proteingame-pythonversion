import streamlit as st
import pandas as pd
from streamlit_ace import st_ace
#from streamlit-extras import st.switch_page
import contextlib
import io
import sys
from Bio.Seq import Seq
from pyversion_funcs import *

from st_pages import hide_pages

hide_pages(["Python Transcription", "Python Translation"])

# welcome user to page
st.title("Python Version")
intro_msg = """Welcome to the Python version! This aspect of our website will integrate Python programming with the Central Dogma of biology.
Especially with transcription and translation, it's often boring and time consuming to do it all by hand. But by using Python, you can have a computer do it for you!

In the first part of this exericse, you'll use Python to transcribe a DNA sequence into mRNA. In the second part, you'll translate your mRNA sequence into an amino acid sequence. 

Whenever you are ready, click Start Exercise to begin!
"""
st.write(intro_msg)

# if they click start exercise
if st.button("Start Exericse"):
    st.switch_page("other_pages//CodeTranscription.py")