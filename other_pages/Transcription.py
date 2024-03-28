from st_pages import Page, Section, show_pages, add_page_title
import streamlit as st
from practice_functions import *
from st_pages import Page, show_pages, add_page_title, hide_pages
st.set_page_config(page_title="My Protein Is Broken!", page_icon=":dna:", layout="wide")
hide_pages(["Transcription", "Identify Mutations", "Translation", "Sandbox Instructions"])
if "transcript_win" not in st.session_state:
    st.session_state["transcript_win"] = False
add_page_title()
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)


transcription()


