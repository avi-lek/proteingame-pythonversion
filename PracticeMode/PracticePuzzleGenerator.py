import random
import time
import requests
import urllib
import os


# codon to amino acid
def codon_to_amino_acid(codon_seq):

    codon_table = {
        'AUA':'I', 'AUC':'I', 'AUU':'I', 'AUG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACU':'T',
        'AAC':'N', 'AAU':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGU':'S', 'AGA':'R', 'AGG':'R',
        'CUA':'L', 'CUC':'L', 'CUG':'L', 'CUU':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCU':'P',
        'CAC':'H', 'CAU':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGU':'R',
        'GUA':'V', 'GUC':'V', 'GUG':'V', 'GUU':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCU':'A',
        'GAC':'D', 'GAU':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGU':'G',
        'UCA':'S', 'UCC':'S', 'UCG':'S', 'UCU':'S',
        'UUC':'F', 'UUU':'F', 'UUA':'L', 'UUG':'L',
        'UAC':'Y', 'UAU':'Y', 'UAA':'_', 'UAG':'_',
        'UGC':'C', 'UGU':'C', 'UGA':'_', 'UGG':'W',
    }

    amino_acid_seq = ''

    for i in range(0, len(codon_seq), 3):
        codon = codon_seq[i:i+3]
        amino_acid = codon_table.get(codon, 'X')
        amino_acid_seq += amino_acid

    return amino_acid_seq

# list of nucleotides
rna_nucleotides = ["A", "C", "G", "U"]

# SCRAPER

amino_acid_dict = {
    'ALA': 'A',  # Alanine
    'ARG': 'R',  # Arginine
    'ASN': 'N',  # Asparagine
    'ASP': 'D',  # Aspartic Acid
    'CYS': 'C',  # Cysteine
    'GLN': 'Q',  # Glutamine
    'GLU': 'E',  # Glutamic Acid
    'GLY': 'G',  # Glycine
    'HIS': 'H',  # Histidine
    'ILE': 'I',  # Isoleucine
    'LEU': 'L',  # Leucine
    'LYS': 'K',  # Lysine
    'MET': 'M',  # Methionine
    'PHE': 'F',  # Phenylalanine
    'PRO': 'P',  # Proline
    'SER': 'S',  # Serine
    'THR': 'T',  # Threonine
    'TRP': 'W',  # Tryptophan
    'TYR': 'Y',  # Tyrosine
    'VAL': 'V'   # Valine
}

def tempRead():
    folder_path = r'C:\Users\bulba\OneDrive - Bellarmine College Preparatory\Documents\Research\pdb_ids'

    files = os.listdir(folder_path)

    selected_file = random.choice(files)

    selected_file_path = os.path.join(folder_path, selected_file)

    # Now you can open and read the file or perform any other operation you need
    with open(selected_file_path, 'r') as file:
        content = file.read()

        codes = content.split(',')
 
        code = [code.strip() for code in codes]

        sel_code = random.choice(codes)

        return sel_code

from Bio import SeqIO
from Bio.PDB import PDBParser
from io import StringIO

def pdb_to_fasta(pdb_code):
    codon_table1 = {
        'I':'AUA', 'I':'AUC', 'I':'AUU', 'M':'AUG',
        'T':'ACA', 'T':'ACC', 'T':'ACG', 'T':'ACU',
        'N':'AAC', 'N':'AAU', 'K':'AAA', 'K':'AAG',
        'S':'AGC', 'S':'AGU', 'R':'AGA', 'R':'AGG',
        'L':'CUA', 'L':'CUC', 'L':'CUG', 'L':'CUU',
        'P':'CCA', 'P':'CCC', 'P':'CCG', 'P':'CCU',
        'H':'CAC', 'H':'CAU', 'Q':'CAA', 'Q':'CAG',
        'R':'CGA', 'R':'CGC', 'R':'CGG', 'R':'CGU',
        'V':'GUA', 'V':'GUC', 'V':'GUG', 'V':'GUU',
        'A':'GCA', 'A':'GCC', 'A':'GCG', 'A':'GCU',
        'D':'GAC', 'D':'GAU', 'E':'GAA', 'E':'GAG',
        'G':'GGA', 'G':'GGC', 'G':'GGG', 'G':'GGU',
        'S':'UCA', 'S':'UCC', 'S':'UCG', 'S':'UCU',
        'F':'UUC', 'F':'UUU', 'L':'UUA', 'L':'UUG',
        'Y':'UAC', 'Y':'UAU', '_':'UAA', '_':'UAG',
        'C':'UGC', 'C':'UGU', '_':'UGA', 'W':'UGG',
    }

    global rndRNAStr
    global sequence
    global RNA_print
    global chlen

    pdb_url = f'https://files.rcsb.org/download/{pdb_code}.pdb'
    pdb_file = urllib.request.urlopen(pdb_url).read()
    pdb_parser = PDBParser(QUIET=True)
    structure = pdb_parser.get_structure(id=pdb_code, file=StringIO(pdb_file.decode('utf-8')))

    sequ = []
    sequence = ''
    RNA_print = ''

    for model in structure:
        for chain in model:
            for residue in chain:
                if residue.get_resname() in amino_acid_dict.keys():
                    sequ.append(amino_acid_dict[residue.get_resname()])
    
    # sequence = sequ.replace("[", "").replace("]", "").replace(",", "").strip()
                    
    sequence = " ".join(str(x) for x in sequ)
    sequence = sequence.replace(" ", "")

    rndRNAStr = ''

    for i in range(0, len(sequence)):
        AA = sequence[i]
        codons = codon_table1.get(AA)
        rndRNAStr += codons

    for i in range(0, len(rndRNAStr), 3):
        RNA_print += rndRNAStr[i:i+3]
        if i + 3 < len(rndRNAStr):
            RNA_print += ' '

    chlen = len(rndRNAStr)-5

# prep for mutation
def mis_replace_characters(RNAStr, nucleotides, start_index, num_characters):
    end_index = start_index + num_characters

    nuc_add = ''.join([random.choice(nucleotides)
                     for nuc in range(num_characters)])

    global RNAMut
    RNAMut = RNAStr[:start_index] + nuc_add + RNAStr[end_index:]

def ins_replace_characters(RNAStr, nucleotides, start_index, num_characters):
    nuc_add = ''.join([random.choice(nucleotides)
                     for nuc in range(num_characters)])

    global RNAMut
    RNAMut = RNAStr[:start_index] + nuc_add + RNAStr[start_index:]

    def round_down_del(input_str):
        length = len(input_str)
        new_length = length - (length % 3)

        return input_str[:new_length]
    RNAMut = round_down_del(RNAMut)

def del_replace_characters(RNAStr, start_index, num_characters):
    global RNAMut
    
    RNAMut = RNAStr[:start_index] + RNAStr[start_index + num_characters:]

    def round_down_del(input_str):
        length = len(input_str)
        new_length = length - (length % 3)

        return input_str[:new_length]
    RNAMut = round_down_del(RNAMut)

def non_replace_characters(AASeq, mutRNA):
    global mutatAA

    mutatAA = ''

    non_index_stop = AASeq.find("_")
    n_index_stop = -1

    if non_index_stop != -1:
        n_index_stop = non_index_stop + 1
        mutatAA = AASeq[:non_index_stop]

    non_index_uaa = mutRNA.find("UAA")
    non_index_uag = mutRNA.find("UAG")
    non_index_uga = mutRNA.find("UGA")

    n_index_uaa_u = -1
    n_index_uag_u = -1
    n_index_uga_u = -1

    if non_index_uaa != -1:
        n_index_uaa_u = non_index_uaa + 1
        mutRNA = mutRNA[:non_index_uaa]
    if non_index_uag != -1:
        n_index_uag_u = non_index_uag + 1
        mutRNA = mutRNA[:non_index_uag]
    if non_index_uga != -1:
        n_index_uga_u = non_index_uga + 1
        mutRNA = mutRNA[:non_index_uga]
    print(mutRNA)

# choose type of mutation
def mut_type_selector():
    type_num = random.randint(0,2)
    if type_num == 0:
        substitution()
    elif type_num == 1:
        insertion()
    elif type_num == 2:
        deletion()

# making mutation puzzles
def substitution():
    global mutAASeq

    start_index = random.randint(5, chlen)
    num_characters = random.randint(1, 9)

    mis_replace_characters(rndRNAStr, rna_nucleotides, start_index, num_characters)

    mutAASeq = ''
    mutAASeq = codon_to_amino_acid(RNAMut)

    if mutAASeq == sequence:
        setup()
    elif "_" in mutAASeq:
        nonsense(RNAMut, sequence, mutAASeq)
    else:
        print("Puzzle type: missense substitution")
        print("")
        print("Original amino acid sequence: " + sequence)

        time.sleep(1)

        print("")
        print("Mutated amino acid sequence: " + mutAASeq)
        print("Mutated RNA sequence: " + RNAMut)

        time.sleep(1)
        print("")
        user_ans_check(rndRNAStr, sequence, mutAASeq, RNAMut)

def insertion():
    global mutAASeq

    start_index = random.randint(5, chlen)
    num_characters = random.randint(3, 9)

    ins_replace_characters(rndRNAStr, rna_nucleotides, start_index, num_characters)

    mutAASeq = ''
    mutAASeq = codon_to_amino_acid(RNAMut)

    if mutAASeq == sequence:
        setup()
    elif "_" in mutAASeq:
        nonsense(RNAMut, sequence, mutAASeq)
    else:
        print("Puzzle type: insertion")
        print("")
        print("Original amino acid sequence: " + sequence)

        time.sleep(1)

        print("")
        print("Mutated amino acid sequence: " + mutAASeq)
        print("Mutated RNA sequence: " + RNAMut)

        time.sleep(1)
        print("")
        user_ans_check(rndRNAStr, sequence, mutAASeq, RNAMut)

def deletion():
    global mutAASeq

    start_index = random.randint(10, chlen)
    num_characters = random.randint(1, 5)

    del_replace_characters(rndRNAStr, start_index, num_characters)

    mutAASeq = ''
    mutAASeq = codon_to_amino_acid(RNAMut)

    if mutAASeq == sequence:
        setup()
    elif "_" in mutAASeq:
        nonsense(RNAMut, sequence, mutAASeq)
    else:
        print("Puzzle type: deletion")
        print("[Note: some nucleotide bases at the end of the mutated sequence may have been deleted to make triplets of bases]")
        print("")
        print("Original amino acid sequence: " + sequence)

        time.sleep(1)
        print("")
        print("Mutated amino acid sequence: " + mutAASeq)
        print("Mutated RNA sequence: " + RNAMut)

        time.sleep(1)
        print("")
        user_ans_check(rndRNAStr, sequence, mutAASeq, RNAMut)

def nonsense(mutRNA, AASeq, mutAA):
    non_replace_characters(mutAA, mutRNA)

    if mutatAA == AASeq:
        setup()
    else:
        print("Puzzle type: nonsense mutation")
        print("")
        print("Original amino acid sequence: " + AASeq)

        time.sleep(1)

        print("")
        print("Mutated amino acid sequence: " + mutatAA)
        print("Mutated RNA sequence: " + mutRNA)

        time.sleep(1)
        print("")
        user_ans_check(rndRNAStr, AASeq, mutAA, mutRNA)

def user_ans_check(RNAStr, AASeq, AAMut, mutatedRNA):
    user_ans_rna = input("What should the original RNA sequence have been? ")

    if user_ans_rna == "0319":
        print("Original RNA: " + RNA_print)
    else:
        user_ans_aa = codon_to_amino_acid(user_ans_rna)

        time.sleep(0.5)
        print("")
        print("Checking your answer...")
        time.sleep(0.5)
    
        if user_ans_aa == sequence:
            print("")
            print("That is correct. WAHOO!!!!!!!")

            time.sleep(1)

            print("")
            play_again = input("Would you like to play again? Y/N ")
            if play_again.upper() == "Y":
                setup()
            elif play_again.upper() == "N":
                print("Ok, thanks for playing!")
            
        else:
            print("")
            print("Wrong xdd.")

            time.sleep(1)

            print("")
            play_again = input("Would you like to play again? Y/N ")
            if play_again.upper() == "Y":
                setup()
            elif play_again.upper() == "N":
                print("Ok, thanks for playing!")

# program start code
def setup():
    pdbcode = tempRead()
    pdb_to_fasta(pdbcode)
    mut_type_selector()

# start puzzle
print("Welcome to 'My Protein Is Broken!'")

time.sleep(0.75)
print("")

start = input("Please type 'start' for a practice puzzle: ")
if start == "start":
    setup()
else:
    print("Error. Please try again.")