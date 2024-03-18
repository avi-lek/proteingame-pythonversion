import streamlit as st

st.markdown('''Welcome to ‘My Protein is Broken!’''')

url = "https://forms.gle/q9mjvDEk1PeHW5aTA"
st.markdown('''For the full teacher instructions, please click here. For the full student instructions, please click here. After using this website, please let us know how you liked it [here](%s)!''' % url)

st.markdown("**Sandbox Mode**")
st.markdown('''In this mode, you can experiment with a protein of your choice and visualize its basic structure and characteristics. You can also try changing its amino acid sequence and observing the resulting structure.''')

st.markdown('''Instructions for use:  
We’ve already preloaded some basic proteins, including myoglobin (1MBN), Human Growth Hormone (1HGU), and glucagon (1GCN). But, you can also personalize the proteins you look at by clicking on the dropdown menu under “PDB Code” and selecting “Select From PDB ID.” From there, find a PDB ID from protein databases like Uniprot and RCSB. ''')

st.markdown('''Afterwards, you’ll see a prediction of the structure of the protein. Study its structure by zooming in and out of the protein and rotating around it. An example structure is shown below.''')

st.image("https://photos.app.goo.gl/ih7q8Bfg6HHMTtWL9")

st.markdown('''In the left sidebar menu, you can also change the color of the protein (“Pick A Color” in the “Visualization Settings” menu), highlight the hydrophobicity of each area (“Hydrophobicity” in “Select View”), and choose between different visualization styles, including cartoon, stick, and sphere styles (“Style” in the “Visualization Settings” menu). For the hydrophobicity setting, a key is provided in the sidebar that explains the color gradient. A few illustrations of the “stick” style and hydrophobicity visualizations are provided below.''')

st.image("https://photos.app.goo.gl/gV2JrYCx8kjmNh6B6")
st.image("https://photos.app.goo.gl/aHaZ79LqeuuX3g5d8")

st.markdown('''You can also test out the effects of mutations on a protein’s structure by turning on “ML Predicted Structure.” Add, delete or insert amino acids in the original protein’s sequence to see the structure of the new, mutated protein compared with the original.''')

st.image("https://photos.app.goo.gl/zhHNWFaKDxS9rmAD8")