"""
Agentic System Wrapper

This module wraps the existing multi-agent CrewAI system to provide
a consistent interface for evaluation against the baseline Gemini.
"""

import os
import sys
from typing import Optional
from datetime import datetime

# Add parent directory to path to import project modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Crew, Process
from dotenv import load_dotenv

load_dotenv()


class AgenticSystem:
    """
    Wrapper for the multi-agent CrewAI system.
    
    Provides the same interface as BaselineGemini for fair comparison,
    but uses the full agent orchestration under the hood.
    """
    
    def __init__(self):
        """Initialize the agentic system with all required agents."""
        # Import here to avoid circular imports and ensure env is loaded
        from financial_agents import FinancialAgents
        from financial_tasks import FinancialTasks
        
        self.agents = FinancialAgents()
        self.tasks = FinancialTasks()
        self.current_date = datetime.now()
    
    def identify_competitors(self, company_name: str) -> str:
        """
        Identify top 3 competitors using the competitor identification agent.
        
        Uses the specialized agent with web search tools and structured output format.
        """
        agent = self.agents.competitor_identification_agent()
        task = self.tasks.identify_competitors_task(agent, company_name)
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        return result.raw
    
    def competitive_intelligence(self, user_company: str, competitor_company: str) -> str:
        """
        Generate competitive intelligence using the specialized agent.
        
        Uses web search tools, structured output format with specific sections,
        strict output rules, and includes regulatory analysis.
        """
        # Step 1: Competitive Intelligence
        intel_agent = self.agents.competitive_intelligence_agent()
        intel_task = self.tasks.competitive_intelligence_task(intel_agent, user_company, competitor_company)
        
        crew = Crew(
            agents=[intel_agent],
            tasks=[intel_task],
            process=Process.sequential,
            verbose=False
        )
        
        competitive_analysis = crew.kickoff()
        competitive_analysis = competitive_analysis.raw
        
        # Step 2: Regulatory Analysis
        # Extract strategic recommendations for context
        strategic_recs = ""
        if "## Strategic Recommendations" in competitive_analysis:
            recs_section = competitive_analysis.split("## Strategic Recommendations")[1]
            if "\n##" in recs_section:
                strategic_recs = recs_section.split("\n##")[0]
            else:
                strategic_recs = recs_section
        
        industry_context = f"{competitor_company} and {user_company} industry"
        
        regulatory_agent = self.agents.regulatory_analyst_agent()
        regulatory_task = self.tasks.regulatory_concerns_task(
            regulatory_agent,
            user_company,
            competitor_company,
            strategic_recs if strategic_recs else "No strategic recommendations available",
            industry_context
        )
        
        regulatory_crew = Crew(
            agents=[regulatory_agent],
            tasks=[regulatory_task],
            process=Process.sequential,
            verbose=False
        )
        
        regulatory_analysis = regulatory_crew.kickoff()
        if regulatory_analysis and regulatory_analysis.raw:
            regulatory_analysis = regulatory_analysis.raw
            
            # Clean up any agent thinking/reasoning text
            if "##" in regulatory_analysis:
                first_heading_idx = regulatory_analysis.find("##")
                regulatory_analysis = regulatory_analysis[first_heading_idx:]
            
            # Remove agent thought lines
            lines = regulatory_analysis.split('\n')
            cleaned_lines = []
            skip_mode = False
            
            for line in lines:
                if line.strip().startswith("Thought:") or \
                   line.strip().startswith("Action:") or \
                   line.strip().startswith("Using Tool:") or \
                   line.strip().startswith("Tool Input:") or \
                   line.strip().startswith("Observation:"):
                    skip_mode = True
                    continue
                
                if line.strip().startswith("##"):
                    skip_mode = False
                
                if not skip_mode:
                    cleaned_lines.append(line)
            
            regulatory_analysis = '\n'.join(cleaned_lines)
        else:
            regulatory_analysis = "## Regulatory & Compliance Concerns\n\nNo significant regulatory concerns identified at this time."
        
        # Combine competitive and regulatory analyses
        combined_analysis = competitive_analysis + "\n\n" + regulatory_analysis
        return combined_analysis
    
    def analyze_financial_document(self, document_content: str, analysis_focus: str = "comprehensive") -> str:
        """
        Analyze a financial document using the document analyzer agent.
        """
        agent = self.agents.financial_document_analyzer_agent()
        task = self.tasks.analyze_financial_document_task(agent, document_content, analysis_focus)
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        return result.raw
    
    def calculate_financial_ratios(self, financial_data: str) -> str:
        """
        Calculate financial ratios using the specialized ratio analyst agent.
        """
        agent = self.agents.financial_ratio_analyst_agent()
        task = self.tasks.calculate_financial_ratios_task(agent, financial_data)
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        return result.raw
    
    def answer_question(self, question: str, context: str = "") -> str:
        """
        Answer a financial/competitive question using the chat response agent.
        """
        # Use strategy synthesis for complex questions
        agent = self.agents.strategy_synthesis_agent()
        task = self.tasks.financial_chat_response_task(agent, question, context)
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        return result.raw
    
    def research_company(self, company_name: str, specific_question: str = None) -> str:
        """
        Research a company using the appropriate agent.
        Uses online_research_agent for specific questions (recency tests) to leverage web search.
        Uses company_research_agent for general research.
        """
        from crewai import Task
        
        if specific_question:
            # Use online research agent for specific/recency questions
            agent = self.agents.online_research_agent()
            task = Task(
                description=f"""Research and answer this specific question about {company_name}:

{specific_question}

Use your web search tools to find the MOST RECENT information available.
Include:
- Specific dates for all events
- Recent stock price movements
- Latest news and announcements
- Any developments from the past 2-4 weeks

Be thorough and cite your sources with dates.""",
                expected_output="Comprehensive answer with specific recent dates, events, and data points",
                agent=agent
            )
        else:
            agent = self.agents.company_research_agent()
            task = self.tasks.research_company_task(agent, company_name)
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        return result.raw
    
    def risk_assessment(self, company_analysis: str) -> str:
        """
        Conduct risk assessment using the risk assessment agent.
        """
        agent = self.agents.risk_assessment_agent()
        task = self.tasks.risk_assessment_task(agent, company_analysis)
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        return result.raw
    
    def regulatory_analysis(self, company_name: str) -> str:
        """
        Analyze regulatory risks using the regulatory analyst agent.
        Uses web search tools for current regulatory information.
        """
        industry_context = f"{company_name} industry"
        
        regulatory_agent = self.agents.regulatory_analyst_agent()
        regulatory_task = self.tasks.regulatory_concerns_task(
            regulatory_agent,
            company_name,
            f"industry competitors of {company_name}",
            "General regulatory compliance analysis",
            industry_context
        )
        
        crew = Crew(
            agents=[regulatory_agent],
            tasks=[regulatory_task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        regulatory_analysis = result.raw
        
        # Clean up any agent thinking/reasoning text
        if "##" in regulatory_analysis:
            first_heading_idx = regulatory_analysis.find("##")
            regulatory_analysis = regulatory_analysis[first_heading_idx:]
        
        # Remove agent thought lines
        lines = regulatory_analysis.split('\n')
        cleaned_lines = []
        skip_mode = False
        
        for line in lines:
            if line.strip().startswith("Thought:") or \
               line.strip().startswith("Action:") or \
               line.strip().startswith("Using Tool:") or \
               line.strip().startswith("Tool Input:") or \
               line.strip().startswith("Observation:"):
                skip_mode = True
                continue
            
            if line.strip().startswith("##"):
                skip_mode = False
            
            if not skip_mode:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def full_competitor_analysis_pipeline(self, user_company: str) -> dict:
        """
        Run the full competitor analysis pipeline:
        1. Identify competitors
        2. Generate intelligence for each competitor
        3. Extract entities and relationships
        
        Returns a dict with all outputs for comprehensive evaluation.
        """
        results = {
            "user_company": user_company,
            "competitor_identification": "",
            "competitor_analyses": {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Step 1: Identify competitors
        results["competitor_identification"] = self.identify_competitors(user_company)
        
        # Step 2: Parse competitor names (simplified extraction)
        import re
        import json
        
        competitors = []
        # Try JSON array first
        try:
            start = results["competitor_identification"].find('[')
            end = results["competitor_identification"].find(']', start)
            if start != -1 and end != -1:
                competitors = json.loads(results["competitor_identification"][start:end+1])
        except:
            pass
        
        # Fallback to pattern matching
        if not competitors:
            pattern = r'\*\*\d+\.\s*([^*\n]+?)\*\*'
            matches = re.findall(pattern, results["competitor_identification"])
            competitors = [m.strip() for m in matches[:3]]
        
        # Step 3: Generate intelligence for each competitor
        for competitor in competitors[:3]:  # Limit to top 3
            try:
                results["competitor_analyses"][competitor] = self.competitive_intelligence(
                    user_company, competitor
                )
            except Exception as e:
                results["competitor_analyses"][competitor] = f"Error: {str(e)}"
        
        return results
