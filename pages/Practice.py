import streamlit as st
from stmol import showmol
from practice_functions import *
import pandas as pd
from setup_puzzle import *
from st_pages import Page, Section, show_pages, add_page_title

st.set_page_config(page_title="Mutations Practice", page_icon=":dna:", layout="wide")
from st_pages import hide_pages
hide_pages(["Translation"])
add_page_title()
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.write("mutations explanation")
st.write("at bottom: to start, change window to transcription at the top right")
