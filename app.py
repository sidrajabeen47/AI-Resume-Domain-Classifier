# import os
# import streamlit as st
# from PyPDF2 import PdfReader
# from google import genai
# from google.genai import types
# from pydantic import BaseModel, Field

# # Ensure API Key is configured
# if "GEMINI_API_KEY" not in os.environ:
#     st.error("Missing API Key! Please set the GEMINI_API_KEY environment variable.")
#     st.stop()

# # ==========================================
# # 1. DEFINE STRUCTURED OUTPUT SCHEMAS
# # ==========================================
# class DomainEligibility(BaseModel):
#     domain: str = Field(description="The engineering or IT domain name (e.g., Java, Python, Cybersecurity, Embedded, etc.)")
#     eligibility_score: int = Field(description="Score from 0 to 100 based strictly on matching skills/projects")
#     matching_skills_found: list[str] = Field(description="List of skills or keywords found in the CV matching this domain")
#     missing_prerequisites: list[str] = Field(description="List of core skills missing for this specific domain")

# class EligibilityReport(BaseModel):
#     candidate_name: str = Field(description="Extracted name of the candidate")
#     primary_eligible_domain: str = Field(description="The single domain with the absolute highest eligibility score")
#     all_domains_analysis: list[DomainEligibility]

# # ==========================================
# # 2. CORE PROCESSING LOGIC FUNCTIONS
# # ==========================================
# def extract_text_from_pdf(uploaded_file) -> str:
#     """Extracts raw text from an uploaded PDF using PyPDF2."""
#     pdf_reader = PdfReader(uploaded_file)
#     extracted_text = ""
#     for page in pdf_reader.pages:
#         text = page.extract_text()
#         if text:
#             extracted_text += text + "\n"
#     return extracted_text

# def analyze_resume_eligibility(cv_text: str) -> EligibilityReport:
#     """Sends CV text to Gemini 2.5 Flash and forces a structured schema output."""
#     client = genai.Client()
    
#     system_instruction = """
#     You are an expert IT and Engineering academic advisor and technical recruiter. 
#     Your objective is to analyze the text of a candidate's CV and calculate a strict eligibility percentage (0-100) 
#     for these exact domains: 
#     - Java Domain
#     - Python Domain
#     - Azure Cloud
#     - Cybersecurity
#     - EEE/Embedded Systems
#     - Robotics
#     - ECE (VLSI/Signal Processing)
#     - Mechanical Engineering
    
#     Be objective. If a candidate completely lacks physical hardware, microcontroller, or robotics skills, 
#     their Robotics/Embedded scores must be near zero. Prioritize actual projects and concrete skill declarations over vague summaries.
#     """

#     response = client.models.generate_content(
#         model='gemini-2.5-flash',
#         contents=f"Analyze this parsed CV text and return the complete routing profile:\n\n{cv_text}",
#         config=types.GenerateContentConfig(
#             system_instruction=system_instruction,
#             response_mime_type="application/json",
#             response_schema=EligibilityReport,
#             temperature=0.1,  # Low temperature guarantees consistent, analytical sorting instead of creative parsing
#         ),
#     )
#     # The SDK automatically validates and returns data parsing into our Pydantic Object
#     return EligibilityReport.model_validate_json(response.text)

# # ==========================================
# # 3. STREAMLIT USER INTERFACE (UI)
# # ==========================================
# st.set_page_config(page_title="AI Profile Router", page_icon="🤖", layout="wide")

# st.title("🤖 AI-Driven Profile Router & Domain Classifier")
# st.markdown("Upload an engineering or tech CV in PDF format. The system parses structural context, measures skill densities, and benchmarks eligibility across 8 distinct professional domains.")

# # Sidebar File Ingestion File uploader
# with st.sidebar:
#     st.header("Upload Document")
#     uploaded_file = st.file_uploader("Drop CV PDF here", type=["pdf"])
#     st.info("Supported formats: PDF. Text extraction handles structural elements natively.")

# # Main Application Window Processing Trigger
# if uploaded_file is not None:
#     st.success(f"Successfully loaded: **{uploaded_file.name}**")
    
#     if st.button("Analyze Profile & Run Eligibility Check", type="primary"):
#         with st.status("Processing Pipeline Running...", expanded=True) as status:
            
#             st.write("Extracting unstructured raw text via PyPDF2...")
#             cv_text = extract_text_from_pdf(uploaded_file)
            
#             if not cv_text.strip():
#                 status.update(label="Extraction Failed", state="error")
#                 st.error("Could not extract any structural text from this PDF. Please check if it's an image-only scan.")
#                 st.stop()
                
#             st.write("Analyzing core matching tokens via Gemini Engine...")
#             try:
#                 report = analyze_resume_eligibility(cv_text)
#                 status.update(label="Analysis Finished Successfully!", state="complete", expanded=False)
#             except Exception as e:
#                 status.update(label="AI Analysis Pipeline Failed", state="error")
#                 st.error(f"Error calling API or parsing schema: {e}")
#                 st.stop()

#         # ==========================================
#         # 4. RENDERING METRICS & ANALYTICS VISUALS
#         # ==========================================
#         st.write("---")
#         st.subheader(f"Analysis Report for: **{report.candidate_name}**")
        
#         # Display Primary Match Banner
#         st.info(f"🎯 **Primary Domain Recommendation:** Your background aligns strongest with **{report.primary_eligible_domain}**.")
        
#         st.write("### Domain Eligibility Breakdown")
        
#         # Sort domains dynamically by high-to-low match score
#         sorted_domains = sorted(report.all_domains_analysis, key=lambda x: x.eligibility_score, reverse=True)
        
#         for element in sorted_domains:
#             # Layout alignment columns
#             col1, col2 = st.columns([1, 3])
            
#             with col1:
#                 st.markdown(f"**{element.domain}**")
#                 st.metric(label="Match Quality", value=f"{element.eligibility_score}%")
            
#             with col2:
#                 # Progress Bar rendering
#                 st.progress(element.eligibility_score / 100)
                
#                 # Expandable tabs showcasing parsed keyword mappings
#                 with st.expander("View Identified Skill Sets & Gaps"):
#                     sub_col_left, sub_col_right = st.columns(2)
#                     with sub_col_left:
#                         st.markdown("**Matched Skills/Keywords Found:**")
#                         if element.matching_skills_found:
#                             for skill in element.matching_skills_found:
#                                 st.markdown(f"✅ *{skill}*")
#                         else:
#                             st.caption("No strong keyword matches identified.")
                            
#                     with sub_col_right:
#                         st.markdown("**Missing Prerequisites / Skill Gaps:**")
#                         if element.missing_prerequisites:
#                             for gap in element.missing_prerequisites:
#                                 st.markdown(f"❌ *{gap}*")
#                         else:
#                             st.caption("No critical domain gaps found!")
#             st.markdown("---")
# else:
#     st.info("Awaiting CV placement. Drag and drop a corporate or academic PDF in the sidebar to run routing diagnostics.")




import os
import streamlit as st
from PyPDF2 import PdfReader
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# Ensure API Key is configured
if "GEMINI_API_KEY" not in os.environ:
    st.error("Missing API Key! Please set the GEMINI_API_KEY environment variable.")
    st.stop()

# ==========================================
# 1. DEFINE STRUCTURED OUTPUT SCHEMAS (UPDATED)
# ==========================================
class DomainEligibility(BaseModel):
    domain: str = Field(description="The engineering or IT domain name (e.g., Java, Python, Cybersecurity, Embedded, etc.)")
    eligibility_score: int = Field(description="Score from 0 to 100 based strictly on matching skills/projects")
    matching_skills_found: list[str] = Field(description="List of skills or keywords found in the CV matching this domain")
    missing_prerequisites: list[str] = Field(description="List of core skills missing for this specific domain")
    # NEW FIELD: Dynamically generated roadmap/syllabus if their score is less than 85%
    recommended_syllabus: list[str] = Field(
        description="A step-by-step custom syllabus/topics list to study to become 100% eligible for this domain. Leave empty if score is 95+."
    )

class EligibilityReport(BaseModel):
    candidate_name: str = Field(description="Extracted name of the candidate")
    primary_eligible_domain: str = Field(description="The single domain with the absolute highest eligibility score")
    all_domains_analysis: list[DomainEligibility]

# ==========================================
# 2. CORE PROCESSING LOGIC FUNCTIONS
# ==========================================
def extract_text_from_pdf(uploaded_file) -> str:
    """Extracts raw text from an uploaded PDF using PyPDF2."""
    pdf_reader = PdfReader(uploaded_file)
    extracted_text = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"
    return extracted_text

def analyze_resume_eligibility(cv_text: str) -> EligibilityReport:
    """Sends CV text to Gemini 2.5 Flash and forces a structured schema output."""
    client = genai.Client()
    
    system_instruction = """
    You are an expert IT and Engineering academic advisor and technical recruiter. 
    Your objective is to analyze the text of a candidate's CV and calculate a strict eligibility percentage (0-100) 
    for these exact domains: 
    - Java Domain
    - Python Domain
    - Azure Cloud
    - Cybersecurity
    - EEE/Embedded Systems
    - Robotics
    - ECE (VLSI/Signal Processing)
    - Mechanical Engineering
    
    CRITICAL INSTRUCTION FOR UP-SKILLING SYLLABUS:
    For any domain where the candidate's score is less than 90%, you must generate a highly detailed, 
    step-by-step training syllabus in the 'recommended_syllabus' field. 
    The syllabus should act as a bridge, telling the candidate exactly what subjects, languages, frameworks, 
    or modules they need to learn to change fields or qualify for that specific domain.
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Analyze this parsed CV text and return the complete routing profile with study syllabi:\n\n{cv_text}",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=EligibilityReport,
            temperature=0.1,  
        ),
    )
    return EligibilityReport.model_validate_json(response.text)

# ==========================================
# 3. STREAMLIT USER INTERFACE (UI)
# ==========================================
st.set_page_config(page_title="AI Profile Router & Coach", page_icon="🤖", layout="wide")

st.title("🤖 AI Profile Router & Career Coach")
st.markdown("Upload a CV in PDF format. The system analyzes eligibility across 8 core domains and provides **personalized study syllabi** to bridge your skill gaps.")

# Sidebar File Ingestion
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Drop CV PDF here", type=["pdf"])
    st.info("Supported formats: PDF.")

# Main Application Window Processing Trigger
if uploaded_file is not None:
    st.success(f"Successfully loaded: **{uploaded_file.name}**")
    
    if st.button("Analyze Profile & Generate Study Plans", type="primary"):
        with st.status("Processing Pipeline Running...", expanded=True) as status:
            
            st.write("Extracting unstructured raw text via PyPDF2...")
            cv_text = extract_text_from_pdf(uploaded_file)
            
            if not cv_text.strip():
                status.update(label="Extraction Failed", state="error")
                st.error("Could not extract any structural text from this PDF.")
                st.stop()
                
            st.write("Analyzing competencies and generating customized bridge syllabi...")
            try:
                report = analyze_resume_eligibility(cv_text)
                status.update(label="Analysis & Syllabus Generation Finished!", state="complete", expanded=False)
            except Exception as e:
                status.update(label="AI Analysis Pipeline Failed", state="error")
                st.error(f"Error calling API or parsing schema: {e}")
                st.stop()

        # ==========================================
        # 4. RENDERING METRICS, VISUALS & SYLLABI
        # ==========================================
        st.write("---")
        st.subheader(f"Analysis Report for: **{report.candidate_name}**")
        
        st.info(f"🎯 **Primary Domain Match:** Your background currently aligns strongest with **{report.primary_eligible_domain}**.")
        
        st.write("### 📊 Domain Eligibility & Custom Study Roadmaps")
        
        # Sort domains dynamically by high-to-low match score
        sorted_domains = sorted(report.all_domains_analysis, key=lambda x: x.eligibility_score, reverse=True)
        
        for element in sorted_domains:
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown(f"#### {element.domain}")
                st.metric(label="Current Match", value=f"{element.eligibility_score}%")
            
            with col2:
                st.progress(element.eligibility_score / 100)
                
                # Expandable tabs showcasing parsed keyword mappings AND the new syllabus feature
                with st.expander(f"View Skill Matching & Educational Bridge Syllabus for {element.domain}"):
                    sub_col_left, sub_col_right = st.columns(2)
                    
                    with sub_col_left:
                        st.markdown("**🔍 Found Skills:**")
                        if element.matching_skills_found:
                            for skill in element.matching_skills_found:
                                st.markdown(f"✅ *{skill}*")
                        else:
                            st.caption("No matching skills found in your CV.")
                            
                        st.markdown("**⚠️ Missing Prerequisites:**")
                        if element.missing_prerequisites:
                            for gap in element.missing_prerequisites:
                                st.markdown(f"❌ *{gap}*")
                        else:
                            st.caption("No major gaps identified!")
                            
                    with sub_col_right:
                        st.markdown("### 📚 Target Study Syllabus")
                        st.markdown("*Learn these topics to bridge the gap and become completely eligible for this domain:*")
                        
                        # Check if a custom syllabus was generated for lower scores
                        if element.recommended_syllabus:
                            for index, topic in enumerate(element.recommended_syllabus, 1):
                                st.markdown(f"**Step {index}:** {topic}")
                        else:
                            st.success("🎉 Excellent! Your current profile is already fully optimized for this domain. No bridge syllabus required.")
                            
            st.markdown("---")
else:
    st.info("Awaiting CV placement. Drag and drop a corporate or academic PDF in the sidebar to run routing diagnostics.")