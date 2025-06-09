import json
import streamlit as st
from ocr import extract_text_from_image
from agent import parse_kyc_documents

st.title("🧾 Onboarding Agent")
st.write("Upload your identity documents based on your nationality. The agent will auto-fill a structured KYC form.")

nationality = st.radio("Select your nationality:", ["Indian", "American"])

uploaded_files = {}
if nationality == "Indian":
    st.subheader("📤 Upload Indian Documents")
    st.write("Please upload at least 2 documents for verification")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        aadhar_file = st.file_uploader("Upload Aadhar Card", type=["jpg", "png", "jpeg", "pdf"], key="aadhar")
        if aadhar_file:
            uploaded_files['aadhar'] = aadhar_file
    
    with col2:
        pan_file = st.file_uploader("Upload PAN Card", type=["jpg", "png", "jpeg", "pdf"], key="pan")
        if pan_file:
            uploaded_files['pan'] = pan_file
    
    with col3:
        dl_file = st.file_uploader("Upload Driving License", type=["jpg", "png", "jpeg", "pdf"], key="dl_in")
        if dl_file:
            uploaded_files['dl'] = dl_file

else:
    st.subheader("📤 Upload US Documents")
    st.write("Please upload at least 1 document for verification")
    
    col1, col2 = st.columns(2)
    with col1:
        ssn_file = st.file_uploader("Upload Social Security Card", type=["jpg", "png", "jpeg", "pdf"], key="ssn")
        if ssn_file:
            uploaded_files['ssn'] = ssn_file
    
    with col2:
        dl_file = st.file_uploader("Upload Driving License", type=["jpg", "png", "jpeg", "pdf"], key="dl_us")
        if dl_file:
            uploaded_files['dl'] = dl_file

if uploaded_files:
    if len(uploaded_files) < 1:
        st.warning("⚠️ Please upload at least 1 document for verification")
    else:
        with st.spinner("🔍 Processing documents..."):
            st.subheader("📝 Extracted Text from Documents")
            for doc_type, file in uploaded_files.items():
                with st.expander(f"Show {doc_type.upper()} text"):
                    extracted_text = extract_text_from_image(file)
                    st.code(extracted_text)
            
            json_output = parse_kyc_documents(uploaded_files, nationality)
            
            st.subheader("✅ KYC JSON Output")
            st.code(json_output, language="json")
            
            st.download_button(
                label="📥 Download JSON",
                data=json_output,
                file_name="kyc.json",
                mime="application/json"
            )