import os
from crewai import Agent, LLM
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_api_key(key_name):
    """Try to get API key from environment variables or Streamlit secrets."""
    # First check environment variables
    api_key = os.getenv(key_name)
    if api_key:
        return api_key
    
    # Then check Streamlit secrets
    try:
        if key_name in st.secrets:
            # Set in os.environ as some libraries expect it there
            os.environ[key_name] = st.secrets[key_name]
            return st.secrets[key_name]
    except (FileNotFoundError, AttributeError):
        pass
        
    return None

# Get API keys
gemini_api_key = get_api_key("GEMINI_API_KEY")
groq_api_key = get_api_key("GROQ_API_KEY")

# Validate keys - we need at least Gemini for the main agents
if not gemini_api_key:
    error_msg = (
        "⚠️ GEMINI_API_KEY not found! \n"
        "Please set it in your .env file (locally) or Streamlit Cloud Secrets.\n"
        "In Streamlit Cloud: Manage App -> Settings -> Secrets"
    )
    print(error_msg) # Print to server logs
    try:
        st.error(error_msg)
        st.stop()
    except:
        raise ValueError(error_msg)

# Define the LLMs
gemini_llm = LLM(
    api_key=gemini_api_key,
    model="gemini/gemini-2.5-flash"
)

# Groq is optional for some agents, but used in the code. 
# If missing, we can fallback to Gemini or raise warning.
if not groq_api_key:
    print("Warning: GROQ_API_KEY not found. Some agents might fail if they strictly require it.")
    # Fallback to Gemini if Groq is missing, or let it fail later?
    # The code uses groq_llm for 'market_comparison_agent'.
    # Let's fallback to Gemini to prevent crash if possible, or just allow None and let it fail if used.
    # For now, we'll initialize it with Gemini key if Groq is missing to keep the app running,
    # but ideally the user should provide it.
    groq_llm = gemini_llm
else:
    groq_llm = LLM(
        api_key=groq_api_key,
        model="groq/llama3-70b-8192"
    )

class FinancialAgents:
    
    def financial_document_analyzer_agent(self):
        return Agent(
            role='Financial Document Analyzer',
            goal="Analyze financial documents (annual reports, 10-K filings, earnings reports) to extract key financial metrics, trends, and insights.",
            backstory=(
                "You are an expert financial analyst with deep knowledge of financial statement analysis, "
                "ratio analysis, and industry benchmarking. You can quickly identify key financial metrics, "
                "trends, risks, and opportunities from complex financial documents."
            ),
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )
        
    def company_research_agent(self):
        return Agent(
            role='Company Research Specialist',
            goal="Research and analyze companies by name, providing comprehensive financial and business insights.",
            backstory=(
                "You are a seasoned equity research analyst who specializes in fundamental company analysis. "
                "You can provide detailed insights about a company's business model, financial performance, "
                "competitive position, management quality, and investment prospects."
            ),
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )

    def financial_ratio_analyst_agent(self):
        return Agent(
            role='Financial Ratio Analyst',
            goal="Calculate and interpret key financial ratios, providing actionable insights about financial health and performance.",
            backstory=(
                "You are a quantitative analyst specializing in financial ratio analysis. "
                "You excel at calculating liquidity ratios, profitability ratios, efficiency ratios, "
                "and leverage ratios, and can interpret what these metrics mean for investors and stakeholders."
            ),
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )

    def investment_advisor_agent(self):
        return Agent(
            role='Investment Advisory Specialist',
            goal="Provide investment recommendations and risk assessments based on financial analysis.",
            backstory=(
                "You are an experienced investment advisor who combines fundamental analysis with "
                "market insights to provide balanced investment recommendations. You consider both "
                "quantitative metrics and qualitative factors in your analysis."
            ),
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )

    def financial_trend_analyst_agent(self):
        return Agent(
            role='Financial Trend Analyst',
            goal="Identify and analyze financial trends, patterns, and anomalies in company performance over time.",
            backstory=(
                "You are a financial data scientist who specializes in identifying trends and patterns "
                "in financial data. You can spot growth trajectories, cyclical patterns, seasonal effects, "
                "and potential red flags in financial performance."
            ),
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )

    def risk_assessment_agent(self):
        return Agent(
            role='Risk Assessment Specialist',
            goal="Evaluate and quantify various types of financial and business risks.",
            backstory=(
                "You are a risk management expert who can identify, assess, and quantify different types "
                "of risks including credit risk, market risk, operational risk, and strategic risk. "
                "You provide clear risk ratings and mitigation strategies."
            ),
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )

    def market_comparison_agent(self):
        return Agent(
            role='Market Comparison Analyst',
            goal="Compare companies against industry peers and market benchmarks.",
            backstory=(
                "You are a comparative analysis expert who specializes in benchmarking companies "
                "against their industry peers and market indices. You can identify relative "
                "strengths, weaknesses, and competitive positioning. Your advanced processing "
                "capabilities allow you to quickly analyze and compare large amounts of market data."
            ),
            llm=groq_llm,  # Using Groq for faster processing of comparative data
            verbose=False,
            allow_delegation=False
        )

    def competitor_identification_agent(self):
        return Agent(
            role='Competitive Intelligence Specialist',
            goal="Identify and analyze the top competitors of a given company in their industry.",
            backstory=(
                "You are a competitive intelligence expert who specializes in identifying "
                "key competitors and understanding competitive landscapes. You can quickly "
                "identify the top 3-5 direct competitors of any company based on industry, "
                "market share, product overlap, and strategic positioning."
            ),
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )

    def competitive_intelligence_agent(self):
        return Agent(
            role='Competitive Analysis Specialist',
            goal="Provide deep competitive intelligence including recent moves, market position, threats, and financial comparisons.",
            backstory=(
                "You are a strategic analyst specializing in competitive intelligence. "
                "You excel at analyzing competitor strategies, recent business moves, market positioning, "
                "and potential competitive threats. You provide comprehensive financial comparisons "
                "and actionable competitive insights that help companies understand their competitive landscape."
            ),
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )

    def knowledge_graph_analyst_agent(self):
        return Agent(
            role='Knowledge Graph Analyst',
            goal="Extract and structure entities and relationships from competitive analysis.",
            backstory=(
                "You are a data scientist specializing in structured data extraction and relationship analysis. "
                "Your task is to quickly identify and extract key entities (companies, products, markets, people) "
                "and their relationships from competitive analysis. You focus on clear, structured output that "
                "can be easily parsed into a knowledge graph."
            ),
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )

    def online_research_agent(self):
        return Agent(
            role='Online Research Specialist',
            goal="Research and gather current market information from online sources to supplement internal knowledge.",
            backstory=(
                "You are an expert market researcher with a talent for finding and synthesizing "
                "information from various online sources. You specialize in gathering current market data, "
                "company information, and competitive intelligence. You excel at validating and cross-referencing "
                "information to ensure accuracy and relevance. You always aim to provide the most up-to-date "
                "and reliable market insights. Your fast processing of web data helps provide quick, accurate insights."
            ),
            llm=gemini_llm,  # Using Groq for faster web search processing
            verbose=False,
            allow_delegation=False
        )

    def strategy_synthesis_agent(self):
        return Agent(
            role='Chief Strategy Officer',
            goal="Synthesize insights from multiple expert analysts to provide comprehensive, well-rounded strategic advice.",
            backstory=(
                "You are a seasoned Chief Strategy Officer with decades of experience in synthesizing "
                "complex business insights. Your expertise lies in understanding and combining different "
                "analytical perspectives - from competitive intelligence and market analysis to risk "
                "assessment and relationship mapping. You excel at distilling multiple expert opinions "
                "into clear, actionable insights. Your role is to consider all angles presented by "
                "your team of experts and deliver a comprehensive yet concise strategic perspective."
            ),
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )

    def company_insights_synthesis_agent(self):
        return Agent(
            role='Company Insights Synthesis Agent',
            goal="Synthesize expert outputs into a short list of actionable, implementable insights for the company.",
            backstory=(
                "You are a pragmatic strategy synthesizer. Your job is to convert research outputs into a prioritized, "
                "actionable list of items the company can implement or investigate. Each insight must be concrete, "
                "operationally relevant, and written as a short directive or suggested action. Avoid stating facts that "
                "aren't directly actionable."
            ),
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )
