import streamlit as st
from stmol import showmol
from practice_functions import *
import pandas as pd
from setup_puzzle import *
from st_pages import Page, Section, show_pages, add_page_title
from st_pages import hide_pages
st.set_page_config(page_title="Mutations Practice", page_icon=":dna:", layout="wide")
hide_pages(["Transcription", "Identify Mutations", "Translation", "Sandbox Instructions"])
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

st.markdown("**Puzzle Mode**")
st.markdown("In this mode, you can solve challenging and fun puzzles dealing with mutated protein sequences to “fix” the mutation based on your understanding of the different types of protein mutations.")

st.markdown("*The Central Dogma of Biology*")

st.image("screenshots//central_dogma.jpg", caption='Credit: Biomed Guide', width=500)

st.markdown("The Central Dogma of molecular biology follows a series of sequential steps, allowing for a clear understanding of how genetic information flows within living organisms. It outlines the processes through which genetic instruction encoded within the DNA is transcribed into RNA, then translated into proteins.")

st.markdown("1. Firstly, DNA replication allows for the duplication of genetic material prior to cell division, ensuring genetic continuity. Then, during transcription, a segment of DNA is transcribed into a messenger RNA (mRNA) with the aid of RNA polymerase and other crucial enzymes and proteins. This mRNA molecule carries the necessary genetic code from the DNA within the nucleus of the cell, to the ribosomes within the cytoplasm, where protein synthesis takes place. After a mature RNA is developed after the removal of introns and the attachment of a poly-A tail to the 3’ end  and a 5’ cap, the mature mRNA is ready to proceed to the next steps.")  
st.markdown("2. In translation, the mRNA sequences attach to its respective anticodons, resulting in the creation of a polypeptide chain of amino acids, each codon coding for individual amino acids. These codons are read from a codon chart, each three letter combination corresponding to a certain amino acid. The process building chains of amino acids is initiated by the assembly of the start codon, and ends due to the signaling of a stop codon.")

st.markdown("*Mutations*")
st.markdown("Mutations, or alterations within the DNA sequence may arise during various cellular processes, posing significant impacts on the protein’s structure and function. There are several types of mutations, each possessing their unique contributions. A majority of these mutations can occur in any given place within the genetic code, some being more harmful to humans than others. Types of mutations are listed below:")

st.markdown("1. Substitution: when a single nucleotide or multiple nucleotides are replaced with different ones, they change the nucleotide sequence. Substitution mutations can be characterized into silent, missense, or nonsense mutations. Silent mutations don't affect the amino acid sequences due to the redundancy within the genetic code (different codon pairs coding for the same amino acid). On the contrary, missense mutations replace one or more amino acids with another. Nonsense mutations on the other hand, introduce a premature stop codon which limits the growth of the protein, posing unintended consequences.")  
st.markdown("2. Insertions/deletions: These involve adding or removing nucleotides from the DNA sequence, potentially causing frameshift mutations which alter the entire protein sequence onwards.")   
st.markdown("3. Frameshift mutations: When insertion and deletion of a number of nucleotides that isn’t a multiple of 3 (like 4 amino acids or 2 or 7) occur, the reading frame of the sequence shifts. For example, if the original sentence is “the fat cat sat,” and 2 letters are inserted, the sentence becomes “tuy hef atc ats at.” Notice how every single codon after the mutation got changed. Frameshift mutations cause a significant change in the overall sequence by shifting the reading frame and thus changing all following amino acids.")

st.markdown("On top of these, repeat expansions lead to genetic disorders because it increases the number of repeated DNA sequences within a gene. In addition, chromosomal mutations such as translocations affect gene function by altering the structure of the protein or amount of chromosomes.")

st.markdown("**If you understand central dogma and mutations, and you feel ready to start the puzzle, click on the 'Start Puzzle' button in the sidebar.**")
if st.sidebar.button("Start Puzzle"):
    st.switch_page("pages//Transcription.py")