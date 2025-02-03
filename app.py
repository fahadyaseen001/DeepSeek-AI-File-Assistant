import os
import re
import json
import streamlit as st
from together import Together
import pdfplumber
from docx import Document
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import io
import base64

LOGO_PATH = "logo.png"


def get_base64_image(image_path):
    """Convert image to base64 for HTML embedding"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error("Logo image not found!")
        return ""

# Get base64 encoded logo
LOGO_BASE64 = get_base64_image(LOGO_PATH)

def extract_text(file_bytes, file_type):
    """Universal text extraction for PDF, DOCX, and images"""
    text = ""
    
    try:
        if file_type == "application/pdf":
            try:
                with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
                if text.strip():
                    return text
            except:
                images = convert_from_bytes(file_bytes)
                for image in images:
                    text += pytesseract.image_to_string(image)
        
        elif file_type in ["image/png", "image/jpeg"]:
            image = Image.open(io.BytesIO(file_bytes))
            text = pytesseract.image_to_string(image)
        
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(io.BytesIO(file_bytes))
            text = "\n".join([para.text for para in doc.paragraphs])
            
        return text.strip()
    
    except Exception as e:
        st.error(f"Text extraction failed: {str(e)}")
        return ""

def analyze_with_deepseek(api_key, text):
    """Structured analysis using DeepSeek via Together API"""
    if not api_key:
        st.error("Please enter your Together API Key")
        return {}
    
    client = Together(api_key=api_key)
    
    prompt = f"""Analyze this document and return JSON with:
{{
  "document_type": ["Resume", "Cover_Letter", "Proposal", "Other"],
  "candidate_name": "Full name",
  "job_title": "Primary position",
  "company": "Main company"
}}

Document:
{text[:3000]}
"""
    
    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        raw_output = response.choices[0].message.content
        json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        return json.loads(json_match.group()) if json_match else {}
        
    except Exception as e:
        st.error(f"AI analysis failed: {str(e)}")
        return {}

def clean_filename(text):
    """Sanitize filename components"""
    return re.sub(r'[^a-zA-Z0-9_-]', '', text.replace(" ", "_")).strip('_')

def generate_filename_variations(analysis, original_filename):
    """Generate multiple filename suggestions with original extension"""
    base, ext = os.path.splitext(original_filename)
    ext = ext.lower()
    
    name = clean_filename(analysis.get("candidate_name", "Document"))
    job = clean_filename(analysis.get("job_title", ""))
    company = clean_filename(analysis.get("company", ""))
    doc_type = clean_filename(analysis.get("document_type", ""))
    
    variations = [
        f"{name}_{job}_{company}_{doc_type}{ext}",
        f"{name}_{job}_{doc_type}{ext}",
        f"{name}_{company}_{doc_type}{ext}",
        f"{name}_{doc_type}{ext}",
        f"{doc_type}_{job}_{company}{ext}"
    ]
    
    return [v for v in variations if not v.startswith('_')]

def main():
    st.set_page_config(
        page_title="DeepSeek Doc Namer",
        layout="centered",
        page_icon=LOGO_PATH
    )
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("## 🔐 API Configuration")
        api_key = st.text_input(
            "Enter Together API Key:", 
            type="password",
            help="Get your API key from Together.ai"
        )
        st.markdown("[Get API Key →](https://together.ai)")
        st.markdown("---")
        st.markdown(
            f"""
            <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{LOGO_BASE64}" style="width: auto; max-width: 50px; height: auto; margin-right: 10px;" />
            <span>Powered by DeepSeek-R1</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Main content area
    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{LOGO_BASE64}" style="width: 40px; height: 40px; margin-right: 10px;"/>
            <h1 style="margin: 0; font-size: 2em;">DeepSeek AI File Assistant</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    # File upload section
    uploaded_file = st.file_uploader(
        "Upload document (PDF/DOCX/Image)", 
        type=["pdf", "docx", "png", "jpg", "jpeg"],
        help="Max file size: 200MB"
    )

    if uploaded_file and uploaded_file.size > 200 * 1024 * 1024:

        st.error("File size exceeds 200MB limit")
    
    # Reset processing when new file is uploaded
    if 'current_file' not in st.session_state:
        st.session_state.current_file = None
        
    if uploaded_file and (uploaded_file != st.session_state.current_file):
        st.session_state.processed = False
        st.session_state.current_file = uploaded_file
        st.session_state.file_bytes = None
        st.session_state.variations = []
    
    if uploaded_file and api_key:
        if 'processed' not in st.session_state:
            st.session_state.processed = False
            
        if not st.session_state.processed:
            with st.spinner("🔍 Analyzing document..."):
                file_bytes = uploaded_file.getvalue()
                original_name = uploaded_file.name
                
                text = extract_text(file_bytes, uploaded_file.type)
                if not text:
                    st.error("Failed to process document")
                    return
                    
                analysis = analyze_with_deepseek(api_key, text)
                variations = generate_filename_variations(analysis, original_name)
                
                # Store results in session state
                st.session_state.file_bytes = file_bytes
                st.session_state.variations = variations
                st.session_state.original_type = uploaded_file.type
                st.session_state.processed = True

        # Display suggestions if processing completed
        if st.session_state.processed:
            st.subheader("📝 Naming Suggestions")
            selected_name = st.selectbox(
                "Choose a filename suggestion:",
                options=st.session_state.variations
            )
            
            # Filename editing
            final_name = st.text_input(
                "✏️ Edit filename (if needed):",
                value=selected_name
            )
            
            # Download button
            st.download_button(
                label="Download File",
                data=st.session_state.file_bytes,
                file_name=final_name,
                mime=st.session_state.original_type,
                type="secondary"
            )

if __name__ == "__main__":
    main()