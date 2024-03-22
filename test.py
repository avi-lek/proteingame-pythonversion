from text_highlighter import text_highlighter
import streamlit as st

# Basic usage
i_text = "John Doe is the founder of MyComp Inc. and lives in New York with his wife Jane Doe."
result = text_highlighter(
    text="John Doe is the founder of MyComp Inc. and lives in New York with his wife Jane Doe.",
    labels=[("ORG", "#0000FF")],
)

# Show the results (in XML format)

# Show the results (as a list)
if len(result)>0:
    st.write("Unselected: " + i_text[0:result[0]["start"]]+i_text[result[0]["end"]:-1])
    st.write("Selected: " + i_text[result[0]["start"]:result[0]["end"]])
st.write(result)