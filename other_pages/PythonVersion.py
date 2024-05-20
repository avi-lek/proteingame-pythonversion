import streamlit as st
from pyversion_funcs import *
from py_version_sidebar_utils import *
from py_version_utils import *
from execute import *

#Formatting
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
st.header("Transcription Task")
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


ms = st.session_state
if "themes" not in ms: 
  ms.themes = {"current_theme": "light",
                    "refreshed": True,
                    
                    "light": {"theme.base": "dark",
                              "theme.backgroundColor": "#0E1117",
                              "theme.primaryColor": "#FF4B4B",
                              "theme.secondaryBackgroundColor": "#262730",
                              "theme.textColor": "#FAFAFA",
                              "button_face": "🌜"},

                    "dark":  {"theme.base": "light",
                              "theme.backgroundColor": "#FFFFFF",
                              "theme.primaryColor": "#FF4B4B",
                              "theme.secondaryBackgroundColor": "#F0F2F6",
                              "theme.textColor": "#31333F",
                              "button_face": "🌞"},
                    }
  

def ChangeTheme():
    previous_theme = ms.themes["current_theme"]
    tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
    for vkey, vval in tdict.items(): 
        if vkey.startswith("theme"): st._config.set_option(vkey, vval)

    ms.themes["refreshed"] = False
    if previous_theme == "dark": ms.themes["current_theme"] = "light"
    elif previous_theme == "light": ms.themes["current_theme"] = "dark"

btn_face = ms.themes["light"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]["button_face"]

st.sidebar.info("Changing to Light/Dark Mode may not work initially. If so, reload page.")
st.sidebar.toggle("Light/Dark Mode", on_change=ChangeTheme)

if ms.themes["refreshed"] == False:
  ms.themes["refreshed"] = True
  st.rerun()























