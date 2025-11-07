# 🤖 CEO AI Assistant: Competitive Intelligence Platform

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-orange.svg)](https://streamlit.io)
[![CrewAI](https://img.shields.io/badge/AI%20Framework-CrewAI-green.svg)](https://www.crewai.com/)

An advanced AI-powered platform designed for executives, strategists, and analysts to gain deep insights into their competitive landscape. This tool goes beyond simple financial analysis, leveraging a crew of specialized AI agents and a dynamic knowledge graph to model and query complex market ecosystems.

Enter your company, and the assistant will identify your top competitors, perform deep-dive analyses, and build an interactive "market brain" that you can query to uncover strategic threats and opportunities.

---

## ✨ Core Features

*   **Dynamic Competitor Identification:** Automatically identifies your top 3 direct competitors based on market, product, and strategic positioning.
*   **In-Depth Competitive Analysis:** Conducts a comprehensive intelligence analysis on selected competitors, covering strategic moves, market position, financial health, and direct threats to your company.
*   **Interactive Knowledge Graph:** Automatically builds and visualizes a knowledge graph of your market. See the web of relationships between companies, products, and markets.
*   **Advanced AI Chat:** Ask complex, relational questions in plain English (e.g., "What markets do we share with our competitor?") and get precise answers powered by the knowledge graph.
*   **Persistent Market Memory:** The knowledge graph evolves with each analysis, creating an ever-smarter "market brain" that becomes more valuable over time.

---

## 🏛️ How It Works: Architecture Overview

This platform uses a sophisticated hybrid AI architecture that combines the broad knowledge of LLMs with the precision of a structured knowledge graph.

1.  **Frontend (Streamlit):** A clean, interactive web interface that orchestrates the user workflow.
2.  **AI Agent Crew (CrewAI):** A team of specialized AI agents, each with a unique role:
    *   **Competitor Identification Agent:** Discovers who your competitors are.
    *   **Competitive Intelligence Agent:** Performs deep-dive research on a specific competitor.
    *   **Knowledge Graph Analyst:** Extracts structured entities from unstructured text and answers complex, graph-based questions.
3.  **Dynamic Knowledge Graph (`networkx`):** The central "brain" of the application.
    *   **Population:** The graph is built and enriched in real-time. An AI agent reads the analysis reports and populates the graph with entities (Companies, Products, Markets) and their relationships (`COMPETES_WITH`, `OPERATES_IN`).
    *   **Querying:** For complex questions, the AI queries this structured graph to provide fast, accurate, and reliable answers.

This architecture allows the system to reason about complex relationships and deliver insights that would be impossible to find with text analysis alone.

---

## 🚀 Getting Started

Follow these instructions to get the project running on your local machine.

### Prerequisites

*   **Python 3.11**
*   **API Keys** for:
    *   [Google AI Studio](https://aistudio.google.com/) (for Gemini)
    *   [GroqCloud](https://console.groq.com/) (for Llama)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone <your-repository-url>
    cd ceo-ai-assistant
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # Create the venv
    python3.11 -m venv .venv

    # Activate on macOS/Linux
    source .venv/bin/activate

    # Activate on Windows
    # .\\.venv\\Scripts\\activate
    ```

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    *   Create a file named `.env` in the root of your project.
    *   Add your API keys to the `.env` file:
        ```env
        GEMINI_API_KEY="your_google_api_key_here"
        GROQ_API_KEY="your_groq_api_key_here"
        ```

---

## 📖 Usage

1.  **Run the application:**
    With your virtual environment active, run the following command in your terminal:
    ```sh
    streamlit run Home.py
    ```

2.  **Start a New Analysis:**
    *   From the sidebar, click **"New Competitive Analysis"**.

3.  **Identify Competitors:**
    *   Enter your company's name in the text input.
    *   Click **"Identify Competitors"**. The AI will analyze the market and present your top 3 competitors.

4.  **Analyze and Explore:**
    *   Click the **"Analyze [Competitor Name]"** button for a competitor you want to investigate.
    *   The AI will perform a deep-dive analysis and populate the knowledge graph.
    *   Navigate to the **"Detailed Analysis"** tab to view the full report and the interactive knowledge graph visualization.

5.  **Ask Questions:**
    *   Use the chat interface on the right to ask simple or complex questions about the competitive landscape.

---

## 🔮 Future Work

*   **Enable Agent Delegation:** Allow agents to autonomously trigger new research tasks to fill in gaps in the knowledge graph.
*   **Time-Series Analysis:** Track changes in the knowledge graph over time to analyze how competitive dynamics evolve.
*   **Deeper Integrations:** Connect to external data sources (e.g., financial APIs, news APIs) to automatically enrich the knowledge graph.