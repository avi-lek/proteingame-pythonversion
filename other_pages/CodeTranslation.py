# translation page
import random
from Bio.Seq import Seq
import streamlit as st
import pandas as pd
from streamlit_ace import st_ace
from execute import *
from st_pages import hide_pages

hide_pages(["Sandbox", "Mutations Practice", "Python Transcription", "Python Translation", "Transcription", "Identify Mutations", "Translation", "Sandbox Instructions"])


def code_translation():
    st.title("RNA to Amino Acids")

    # RNA input and expected AA user output - RNA HARD CODED, FOR NOW
    mrna = "AUUACGCUAGGUUGAGGUUACGAUGGAUACCUAAUUGACACGGCAUGAAUUGUGAUUAGUUUGUGUAGUCUAGGUCGAGAAUCUAGCUGG"
    aa = rna_to_aa_super_secret(mrna, "123456789")
    num_codons = int(len(mrna) / 3)

    # for codon chart in pre_code later
    curly1 = "{"
    curly2 = "}"


    # pre-existing code for user 
    translate_pre_code = f"""# your mRNA sequence:
    mrna = "{mrna}"

    # number of codons (groups of 3) in the mRNA sequence:
    num_codons = {num_codons}

    # here's a Python dictionary that contains all codons and their corresponding amino acids:
    codon_table = {curly1}
        'UUU': 'F', 'UUC': 'F',
        'UUA': 'L', 'UUG': 'L', 'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
        'AUU': 'I', 'AUC': 'I', 'AUA': 'I',
        'AUG': 'M',
        'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
        'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S', 'AGU': 'S', 'AGC': 'S',
        'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'UAU': 'Y', 'UAC': 'Y',
        'UAA': '*', 'UAG': '*', 'UGA': '*',
        'CAU': 'H', 'CAC': 'H',
        'CAA': 'Q', 'CAG': 'Q',
        'AAU': 'N', 'AAC': 'N',
        'AAA': 'K', 'AAG': 'K',
        'GAU': 'D', 'GAC': 'D',
        'GAA': 'E', 'GAG': 'E',
        'UGU': 'C', 'UGC': 'C',
        'UGG': 'W',
        'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'AGA': 'R', 'AGG': 'R',
        'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
    {curly2}

    # amino acid sequence: (this should be empty at the start. it'll be complete once you translate each codon below!)
    aa = ""

    # iterate through every codon in the mRNA sequence:
    for i in range(num_codons):
        # translate each codon into its corresponding AA:

        



        # add the translated codon to the amino acid sequence:

        





    # at the end, print your amino acid sequence!
    print(aa)
    """


    translate_instructs = f"""In actuality, mutations in proteins can be much larger than just a couple nucleotides, requiring scientists to study significantly longer sequences of DNA or mRNA. 
    Here, we are looking at an mRNA sequence that is {num_codons * 3} nucleotides long. That means that its corresponding amino acid sequence will be {num_codons} amino acids long!
    Using a Python script, iterate through the mRNA sequence and translate it into its corresponding polypeptide.

    Once you're confident in your code, first click APPLY to save your work, and then hit Run Code!
    """


    st.write(translate_instructs)

    #user code
    code = st_ace(value = translate_pre_code, language = 'python', height = 800)

    #if user tries to run their code:
    if st.button("Run Code"):
        output, matches = execute_code(code, mrna, "translation")

        # if output is error msg
        if output[0: 21] == 'Error executing code:':
            st.error(output)

        # if they didn't fuck up
        else:
            st.write("The amino acid sequence you got was " + output + ".") 

        if matches:
            st.success("Congratulations, your code works!")
        else:
            st.warning("Not quite. Try again")