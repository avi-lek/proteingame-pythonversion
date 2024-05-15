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
                In Python, a string is a datatype that represents a sequence of characters. For example, you might use strings to store names, messages, and other text. You can create a new string by setting it equal to another string, or setting it equal to text enclosed by either single or double quotes. 
            ''')
            string_code_example = '''
            #String Initialization Example:
            single_quote_string = 'This is a valid string'
            double_quote_string = "This is also a valid string"
            '''
            st.code(string_code_example, language='python')

            st.write('''You can also combine strings by simply using the + operator. ''')
            string_code_example = '''
            #Combining Strings Example:
            string1 = "cat"
            string2 = "dog"
            string3 = string1+string2

            #string3 now contains "catdog"
            '''
            st.code(string_code_example, language='python')
        with st.expander("For Loops"):
            st.write('''In Python, a for loop is used to iterate over a sequence (like a list, tuple, dictionary, set, or string). When using a for loop to go through a string, you can access each character in the string one by one.''')
            string_code_example = '''
            #This code prints out each character in “Hello, World!” individually. 
            my_string = "Hello, World!"
            for char in my_string:
                print(char)

            # Output:
            # H
            # e
            # l
            # l
            # o
            # ,
            # 
            # W
            # o
            # r
            # l
            # d
            # !
            '''
            st.code(string_code_example, language='python')
        with st.expander("If Statements"):
            st.write('''In Python, if statements can be used to compare strings. You can compare two strings using the == (equality) and != (inequality) operators.''')
            string_code_example = '''
            #In this example, the output will be "The strings are not equal." because "hello" is not equal to "world".
            string1 = "hello"
            string2 = "world"

            if string1 == string2:
                print("The strings are equal.")
            else:
                print("The strings are not equal.")
            '''
            st.code(string_code_example, language='python')
    with codon_chart:
        st.image('screenshots//codon_wheel.png')



def update_progress_bar():
    st.session_state.percent_complete = st.session_state.percent_complete + 20
    tag =  st.session_state.checkpoints[int(st.session_state.percent_complete/20)-1]
    st.session_state.progress_bar.progress(st.session_state.percent_complete, text=tag)

