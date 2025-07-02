import streamlit as st
import pdfplumber
import re
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Legal Document Analyzer", layout="wide")

# Title
st.title("📄 AI Legal Document Analyzer")
st.markdown("Upload a PDF legal document and detect important clauses. Optionally translate the text.")

# Upload PDF
uploaded_file = st.file_uploader("Upload a Legal Document (PDF)", type="pdf")

# Clause patterns
clause_patterns = {
    "Termination Clause": r"\btermination\b",
    "Confidentiality Clause": r"\bconfidentiality\b",
    "Indemnity Clause": r"\bindemnity\b",
    "Jurisdiction Clause": r"\bjurisdiction\b",
    "Payment Terms": r"\bpayment\b.*?\bterms\b",
    "Force Majeure": r"\bforce\smajeure\b",
}

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join(page.extract_text() or '' for page in pdf.pages)

def clean_text(text):
    return re.sub(r'\s+', ' ', text.lower())

def detect_clauses(text, patterns):
    results = {}
    for clause, pattern in patterns.items():
        results[clause] = bool(re.search(pattern, text, re.IGNORECASE))
    return results

if uploaded_file:
    st.success("✅ File uploaded successfully!")

    # Extract and clean
    raw_text = extract_text_from_pdf(uploaded_file)
    cleaned_text = clean_text(raw_text)

    # Clause detection
    st.subheader("📌 Clause Detection Results:")
    clause_results = detect_clauses(cleaned_text, clause_patterns)
    for clause, present in clause_results.items():
        st.write(f"- **{clause}**: {'✅ Present' if present else '❌ Missing'}")

    # Show extracted text
    with st.expander("📃 Show Raw Extracted Text"):
        st.text_area("Text from PDF", raw_text, height=300)

    # Translate option
    st.subheader("🌐 Translate (optional)")
    lang_code = st.selectbox("Choose language", ["", "hi", "ta", "te", "fr", "de"], format_func=lambda x: {
        "": "Select language", "hi": "Hindi", "ta": "Tamil", "te": "Telugu", "fr": "French", "de": "German"
    }.get(x, x))

    if lang_code:
        try:
            translated = GoogleTranslator(source='auto', target=lang_code).translate(raw_text[:3000])
            st.text_area("📖 Translated Text (partial)", translated, height=200)
        except Exception as e:
            st.error(f"Translation failed: {e}")
