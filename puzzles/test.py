from puzzle_help import *

rna = amino_acids_to_rna("EQLLKALEFLLKELLEKL")

for i in range(5):
    print(mutate(rna))