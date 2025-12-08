"""
Basic Gemini Wrapper

This module provides the simplest Gemini interface with basic conversational prompts.
This represents a typical user query without any structured instructions.
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


class BasicGemini:
    """
    Basic Gemini wrapper with simple conversational prompts.
    
    This represents the simplest approach - just asking the LLM directly
    without any structured instructions, formatting rules, or guidance.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash"):
        """
        Initialize the basic Gemini model.
        
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
        Identify top 3 competitors using the simplest possible prompt.
        """
        prompt = f"""Who are the top 3 competitors of {company_name}? Explain why they compete."""
        
        return _call_with_retry(self.model, prompt)
    
    def competitive_intelligence(self, user_company: str, competitor_company: str) -> str:
        """
        Generate competitive intelligence using the simplest possible prompt.
        """
        prompt = f"""Do market research on {competitor_company} as a competitor to {user_company}. 
Include recent news (today is {self.current_date.strftime('%B %d, %Y')}), financial information, strategic recommendations for {user_company}, and regulatory concerns they might face."""
        
        return _call_with_retry(self.model, prompt)
    
    def analyze_financial_document(self, document_content: str, analysis_focus: str = "comprehensive") -> str:
        """
        Analyze a financial document using the simplest possible prompt.
        """
        prompt = f"""Analyze this financial document and tell me what's important.

DOCUMENT:
{document_content[:50000]}"""  # Truncate very long documents
        
        return _call_with_retry(self.model, prompt)
    
    def calculate_financial_ratios(self, financial_data: str) -> str:
        """
        Calculate financial ratios using the simplest possible prompt.
        """
        prompt = f"""Calculate the key financial ratios from this data and explain them.

FINANCIAL DATA:
{financial_data}"""
        
        return _call_with_retry(self.model, prompt)
    
    def answer_question(self, question: str, context: str = "") -> str:
        """
        Answer a question using the simplest possible prompt.
        """
        prompt = f"""{question}

{context[:30000] if context else ""}"""
        
        return _call_with_retry(self.model, prompt)
    
    def research_company(self, company_name: str, specific_question: str = None) -> str:
        """
        Research a company using the simplest possible prompt.
        If specific_question is provided, answer that instead.
        """
        if specific_question:
            prompt = specific_question
        else:
            prompt = f"""Tell me about {company_name} - their business, finances, competition, and risks."""
        
        return _call_with_retry(self.model, prompt)
    
    def risk_assessment(self, company_analysis: str) -> str:
        """
        Conduct risk assessment using the simplest possible prompt.
        """
        prompt = f"""What are the risks for this company?

COMPANY ANALYSIS:
{company_analysis[:30000]}"""
        
        return _call_with_retry(self.model, prompt)
    
    def regulatory_analysis(self, company_name: str) -> str:
        """
        Analyze regulatory risks using the simplest possible prompt.
        """
        prompt = f"""What are the regulatory and compliance risks for {company_name}? Today is {self.current_date.strftime('%B %d, %Y')}."""
        
        return _call_with_retry(self.model, prompt)
