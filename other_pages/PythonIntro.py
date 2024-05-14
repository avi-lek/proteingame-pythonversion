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

if st.button("Next"):
    st.switch_page("other_pages//CodeTranscription.py")