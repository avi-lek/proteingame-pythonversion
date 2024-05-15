import streamlit as st

def init_sidebar():
    progress, py_ref, codon_chart = st.sidebar.tabs(["Progress", "Python Reference", "Codon Wheel"])
    with progress:
        if "progress_bar" not in st.session_state or "percent_complete" not in st.session_state or "checkpoints" not in st.session_state:
            st.session_state.percent_complete = 0
            st.session_state.checkpoints = ["item1", "item2", "item3", "item4", "Complete"]
            st.session_state.progress_bar = st.progress(0, text="Introduction")
    
    with py_ref:
        with st.expander("Strings"):
            st.write('''
                In Python, a string is a datatype that represents a sequence of characters. For example, you might use strings to store names, messages, and other text. You can *initialize*, or create, a new string by assigning the name of the string to some text in quotations, with the equals sign. 
            ''')
            string_code_example = '''
            # String Initialization Example:
            school_name = "Bellarmine College Preparatory"
            '''
            st.code(string_code_example, language='python')

            st.write('''You can also combine strings by simply using the + operator. ''')
            string_code_example = '''
            # Combining Strings Example:
            street_number = "960 "
            street_name = "W Hedding St"

            address = street_number + street_name
            # address now contains "960 W Hedding St"
            '''
            st.code(string_code_example, language='python')

            st.write('''Finally, you can also combine strings with the += operator, as shown below:''')

            string_code_example = '''
            # Combing Strings Example #2:
            address = "960 "
            address += "W Hedding St"

            # address now contains "960 W Hedding St"
            '''
            st.code(string_code_example, language='python')

            st.write('''Effectively, you get the same result as the earlier example, just without having to initialize a second string for "W Hedding St". When using +=, "W Hedding St" is added to the end of address.''')

        with st.expander("For Loops"):
            st.write('''In Python, a **for loop** is used to *iterate* over, or go through, a sequence (like strings, but so lists, dictionaries, and other datatypes). When using a **for loop** to go through a string, you can access each character in the string one by one.''')
            string_code_example = '''
            # This code prints out each character in school_name individually:
            school_name = "Bellarmine"
            for letter in school_name:
                print(letter)

            # Output:
            # B
            # E
            # L
            # L
            # A
            # R
            # M
            # I
            # N
            # E
            '''
            st.code(string_code_example, language='python')
            st.write('''Essentially, for every letter in the string, school_name, the for loop is going to print that letter. *For the purposes of transcription, you can use for loops to iterate through not just words, but DNA sequences too! They're basically super long words.*''')

        with st.expander("If Statements"):
            st.write('''In Python, **if statements** can be used to check if something is true.''')
            string_code_example = '''
            # If Statement Example #1:
            school_name = "Bellarmine"

            if school_name == "Bellarmine":
                print("Go Bells!")
            '''
            st.code(string_code_example, language='python')
            st.write('''Here, we're checking school_name to verify that it's "Bellarmine." If so, we say "Go Bells!" *Keep in mind that we use two equal signs == in the if statement to verify a comparison!*''')
            st.write('''However, if statements can also account for multiple "ifs": ''')
            string_code_example = '''
            # If Statement Example #2:
            school_name = "Bellarmine"

            if school_name == "Bellarmine":
                print("Go Bells!")
            elif school_name == "Archbishop Mitty":
                print("Go Monarchs!")
            else:
                print("What's your school mascot?")
            '''
            st.code(string_code_example, language='python')
            st.write('''Here, we're running multiple if statements. First, we check if the school is Bellarmine. If so, we print Go Bells! If not, we run the second if statement using "elif" (short for "else if") and check if the school is Mitty. If so, we print Go Monarchs! If both those conditions are false and the school is neither Bell or Mitty, then we'll simply ask what the school mascot is using "else."''')
    with codon_chart:
        st.image('screenshots//codon_wheel.png')



def update_progress_bar():
    st.session_state.percent_complete = st.session_state.percent_complete + 20
    tag =  st.session_state.checkpoints[int(st.session_state.percent_complete/20)-1]
    st.session_state.progress_bar.progress(st.session_state.percent_complete, text=tag)

