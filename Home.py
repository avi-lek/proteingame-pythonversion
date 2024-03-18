import streamlit as st
import pandas as pd
from st_pages import Page, show_pages, add_page_title, hide_pages
import time
from st_pages import Page, Section, show_pages, add_page_title

st.set_page_config(page_title="Protein Game", page_icon=":dna:", layout="wide")
add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("Home.py", "Home"),
        Page("pages//Sandbox.py", "Sandbox"),
        Page("pages//Practice.py", "Mutations Practice", in_section = True),
        Page("pages//Transcription.py", "Transcription", in_section = True),
        Page("pages//Translation.py", "Translation", in_section = True),
    ]
)

if "hide_transcript" not in st.session_state:
    st.session_state["hide_transcript"] = True

if "hide_translate" not in st.session_state:
    st.session_state["hide_translate"] = True

if st.session_state["hide_transcript"]:
      hide_pages(["Transcription"])
if st.session_state["hide_translate"]:
      hide_pages(["Translation"])



