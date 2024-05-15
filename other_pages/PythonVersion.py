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
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.header("Python Version")
init_sidebar()

init_intro()
if "show" not in st.session_state:
    st.session_state.show = False

if st.button("show"):
    st.session_state.show = True
if st.button("hide"):
    st.session_state.show = False


if st.session_state.show:
    init_for_loops()




























