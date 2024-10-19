import streamlit as st
from src.api.model_integration import stream_response
from src.utils.prompts_prototype import (
    get_summary_prompt,
    get_draft_prompt,
    get_legal_research_prompt
)
from config.config import Config

def stp_page():
    """
    Sets up the page with custom styles and page configuration.
    """
    st.set_page_config(
        page_title="Alberdi.AI",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        """
        <style>
        :root {
            --llama-color: #4e8cff;
            --llama-color-light: #e6f0ff;
            --llama-color-dark: #1a3a6c;
            --llama-gradient-start: #4e54c8;
            --llama-gradient-end: #8f94fb;
        }
        .stApp {
            margin: auto;
            background-color: var(--background-color);
            color: var(--text-color);
        }
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 1rem;
        }
        .logo-container img {
            width: 150px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    stp_page()

    st.markdown("""
    <style>
    /* Style for the text area placeholder */
    .custom-textarea .stTextArea textarea::placeholder {
        color: #aaa;
        opacity: 1; /* Fully opaque placeholder */
    }
    /* Style for the text area when user types */
    .custom-textarea .stTextArea textarea:not(:placeholder-shown) {
        color: #000; /* Change text color when typing */
    }
    </style>
    """, unsafe_allow_html=True)

    # Header section with title and subtitle
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 class="header-title">⚖️ Alberdi.AI - LegalTech app for legal tasks </h1>
            <p class="header-subtitle"Summarizes, drafts, researches. Easy-to-use tools for lawyers.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Alberdi.AI logo
    st.markdown(
        """
        <div class="logo-container">
            <img src="https://i.ibb.co/Zhpkntf/DALL-E-2024-10-18-16-26-53-A-futuristic-portrayal-of-Juan-Bautista-Alberdi-blending-his-19th-century.webp" alt="Alberdi.AI">
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.title("🔧 Choose AI Model and Task")
        model_name = st.selectbox("Choose a model", Config.AVAILABLE_MODELS)

        # User selects which function to use: Summarization, Drafting, or Legal Research
        task = st.selectbox("Choose Task", ["Summarization", "Drafting", "Legal Research"])

        # Additional options based on task selection
        if task == "Summarization":
            case_type = st.selectbox(
                "Case Type (optional)", 
                ["Contract Law", "Criminal Law", "Family Law", "Corporate Law", "Other"]
            )
            decision_focus = st.checkbox("Focus on Court Decisions?", value=False)

        elif task == "Drafting":
            document_type = st.selectbox(
                "Document Type", ["Contract", "Agreement", "Pleading", "Other"]
            )

            st.markdown('<div class="custom-textarea">', unsafe_allow_html=True)
            template = st.text_area(
                "Template (optional)", 
                placeholder="Enter document structure or leave blank for default template", 
                height=100
            )
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="custom-textarea">', unsafe_allow_html=True)
            clauses = st.text_area(
                "Legal Clauses (optional)", 
                placeholder="Enter specific clauses to include, one per line", 
                height=100
            ).splitlines()
            st.markdown('</div>', unsafe_allow_html=True)

        elif task == "Legal Research":
            st.markdown('<div class="custom-textarea">', unsafe_allow_html=True)
            research_query = st.text_area(
                "Legal Query", 
                "Enter the legal question or area of research", 
                height=100
            )
            st.markdown('</div>', unsafe_allow_html=True)

    # Main container with border
    main_container = st.container(border=True)
    
    with main_container:
        st.header(f"{task} Task")
        
        if task == "Summarization":
            # Input for the legal document text to summarize
            st.markdown('<div class="custom-textarea">', unsafe_allow_html=True)
            legal_text = st.text_area(
                "Legal Document Text",
                placeholder="Enter the lengthy legal document here...",
                height=300,
            )
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption(f"Character count: {len(legal_text)}")
    
            if st.button("Summarize", type="primary"):
                if legal_text:    
                    
                    # Generating summary using the prompt
                    summary_prompt = get_summary_prompt(legal_text, case_type, decision_focus)
                    stream_response(
                        [{"role": "user", "content": summary_prompt}],
                        main_container,
                        model_name,
                    )


        elif task == "Drafting":
            # Input for creating a draft legal document
            st.text_area(
                "Input Document Details", 
                f"Prepare a {document_type} with customizable clauses", 
                height=300
            )
            if st.button("Generate Draft", type="primary"):
                if document_type:
                    draft_prompt = get_draft_prompt(document_type, clauses, template)
                    stream_response(
                        [{"role": "user", "content": draft_prompt}],
                        main_container,
                        model_name,
                    )

        elif task == "Legal Research":
            # Input for legal research query
            if st.button("Conduct Research", type="primary"):
                if research_query:
                    research_prompt = get_legal_research_prompt(research_query)
                    research_result = stream_response(
                        [{"role": "user", "content": research_prompt}],
                        main_container,
                        model_name,
                    )
    
                    tab1, tab2, tab3 = st.tabs(
                        ["Relevant Case Law", "Precedent Analysis", "Conclusions"]
                    )
    
                    # Tab 1: Relevant Case Law
                    with tab1:
                        st.subheader("Relevant Case Law")
                        st.write(research_result.get("case_law", ""))
    
                    # Tab 2: Precedent Analysis
                    with tab2:
                        st.subheader("Precedent Analysis")
                        st.write(research_result.get("precedents", ""))
    
                    # Tab 3: Conclusions
                    with tab3:
                        st.subheader("Conclusions")
                        st.write(research_result.get("conclusions", ""))
    
        # Sidebar for additional information and feedback
        with st.sidebar:
            st.subheader("About")
            st.info("This prototype demonstrates Meta's Llama 3.2 capabilities for Edge Runners 3.2 | Lablab.ai.")
    
            st.subheader("Feedback")
            feedback = st.text_area("Leave your feedback here", height=100)
            if st.button("Submit Feedback"):
                st.success("Thank you for your feedback!")


if __name__ == "__main__":
    main()