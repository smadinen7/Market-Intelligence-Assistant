# 📈 Scalability Guide

This guide explains how to extend the Market Intelligence Assistant with new agents, features, and capabilities.

---

## 📋 Table of Contents

1. [Architecture Overview](#-architecture-overview)
2. [Adding New Agents](#-adding-new-agents)
3. [Adding New Tasks](#-adding-new-tasks)
4. [Adding New Pages](#-adding-new-pages)
5. [Adding New Tools](#-adding-new-tools)
6. [Integrating New Data Sources](#-integrating-new-data-sources)
7. [Adding New Crews](#-adding-new-crews)
8. [Performance Optimization](#-performance-optimization)
9. [Best Practices](#-best-practices)

---

## 🏗️ Architecture Overview

```
Market-Intelligence-Assistant/
├── Home.py                    # Main entry point
├── financial_agents.py        # Agent definitions (ADD NEW AGENTS HERE)
├── financial_tasks.py         # Task definitions (ADD NEW TASKS HERE)
├── pages/                     # Streamlit pages (ADD NEW PAGES HERE)
│   ├── 1_Internal_Analysis.py
│   └── 2_Market_Analysis.py
├── knowledge_graph.py         # Knowledge graph visualization
├── background_workers.py      # Async task processing
└── utils.py                   # Helper functions
```

### Current Agent Count: 12

| Crew | Agents |
|------|--------|
| **Internal Analysis** | Financial Document Analyzer, Financial Ratio Analyst, Financial Trend Analyst, Risk Assessment Specialist, Investment Advisor |
| **Market Analysis** | Company Research, Competitor ID, Competitive Intelligence, Market Comparison |
| **Research & Strategy** | Online Research, Regulatory Analyst, Chief Strategy Officer |

---

## 🤖 Adding New Agents

### Step 1: Define the Agent in `financial_agents.py`

Add a new method to the `FinancialAgents` class:

```python
# financial_agents.py

class FinancialAgents:
    
    # ... existing agents ...
    
    def supply_chain_analyst_agent(self):
        """NEW AGENT: Analyzes supply chain risks and opportunities."""
        return Agent(
            role='Supply Chain Analyst',
            goal="Analyze supply chain dependencies, risks, and optimization opportunities for companies.",
            backstory=(
                "You are an expert in global supply chain management with deep knowledge of "
                "logistics, procurement, vendor relationships, and supply chain risk assessment. "
                "You can identify single points of failure, geopolitical risks, and opportunities "
                "for supply chain optimization."
            ),
            tools=[search_tool] if search_tool else [],  # Add tools if needed
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )
```

### Step 2: Create a Task for the Agent in `financial_tasks.py`

```python
# financial_tasks.py

class FinancialTasks:
    
    # ... existing tasks ...
    
    def supply_chain_analysis_task(self, agent, company_name):
        """Task for supply chain analysis."""
        return Task(
            description=f"""
            Analyze the supply chain for {company_name}:
            
            1. Identify key suppliers and dependencies
            2. Assess geopolitical and logistical risks
            3. Evaluate supply chain resilience
            4. Identify optimization opportunities
            5. Provide risk mitigation recommendations
            
            Focus on actionable insights for strategic decision-making.
            """,
            expected_output="""
            A structured supply chain analysis including:
            - Key supplier mapping
            - Risk assessment (HIGH/MEDIUM/LOW)
            - Vulnerability analysis
            - Optimization recommendations
            """,
            agent=agent
        )
```

### Step 3: Integrate into a Crew

Add the agent and task to an existing crew or create a new one:

```python
# In your page file (e.g., pages/2_Market_Analysis.py)

from financial_agents import FinancialAgents
from financial_tasks import FinancialTasks
from crewai import Crew, Process

agents = FinancialAgents()
tasks = FinancialTasks()

# Create agent instance
supply_chain_agent = agents.supply_chain_analyst_agent()

# Create task
supply_chain_task = tasks.supply_chain_analysis_task(
    agent=supply_chain_agent,
    company_name=company_name
)

# Add to crew
crew = Crew(
    agents=[supply_chain_agent, ...other_agents...],
    tasks=[supply_chain_task, ...other_tasks...],
    process=Process.sequential,
    verbose=False
)

result = crew.kickoff()
```

---

## 📝 Adding New Tasks

Tasks define what agents should do. Add new tasks in `financial_tasks.py`:

```python
# financial_tasks.py

def esg_analysis_task(self, agent, company_name):
    """Task for ESG (Environmental, Social, Governance) analysis."""
    return Task(
        description=f"""
        Conduct an ESG analysis for {company_name}:
        
        **Environmental:**
        - Carbon footprint and emissions
        - Sustainability initiatives
        - Environmental risks
        
        **Social:**
        - Employee relations and diversity
        - Community impact
        - Human rights practices
        
        **Governance:**
        - Board composition
        - Executive compensation
        - Transparency and ethics
        
        Provide an overall ESG score and improvement recommendations.
        """,
        expected_output="""
        Structured ESG report with:
        - Environmental Score (1-10)
        - Social Score (1-10)
        - Governance Score (1-10)
        - Overall ESG Rating
        - Key risks and opportunities
        - Improvement recommendations
        """,
        agent=agent
    )
```

---

## 📄 Adding New Pages

### Step 1: Create a New Page File

Create a new file in the `pages/` directory with a number prefix for ordering:

```python
# pages/3_ESG_Analysis.py

import streamlit as st
from crewai import Crew, Process
from financial_agents import FinancialAgents
from financial_tasks import FinancialTasks

st.set_page_config(
    page_title="ESG Analysis",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 ESG Analysis")
st.markdown("Analyze Environmental, Social, and Governance factors")

# Initialize agents and tasks
agents = FinancialAgents()
tasks = FinancialTasks()

# User input
company_name = st.text_input("Enter company name:")

if st.button("🔍 Analyze ESG"):
    with st.spinner("Analyzing ESG factors..."):
        # Create crew and run analysis
        esg_agent = agents.company_research_agent()  # or create a dedicated ESG agent
        esg_task = tasks.esg_analysis_task(esg_agent, company_name)
        
        crew = Crew(
            agents=[esg_agent],
            tasks=[esg_task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        st.markdown(result.raw)
```

### Step 2: Page Will Auto-Appear

Streamlit automatically discovers pages in the `pages/` directory. The number prefix (e.g., `3_`) controls the order in the sidebar.

---

## 🔧 Adding New Tools

### Using Built-in CrewAI Tools

```python
from crewai_tools import (
    SerperDevTool,       # Web search
    ScrapeWebsiteTool,   # Web scraping
    FileReadTool,        # Read files
    PDFSearchTool,       # Search PDFs
    YoutubeVideoSearchTool,  # YouTube search
)

# Example: Add web scraping capability
scrape_tool = ScrapeWebsiteTool()

def my_agent_with_scraping(self):
    return Agent(
        role='Web Research Specialist',
        tools=[search_tool, scrape_tool],  # Multiple tools
        ...
    )
```

### Creating Custom Tools

```python
from crewai_tools import BaseTool
from pydantic import BaseModel, Field

class StockPriceInput(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL)")

class StockPriceTool(BaseTool):
    name: str = "Stock Price Lookup"
    description: str = "Gets the current stock price for a given ticker symbol"
    args_schema: type[BaseModel] = StockPriceInput
    
    def _run(self, ticker: str) -> str:
        # Your implementation here
        import yfinance as yf
        stock = yf.Ticker(ticker)
        price = stock.info.get('currentPrice', 'N/A')
        return f"Current price of {ticker}: ${price}"

# Use the custom tool
stock_tool = StockPriceTool()

def financial_agent_with_stock_tool(self):
    return Agent(
        role='Financial Analyst',
        tools=[stock_tool],
        ...
    )
```

---

## 📊 Integrating New Data Sources

### Example: Adding a Database Connection

```python
# utils.py

import sqlite3
import pandas as pd

def get_financial_data(company_ticker: str) -> pd.DataFrame:
    """Fetch financial data from local database."""
    conn = sqlite3.connect('financial_data.db')
    query = f"SELECT * FROM financials WHERE ticker = '{company_ticker}'"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def save_analysis_result(company: str, analysis: str):
    """Save analysis results to database."""
    conn = sqlite3.connect('analyses.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO analyses (company, analysis, timestamp) VALUES (?, ?, datetime('now'))",
        (company, analysis)
    )
    conn.commit()
    conn.close()
```

### Example: Adding an External API

```python
# utils.py

import requests

def get_sec_filings(ticker: str) -> dict:
    """Fetch SEC filings from Edgar API."""
    url = f"https://data.sec.gov/submissions/CIK{ticker}.json"
    headers = {'User-Agent': 'YourApp/1.0'}
    response = requests.get(url, headers=headers)
    return response.json()

def get_news_sentiment(company: str) -> dict:
    """Fetch news sentiment from external API."""
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={api_key}"
    response = requests.get(url)
    return response.json()
```

---

## 👥 Adding New Crews

Crews are groups of agents working together. Create specialized crews for different use cases:

```python
# financial_tasks.py or a new crews.py file

from crewai import Crew, Process

def create_ma_analysis_crew(target_company: str, acquiring_company: str):
    """Create a crew for M&A (Mergers & Acquisitions) analysis."""
    
    agents_instance = FinancialAgents()
    tasks_instance = FinancialTasks()
    
    # Define specialized agents
    valuation_agent = agents_instance.financial_ratio_analyst_agent()
    risk_agent = agents_instance.risk_assessment_agent()
    strategy_agent = agents_instance.strategy_synthesis_agent()
    
    # Define tasks
    valuation_task = Task(
        description=f"Analyze the valuation of {target_company} for acquisition by {acquiring_company}",
        agent=valuation_agent,
        expected_output="Detailed valuation report with fair value estimate"
    )
    
    risk_task = Task(
        description=f"Assess risks of {acquiring_company} acquiring {target_company}",
        agent=risk_agent,
        expected_output="Risk assessment with mitigation strategies"
    )
    
    synthesis_task = Task(
        description="Synthesize valuation and risk analysis into M&A recommendation",
        agent=strategy_agent,
        expected_output="Go/No-Go recommendation with strategic rationale",
        context=[valuation_task, risk_task]  # Uses output from previous tasks
    )
    
    return Crew(
        agents=[valuation_agent, risk_agent, strategy_agent],
        tasks=[valuation_task, risk_task, synthesis_task],
        process=Process.sequential,
        verbose=False
    )
```

---

## ⚡ Performance Optimization

### 1. Use Hierarchical Process for Complex Analyses

```python
from crewai import Crew, Process

crew = Crew(
    agents=[manager_agent, worker1, worker2, worker3],
    tasks=[complex_task],
    process=Process.hierarchical,  # Manager delegates to workers
    manager_llm=gemini_llm
)
```

### 2. Enable Caching

```python
# Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=100)
def get_company_data(company_name: str):
    # Expensive API call
    return fetch_from_api(company_name)
```

### 3. Use Background Workers

```python
# background_workers.py already has async patterns

import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=3)

def run_async_analysis(company):
    """Run analysis in background."""
    future = executor.submit(run_crew_analysis, company)
    return future
```

### 4. Optimize Token Usage

```python
# Use shorter prompts for simple tasks
def quick_summary_agent(self):
    return Agent(
        role='Summarizer',
        goal="Provide brief, factual summaries",
        backstory="You are concise and efficient.",  # Short backstory
        llm=LLM(model="groq/llama3-8b-8192"),  # Smaller, faster model
        ...
    )
```

---

## ✅ Best Practices

### Agent Design

| Do | Don't |
|----|-------|
| ✅ Give specific, focused roles | ❌ Create "do everything" agents |
| ✅ Use clear, actionable goals | ❌ Use vague goals |
| ✅ Include relevant expertise in backstory | ❌ Write generic backstories |
| ✅ Only give necessary tools | ❌ Give all tools to all agents |

### Task Design

| Do | Don't |
|----|-------|
| ✅ Be specific about expected output | ❌ Leave output format ambiguous |
| ✅ Break complex tasks into subtasks | ❌ Create monolithic tasks |
| ✅ Use context for task dependencies | ❌ Repeat information across tasks |
| ✅ Include success criteria | ❌ Be vague about what "done" means |

### Code Organization

```
# Recommended structure for large projects
Market-Intelligence-Assistant/
├── agents/
│   ├── __init__.py
│   ├── internal_agents.py
│   ├── market_agents.py
│   └── custom_agents.py
├── tasks/
│   ├── __init__.py
│   ├── internal_tasks.py
│   └── market_tasks.py
├── crews/
│   ├── __init__.py
│   ├── internal_crew.py
│   └── market_crew.py
├── tools/
│   ├── __init__.py
│   └── custom_tools.py
├── pages/
│   └── ...
└── Home.py
```

---

## 🔄 Migration Checklist

When adding new features:

- [ ] Add agent to `financial_agents.py`
- [ ] Add task to `financial_tasks.py`
- [ ] Create or update page in `pages/`
- [ ] Add any new dependencies to `requirements.txt`
- [ ] Add any new API keys to `.env.example`
- [ ] Update `DEPLOYMENT.md` if new secrets needed
- [ ] Test locally before deploying
- [ ] Update `USER_GUIDE.md` with new feature documentation

---

## 📞 Support

For questions about extending the system:
1. Review existing agent/task patterns in the codebase
2. Check [CrewAI Documentation](https://docs.crewai.com/)
3. Review the [LLM_CONFIGURATION.md](LLM_CONFIGURATION.md) for model changes
