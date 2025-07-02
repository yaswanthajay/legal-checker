import streamlit as st
import pdfplumber
import re
from googletrans import Translator

# Clause patterns
clause_patterns = {
    "Confidentiality": r"confidential|non[-\s]?disclosure",
    "Termination": r"termination|cancel.*agreement",
    "Indemnification": r"indemnif(?:y|ication)",
    "Payment Terms": r"payment terms|fees|charges",
    "Dispute Resolution": r"arbitration|jurisdiction|dispute resolution",
    "Governing Law": r"governing law|under the laws of",
}

# Text extractor
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

# Cleaner
def clean_text(text):
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

# Clause checker
def detect_clauses(text):
    results = {}
    for clause, pattern in clause_patterns.items():
        results[clause] = bool(re.search(pattern, text, re.IGNORECASE))
    return results

# Translator
def translate_text(text, dest_lang):
    translator = Translator()
    translated = translator.translate(text, dest=dest_lang)
    return translated.text

# Streamlit UI
st.title("📄 Legal Document Analyzer (No AI, Free!)")

uploaded_file = st.file_uploader("Upload a Legal PDF", type="pdf")

if uploaded_file:
    st.success("✅ File uploaded")
    raw_text = extract_text_from_pdf(uploaded_file)
    cleaned_text = clean_text(raw_text)
    
    st.subheader("🔍 Extracted Text Preview")
    st.text_area("Text", cleaned_text[:1000], height=200)
    
    clause_results = detect_clauses(cleaned_text)
    st.subheader("📘 Clause Detection")
    
    for clause, present in clause_results.items():
        st.write(f"**{clause}**: {'✅ Found' if present else '❌ Missing'}")

    st.subheader("🌐 Translate Clause Results")
    lang = st.selectbox("Choose language", ["hi", "te", "ta", "bn", "kn", "ml", "mr", "gu"])  # Hindi, Telugu, Tamil, etc.

    translated_output = "\n".join([f"{clause}: {'Found' if present else 'Missing'}" for clause, present in clause_results.items()])
    translated_text = translate_text(translated_output, dest_lang=lang)

    st.text_area("Translated Output", translated_text, height=200)
