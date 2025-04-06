import streamlit as st
import fitz  # PyMuPDF
import pandas as pd

st.title("PDF to CSV Extractor")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    
    lines = text.split('\n')
    result = []

    for i in range(len(lines)):
        if "ID" in lines[i]:
            id_line = lines[i]
            item_no = lines[i+1] if i+1 < len(lines) else ""
            code = lines[i+3] if i+3 < len(lines) else ""
            result.append({'ID': id_line, 'item_no': item_no, 'code': code})

    if result:
        df = pd.DataFrame(result)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv, file_name="output.csv", mime="text/csv")
    else:
        st.warning("No matching entries found.")