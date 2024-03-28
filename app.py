import streamlit as st
import pandas as pd
from st_pages import Page, show_pages, add_page_title, hide_pages
import time
from st_pages import Page, Section, show_pages, add_page_title
from datetime import datetime

show_pages(
    [
        Page("other_pages//Home.py", "Home"),
        Page("other_pages//Sandbox.py", "Sandbox"),
        Page("other_pages//Sandbox_instructions.py", "Sandbox Instructions"),
        Page("other_pages//Practice.py", "Mutations Practice"),
        Page("other_pages//Transcription.py", "Transcription"),
        Page("other_pages//Translation.py", "Translation"),
        Page("other_pages//MutationQuiz.py", "Identify Mutations")
    ]
)
st.switch_page("other_pages//Home.py")


