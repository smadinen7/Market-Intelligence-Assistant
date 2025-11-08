# GEMINI.md - CEO AI Assistant Project Documentation

## 1. Project Overview

This project is a Streamlit web application called "CEO AI Assistant". It has evolved into a sophisticated intelligence platform for executives, strategists, and analysts. The application provides two main workflows:

1.  **Internal Analysis:** Users can upload their own financial documents for analysis. (This workflow has not been the focus of recent development).

2.  **Competitive Intelligence:** A powerful, multi-step workflow where users can identify their top competitors, conduct deep-dive analyses, and explore the competitive landscape through an interactive knowledge graph and an advanced AI chat.

The application is built using Python and leverages a hybrid AI architecture combining the power of Large Language Models (LLMs) with the precision of a structured knowledge graph.

---

## 2. Architecture

The application's architecture is designed to be modular and scalable, with a clear separation of concerns between the frontend, the AI agents, and the knowledge base.

*   **Frontend:** Streamlit
*   **AI Framework:** CrewAI
*   **Large Language Models (LLMs):** Google Gemini and Groq Llama
*   **Core Backend Components:**
    *   **AI Agent Crew:** A team of specialized AI agents, each with a distinct role:
        *   `Competitor Identification Agent`: Discovers a user's top competitors based on market and product data.
        *   `Competitive Intelligence Agent`: Performs a deep-dive analysis of a selected competitor, covering strategy, financials, and market position.
        *   `Knowledge Graph Analyst`: A specialized agent that extracts structured entities (companies, products, markets) from unstructured text and answers complex, relational questions by querying the knowledge graph.
    *   **Dynamic Knowledge Graph:** The central "market brain" of the application, built with the `networkx` library. This graph is not static; it is built and enriched in real-time during user sessions, creating a persistent and ever-growing model of the market ecosystem.
    *   **Data Pipeline:** A crucial workflow that transforms information from unstructured to structured:
        1.  An AI agent generates an unstructured text analysis.
        2.  The `Knowledge Graph Analyst` agent reads this text and extracts structured entities and relationships.
        3.  A parser populates the knowledge graph with this new, structured data.

---

## 3. Competitive Intelligence Workflow

The main user journey is a state-driven process managed within the Streamlit application:

1.  **`awaiting_user_company`**: The user is prompted to enter their company name.
2.  **`identifying_competitors`**: The `Competitor Identification Agent` is triggered. Upon completion, the user's company and the identified competitors are used to **seed the knowledge graph** with the initial `Company` nodes and `competes_with` relationships.
3.  **`competitors_identified`**: The user is shown the list of competitors and prompted to select one for analysis.
4.  **`analyzing_competitor`**: This is the core enrichment step.
    *   The `Competitive Intelligence Agent` generates a deep-dive text analysis.
    *   The `Knowledge Graph Analyst` runs an `entity_extraction_task` on this text.
    *   A `parse_entity_extraction` function processes the structured text output and **enriches the knowledge graph** with new entities (`Product`, `Market`) and new relationships (`OPERATES_IN`, `HAS_PRODUCT`).
5.  **`competitor_selected`**: The analysis is complete. The user can view the text report, explore the interactive knowledge graph visualization, or ask questions in the chat.

### Intelligent Chat

The chat feature uses a smart routing system to provide the best possible answers:
*   **Simple Queries:** Handled by a standard agent using the text analysis as context.
*   **Complex/Relational Queries:** If the user's question contains keywords like "share", "compare", "relationship", or "network", it is routed to the `Knowledge Graph Analyst`. This agent queries the knowledge graph directly to provide a fast, accurate, and factual answer based on the structured data.

---

## 4. Building and Running

To build and run this project, you will need Python 3.11 and `pip`. You will also need API keys from Google AI Studio and GroqCloud.

1.  **Clone the repository:**
    ```sh
    git clone <your-repository-url>
    cd ceo-ai-assistant
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    python3.11 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a file named `.env` in the root of your project and add your API keys:
    ```env
    GEMINI_API_KEY="your_google_api_key_here"
    GROQ_API_KEY="your_groq_api_key_here"
    ```

5.  **Run the application:**
    ```sh
    streamlit run Home.py
    ```

---

## 5. Current Project Status & Next Steps

*   **Status:** The Competitive Intelligence feature is **fully implemented and operational**. The core data pipeline (Analysis -> Extraction -> Graph Population) is complete, and the application successfully leverages the knowledge graph to provide advanced insights and visualizations.

*   **Identified Areas for Refinement:**
    1.  **Prompt Engineering:** The prompt for the `knowledge_graph_query_task` can be refined to instruct the AI to provide more natural, direct answers instead of explicitly mentioning the "knowledge graph".
    2.  **Agent Delegation:** A potential future enhancement is to enable agent delegation (`allow_delegation=True`). This would allow the `Knowledge Graph Analyst` to proactively trigger new research tasks to fill in gaps in its knowledge when it can't answer a question from the existing graph.
