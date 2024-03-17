from puzzle_help import *
import random
import pandas as pd

labels = ['pdb_id', 'w_aa', 'w_rna', 'w_rna_window', 'm_rna', 'm_rna_window',"m_start", "m_len",  "m_type"]
data = pd.DataFrame(columns=labels)
file = open("puzzles/rcsb_pdb_ids.txt", "r")
content = file.read(34504)
for n in range(30):
    index = random.randrange(4,34504)
    for i in range(5):
        if content[index-i]==',':
            id = content[(index-4-i):(index-i)]
    aa_seq = pdb_to_fasta(id)
    rna = amino_acids_to_rna(aa_seq)        
    mut_window_seq, mut_seq, window_seq, rna_seq, mut_start, mut_len, mtype = mutate(rna)
    row = {'pdb_id':id, 
       'w_aa':aa_seq, 
       'w_rna':rna_seq, 
       'w_rna_window':window_seq, 
       'm_rna':mut_seq, 
       'm_rna_window':mut_window_seq,
       "m_start":mut_start, 
       "m_len":mut_len,  
       "m_type":mtype}
    data.loc[len(data)] = row
    print(str(n/10)+"%")
data.to_csv("puzzles/puzzle_table.csv")
file.close()
