import streamlit as st
from streamlit_ace import st_ace
import contextlib
import io
import sys
from Bio.Seq import Seq

@contextlib.contextmanager
def capture_stdout_stderr():
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    sys.stdout = stdout_capture
    sys.stderr = stderr_capture
    try:
        yield stdout_capture, stderr_capture
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

def execute_code(code, sequence):
    try:
        with capture_stdout_stderr() as (stdout_capture, stderr_capture):
            # If the code contains multiple lines, execute it as multiline code
            if '\n' in code:
                # Execute the code in a custom namespace
                exec_namespace = {}
                exec(code, exec_namespace)

                # Move defined functions to the global namespace
                for name, obj in exec_namespace.items():
                    if callable(obj) and not name.startswith("__"):
                        globals()[name] = obj

                # Execute the main function if it exists
                if 'main' in exec_namespace:
                    output = exec_namespace['main']()
                    return output, output == rna_to_aa(sequence)

            else:
                # Execute single-line code
                exec(code, globals())

        # Get captured output from stdout and stderr
        stdout_output = stdout_capture.getvalue().strip()
        stderr_output = stderr_capture.getvalue().strip()

        # Display the output
        if stdout_output:
            return stdout_output, stdout_output == rna_to_aa(sequence)
        elif stderr_output:
            return stderr_output, False
        else:
            return ""
            
    except Exception as e:
        return f"Error executing code: {e}", False


def main():
    st.title("RNA to AA Sequencing")

    sequence = st.text_input("Enter an RNA sequence:")

    code = st_ace(value="", language="python", height=300)

    if st.button("Run Code"):
        output, matches = execute_code(code, sequence)
        st.write("Output: " + output)
        if matches:
            st.write("Congratulations, your code works!")
        else:
            st.write("Not quite. Try again")

def rna_to_aa(rna_sequence):
    try:
        seq = Seq(rna_sequence)
        return str(seq.translate())
    except:
        return "Invalid RNA sequence!"

if __name__ == "__main__":
    main()
