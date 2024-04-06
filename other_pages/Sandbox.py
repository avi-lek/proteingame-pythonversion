import streamlit as st
from sandbox_functions import *
from st_pages import hide_pages
from utils import *
st.set_page_config(page_title="My Protein Is Broken!", page_icon=":dna:", layout="wide")
hide_pages(["Transcription", "Identify Mutations", "Translation", "Sandbox Instructions"])
st.header("Sandbox")
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



if "instructions_read" not in st.session_state or st.sidebar.button("Instructions"):
    st.session_state["instructions_read"] = True
    st.switch_page("other_pages//Sandbox_instructions.py")

#Set up sidebar
#Define the two tabs
settings, viz_settings, info = st.sidebar.tabs(["General Settings", "Visualization Settings", "Source Protein Info"])

#Get PDB ID
protein_ids = {
    'Myoglobin': '1MBN',
    'Human Growth Hormone': '1HGU',
    'Glucagon': '1GCN',
    'Human Rac1 G-protein': '1MH1',
    'Beetle Antifreeze Protein': '1EZG',
    'Hemoglobin': '1a3n'
}
options = list(protein_ids.keys())
options.append("Select From PDB ID")
st.session_state["code"] = settings.selectbox("Select Protein",  options)
if st.session_state["code"] == "Select From PDB ID":
    st.session_state["code"] = settings.text_input('PDB Code')
    #MAKE SURE TO DISALLOW INCORRECT CODES
else: 
    st.session_state["code"] = protein_ids[st.session_state["code"]]

if exists(f'https://files.rcsb.org/download/{st.session_state["code"].upper()}.pdb'):
    
    #Determine whether to use ESMfold
    st.session_state["use_esm"] = settings.toggle('ML Predicted Structure')
    use_overlay=False
    if st.session_state["use_esm"]:
        #Determine whether to overlay multiple proteins
        use_overlay = settings.toggle('Overlay Structures')
        if use_overlay:
            #call function that overlays esm proteins
            vis_esm()
        else:
            st.session_state["esm_seq"] = settings.text_area("Input Sequence", pdb_to_fasta(st.session_state["code"]))

    if use_overlay==False:
        #Get Model Type
        model_type = viz_settings.selectbox('Model Type',['Ball and Stick','Ribbon Diagram','Both'])
        if model_type == 'Ball and Stick':
            st.session_state["style"]= (True, False)
        elif model_type == 'Ribbon Diagram':
            st.session_state["style"]= (False, True)
        else:
            st.session_state["style"]= (True, True)

        #get ribbon opacity
        if st.session_state["style"] == (True, True):
            st.session_state["ribbon_opacity"] = viz_settings.slider("Ribbon Opacity", min_value=0.0,max_value=1.0, value=0.8)
        else:
            st.session_state["ribbon_opacity"] = 1

        st.session_state["ribbon_color"]='None'
        if st.session_state["style"][1]:
            #get ribbon color
            st.session_state["ribbon_color"] = viz_settings.selectbox('Ribbon Highlighting', ('None', 'Hydrophobicity'))
            if st.session_state["ribbon_color"] == 'Hydrophobicity':
                with viz_settings.expander("Hydrophobicity Key"):
                    st.image('screenshots//h_key.png')

        #Generating VDW Surface:
        st.session_state["make_surface"] = viz_settings.checkbox("Generate Surface")
        if st.session_state["make_surface"] :
            st.session_state["VDW_opacity"] = viz_settings.slider("Surface Opacity", min_value=0.0,max_value=1.0, value=0.5)
        
        vis_none()
else:
    if len(st.session_state["code"])>0:
        settings.warning("Invalid Protein ID")
#change_theme()



