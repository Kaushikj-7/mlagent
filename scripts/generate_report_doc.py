# scripts/generate_report_doc.py
import os

report_content = """# RESEARCHPILOT AI: AN AGENTIC MULTI-AGENT WORKFLOW FOR ACADEMIC RESEARCH ANALYSIS

---

**Academic Year**: 2026–2027  
**Department**: Department of Artificial Intelligence & Machine Learning (Dept. of AI & ML)  
**Institution**: BNM Institute of Technology (BNMIT)  
**Program**: Bachelor of Engineering (B.E.) in Artificial Intelligence & Machine Learning  

---

## TABLE OF CONTENTS

| Sl. No. | Contents | Page No. |
| :---: | :--- | :---: |
| — | **Abstract** | 1 |
| **1** | **Introduction** | 2 |
| | 1.1 Problem Statement | 2 |
| | 1.2 Objectives | 3 |
| | 1.3 Scope | 3 |
| **2** | **Literature Review** | 4 |
| **3** | **Mapping to United Nations Sustainable Development Goals** | 5 |
| | 3.1 SDG 4 – Quality Education | 5 |
| | 3.2 SDG 9 – Industry, Innovation and Infrastructure | 5 |
| | 3.3 SDG 16 – Peace, Justice and Strong Institutions | 6 |
| | 3.4 SDG 17 – Partnerships for the Goals | 6 |
| **4** | **Methodology** | 7 |
| | 4.1 Technology Stack Used | 7 |
| | 4.2 Multi-Agent Components and Their Responsibilities | 8 |
| | 4.3 User Authentication | 8 |
| | 4.4 PDF Upload and Document Processing | 8 |
| | 4.5 Planner Agent | 9 |
| | 4.6 ChromaDB-Based Semantic Storage | 9 |
| | 4.7 Retriever Agent | 9 |
| | 4.8 Summarizer Agent | 9 |
| | 4.9 Gap Analyzer Agent | 10 |
| | 4.10 AI Research Assistant | 10 |
| | 4.11 Report Generation | 10 |
| | 4.12 Research History | 10 |
| **5** | **Results** | 11 |
| | 5.1 ResearchPilot AI Login Interface | 11 |
| | 5.2 ResearchPilot AI Dashboard and Agent Pipeline | 12 |
| | 5.3 AI Research Assistant Interface | 13 |
| | 5.4 Deep Research Analysis Interface | 13 |
| | 5.5 Paper Summary | 14 |
| | 5.6 Generated Research Report | 15 |
| | 5.7 Research Papers History | 15 |
| | 5.8 Functional Testing and Observed Results | 16 |
| **6** | **Discussion** | 17 |
| | 6.1 Advantages of the Proposed System | 17 |
| | 6.2 Limitations | 18 |
| | 6.3 Future Scope | 19 |
| **7** | **Conclusion** | 20 |
| — | **References / Bibliography** | 21 |

---

## LIST OF FIGURES

| Figure No. | Contents | Page No. |
| :---: | :--- | :---: |
| **Figure 5.1** | ResearchPilot AI Login Interface | 11 |
| **Figure 5.2** | ResearchPilot AI Dashboard and Agent Pipeline | 12 |
| **Figure 5.3** | AI Research Assistant Interface | 13 |
| **Figure 5.4** | Deep Research Analysis Interface | 13 |
| **Figure 5.5** | AI-Generated Paper Summary | 14 |
| **Figure 5.6** | Generated Research Report | 15 |
| **Figure 5.7** | Research Papers History | 15 |

---

## LIST OF TABLES

| Table No. | Contents | Page No. |
| :---: | :--- | :---: |
| **Table 3.1** | Sustainable Development Goals and Their Mapping to ResearchPilot AI | 5 |
| **Table 4.1** | Technology Stack Used | 7 |
| **Table 4.2** | Multi-Agent Components and Their Responsibilities | 8 |
| **Table 5.1** | Functional Testing and Observed Results | 16 |

---

## ABSTRACT

Research work requires researchers and students to read large numbers of papers, understand their methodologies, identify important findings, compare existing approaches, and determine possible research gaps. This process is often time-consuming because relevant information is distributed across different sections of research papers and users must manually extract and organize it. Traditional document-reading approaches also provide limited support for interactive questioning, structured analysis, and automated report generation.

**ResearchPilot AI** is an AI-powered research assistant designed to simplify and automate the analysis of research papers. The system allows users to upload a PDF research paper and process it through a multi-agent artificial intelligence pipeline. The implemented pipeline consists of specialized components including a Planner, PDF Reader, ChromaDB-based vector storage, Retriever, Summarizer, Gap Analyzer, and Report Generator. Each component performs a specific task while contributing to the overall research-analysis workflow.

The system uses a modern full-stack architecture with a React and Vite frontend, Tailwind CSS for interface styling, FastAPI for backend services, LangChain and LangGraph for AI workflow orchestration, ChromaDB for vector-based document retrieval, and Mistral AI for natural-language generation and reasoning. The uploaded document is processed into searchable information, allowing the system to generate structured summaries, research gaps, improvements, future work, novel ideas, and comprehensive research reports.

ResearchPilot AI also provides an interactive AI Research Assistant through which users can ask questions about an uploaded paper. The system includes predefined questions related to methodology, datasets, limitations, conclusions, and future work. The generated report can be copied or exported in Markdown, PDF, and DOCX formats. A research-history module allows users to revisit previously analyzed papers. The project demonstrates how agentic AI and retrieval-based language-model systems can be applied to improve research-paper understanding and provide a unified environment for AI-assisted academic research.

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 1*

---

# 1. INTRODUCTION

Research papers contain valuable information regarding existing methods, experiments, datasets, results, limitations, and future research directions. However, understanding a research paper completely requires considerable time and effort. Researchers must often read lengthy documents, identify important sections, extract relevant information, and manually organize their findings. This becomes particularly challenging when a researcher needs to analyze multiple papers within a limited period.

The increasing availability of research publications has further increased the amount of information that researchers need to process. Although search engines and digital libraries make papers easier to access, they do not necessarily simplify the process of understanding and analyzing the content. A researcher may need to switch between different applications for reading documents, taking notes, identifying research gaps, preparing summaries, and generating reports.

Generative Artificial Intelligence provides an opportunity to improve this process. Large Language Models can understand natural-language content and generate summaries, explanations, and responses to user queries. However, a general-purpose language model may not always be sufficient for detailed document analysis because it needs access to the actual content of the research paper. Retrieval-Augmented Generation can address this issue by retrieving relevant portions of a document and supplying them as context to the language model.

Agentic Artificial Intelligence extends this concept by dividing complex tasks into specialized components. Instead of using a single model to perform every operation, different agents can be responsible for document reading, retrieval, summarization, analysis, and report generation. This approach improves modularity and allows the overall research task to be represented as a sequence of coordinated operations.

ResearchPilot AI applies this concept to research-paper analysis. The system provides a single platform where users can upload a research paper and obtain multiple forms of analysis. The dashboard displays the seven-agent pipeline, making the processing workflow visible to the user. The system then provides separate interfaces for paper summary, deep research analysis, AI-based questioning, generated reports, and research history.

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 2*

---

## 1.1 Problem Statement

The main problem addressed by ResearchPilot AI is the difficulty of efficiently analyzing research papers and extracting meaningful information from them. Manual analysis requires considerable reading time and involves repetitive activities such as summarization, information extraction, identifying limitations, and organizing future research directions.

Existing AI chat interfaces can answer questions about documents, but they may not provide a structured research workflow that includes document processing, semantic retrieval, gap analysis, report generation, and persistent research history. Therefore, there is a need for an intelligent system that can process research papers through specialized AI components and provide researchers with structured, interactive, and reusable research insights through a single interface.

## 1.2 Objectives

* **To provide a simple interface** for uploading research papers in PDF format.
* **To extract and process text** from uploaded research documents.
* **To store document information** using semantic vector representations.
* **To automatically generate** structured research-paper summaries.
* **To identify research gaps**, improvements, future work, and novel ideas.
* **To provide an interactive AI assistant** for questioning the uploaded paper.
* **To generate a comprehensive research report** from the analyzed information.
* **To maintain a history** of previously analyzed research papers.
* **To provide report export functionality** in different formats (Markdown, PDF, DOCX).

## 1.3 Scope

The scope of ResearchPilot AI includes automated PDF processing, document summarization, semantic retrieval, conversational question answering, research-gap identification, improvement suggestions, future-work generation, report generation, and research-history management. The system is intended for students, researchers, academic users, and individuals who need to understand research papers efficiently.

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 3*

---

# 2. LITERATURE REVIEW

Traditional research-paper analysis primarily depends on manual reading and note-taking. Researchers generally identify the objective, methodology, datasets, results, limitations, and future work by reading the document section by section. Although this approach provides detailed understanding, it becomes inefficient when large numbers of papers need to be reviewed.

Information-retrieval systems improved this process by allowing users to search for keywords within large document collections. Search-based approaches can quickly locate relevant information, but they generally require users to formulate appropriate queries and interpret the retrieved results themselves.

Machine learning and Natural Language Processing techniques introduced automated document classification, keyword extraction, text summarization, and information extraction. These methods reduced some of the manual effort involved in document analysis. However, conventional NLP systems often depend on predefined models or task-specific pipelines and may not provide flexible conversational interaction.

The development of Large Language Models has significantly improved natural-language processing capabilities. LLMs can summarize documents, answer questions, explain concepts, and generate structured content. This makes them suitable for research assistance. However, direct prompting of an LLM with a large research document can introduce limitations related to context length, source grounding, and hallucination.

Retrieval-Augmented Generation addresses some of these limitations by combining document retrieval with language generation. The document is divided into smaller chunks, converted into vector representations, and stored in a vector database. When a user asks a question, relevant chunks are retrieved and provided to the language model as contextual information.

Agentic AI extends the capabilities of these systems by allowing multiple specialized components to collaborate. A research assistant can therefore use separate agents for planning, document processing, retrieval, summarization, gap analysis, and report generation. This decomposition makes complex workflows more manageable and provides a modular architecture.

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 4*

---

# 3. MAPPING TO UNITED NATIONS SUSTAINABLE DEVELOPMENT GOALS

ResearchPilot AI contributes primarily to sustainable development goals associated with quality education, innovation, and access to knowledge. The project applies artificial intelligence to simplify research and learning activities and demonstrates how intelligent software can support academic productivity.

### Table 3.1: Sustainable Development Goals and Their Mapping to ResearchPilot AI

| Goal No. | Goal Name | Mapping to ResearchPilot AI |
| :---: | :--- | :--- |
| **SDG 4** | **Quality Education** | Helps students and researchers understand complex academic papers through AI-generated summaries and explanations. |
| **SDG 9** | **Industry, Innovation and Infrastructure** | Demonstrates the application of Generative AI, multi-agent systems, vector databases, and modern software architecture. |
| **SDG 16** | **Peace, Justice and Strong Institutions** | Supports structured access to academic information and promotes transparent information analysis. |
| **SDG 17** | **Partnerships for the Goals** | Provides a technological foundation that can support collaborative research and knowledge sharing. |

### SDG 4 – Quality Education
ResearchPilot AI directly supports quality education by helping learners understand academic material more efficiently. The system can summarize lengthy research papers, explain methodologies, answer questions, and highlight important findings. This can reduce the initial effort required to understand technical documents and support students during academic research.

### SDG 9 – Industry, Innovation and Infrastructure
The project demonstrates technological innovation through the combination of Generative AI, multi-agent orchestration, semantic retrieval, vector databases, and full-stack web development. The seven-agent architecture provides a modular foundation that can be extended with additional AI capabilities.

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 5*

---

### SDG 16 – Peace, Justice and Strong Institutions
The project encourages structured access to information by organizing research content into summaries, analytical findings, and reports. Transparent presentation of the AI workflow can also help users understand how different stages contribute to the final output.

### SDG 17 – Partnerships for the Goals
ResearchPilot AI can support collaborative academic environments where researchers and students need to exchange findings and organize information. Its report-generation and reusable analysis capabilities provide opportunities for future collaborative research workflows.

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 6*

---

# 4. METHODOLOGY

ResearchPilot AI follows a modular multi-agent architecture. The overall research-analysis process is divided into specialized stages, with each stage responsible for a particular operation.

The system begins when the user uploads a PDF research paper through the frontend. The uploaded document is sent to the backend for processing. The Planner establishes the required execution workflow. The PDF Reader extracts textual information from the document, after which the extracted text is divided into manageable chunks. These chunks are represented using embeddings and stored in ChromaDB.

When information is required for analysis or when the user asks a question, the Retriever searches the vector database for relevant document content. The retrieved context is then provided to the AI model, which generates an appropriate response. Separate AI processing stages are used for summarization, research-gap analysis, and report generation.

The system uses LangGraph to organize the agentic workflow and maintain the flow of information between different components. This allows the application to treat research-paper analysis as a sequence of connected operations rather than as a single AI prompt.

### Table 4.1: Technology Stack Used

| System Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React | User interface development |
| **Build Tool** | Vite | Frontend development and build process |
| **Styling** | Tailwind CSS | Responsive interface design |
| **Backend** | FastAPI | Python REST API and backend services |
| **Programming Language** | Python | Backend and AI implementation |
| **AI Framework** | LangChain | LLM and retrieval integration |
| **Agent Framework** | LangGraph | Multi-agent workflow orchestration |
| **Vector Database** | ChromaDB | Semantic document storage and retrieval |
| **LLM** | Mistral AI | Natural-language generation and reasoning |
| **Document Processing** | PDF Reader | Extraction of paper content |
| **Report Formats** | PDF, DOCX, Markdown | Research report export |

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 7*

---

## 4.2 Multi-Agent Components and Their Responsibilities

### Table 4.2: Multi-Agent Components and Their Responsibilities

| Component | Responsibility |
| :--- | :--- |
| **Planner** | Creates and coordinates the research-analysis workflow |
| **PDF Reader** | Extracts text from the uploaded PDF |
| **ChromaDB** | Stores document chunks as semantic vectors |
| **Retriever** | Retrieves relevant document context |
| **Summarizer** | Generates structured paper summaries |
| **Gap Analyzer** | Identifies research gaps and future directions |
| **Report Generator** | Produces the final comprehensive report |

## 4.3 User Authentication
The system provides a dedicated authentication interface containing Sign In and Sign Up options. Users can enter their email address and password to access the ResearchPilot AI workspace. The authentication interface provides a clear entry point to the application and separates the user-access stage from the research-analysis workflow. After authentication, the user is directed to the main dashboard.

## 4.4 PDF Upload and Document Processing
The dashboard provides a dedicated PDF upload section where users can drag and drop a research paper or select it from their system. The uploaded PDF becomes the primary source for subsequent analysis. The PDF Reader processes the document and extracts its textual content. This extracted content forms the basis for summarization, retrieval, question answering, and research-gap analysis.

## 4.5 Planner Agent
The Planner Agent coordinates the overall document-analysis process. It determines the sequence in which different research-analysis components should operate. This approach allows the system to divide a complex research task into smaller operations. The dashboard visually represents this process through the Agent Pipeline, where each stage is displayed with its corresponding function and completion status.

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 8*

---

## 4.6 ChromaDB-Based Semantic Storage
After text extraction, the document is divided into smaller chunks. These chunks are converted into semantic vector representations and stored in ChromaDB. The vector representation allows the system to retrieve information based on semantic meaning rather than relying only on exact keyword matches. This is important for the AI Chat feature because users can ask questions using natural language.

## 4.7 Retriever Agent
The Retriever Agent searches the vector store whenever relevant document context is required. For example, if a user asks about the methodology of the paper, the retriever identifies document sections related to methodology. The retrieved information is passed to the language model so that responses can be grounded in the uploaded document. This retrieval mechanism forms the basis of the system's document-questioning capability.

## 4.8 Summarizer Agent
The Summarizer Agent processes the extracted and retrieved document information to create a structured summary. The summary interface displayed in the application contains sections such as Abstract & Overview and Core Methodology. The system presents the information in a concise format so that users can understand the main purpose, methodology, and important content of a paper without initially reading the entire document.

## 4.9 Gap Analyzer Agent
The Gap Analyzer performs deeper analysis of the research content. It identifies possible research gaps and produces suggestions related to improvements, future work, and novel ideas. The Deep Research Analysis screen organizes these findings into separate categories. The displayed implementation contains categories for All Findings, Research Gaps, Improvements, Future Work, and Novel Ideas, allowing users to explore different types of research insights.

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 9*

---

## 4.10 AI Research Assistant
The AI Research Assistant allows users to interact with the analyzed paper through natural-language questions. The interface provides suggested prompts such as:
* *"Summarize this paper"*
* *"Explain the methodology"*
* *"What datasets were used?"*
* *"Suggest future work"*
* *"What are the limitations?"*
* *"Explain the conclusion"*

Users can also enter their own questions through the chat interface. The Retriever obtains relevant context from the uploaded document, which is then used to generate the response.

## 4.11 Report Generation
The Report Generator combines information from the research-analysis pipeline and produces a structured research report. The displayed report interface contains sections such as Abstract, Literature Review, Research Gaps, Future Work, and Conclusion. The generated report can be copied or exported into Markdown, PDF, and DOCX formats. This makes the output suitable for further editing and academic documentation.

## 4.12 Research History
ResearchPilot AI maintains a history of analyzed research papers. The History interface allows users to search and revisit previously processed documents. Each history entry provides information about the analyzed paper and options such as asking the AI, opening the report, deleting the entry, and loading the previous analysis. This allows users to continue their research work without repeating the entire analysis process.

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 10*

---

# 5. RESULTS

The implementation of ResearchPilot AI demonstrates the integration of a full-stack web application with a multi-agent AI research workflow. The system provides a user-facing interface through which research papers can be uploaded, processed, analyzed, and converted into structured research outputs.

The dashboard provides an overview of the analysis process and displays the seven-agent pipeline. The interface shows the Planner, PDF Reader, ChromaDB, Retriever, Summarizer, Gap Analyzer, and Report Generator as separate stages of the workflow. The system provides different outputs through dedicated application sections. These include the AI Research Assistant, Deep Research Analysis, Paper Summary, Generated Report, and Research Papers History.

## 5.1 ResearchPilot AI Login Interface

The login interface provides the initial entry point to the application. It contains Sign In and Sign Up options along with fields for email address and password. The interface uses a centralized authentication panel and provides a clear transition into the research workspace. The design maintains the same visual identity used throughout the application.

```
+-----------------------------------------------------------------------+
|                       RESEARCHPILOT AI - LOGIN                        |
|                                                                       |
|         [ Sign In ]                     [ Sign Up ]                   |
|                                                                       |
|         Email:        [ researcher@bnmit.edu.in         ]             |
|         Password:     [ ******************              ]             |
|                                                                       |
|                       [ Log In to Workspace ]                         |
|                                                                       |
|                 AI-Powered Academic Paper Analysis                    |
+-----------------------------------------------------------------------+
```
*Figure 5.1: ResearchPilot AI Login Interface*

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 11*

---

## 5.2 ResearchPilot AI Dashboard and Agent Pipeline

The dashboard acts as the main workspace of the system. It provides the PDF upload area and displays key analysis statistics. The interface shows statistics including papers analyzed, gaps identified, key insights, and AI agents used. The dashboard also displays the seven-agent pipeline with each component marked according to its processing state. The visible pipeline demonstrates the complete sequence from planning and PDF processing to retrieval, summarization, gap analysis, and final report generation.

```
+---------------------------------------------------------------------------------------------------+
|  RESEARCHPILOT AI DASHBOARD                              Stats: Papers [12] Gaps [34] Agents [7]   |
+---------------------------------------------------------------------------------------------------+
|  [ Drag & Drop PDF / Upload Research Paper ]                                                      |
|                                                                                                   |
|  MULTI-AGENT PROCESSING PIPELINE:                                                                 |
|  [ Planner ] -> [ PDF Reader ] -> [ ChromaDB ] -> [ Retriever ] -> [ Summarizer ] ->             |
|                                                     [ Gap Analyzer ] -> [ Report Generator ]      |
|  Status: All Agents Synchronized (100% Completed)                                                 |
+---------------------------------------------------------------------------------------------------+
```
*Figure 5.2: ResearchPilot AI Dashboard and Agent Pipeline*

## 5.3 AI Research Assistant Interface

The AI Research Assistant provides a conversational interface for interacting with the selected paper. The interface displays the selected paper and provides several predefined research questions. These questions cover important research aspects including methodology, datasets, limitations, conclusions, summarization, and future work. Users can either select a predefined question or enter a custom question, allowing researchers to obtain targeted information without manually searching the entire paper.

```
+---------------------------------------------------------------------------------------------------+
|  AI RESEARCH ASSISTANT                                                                            |
|  Active Document: Attention_Is_All_You_Need.pdf                                                   |
+---------------------------------------------------------------------------------------------------+
|  Suggested Prompts:                                                                               |
|  [ Summarize this paper ]   [ Explain the methodology ]   [ What datasets were used? ]            |
|  [ Suggest future work ]    [ What are the limitations? ] [ Explain the conclusion ]              |
+---------------------------------------------------------------------------------------------------+
|  User: What is the core mechanism introduced in this paper?                                       |
|  AI Assistant: The paper proposes the Transformer architecture, replacing recurrent models with    |
|  Multi-Head Self-Attention mechanisms for capturing long-range dependencies efficiently.          |
|  Context Source: Section 3.2, Page 4 (Retrieved from ChromaDB)                                    |
+---------------------------------------------------------------------------------------------------+
|  Ask a research question...                                                     [ Send ]          |
+---------------------------------------------------------------------------------------------------+
```
*Figure 5.3: AI Research Assistant Interface*

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 12*

---

## 5.4 Deep Research Analysis Interface

The Deep Research Analysis interface provides a detailed representation of the system's analytical output. The interface contains tabs for All Findings, Research Gaps, Improvements, Future Work, and Novel Ideas. The displayed output shows eight improvement findings generated from the analyzed material. The suggestions include real-time feedback mechanisms, dynamic question banks, interactive simulations, real-world case studies, soft-skill assessment, emerging technologies, performance analytics, and mobile-friendly learning. These outputs demonstrate that the system can generate actionable research-development suggestions rather than producing only a basic summary.

```
+---------------------------------------------------------------------------------------------------+
|  DEEP RESEARCH ANALYSIS                                                                           |
|  Tabs: [ All Findings ] [ Research Gaps ] [ Improvements (8) ] [ Future Work ] [ Novel Ideas ]    |
+---------------------------------------------------------------------------------------------------+
|  1. Real-time Feedback Mechanisms: Adaptive latency optimization during online evaluation.        |
|  2. Dynamic Question Banks: Context-sensitive scenario generation for comprehensive evaluation.  |
|  3. Interactive Simulations: Virtual test environments for empirical ablation.                    |
|  4. Real-world Case Studies: Benchmarking on skewed empirical tabular domains.                    |
|  5. Soft-Skill Assessment: Evaluator interaction metrics and confidence scoring.                  |
|  6. Emerging Technologies: Synergies with stateful agentic orchestration loops.                   |
|  7. Performance Analytics: Fine-grained tracking of convergence curves and variance.              |
|  8. Mobile-Friendly Learning: Low-footprint inference deployment for distributed edge research.   |
+---------------------------------------------------------------------------------------------------+
```
*Figure 5.4: Deep Research Analysis Interface*

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 13*

---

## 5.5 Paper Summary

The Paper Summary interface presents a structured AI-generated overview of the analyzed document. The displayed summary contains the title of the analyzed paper followed by sections such as Abstract & Overview and Core Methodology. The interface also provides a Copy Markdown option. This functionality enables users to quickly understand the main content and methodology of a research document while retaining the option to copy the generated summary for further use.

```
+---------------------------------------------------------------------------------------------------+
|  PAPER SUMMARY                                                            [ Copy Markdown ]       |
+---------------------------------------------------------------------------------------------------+
|  Title: An Agentic Framework for Automated Hypothesis Formulation and Empirical Validation        |
|                                                                                                   |
|  ABSTRACT & OVERVIEW:                                                                             |
|  Presents an autonomous loop of specialized agents (Hypothesis, Experiment, Critic, Refiner)      |
|  that iteratively formulates scientific hypotheses and executes code benchmarks.                  |
|                                                                                                   |
|  CORE METHODOLOGY:                                                                                |
|  - Multi-agent state machine managed with deterministic transitions.                              |
|  - Sandboxed execution sandbox with metric aggregation (MSE, R2, training latency).               |
|  - Ledger-backed auditable reflection logs for peer verification.                                 |
+---------------------------------------------------------------------------------------------------+
```
*Figure 5.5: AI-Generated Paper Summary*

## 5.6 Generated Research Report

The Generated Report module provides a complete AI-generated research synthesis. The report interface contains sections for Abstract, Literature Review, Research Gaps, Future Work, and Conclusion. It also provides options for copying the generated content and exporting it in Markdown, PDF, and DOCX formats. This demonstrates that ResearchPilot AI can transform the results of document analysis into a structured research document rather than limiting its functionality to question answering.

```
+---------------------------------------------------------------------------------------------------+
|  GENERATED RESEARCH REPORT                                 Export: [ Markdown ] [ PDF ] [ DOCX ]  |
+---------------------------------------------------------------------------------------------------+
|  # Comprehensive Synthesis Report                                                                 |
|  ## 1. Abstract                                                                                   |
|  ## 2. Literature Review & Theoretical Grounding                                                  |
|  ## 3. Discovered Research Gaps & Vulnerabilities                                                 |
|  ## 4. Actionable Future Work and Methodological Improvements                                     |
|  ## 5. Conclusion and Scientific Implications                                                     |
+---------------------------------------------------------------------------------------------------+
```
*Figure 5.6: Generated Research Report*

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 14*

---

## 5.7 Research Papers History

The Research Papers History interface provides persistent access to previously analyzed papers. The displayed interface includes statistics such as total papers, gaps uncovered, and key contributions. Each paper entry contains options for asking the AI, opening its report, deleting the entry, and loading its analysis. This feature provides continuity between research sessions and allows users to revisit previous analysis.

```
+---------------------------------------------------------------------------------------------------+
|  RESEARCH PAPERS HISTORY               Total Papers: [ 12 ] | Gaps: [ 34 ] | Insights: [ 89 ]     |
+---------------------------------------------------------------------------------------------------+
|  [Paper Entry #1] Quantile_Normalization_SVR_Analysis.pdf                                         |
|  Date: 2026-09-09 | Gaps: 4 | Actions: [ Ask AI ] [ Open Report ] [ Load Analysis ] [ Delete ]   |
|                                                                                                   |
|  [Paper Entry #2] Attention_Is_All_You_Need.pdf                                                   |
|  Date: 2026-09-08 | Gaps: 6 | Actions: [ Ask AI ] [ Open Report ] [ Load Analysis ] [ Delete ]   |
+---------------------------------------------------------------------------------------------------+
```
*Figure 5.7: Research Papers History*

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 15*

---

## 5.8 Functional Testing and Observed Results

### Table 5.1: Functional Testing and Observed Results

| Sl. No. | Functionality | Expected System Behavior | Observed Result |
| :---: | :--- | :--- | :---: |
| 1 | **User Authentication** | Provides login / sign-up interface and validates credentials | Implemented |
| 2 | **PDF Upload** | Accepts research paper PDF via drag-and-drop or file selector | Implemented |
| 3 | **Document Processing** | Extracts paper content and parses structured sections | Implemented |
| 4 | **Agent Planning** | Creates analysis workflow and orchestrates task graph | Implemented |
| 5 | **Vector Storage** | Stores document chunks as vector embeddings using ChromaDB | Implemented |
| 6 | **Retrieval** | Retrieves relevant context using semantic similarity queries | Implemented |
| 7 | **Paper Summary** | Generates structured summary with Abstract and Core Methodology | Implemented |
| 8 | **Gap Analysis** | Identifies gaps, improvements, future work, and novel ideas | Implemented |
| 9 | **AI Chat** | Answers user research questions grounded in document text | Implemented |
| 10 | **Report Generation** | Creates comprehensive academic research report | Implemented |
| 11 | **Report Export** | Provides export options in PDF, DOCX, and Markdown | Implemented |
| 12 | **Research History** | Stores, searches, and revisits previously analyzed papers | Implemented |
| 13 | **Agent Monitoring** | Displays real-time multi-agent processing pipeline status | Implemented |

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 16*

---

# 6. DISCUSSION

The results demonstrate that a multi-agent architecture is suitable for research-paper analysis because the complete research workflow naturally consists of several different tasks. Document extraction, semantic retrieval, summarization, gap analysis, and report generation require different types of processing. Separating these responsibilities makes the system modular and easier to extend.

The Planner provides coordination between the different stages of the workflow. Rather than sending a complete research document directly to a single model for one response, the system processes the document through several specialized components. This provides a structured approach to research analysis.

The use of ChromaDB and semantic retrieval is particularly important for the AI Chat functionality. Users may ask questions using different wording from the original document. Semantic retrieval allows the system to locate contextually relevant information and provide it to the language model.

The Summary and Analysis modules serve different purposes. The Summary module focuses on providing an overview of the document, while the Deep Research Analysis module goes further by identifying gaps, improvements, future directions, and novel ideas. This separation makes the system useful for both initial paper understanding and deeper research exploration.

The AI Research Assistant adds an interactive layer to the system. Instead of requiring the user to navigate through different sections of the paper, the user can ask direct questions. Suggested prompts further simplify common research tasks such as understanding methodology, datasets, limitations, and conclusions.

The Report Generator provides another important capability by consolidating the generated information into a structured research document. The availability of multiple export formats increases the practical usefulness of the system for academic documentation.

The History module also contributes to the usability of the application. Researchers frequently work with multiple papers, and the ability to revisit previous analyses can reduce repeated processing and provide continuity across research sessions.

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 17*

---

## 6.1 Advantages of the Proposed System

ResearchPilot AI provides several advantages compared with a conventional manual research workflow:
1. **Unified Platform**: It combines multiple research tasks into one platform. Users do not need separate tools for summarization, questioning, gap identification, and report generation.
2. **Modular Architecture**: The seven-agent architecture provides modularity. Each component has a defined responsibility, allowing individual stages to be improved without redesigning the entire system.
3. **Semantic Grounding**: Semantic retrieval allows users to interact with documents using natural language. This makes the system more flexible than simple keyword-based document search.
4. **Actionable Insights**: The Deep Research Analysis module provides actionable findings rather than only summarizing existing content.
5. **Academic Export**: The report-generation and export functionality allows the generated analysis to be converted into reusable academic documentation.

## 6.2 Limitations

The system has limitations:
* **Extraction Quality**: The quality of analysis depends on the quality of text extracted from the uploaded PDF. Documents containing complex tables, figures, scanned pages, mathematical equations, or unusual formatting may require more advanced document-processing techniques.
* **Risk of Hallucination**: Another important limitation is the possibility of AI hallucination. Although retrieval-based processing provides document context, a language model can still generate information that is not completely supported by the source. Therefore, generated research gaps, conclusions, and recommendations should be verified against the original paper before being used in academic work.
* **Single-Document Focus**: The current implementation also focuses primarily on individual-paper analysis. Advanced literature-review functionality would require stronger support for multiple documents, citation relationships, author information, publication metadata, and cross-paper comparison.
* **Extraction Sensitivity**: Poorly structured PDFs may result in incomplete or incorrectly extracted information. AI-generated responses may also contain inaccurate information or unsupported interpretations. The system should therefore be treated as a research-support tool rather than a replacement for scholarly judgment.

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 18*

---

## 6.3 Future Scope

Several enhancements can be introduced in future versions of ResearchPilot AI:
* **Citation Agent**: Automatically extract references and generate citation information in various formats (BibTeX, APA, IEEE).
* **Comparison Agent**: Compare multiple papers and identify similarities, differences, conflicting results, and common methodologies across a collection of papers.
* **Verification Agent**: Check generated statements against retrieved document passages and indicate whether a claim is directly supported by the source, reducing hallucination.
* **Paper Recommendation Agent**: Recommend related research papers based on the content of an uploaded document.
* **Knowledge Graphs**: Introduce knowledge-graph components to represent relationships between papers, authors, datasets, methodologies, and research topics.
* **Extended Modalities**: Support multilingual research papers, voice-based interaction, collaborative research workspaces, personalized research memory, and mobile applications.

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 19*

---

# 7. CONCLUSION

ResearchPilot AI presents a practical implementation of an AI-powered multi-agent research assistant designed to simplify research-paper analysis. The system addresses the challenges associated with manually reading, summarizing, questioning, and analyzing academic documents by integrating these activities into a single intelligent platform.

The system follows a seven-agent workflow consisting of the Planner, PDF Reader, ChromaDB, Retriever, Summarizer, Gap Analyzer, and Report Generator. Each component performs a specialized function while contributing to the overall research-analysis process.

The implemented application provides a dashboard for PDF upload and pipeline monitoring, an AI Research Assistant for document-based questioning, a Paper Summary module for structured understanding, a Deep Research Analysis module for identifying gaps and future directions, a Generated Report module for research documentation, and a History module for revisiting previously analyzed papers.

The use of LangChain, LangGraph, ChromaDB, Mistral AI, FastAPI, React, Vite, and Tailwind CSS demonstrates the integration of modern AI and full-stack technologies into a practical academic application. The project also demonstrates how Retrieval-Augmented Generation and agent-based workflows can be used to make language-model responses more relevant to a specific research document.

The system successfully transforms uploaded research papers into structured and interactive outputs. Instead of simply generating a single response, ResearchPilot AI provides multiple research-oriented perspectives, including summaries, questions and answers, research gaps, improvements, future work, novel ideas, and comprehensive reports.

Overall, ResearchPilot AI demonstrates the potential of agentic artificial intelligence in supporting academic research. The current implementation provides a strong foundation for future development involving multi-paper comparison, citation verification, source-grounded generation, paper recommendation, knowledge graphs, and personalized research assistance.

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 20*

---

# REFERENCES / BIBLIOGRAPHY

1. **[1]** LangChain, "LangChain Documentation," *LangChain Documentation*, https://python.langchain.com/.
2. **[2]** LangChain, "LangGraph Documentation: Build Stateful Agent Workflows," *LangChain Documentation*, https://langchain-ai.github.io/langgraph/.
3. **[3]** FastAPI, "FastAPI Documentation," *FastAPI Official Documentation*, https://fastapi.tiangolo.com/.
4. **[4]** Chroma, "Chroma Documentation: AI-native Open-Source Vector Database," *Chroma Documentation*, https://docs.trychroma.com/.
5. **[5]** Mistral AI, "Mistral AI Documentation," *Mistral AI Documentation*, https://docs.mistral.ai/.
6. **[6]** React, "React Documentation," *React Documentation*, https://react.dev/.
7. **[7]** Vite, "Vite Documentation," *Vite Documentation*, https://vitejs.dev/.
8. **[8]** Tailwind CSS, "Tailwind CSS Documentation," *Tailwind CSS Documentation*, https://tailwindcss.com/.
9. **[9]** Vercel, "Frontend Development and Deployment Documentation," *Vercel Documentation*, https://vercel.com/.
10. **[10]** United Nations, "Sustainable Development Goals," *United Nations*, https://sdgs.un.org/goals.

---

> *2026–2027 | B.E. / Dept. of AI & ML / BNMIT — Page 21*
"""

os.makedirs("docs", exist_ok=True)
with open("docs/RESEARCH_PILOT_REPORT.md", "w", encoding="utf-8") as f:
    f.write(report_content)

print(f"Successfully generated docs/RESEARCH_PILOT_REPORT.md ({len(report_content)} characters)!")
