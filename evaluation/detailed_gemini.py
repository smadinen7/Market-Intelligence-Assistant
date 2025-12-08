"""
Detailed Gemini Wrapper

This module provides a Gemini interface with moderately structured prompts
that provide guidance but without extensive formatting requirements.
Represents an improved single-LLM approach between Basic and Agentic.
"""

import os
import time
from typing import Optional
from datetime import datetime, timedelta
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Rate limiting settings
RATE_LIMIT_DELAY = 30  # seconds between API calls (increased for free tier)
MAX_RETRIES = 5


def _call_with_retry(model, prompt: str) -> str:
    """Call model with retry logic for rate limits."""
    for attempt in range(MAX_RETRIES):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                wait_time = RATE_LIMIT_DELAY * (attempt + 1)
                print(f"      Rate limited, waiting {wait_time}s (attempt {attempt + 1}/{MAX_RETRIES})...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")


class DetailedGemini:
    """
    Gemini wrapper with moderately structured prompts.
    
    This represents an improved single-LLM approach with better prompting
    and some structure, but without multi-agent orchestration, specialized
    tools, or web search capabilities.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash"):
        """
        Initialize the detailed Gemini model.
        
        Args:
            api_key: Google API key. If None, reads from GEMINI_API_KEY env var.
            model: Model to use. Default matches the agentic system's model.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it in .env or pass as argument.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)
        self.current_date = datetime.now()
        self.six_weeks_ago = self.current_date - timedelta(weeks=6)
    
    def identify_competitors(self, company_name: str) -> str:
        """
        Identify top 3 competitors with some structure.
        """
        prompt = f"""Identify the top 3 direct competitors of {company_name}.

For each competitor, briefly explain:
- What market/industry they overlap in
- Why they are a threat

Be concise but specific."""
        
        return _call_with_retry(self.model, prompt)
    
    def competitive_intelligence(self, user_company: str, competitor_company: str) -> str:
        """
        Generate competitive intelligence report with moderate structure.
        """
        prompt = f"""Analyze {competitor_company} as a competitor to {user_company}.

Cover these areas:
1. Recent developments (past 6 weeks if available)
2. Main products and markets
3. Key financial metrics
4. Threats they pose to {user_company}
5. Recommendations for {user_company}
6. Any regulatory concerns

Today's date: {self.current_date.strftime('%B %d, %Y')}"""
        
        return _call_with_retry(self.model, prompt)
    
    def analyze_financial_document(self, document_content: str, analysis_focus: str = "comprehensive") -> str:
        """
        Analyze a financial document with some structure.
        """
        prompt = f"""Analyze this financial document.

Focus: {analysis_focus}

Provide:
- Key takeaways
- Important financial metrics
- Notable strengths and concerns

DOCUMENT:
{document_content[:50000]}"""
        
        return _call_with_retry(self.model, prompt)
    
    def calculate_financial_ratios(self, financial_data: str) -> str:
        """
        Calculate financial ratios with some guidance.
        """
        prompt = f"""Calculate key financial ratios from this data.

Include liquidity, profitability, and leverage ratios.
Explain what each ratio means.

FINANCIAL DATA:
{financial_data}"""
        
        return _call_with_retry(self.model, prompt)
    
    def answer_question(self, question: str, context: str = "") -> str:
        """
        Answer a question with context awareness.
        """
        context_section = f"\nContext:\n{context[:30000]}" if context else ""
        
        prompt = f"""Answer this question clearly and directly.

Question: {question}{context_section}"""
        
        return _call_with_retry(self.model, prompt)
    
    def research_company(self, company_name: str, specific_question: str = None) -> str:
        """
        Research a company with moderate structure.
        If specific_question is provided, answer that instead.
        """
        if specific_question:
            prompt = f"""Research and answer this question:
{specific_question}

Provide specific details including dates, numbers, and sources where possible."""
        else:
            prompt = f"""Provide an analysis of {company_name}.

Cover:
- Business overview
- Financial performance
- Competitive position
- Key risks
- Growth outlook"""
        
        return _call_with_retry(self.model, prompt)
    
    def risk_assessment(self, company_analysis: str) -> str:
        """
        Conduct risk assessment with some structure.
        """
        prompt = f"""Based on this analysis, identify the key risks.

Categorize by: financial, operational, market, and strategic risks.
Rate each as Low, Medium, or High.

COMPANY ANALYSIS:
{company_analysis[:30000]}"""
        
        return _call_with_retry(self.model, prompt)
    
    def regulatory_analysis(self, company_name: str) -> str:
        """
        Analyze regulatory risks with moderate structure.
        """
        prompt = f"""Analyze the regulatory and compliance landscape for {company_name}.

Cover these areas:
1. Key industry regulations affecting them
2. Current compliance risks (rate severity)
3. Recent regulatory actions or investigations
4. Cross-border/international considerations
5. Upcoming regulatory changes to watch

Today's date: {self.current_date.strftime('%B %d, %Y')}"""
        
        return _call_with_retry(self.model, prompt)
