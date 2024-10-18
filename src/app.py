import streamlit as st
from src.api.model_integration import stream_response
from src.utils.prompts_prototype import (
    get_summary_prompt,
    get_draft_prompt,
    get_legal_research_prompt
)
from config.config import Config

def setup_page():
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
    setup_page()

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
            <img src="https://ibb.co/p3B9tG1" alt="Alberdi.AI">
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.sidebar:
    st.title("⚖️ LegalTech App Settings")
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
        template = st.text_area(
            "Template (optional)", 
            "Enter document structure or leave blank for default template", 
            height=100
        )
        clauses = st.text_area(
            "Legal Clauses (optional)", 
            "Enter specific clauses to include, one per line", 
            height=100
        ).splitlines()

    elif task == "Legal Research":
        research_query = st.text_area(
            "Legal Query", 
            "Enter the legal question or area of research", 
            height=100
        )

# Main container with border
main_container = st.container(border=True)

with main_container:
    st.header(f"{task} Task")
    
    if task == "Summarization":
        # Input for the legal document text to summarize
        legal_text = st.text_area(
            "Legal Document Text",
            "Enter the lengthy legal document here...",
            height=300,
        )
        st.caption(f"Character count: {len(legal_text)}")

        if st.button("Summarize", type="primary"):
            if legal_text:
                tab1, tab2, tab3 = st.tabs(
                    ["Key Legal Points", "Decisions and Judgments", "Additional Notes"]
                )

                # Generating summary using the prompt
                summary_prompt = get_summary_prompt(legal_text, case_type, decision_focus)
                summary_result = stream_response(
                    [{"role": "user", "content": summary_prompt}],
                    main_container,
                    model_name,
                )

                # Tab 1: Key Legal Points
                with tab1:
                    st.subheader("Key Legal Points")
                    st.write(summary_result.get("key_points", ""))

                # Tab 2: Decisions and Judgments
                with tab2:
                    st.subheader("Decisions and Judgments")
                    st.write(summary_result.get("decisions", ""))

                # Tab 3: Additional Notes
                with tab3:
                    st.subheader("Additional Notes")
                    st.write(summary_result.get("notes", ""))

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
                draft_result = stream_response(
                    [{"role": "user", "content": draft_prompt}],
                    main_container,
                    model_name,
                )

                # Displaying the generated draft
                st.subheader(f"Draft {document_type}")
                st.write(draft_result)

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
        st.info("This app demonstrates Meta's Llama 3.1 capabilities.")

        st.subheader("Feedback")
        feedback = st.text_area("Leave your feedback here", height=100)
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback!")


if __name__ == "__main__":
    main()