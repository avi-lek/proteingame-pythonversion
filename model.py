import requests

def get_esm_pdb(aa_seq, fname):

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=aa_seq, verify=False)

    with open('pdb\\'+fname+'.pdb', 'wb') as f:
        f.write(response.content)