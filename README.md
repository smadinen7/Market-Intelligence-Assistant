# 🤖 CEO AI Assistant: Market Intelligence Platform

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-orange.svg)](https://streamlit.io)
[![CrewAI](https://img.shields.io/badge/AI%20Framework-CrewAI-green.svg)](https://www.crewai.com/)
[![Gemini](https://img.shields.io/badge/LLM-Gemini%202.5%20Flash-purple.svg)](https://ai.google.dev/)

An advanced AI-powered platform designed for executives, strategists, and analysts to gain deep insights into their competitive landscape and internal financial health. This tool leverages a crew of specialized AI agents with real-time web search capabilities to deliver up-to-date market intelligence and actionable strategic recommendations.

---

## ✨ Core Features

### 📈 Market Analysis
*   **Dynamic Competitor Identification:** Automatically identifies your top 3 direct competitors based on market, product, and strategic positioning using real-time web search.
*   **In-Depth Competitive Analysis:** Conducts comprehensive intelligence analysis on selected competitors, covering:
    - Recent moves (last 6 weeks with specific dates and details)
    - Major markets with size/share data
    - Hero products and competitive positioning
    - Financial snapshot with 2024/2025 figures
    - Direct threats to your company with impact assessment
    - Strategic recommendations with priority levels (**[HIGH/MEDIUM/LOW]**)
*   **Real-Time Web Search:** All analyses pull current 2024/2025 data from the web - no stale training data.
*   **Multi-Competitor Analysis:** Analyze multiple competitors in a single session with tabbed views for easy comparison.
*   **Contextual Chat:** Ask follow-up questions about any analysis. The AI maintains full context of all competitor analyses to provide detailed, actionable responses.

### 📄 Internal Analysis
*   **Financial Document Analysis:** Upload 10-K filings, earnings reports, annual reports, or CSV data for AI-powered analysis.
*   **Quick Financial Summary:** Get instant key highlights, financial health scores, and investment views.
*   **Financial Ratio Analysis:** Generate detailed ratio analysis on demand.
*   **Risk Assessment:** Identify and assess financial risks from your documents.
*   **Contextual Chat:** Ask questions about your uploaded documents with full context of all generated analyses.

### 💬 Intelligent Chat Interface
*   **Context-Aware Responses:** Chat maintains context from all analyses, both internal and competitive.
*   **Action-Oriented Formatting:** Recommendations include clear **Action** and **Impact** sections.
*   **Priority-Based Guidance:** Strategic recommendations are tagged with priority levels for executive decision-making.
*   **Dollar Sign Formatting:** Currency values display correctly without LaTeX rendering issues.

---

## 🏛️ Architecture Overview

This platform uses a sophisticated multi-agent AI architecture powered by CrewAI and Gemini 2.5 Flash.

### Frontend
- **Streamlit:** Clean, interactive web interface with two-column layout (analysis + chat)
- **Session Management:** Persistent state across analyses

### AI Agent Crew (CrewAI)
- **Competitor Identification Agent:** Discovers competitors using web search
- **Competitive Intelligence Agent:** Performs deep-dive research with real-time data
- **Online Research Agent:** Conducts web searches for current market information
- **Financial Document Analyzer:** Analyzes uploaded financial documents
- **Financial Ratio Analyst:** Calculates and interprets financial ratios
- **Risk Assessment Agent:** Identifies and assesses financial risks
- **Market Comparison Agent:** Provides peer comparison analysis

### Backend Components
- **Knowledge Graph (networkx):** Models relationships between companies, products, and markets
- **Central Memory System:** Maintains context across all analyses for intelligent chat responses
- **Serper API Integration:** Real-time web search for current market data

---

## 🚀 Getting Started

### Prerequisites

*   **Python 3.11+**
*   **API Keys** for:
    *   [Google AI Studio](https://aistudio.google.com/) (for Gemini 2.5 Flash)
    *   [Serper](https://serper.dev/) (for web search)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/smadinen7/Market-Intelligence-Assistant.git
    cd Market-Intelligence-Assistant
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    python3.11 -m venv .venv
    source .venv/bin/activate  # macOS/Linux
    # or: .\.venv\Scripts\activate  # Windows
    ```

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a `.env` file in the root directory:
    ```env
    GEMINI_API_KEY="your_google_api_key_here"
    SERPER_API_KEY="your_serper_api_key_here"
    ```

---

## 📖 Usage

### Running the App
```sh
streamlit run Home.py
```

### Market Analysis Workflow
1. Navigate to **Market Analysis** from the sidebar
2. Enter your company name and click **Start Competitive Analysis**
3. Review the identified competitors and their competitive positioning
4. Click **Analyze** on any competitor for a deep-dive intelligence report
5. Use the chat to ask follow-up questions like:
   - "What should be our top priority?"
   - "Tell me more about [specific recommendation]"
   - "How does [Competitor A] compare to [Competitor B]?"

### Internal Analysis Workflow
1. Navigate to **Internal Analysis** from the sidebar
2. Upload your financial documents (PDF, TXT, MD, or CSV)
3. Click **Start Analysis** for an instant financial summary
4. Use the **Key Metrics** tab to generate:
   - Detailed ratio analysis
   - Risk assessment
5. Use the chat to ask questions about your documents

---

## 🔧 Recent Updates

- **Real-Time Data:** All analyses now use current 2024/2025 data via web search
- **Enhanced Output:** 6-10 detailed bullets per section with specific facts and figures
- **Priority Recommendations:** Strategic recommendations include HIGH/MEDIUM/LOW priority levels
- **Improved Formatting:** Action/Impact sections on separate lines for readability
- **Context Preservation:** Chat maintains full context of all analyses for better follow-up responses
- **Dollar Sign Fix:** Currency values like $245.1B display correctly in markdown

---

## 🔮 Future Work

*   **Automated Report Generation:** Export comprehensive PDF reports
*   **Time-Series Analysis:** Track competitive dynamics over time
*   **Industry Benchmarking:** Compare against industry averages
*   **Alert System:** Notify on significant competitor moves
*   **Deeper Integrations:** Connect to financial APIs for real-time stock data
