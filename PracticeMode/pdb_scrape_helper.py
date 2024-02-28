import requests
import urllib

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

def get_pdb_codes(min_amino_acids=100):
    # Define the PDB API endpoint
    pdb_api_url = "https://data.rcsb.org/rest/v1/core/assembly/"
    #pdb_api_url = "https://data.rcsb.org/rest/v1/core/entry/"

    # Fetch the list of all PDB entries 
    response = requests.get(pdb_api_url)
    entries = response.json().get('id', [])

    # Filter entries based on amino acid count
    filtered_entries=[]
    for entry in entries:
        x=get_amino_acid_count(entry)
        if x > min_amino_acids:
            filtered_entries.append(entry)
    #filtered_entries = [entry for entry in entries if get_amino_acid_count(entry) > min_amino_acids]

    return filtered_entries

def get_amino_acid_count(pdb_code):
    entry_url = f"https://data.rcsb.org/rest/v1/core/assembly/{pdb_code}/{1}"
    response = requests.get(entry_url)
    details = response.json()
    amino_acid_count = details.get("rcsb_assembly_info", {}).get("modeled_polymer_monomer_count", 0)
    return amino_acid_count

from Bio import SeqIO
from Bio.PDB import PDBParser
from io import StringIO

def pdb_to_fasta(pdb_code):
    pdb_url = f'https://files.rcsb.org/download/{pdb_code}.pdb'
    pdb_file = urllib.request.urlopen(pdb_url).read()
    pdb_parser = PDBParser(QUIET=True)
    structure = pdb_parser.get_structure(id=pdb_code, file=StringIO(pdb_file.decode('utf-8')))

    sequence = []
    for model in structure:
        for chain in model:
            for residue in chain:
                if residue.get_resname() in amino_acid_dict.keys():
                    sequence.append(amino_acid_dict[residue.get_resname()])

    return sequence

print("".join(pdb_to_fasta('3I40')))


