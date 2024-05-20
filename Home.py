import streamlit as st
from st_pages import show_pages_from_config
from pyversion_funcs import get_rand_dna_with_len_two_strands, get_rand_dna_with_len
from dna_viz import viz_double_strand, viz_single_strand
#Configure Page
st.set_page_config(page_title="Python Transcription Task", page_icon=":dna:", layout="wide")

st.header("Home")
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                    padding-bottom: 1rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)
show_pages_from_config()

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

# Write Instructions
url_feedback = "https://forms.gle/33tUxLnaLnmneQHA8"
st.markdown('''After using this website, please let us know how you liked it [here](%s)!''' % url_feedback)
st.write("\n")
st.write("Fun DNA Model:")
dna_len = st.number_input(label="DNA Sequence Length", min_value=0, max_value=1000, step=1)
model_both_strands = st.checkbox(label="Model Both Strands", value=True)

if model_both_strands:
        dna1, dna2 = get_rand_dna_with_len_two_strands(dna_len)
        viz_double_strand(dna1, dna2, height=400, width=1150)
else:
        dna_seq = get_rand_dna_with_len(dna_len)
        viz_single_strand(dna_seq, height=400, width=1150)

#rain(emoji="🧬", font_size=40, falling_speed=10, animation_length='infinite')




