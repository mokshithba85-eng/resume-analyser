
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from services.analysis_service import AnalysisService
from utils.pdf_parser import extract_text_from_pdf
from utils.report_generator import generate_pdf_report
from utils.helper import validate_file_extension, validate_file_size

# Set up page configurations
st.set_page_config(
    page_title="Semantic Resume Matcher - AI Analysis System",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium UI Styling using Custom CSS
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
    }

    .section-subheader {
        font-size: 1.15rem;
        font-weight: 600;
        color: #4F46E5;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_skill_badges(skills: list, theme: str = "success") -> None:
  
    if not skills:
        st.write("*No specific skills highlighted in this category.*")
        return

   
    if theme == "success":
        bg = "#DCFCE7"       # Soft green
        text = "#166534"     # Dark green
        border = "#BBF7D0"   # Light green border
    else:
        bg = "#FEE2E2"       # Soft red
        text = "#991B1B"     # Dark red
        border = "#FCA5A5"   # Light red border

    badges_html = ""
    for skill in skills:
        badges_html += f"""
        <span style="
            display: inline-block;
            background-color: {bg};
            color: {text};
            border: 1px solid {border};
            padding: 5px 12px;
            margin: 4px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        ">{skill}</span>
        """
    st.markdown(
        f'<div style="margin-bottom: 1rem;">{badges_html}</div>',
        unsafe_allow_html=True
    )


def initialize_app() -> None:
  
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None

 
    header_html = """
    <div style="
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%);
        padding: 2.2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.4);
    ">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800; letter-spacing: -0.03em;">Semantic Resume Matcher</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.92; font-size: 1.1rem; font-weight: 400; letter-spacing: 0.01em;">
            AI-Powered Resume Analysis & Job Description Gap Assessor
        </p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def main() -> None:
  
    initialize_app()

   
    env_api_key = os.getenv("GEMINI_API_KEY", "")

   
    st.sidebar.markdown("### ⚙️ Control Panel")
    
   
    api_key_input = st.sidebar.text_input(
        "Google Gemini API Key",
        value=env_api_key,
        type="password",
        help="Input your Gemini API Key. Get one from Google AI Studio. If set in .env, this loads automatically."
    )

    st.sidebar.divider()

    # Upload Resume
    uploaded_file = st.sidebar.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
        help="Upload candidate resume in PDF format. Limit: 10MB."
    )

    # Job Description Input
    job_description = st.sidebar.text_area(
        "Target Job Description",
        height=250,
        placeholder="Paste the target job description requirements here...",
        help="Copy-paste the complete Job Description text here."
    )

    analyze_button = st.sidebar.button(
        "🚀 Run Semantic Matcher",
        use_container_width=True,
        type="primary"
    )

    st.sidebar.markdown(
        """
        <div style="font-size: 0.8rem; color: #94A3B8; text-align: center; margin-top: 2rem;">
            Semantic Resume Matcher v1.0.0<br/>
            Engineered with Gemini 2.5 & text-embedding-004
        </div>
        """,
        unsafe_allow_html=True
    )

    # Logic when button is clicked
    if analyze_button:
        # Input Validation
        if not api_key_input:
            st.error("⚠️ API Key Missing! Please provide a Google Gemini API Key in the sidebar or via .env configuration.")
            return
        
        if not uploaded_file:
            st.error("⚠️ Resume File Missing! Please upload a candidate resume PDF in the sidebar.")
            return

        if not job_description.strip():
            st.error("⚠️ Job Description Missing! Please paste the job description text in the sidebar.")
            return

        # File integrity validations
        if not validate_file_extension(uploaded_file.name):
            st.error("⚠️ Invalid File Format! Only PDF files are supported.")
            return
        
        # Check size (10MB limit)
        if not validate_file_size(uploaded_file.size, max_size_mb=10.0):
            st.error("⚠️ File Too Large! Uploaded PDF exceeds the 10MB limit.")
            return

        # Pipeline execution
        try:
            # Custom spinner messages representing different components
            with st.spinner("⏳ Extracting text from resume PDF..."):
                resume_text = extract_text_from_pdf(uploaded_file)

            with st.spinner("🧠 Generating embeddings and performing semantic analysis..."):
                # Initialize analysis service with user provided key
                analysis_service = AnalysisService(api_key=api_key_input)
                cosine_score, analysis_data = analysis_service.run_analysis(resume_text, job_description)

            # Store in session state
            st.session_state.analysis_results = {
                "cosine_score": cosine_score,
                "analysis_data": analysis_data,
                "resume_text": resume_text,
                "job_description": job_description
            }
            st.toast("✅ Analysis completed successfully!", icon="🎉")

        except Exception as e:
            st.error(f"❌ Analysis Failed: {str(e)}")
            st.info("💡 Please verify that your Gemini API key is valid and has access to 'gemini-2.5-flash' and 'text-embedding-004'.")

  
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        cosine_score = results["cosine_score"]
        analysis_data = results["analysis_data"]

      
        st.markdown("### 📊 Matching Metrics")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #E2E8F0; text-align: center;">
                    <div style="font-size: 0.9rem; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">
                        Semantic Match Score (Embeddings)
                    </div>
                    <div style="font-size: 3rem; font-weight: 800; color: #4F46E5; margin: 0.5rem 0;">
                        {cosine_score:.1f}%
                    </div>
                    <div style="font-size: 0.85rem; color: #94A3B8;">
                        Mathematical similarity calculation via text-embedding-004
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
          
            st.progress(min(max(cosine_score / 100.0, 0.0), 1.0))

        with col2:
            qualitative_score = analysis_data.get("match_score", 0)
            st.markdown(
                f"""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #E2E8F0; text-align: center;">
                    <div style="font-size: 0.9rem; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">
                        AI Qualitative Score (Gemini)
                    </div>
                    <div style="font-size: 3rem; font-weight: 800; color: #7C3AED; margin: 0.5rem 0;">
                        {qualitative_score}%
                    </div>
                    <div style="font-size: 0.85rem; color: #94A3B8;">
                        Cognitive appraisal of suitability, projects, and domain depth
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
           
            st.progress(min(max(qualitative_score / 100.0, 0.0), 1.0))

        st.divider()

       
        st.markdown("### 🧩 Skills Alignment Check")
        col_skills_1, col_skills_2 = st.columns(2)

        with col_skills_1:
            st.markdown('<p class="section-subheader">✅ Matched Skills</p>', unsafe_allow_html=True)
            render_skill_badges(analysis_data.get("matched_skills", []), theme="success")

        with col_skills_2:
            st.markdown('<p class="section-subheader">❌ Missing Skills</p>', unsafe_allow_html=True)
            render_skill_badges(analysis_data.get("missing_skills", []), theme="danger")

        st.divider()

      
        st.markdown("### 🔍 Evaluation Profile")
        col_eval_1, col_eval_2 = st.columns(2)

        with col_eval_1:
            st.markdown('<p class="section-subheader">💪 Key Strengths</p>', unsafe_allow_html=True)
            strengths = analysis_data.get("strengths", [])
            if strengths:
                for strength in strengths:
                    st.success(strength)
            else:
                st.write("No distinct strengths highlighted.")

        with col_eval_2:
            st.markdown('<p class="section-subheader">⚠️ Identified Gaps</p>', unsafe_allow_html=True)
            weaknesses = analysis_data.get("weaknesses", [])
            if weaknesses:
                for weakness in weaknesses:
                    st.warning(weakness)
            else:
                st.write("No significant experience gaps identified.")

        st.divider()

        # --- ROW 4: ACTIONABLE SECTIONS (EXPANDERS / TABS) ---
        st.markdown("### 🛠️ Optimization & Career Guidance")
        
        tab_improvements, tab_questions, tab_courses = st.tabs([
            "📝 Resume Improvement Suggestions",
            "💬 Custom Interview Questions",
            "🎓 Recommended Learning Path"
        ])

        with tab_improvements:
            improvements = analysis_data.get("resume_improvements", [])
            if improvements:
                for item in improvements:
                    st.markdown(f"- **Improvement:** {item}")
            else:
                st.write("Your resume is well-tailored for this role!")

        with tab_questions:
            questions = analysis_data.get("interview_questions", [])
            if questions:
                for idx, q in enumerate(questions, 1):
                    st.info(f"**Q{idx}:** {q}")
            else:
                st.write("No interview questions generated.")

        with tab_courses:
            courses = analysis_data.get("recommended_courses", [])
            if courses:
                for course in courses:
                    st.markdown(f"- 🎓 {course}")
            else:
                st.write("No specific upgrade paths recommended.")

        st.divider()

      
        st.markdown("### 📥 Document Exports")
        try:
            pdf_bytes = generate_pdf_report(analysis_data, cosine_score)
            
            # Center the download button
            _, dl_col, _ = st.columns([1, 2, 1])
            with dl_col:
                st.download_button(
                    label="📥 Download Detailed PDF Evaluation Report",
                    data=pdf_bytes,
                    file_name="resume_evaluation_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        except Exception as pdf_err:
            st.error(f"Could not generate PDF download block: {str(pdf_err)}")

    else:
        # Default Welcome State
        st.info("👈 Use the **Control Panel** in the sidebar to enter your Gemini API Key, upload your PDF resume, paste the target Job Description, and hit **Run Semantic Matcher**!")
        
        # Project Overview Cards
        st.markdown("### ℹ️ How it Works")
        col_info_1, col_info_2, col_info_3 = st.columns(3)
        
        with col_info_1:
            st.markdown(
                """
                <div style="background: #F8FAFC; padding: 1.5rem; border-radius: 12px; border: 1px solid #E2E8F0; min-height: 200px;">
                    <h4 style="color: #4F46E5; margin-top: 0;">1. Text Parsing</h4>
                    <p style="font-size: 0.9rem; color: #475569;">
                        We parse text from your uploaded PDF resume using <code>pdfplumber</code> and perform cleaning to remove control artifacts while preserving semantic structure.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col_info_2:
            st.markdown(
                """
                <div style="background: #F8FAFC; padding: 1.5rem; border-radius: 12px; border: 1px solid #E2E8F0; min-height: 200px;">
                    <h4 style="color: #7C3AED; margin-top: 0;">2. Semantic Embeddings</h4>
                    <p style="font-size: 0.9rem; color: #475569;">
                        Instead of simple keyword counts, we use Gemini's <code>text-embedding-004</code> to map the semantic content of your resume and target JD into dense vectors.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col_info_3:
            st.markdown(
                """
                <div style="background: #F8FAFC; padding: 1.5rem; border-radius: 12px; border: 1px solid #E2E8F0; min-height: 200px;">
                    <h4 style="color: #DB2777; margin-top: 0;">3. LLM Gap Assessment</h4>
                    <p style="font-size: 0.9rem; color: #475569;">
                        Gemini 2.5 Flash analyzes alignment qualities, detects missing capabilities, generates interview prompts, and offers precise optimization suggestions in structured JSON.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


if __name__ == "__main__":
    main()
