import random
from Bio.Seq import Seq


# gets random DNA sequence
def get_rand_dna():
    # get random length
    lengths = [84, 87, 90, 93, 96, 99, 102, 105]
    dna_len = random.choice(lengths)

    # generate dna sequence
    dna = ""
    nucleotides = ['A', 'C', 'G', 'T']
    for i in range(dna_len):
        dna += random.choice(nucleotides)
    return dna

# gets random DNA sequence
def get_rand_dna_with_len_two_strands(dna_len):
    # generate dna sequence
    dna1 = ""
    dna2 = ""

    nucleotides = [('A', 'T'), ('C','G'), ('G','C'), ('T','A')]
    for i in range(dna_len):
        bases = random.choice(nucleotides)
        dna1+=bases[0]
        dna2+=bases[1]
    return dna1, dna2
# gets random DNA sequence
def get_rand_dna_with_len(dna_len):
    # generate dna sequence
    dna = ""
    nucleotides = ['A', 'C', 'G', 'T']
    for i in range(dna_len):
        dna += random.choice(nucleotides)
    return dna

# goes from DNA to RNA
def dna_to_rna(dna_sequence, key):
    if key == "123456789":
        rna = ""
        for nucleotide in dna_sequence:
            if nucleotide == 'A':
                rna += 'U'
            elif nucleotide == 'C':
                rna += 'G'
            elif nucleotide == 'G':
                rna += 'C'
            elif nucleotide == 'T':
                rna += 'A'
        return rna

# goes from RNA to AA
def rna_to_aa_super_secret(rna_sequence, key):
    if key == "123456789":
        seq = Seq(rna_sequence)
        return str(seq.translate())







