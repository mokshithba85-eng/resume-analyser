"""
Script to generate a professional sample resume PDF for testing the Semantic Resume Matcher.
Uses fpdf2 to build a clean document layout.
"""

import os
from fpdf import FPDF


class ResumePDF(FPDF):
    """
    Layout configuration for sample resume PDF.
    """
    def header(self) -> None:
        pass  # Custom header not needed for standard resume layout

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"John Doe - Machine Learning Engineer Resume | Page {self.page_no()}", align="C")


def create_sample_resume(output_path: str) -> None:
    """
    Generates a professional Machine Learning Resume PDF.
    """
    pdf = ResumePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # 1. Contact Info / Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "John Doe")
    pdf.ln(10)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, "Email: john.doe@email.com | Phone: +1-555-0199 | GitHub: github.com/johndoe | Portfolio: johndoe.ai")
    pdf.ln(8)
    
    # Divider line
    pdf.set_draw_color(226, 232, 240)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)
    
    # 2. Professional Summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(0, 6, "Professional Summary")
    pdf.ln(8)
    
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(51, 65, 85)
    summary_text = (
        "Innovative Machine Learning Engineer with 3+ years of experience designing, training, "
        "and deploying generative AI systems and predictive models. Proven track record in optimizing "
        "large language model (LLM) pipelines, implementing Retrieval-Augmented Generation (RAG) structures, "
        "and creating production-ready APIs. Passionate about applying state-of-the-art NLP techniques to "
        "solve complex business challenges and drive operational efficiency."
    )
    pdf.multi_cell(0, 5, summary_text)
    pdf.ln(6)
    
    # 3. Technical Skills
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(0, 6, "Technical Skills")
    pdf.ln(8)
    
    skills = [
        ("Programming Languages", "Python (Expert), SQL, C++, Bash"),
        ("Machine Learning", "PyTorch, TensorFlow, Scikit-Learn, XGBoost"),
        ("Generative AI & NLP", "Hugging Face, LLMs (Gemini, Llama, GPT), LangChain, Vector Databases (Pinecone, ChromaDB), RAG"),
        ("Data Engineering", "Pandas, NumPy, Apache Spark, Kafka"),
        ("Cloud & DevOps", "Docker, Kubernetes, AWS (S3, EC2, SageMaker), Git, CI/CD")
    ]
    
    for category, items in skills:
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(0, 5, f"{category}:")
        pdf.ln(5)
        pdf.set_font("Helvetica", "", 9.5)
        pdf.multi_cell(0, 5, items)
        pdf.ln(2)
    pdf.ln(4)
    
    # 4. Work Experience
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(0, 6, "Work Experience")
    pdf.ln(8)
    
    # Job 1
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 5, "Machine Learning Engineer (June 2024 - Present)")
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 9.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, "Apex Tech Solutions, San Francisco, CA")
    pdf.ln(6)
    
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(51, 65, 85)
    bullet_points_1 = [
        "Architected a Retrieval-Augmented Generation (RAG) system utilizing LangChain, Pinecone, and Gemini 1.5, reducing customer support response time by 45% and achieving 94% response accuracy.",
        "Fine-tuned open-source LLMs (Llama-3, Mistral) using LoRA/QLoRA on proprietary domain datasets, reducing hardware requirements and cutting inference latency by 30%.",
        "Developed and maintained modular ETL pipelines processing over 10M text records daily using Apache Spark and Pandas.",
        "Deployed ML models as high-throughput REST APIs using FastAPI and Docker in AWS Elastic Kubernetes Service (EKS)."
    ]
    for bullet in bullet_points_1:
        pdf.multi_cell(0, 4.5, f"- {bullet}")
        pdf.ln(1)
    pdf.ln(4)

    # Job 2
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 5, "Junior Data Scientist (January 2023 - May 2024)")
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 9.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, "ByteCraft Analytics, Boston, MA")
    pdf.ln(6)
    
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(51, 65, 85)
    bullet_points_2 = [
        "Built and evaluated predictive classification models using Scikit-Learn, XGBoost, and LightGBM to improve customer churn prediction accuracy by 15%.",
        "Designed and conducted A/B testing frameworks for recommendation algorithms, driving a 6.2% lift in user click-through rate.",
        "Created interactive data visualization dashboards using Streamlit and Plotly to communicate ML metrics to executive stakeholders."
    ]
    for bullet in bullet_points_2:
        pdf.multi_cell(0, 4.5, f"- {bullet}")
        pdf.ln(1)
    pdf.ln(6)

    # 5. Projects
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(0, 6, "Projects")
    pdf.ln(8)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 5, "AI-Powered PDF Semantic Analyzer (Personal Project)")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 4.5, (
        "Designed an end-to-end web application that parses PDFs, indexes content in a vector database, "
        "and uses text-embedding-004 and Gemini for similarity scoring and semantic analysis. "
        "Implemented the dashboard interface with Streamlit, yielding a highly responsive user experience."
    ))
    pdf.ln(6)

    # 6. Education
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(0, 6, "Education")
    pdf.ln(8)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 5, "B.S. in Computer Science (Graduated May 2022)")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "University of Massachusetts, Amherst, MA")
    pdf.ln(6)
    
    # Save PDF
    pdf.output(output_path)
    print(f"Sample resume created successfully at: {output_path}")


if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    create_sample_resume("assets/sample_resume.pdf")
