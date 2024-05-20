import streamlit as st
from st_pages import show_pages_from_config
from streamlit_extras.let_it_rain import rain 
from pyversion_funcs import *
from dna_viz import *
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

# Write Instructions
url_feedback = "https://forms.gle/q9mjvDEk1PeHW5aTA"
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




