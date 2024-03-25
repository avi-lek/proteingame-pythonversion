from st_pages import Page, Section, show_pages, add_page_title
import streamlit as st
from practice_functions import *
from st_pages import Page, show_pages, add_page_title, hide_pages

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


mut_quiz()