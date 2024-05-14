import streamlit as st
from st_pages import show_pages_from_config, hide_pages
from streamlit_extras.let_it_rain import rain 
import toml

#Configure Page
st.set_page_config(page_title="My Protein Is Broken!", page_icon=":dna:", layout="wide")

hide_pages(["Python Transcription", "Python Translation"])
st.header("Home")
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
show_pages_from_config()

# Write Instructions
st.markdown('''Welcome to ‘My Protein is Broken!’''')
url_teacher = "https://docs.google.com/document/d/14zIgoskGYacwCwsGN8mQvRdwzLc7TBYxQ_2MY5g0cag/edit?usp=sharing"
url_student = "https://docs.google.com/document/d/1HTCqOur0ZR2f5Wvn18qWMzd7jZ9MobXrmC9aUUw5jZE/edit?usp=sharing"
url_feedback = "https://forms.gle/q9mjvDEk1PeHW5aTA"
st.markdown('''For the full teacher instructions, please click [here](%s)!''' % url_teacher)  
st.markdown('''For the full student instructions, please click [here](%s)!''' % url_student)  
st.markdown('''After using this website, please let us know how you liked it [here](%s)!''' % url_feedback)
rain(emoji="🧬", font_size=40, falling_speed=10, animation_length='infinite')




