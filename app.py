import streamlit as st
import PyPDF2
from summarizer import summarize_any, is_code

st.set_page_config(
    page_title="AI Text & Code Summarizer",
    layout="centered"
)

st.title("🧠 AI Text & Code Summarizer")
st.write("Summarize text, PDFs, and explain programming code.")

input_type = st.radio(
    "Choose Input Type",
    ["Text / Code", "PDF"]
)

content = ""

if input_type == "Text / Code":
    content = st.text_area(
        "Paste your text or code here",
        height=300
    )

elif input_type == "PDF":
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
    if pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            if page.extract_text():
                content += page.extract_text()

if st.button("Generate Output"):
    if len(content.strip()) < 30:
        st.warning("Please provide sufficient input.")
    else:
        with st.spinner("Processing..."):
            result = summarize_any(content)

        # CODE HIGHLIGHTING
        if is_code(content):
            st.subheader("💻 Code (Highlighted)")
            st.code(content)

            st.subheader("🧠 Code Explanation")
            st.write(result)
        else:
            st.subheader("📄 Summary")
            st.write(result)
