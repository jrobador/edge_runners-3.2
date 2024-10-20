# edge_runners-3.2
Project for Edge Runners 3.2 Hackaton


## High-Level Overview of the Project
Model: 
- Meta-Llama-3.2-90B-Vision-Instruct-Turbo for remotely server purpose.
- Llama3.2 3B parameters for locally running.

Prototype capabilities:
1. Automatically summarize lengthy legal documents, extracting the most important key points and decisions.
2. Generate drafts of legal documents (contracts, agreements, pleadings) from customizable templates, with automatic suggestions of legal clauses
3. Legal Research and Case Law Analysis: Lawyers need to find relevant case law or legal precedents.


# Alberdi.AI - LegalTech AI-Powered Assistant

Alberdi.AI is an advanced LegalTech application designed to help lawyers and legal professionals with various legal tasks. By leveraging AI models, it offers tools for document summarization, legal drafting, and legal research. This app streamlines complex legal processes, making it an invaluable tool for law firms and individual practitioners alike.

## **Functionalities:**

### 1. **Summarization**
   - **Description:** Allows users to input lengthy legal documents and receive concise summaries.
   - **Features:**
     - Summarizes complex legal texts in seconds.
     - Optional focus on specific case types like Contract Law, Criminal Law, Family Law, and more.
     - Customizable to include court decisions in the summary.
   - **Usage Example:**
     - Input a contract or legal case document and choose the focus for the summary.
     - Click "Summarize" to generate a brief overview of the legal document.

### 2. **Drafting**
   - **Description:** Enables the drafting of legal documents such as contracts and agreements with customizable clauses.
   - **Features:**
     - Supports multiple document types (Contracts, Agreements, Pleadings, etc.).
     - Option to enter a document template or use a default structure.
     - Ability to include specific legal clauses tailored to the user's needs.
   - **Usage Example:**
     - Select a document type (e.g., Contract) and input specific clauses to be included.
     - Click "Generate Draft" to create a tailored legal document.

### 3. **Legal Research**
   - **Description:** Provides AI-powered legal research tools to analyze legal queries and return relevant case law, precedent analysis, and conclusions.
   - **Features:**
     - Conducts thorough research on specific legal questions or topics.
     - Presents findings in a structured format with case law, precedent analysis, and conclusions.
     - Ideal for quickly gathering relevant legal information.
   - **Usage Example:**
     - Enter a legal research query and click "Conduct Research" to generate a report of relevant cases and analyses.

### 4. **Multimodal Input and Interface**
   - **Description:** Offers an intuitive, user-friendly interface with support for text input areas, dropdowns, and checkboxes for customizing tasks.
   - **Features:**
     - Clean and responsive design for ease of use.
     - Sidebar menu for selecting AI models and tasks.
     - Tabs for detailed results in legal research (Case Law, Precedent Analysis, Conclusions).
     - Supports real-time feedback submission from users.

## **Market Value:**

- **Efficiency and Time Savings:** Alberdi.AI can save legal professionals hours of manual work, providing quick access to summarized legal information, draft documents, and in-depth research.
- **Cost-Effective Solution:** Law firms and individuals can reduce legal research and drafting costs by relying on AI-powered tools.
- **Global Accessibility:** With its multilingual support, Alberdi.AI can be used by legal professionals across the world, regardless of language barriers.
- **Niche Market:** LegalTech is an evolving field, and AI-driven solutions like Alberdi.AI are gaining traction for their ability to streamline repetitive legal tasks.
- **Scalability:** The project can easily scale to integrate new AI models, expand document types, or add additional legal tasks, making it a flexible solution in the legal industry.

## **How to Implement This Project:**

1. **Install Dependencies:**
   - Install necessary Python packages, including `streamlit`, AI model libraries, and any other dependencies for the project.
   - Set up a Python environment and ensure all required libraries are properly installed.
   ```bash
   pip install streamlit
   pip install openai
