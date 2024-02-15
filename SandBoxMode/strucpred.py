from stmol import showmol
import streamlit as st
import py3Dmol

# 1A2C
# Structure of thrombin inhibited by AERUGINOSIN298-A from a BLUE-GREEN ALGA

view = py3Dmol.view(query='pdb:2JMY') 

#visualization
style = st.sidebar.selectbox('style',['stick','sphere','cartoon'])
view.setStyle({style:{'color':'spectrum'}})
showmol(view, height = 500,width=800)
