# Prompts prototype
This file contains functions that generate well-structured prompts for interacting with LLaMA 3.2. These prompts guide the model to perform the prototyping tasks: 
- Automatically summarize lengthy legal documents, extracting the most important key points and decisions.
- Generate drafts of legal documents (contracts, agreements, pleadings) from customizable templates, with automatic suggestions of legal clauses.
- Legal Research and Case Law Analysis: Lawyers need to find relevant case law or legal precedents.
The way a prompt is crafted can significantly influence the quality of the model's output.

## Automatically Summarize Lengthy Legal Documents
This function will generate a prompt that instructs the LLaMA model to summarize a legal document by extracting key points, decisions, and other relevant details.

### Arguments:
- case_type: Optional, allowing you to specify the legal domain (e.g., derecho contractual or derecho penal).
- decision_focus: A flag that, when True, adds instructions to focus heavily on court decisions.

## Generate Drafts of Legal Documents
This function generates a customizable prompt that guides the LLaMA model to draft legal documents based on templates, with suggestions for legal clauses.

### Arguments:
- document_type: The type of legal document you are drafting, such as contrato (contract), acuerdo (agreement), or demanda (pleading).
- clauses: A list of legal clauses you want to include in the document, formatted accordingly.
- template: The structure or template of the document, if any, is provided to guide the drafting.

## Legal Research and Case Law Analysis
This function builds a prompt for conducting legal research and retrieving relevant case law or legal precedents, allowing the model to perform deep research tasks.

### Arguments:
- query: Finds and analyzes relevant case law and legal precedents for a given legal query.