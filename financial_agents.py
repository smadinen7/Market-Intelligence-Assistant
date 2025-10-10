import os
from crewai import Agent, LLM
from dotenv import load_dotenv

load_dotenv()

# Define the LLMs
gemini_llm = LLM(
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini/gemini-2.5-flash-lite"
)

groq_llm = LLM(
    api_key=os.getenv("GROQ_API_KEY"),
    model="groq/llama-3.1-8b-instant"
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
            llm=groq_llm,
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
            llm=groq_llm,
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
            llm=groq_llm,
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
                "strengths, weaknesses, and competitive positioning."
            ),
            llm=groq_llm,
            verbose=False,
            allow_delegation=False
        )