import pandas
import streamlit as st
def get_puzzle():
    #imports csv into a Pandas DataFrame
    reader = pandas.read_csv('puzzles//puzzle_table.csv')
    #get random row
    random_row = reader.sample()
    st.session_state['puzzle_info'] = {
        "pdb_id": random_row["pdb_id"].values[0],
        "w_aa" : random_row["w_aa"].values[0],
        "w_rna" : random_row["w_rna"].values[0],
        "w_rna_window" : random_row["w_rna_window"].values[0],
        "m_rna" : random_row["m_rna"].values[0],
        "m_rna_window" : random_row["m_rna_window"].values[0],
        "m_start" : random_row["m_start"].values[0],
        "m_len" : random_row["m_len"].values[0],
        "m_type" : random_row["m_type"].values[0],
    }
    
#hello