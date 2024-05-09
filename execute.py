import streamlit as st
from streamlit_ace import st_ace
import contextlib
import io
import sys
from Bio.Seq import Seq
from pyversion_funcs import rna_to_aa_super_secret
from pyversion_funcs import dna_to_rna

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

def execute_code(code, sequence, type):
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
                
            else:
                # Execute single-line code
                exec(code, globals())


        # Get captured output from stdout and stderr
        stdout_output = stdout_capture.getvalue().strip()
        stderr_output = stderr_capture.getvalue().strip()

        # Display the output
        # if it's translation
        if type == "translation":
            if stdout_output:
                return stdout_output, stdout_output == rna_to_aa_super_secret(sequence, "123456789")
            elif stderr_output:
                return stderr_output, False
            else:
                return ""
        
        # if it's transcription
        else:
            if stdout_output:
                return stdout_output, stdout_output == dna_to_rna(sequence, "123456789")
            elif stderr_output:
                return stderr_output, False
            else:
                return ""
        
    except Exception as e:
        return f"Error executing code: {e}", False
