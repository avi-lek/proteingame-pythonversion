import streamlit as st
from pyversion_funcs import *
from st_pages import hide_pages
from py_version_sidebar_utils import *
from py_version_utils import *
from execute import *

#Formatting
hide_pages(["Python Transcription", "Python Translation"])
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 1rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

if "py_step" not in st.session_state:
    st.session_state.py_step = 0
st.header("Python Version")
init_sidebar()


init_intro()
if st.session_state.py_step > 0:
    st.divider()
    init_string()
if st.session_state.py_step > 1:
    st.divider()
    init_for_loops()
if st.session_state.py_step > 2:
    st.divider()
    init_if()
if st.session_state.py_step > 3:
    st.divider()
    transcription_exercise()

if st.session_state.py_step < 4:
    if st.button("Next Step"):
        st.session_state.py_step += 1
        st.rerun()


























