import streamlit as st
import pandas as pd
from Bio import SeqIO
import os
import base64

def generate_grnas(sequence, pam="NGG"):
    """Generate gRNAs with PAM sequences"""
    grnas = []
    pam_length = len(pam)
    for i in range(len(sequence) - pam_length):
        if sequence[i + pam_length : i + 2 * pam_length] == pam:
            grnas.append(sequence[i : i + 20])  # Typical gRNA length is 20bp
    return grnas

def analyze_off_targets(grnas):
    """Placeholder for off-target analysis using CRISPOR or CRISPResso"""
    # This function should integrate actual tools for off-target prediction
    return [f"Predicted off-targets for {grna}" for grna in grnas]

def file_download(data, filename="output.csv"):
    """Generate a downloadable link for the results."""
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV File</a>'
    return href

# Streamlit UI
st.title("CRISPR Design Tool")
st.write("Upload a FASTA file to analyze gRNA sequences and predict off-target effects.")

uploaded_file = st.file_uploader("Upload FASTA file", type=["fasta", "fa"])
if uploaded_file is not None:
    fasta_sequences = list(SeqIO.parse(uploaded_file, "fasta"))
    results = []
    
    for seq_record in fasta_sequences:
        sequence = str(seq_record.seq)
        grnas = generate_grnas(sequence)
        off_targets = analyze_off_targets(grnas)
        
        for grna, off_target in zip(grnas, off_targets):
            results.append([seq_record.id, grna, off_target])
    
    df_results = pd.DataFrame(results, columns=["Sequence ID", "gRNA", "Off-Target Predictions"])
    st.write(df_results)
    st.markdown(file_download(df_results), unsafe_allow_html=True)
