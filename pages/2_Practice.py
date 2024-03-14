import streamlit as st
from stmol import showmol
from practice_functions import *
import pandas as pd
from setup_puzzle import *
from puzzle_help import *

st.title("Practice")
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

if st.sidebar.button("Start Mutations Puzzle"):
    st.session_state["do_puzzle"] = True

if "do_puzzle" in st.session_state and st.session_state["do_puzzle"]:
    practice()

