import streamlit as st
import pandas as pd
from code_editor import code_editor
from Bio.Seq import Seq
import pandas as pd
from streamlit_ace import st_ace
from pyversion_funcs import *
from st_pages import hide_pages
from execute import *
from py_version_sidebar_utils import *

# intro
def init_intro():
    # INTRODUCTION TEXT
    # welcome user to page

    st.write('''Welcome to the Python version! This aspect of our website will integrate Python programming with the central dogma of biology.
    In actuality, the DNA sequences bioinformaticians and data analysts deal with can be thousands of nucleotides long, making it unfeasible to transcribe DNA or translate mRNA by hand. Especially when dealing with larger datasets, it makes a lot more sense to use programming tools like Python to analyze our data. 
    ''')
    st.write('''No experience with Python? No worries! This exercise will teach you how to transcribe long sequences of DNA using Python with step-by-step instructions that'll introduce you to different Python concepts. In the sidebar, there'll also be more in depth info on Python under "Python Reference" if you're stuck!
    ''')

def init_string():
    st.write('''
    To start, in order to transcribe a DNA sequence, we need to store it somewhere first. 
    We can store DNA sequences in a ***Python string***, a data type that can store words and sentences. Think of the string dna_sequence below as one long word with each base being a letter. 
    Here's an example of a short DNA sequence stored in a string:
    ''')

    # show string ex
    string_code = '''
    # DNA sequence stored in a Python string:
    dna_sequence = "ATGCTAGTA"
    '''
    st.code(string_code, language = "python", line_numbers = True)

# start of Python tutorial - prob good to have button to show this part 
def init_for_loops():
    # PART 1: FOR LOOPS...
    # introduce the for loop
    st.write('''In order to transcribe this sequence though, we need to be able read through every “letter,” or nucleotide, of the sequence. 
    An efficient way to go through the sequence is with ***for loops***''')

    # more for loop explanation
    for_loop_exp = '''The ***for loop*** above reads through every nucleotide in the DNA sequence and print every nucleotide individually. 
    Hover over the bottom right of the code box and click Run to see!
    '''
    st.write(for_loop_exp)

    # show for loop ex
    for_loop_code = '''# DNA sequence stored in a Python string:
dna_sequence = "ATGCTAGTA"

# for every nucleotide in the sequence, print it:
for nucleotide in dna_sequence:
    print(nucleotide)
    '''
    quick_execute(for_loop_code)
    

def init_if():
    if_intro = '''However, with the **for loops**, we might also want to make decisions inside of the for loop. 
    For example, if you wanted to output an RNA sequence given the coding strand of DNA, you would need to use ***if statements*** inside a for loop to replace only Thymine with Uracil.
    '''
    st.write(if_intro)
    if_statement_ex = ''' 
dna_sequence = "ATGCTAGTA"

# your RNA sequence: (this is empty for now - it'll fill up as you iterate through the DNA and add bases one by one!)
rna_sequence = ""

# for each nucleotide in the DNA:
for nucleotide in dna_sequence:
    # if the nucleotide is Thymine", add "U" to the RNA sequence 
    if nucleotide == "T":
        rna_sequence += "U"
    # otherwise, add the DNA base to the RNA sequence
    else: 
        rna_sequence += nucleotide

print(rna_sequence)'''

    quick_execute(if_statement_ex)

def transcription_exercise():
    # DNA input & expected RNA user output
    if 'dna' not in st.session_state:
        st.session_state['dna'] = get_rand_dna()

    if 'mrna' not in st.session_state:
        st.session_state['mrna'] = dna_to_rna(st.session_state.dna, "123456789")

    # pre code for user
    transcribe_pre_code = f'''# your DNA sequence:
dna_sequence = "{st.session_state.dna}"

# your RNA output (this is empty for now... it'll be complete once you transcribe the DNA below!)
rna_sequence = ""

# how do you transcribe each nucleotide individually by reading the DNA sequence?


# at the end, print your RNA sequence!
print(rna_sequence)
    '''

    # instructions
    transcribe_instructs = f'''
    Now, let's do the full transcription of a DNA sequence that's much longer than the one in the examples. 
    Here, we are looking to transcribe a DNA sequence that is {len(st.session_state.dna)} nucleotides long. Think back to what you learned from earlier!
    As always, if you need greater explanation on some Python concepts, feel free to check out more in-depth explanations in the sidebar under "Python Reference."
    Once you're confident in your code, hover over the bottom right corner of the text editor window and click Run.  
    '''
    st.write(transcribe_instructs)

    # code editor config variables
    height = [19, 22]
    language="python"
    theme="default"
    shortcuts="vscode"
    focus=False
    wrap=True
    editor_btns = [{
        "name": "Run",
        "feather": "Play",
        "primary": True,
        "hasText": True,
        "showWithIcon": True,
        "commands": ["submit"],
        "style": {"bottom": "0.44rem", "right": "0.4rem"}
    }]

    code = code_editor(transcribe_pre_code,  height = height, lang=language, theme=theme, shortcuts=shortcuts, focus=focus, buttons=editor_btns, options={"wrap": wrap, "showLineNumbers": True})
    
    # show response dict
    if len(code['id']) != 0 and (code['type'] == "selection" or code['type'] == "submit" ):
        # Capture the text part
        user_text = code['text']
        output, matches = execute_code(user_text, st.session_state.dna, "transription")

        # if output is error msg
        if output[0: 21] == 'Error executing code:':
            st.error(output)

        # if their code compiles
        else:
            st.code(output) 

        if matches:
            st.success("Congratulations, your code works! You've now finished the exercise!")
            
        else:
            st.warning("Not quite. Try again.")

def quick_execute(new_code):
    # config it
    height = [6, 22]
    language="python"
    theme="default"
    shortcuts="vscode"
    focus=False
    wrap=True
    editor_btns = [{
        "name": "Run",
        "feather": "Play",
        "primary": True,
        "hasText": True,
        "showWithIcon": True,
        "commands": ["submit"],
        "style": {"bottom": "0.44rem", "right": "0.4rem"}
    }]

    code = code_editor(new_code,  height = height, lang=language, theme=theme, shortcuts=shortcuts, focus=focus, buttons=editor_btns, options={"wrap": wrap, "showLineNumbers": True})
    for_loop_result, err = execute_code_output(code["text"])
    # show result of for loop print
    if err==False:
        st.error(for_loop_result)
    else:
        st.code(for_loop_result)

def init_indent():
    st.write('''Keep in mind that for both **for loops** and **if statements** that you're using the right syntax! That means indenting the lines inside the for loop. Here are the two most common mistakes:''')
    indent_ex = '''
    # missing the indent:
    for nucleotide in dna_sequence:
    print(nucleotide)

    # missing the colon:
    for nucleotide in dna_sequence
        print(nucleotide)
    '''
    st.code(indent_ex, language = "python", line_numbers = True)
    st.write('''If you're using the correct syntax, everything should run smoothly. Here's an example of a correctly written **for loop**:''')
    indent_correct_ex = '''
    # what you SHOULD do:
    for nucleotide in dna_sequence:
        print(nucleotide)
    '''
    st.code(indent_correct_ex, language = "python", line_numbers = True)

    st.write('''The same goes for **if statements**! Make sure your code doesn't look like this:''')
    index_if_ex = '''
    # missing the indent:
    if nucleotide == "A":
    rna_sequence += "U"
    
    # missing the colon:
    if nucleotide == "A"
        rna_sequence += "U"

    # only using one equals '=' sign:
    if nucleotide = "A":
        rna_sequence += "U"
    '''
    st.code(index_if_ex, language = "python", line_numbers = True)
    st.write('''Make sure that you're adding colons and indenting just like with **for loops** while also using two equals signs '==' to check what the nucleotide is!
             *When attaching the nucleotide to the end of the RNA sequence, also make sure to use the "+=" operator!*
             ''')