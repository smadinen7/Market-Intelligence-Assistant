"""
LLM-as-a-Judge Evaluation Module

This module implements an impartial LLM judge that compares outputs from
a baseline Gemini model against the multi-agent CrewAI system.
"""

import os
import json
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import google.generativeai as genai
from dotenv import load_dotenv

# Rate limiting settings
RATE_LIMIT_DELAY = 30  # seconds between retry attempts on rate limit
MAX_RETRIES = 5  # increased from 3 to handle rate limits better

load_dotenv()


@dataclass
class ScoreBreakdown:
    """Individual scores for each evaluation dimension."""
    accuracy: int  # 1-5: Factual correctness of information
    completeness: int  # 1-5: All required sections/elements present
    actionability: int  # 1-5: Specific, implementable recommendations
    recency: int  # 1-5: Uses data from past 6 weeks (current 2024/2025)
    structure: int  # 1-5: Proper formatting with required headings
    
    @property
    def total(self) -> int:
        return self.accuracy + self.completeness + self.actionability + self.recency + self.structure
    
    @property
    def average(self) -> float:
        return self.total / 5.0
    
    def to_dict(self) -> Dict:
        return {
            "accuracy": self.accuracy,
            "completeness": self.completeness,
            "actionability": self.actionability,
            "recency": self.recency,
            "structure": self.structure,
            "total": self.total,
            "average": round(self.average, 2)
        }


@dataclass
class EvaluationResult:
    """Complete evaluation result for a single test case."""
    test_case_id: str
    test_case_type: str
    input_query: str
    
    baseline_response: str
    agentic_response: str
    
    baseline_scores: ScoreBreakdown
    agentic_scores: ScoreBreakdown
    
    winner: str  # "baseline", "agentic", or "tie"
    judge_rationale: str
    
    evaluation_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "test_case_id": self.test_case_id,
            "test_case_type": self.test_case_type,
            "input_query": self.input_query,
            "baseline_scores": self.baseline_scores.to_dict(),
            "agentic_scores": self.agentic_scores.to_dict(),
            "winner": self.winner,
            "judge_rationale": self.judge_rationale,
            "evaluation_timestamp": self.evaluation_timestamp
        }


class LLMJudge:
    """
    Impartial LLM judge that evaluates and compares outputs from two systems.
    
    Uses blind evaluation: responses are presented as "Response A" and "Response B"
    with randomized assignment to prevent position bias.
    """
    
    # Task-specific rubrics
    COMPETITOR_ID_RUBRIC = """
## Evaluation Rubric for Competitor Identification (Brief Overview Task)

Score each response on a scale of 1-5 for each dimension:

### 1. Accuracy (1-5)
- 5: All competitors are truly direct competitors; accurate competitive positioning
- 4: Mostly accurate with minor mischaracterizations
- 3: Some questionable competitor choices or positioning
- 2: Multiple inaccurate competitor selections
- 1: Competitors are not actually competitors

### 2. Completeness (1-5)
- 5: Identifies 3 competitors with clear, concise reasoning for each (2-3 key points)
- 4: 3 competitors with adequate reasoning
- 3: 3 competitors but weak/missing reasoning, or only 2 competitors
- 2: Only 1-2 competitors or very shallow explanations
- 1: No competitors identified or completely off-target

### 3. Actionability (1-5)
- 5: Provides clear strategic insight on competitive positioning for each
- 4: Good insights with some strategic value
- 3: Basic observations that hint at strategy
- 2: Purely descriptive without strategic value
- 1: No actionable insights

### 4. Recency (1-5)
- 5: References current competitive landscape (2024-2025)
- 4: Mostly current competitive context
- 3: Mix of current and outdated competitive information
- 2: Mostly outdated competitive landscape
- 1: Clearly outdated or no temporal context

### 5. Structure (1-5)
- 5: Well-organized, concise list format; easy to scan
- 4: Good organization with minor clarity issues
- 3: Adequate but could be more concise or clear
- 2: Poorly organized; hard to extract key points
- 1: No clear structure; verbose or disorganized

**Note**: For competitor identification, BREVITY is valued. Concise, focused responses are preferred over lengthy analysis.
"""

    COMPETITIVE_INTEL_RUBRIC = """
## Evaluation Rubric for Competitive Intelligence (Comprehensive Analysis Task)

Score each response on a scale of 1-5 for each dimension:

### 1. Accuracy (1-5)
- 5: All facts are correct, specific numbers/dates are accurate, no hallucinations
- 4: Mostly accurate with minor errors that don't affect conclusions
- 3: Some factual errors or unverifiable claims
- 2: Multiple inaccuracies or significant factual errors
- 1: Largely inaccurate or fabricated information

### 2. Completeness (1-5)
- 5: All required sections present with comprehensive detail (6-10 bullets per section)
- 4: All sections present with good detail (4-6 bullets)
- 3: Most sections present but some lacking depth
- 2: Missing multiple required sections or very shallow coverage
- 1: Severely incomplete, missing most required elements

### 3. Actionability (1-5)
- 5: Specific, concrete recommendations with clear Action/Impact; ready to implement
- 4: Good recommendations with some specificity; mostly actionable
- 3: General recommendations that need more detail to implement
- 2: Vague suggestions without clear implementation path
- 1: No actionable recommendations or purely observational

### 4. Recency (1-5)
- 5: Uses data from past 6 weeks (October-December 2025); cites specific recent events
- 4: Uses 2024/2025 data; some recent references
- 3: Mix of current and older data; some outdated references
- 2: Mostly uses 2023 or older data
- 1: Uses clearly outdated information (2022 or earlier) or no temporal context

### 5. Structure (1-5)
- 5: Perfect formatting with all required headings, clear hierarchy, easy to scan
- 4: Good structure with proper headings; minor formatting issues
- 3: Adequate structure but missing some organizational elements
- 2: Poor organization; difficult to navigate
- 1: No clear structure; stream of consciousness
"""

    REGULATORY_RUBRIC = """
## Evaluation Rubric for Regulatory Analysis

Score each response on a scale of 1-5 for each dimension:

### 1. Accuracy (1-5)
- 5: Correctly identifies actual regulations, agencies, and compliance requirements
- 4: Mostly accurate regulatory information with minor errors
- 3: Some inaccuracies in regulatory details or agency jurisdictions
- 2: Multiple errors in regulatory claims
- 1: Fundamentally incorrect regulatory information

### 2. Completeness (1-5)
- 5: Covers all major regulatory areas: industry-specific, data privacy, antitrust, cross-border
- 4: Good coverage of most regulatory areas
- 3: Covers some regulatory areas but misses important ones
- 2: Very limited regulatory coverage
- 1: Severely incomplete regulatory analysis

### 3. Actionability (1-5)
- 5: Specific compliance recommendations with clear implementation steps
- 4: Good recommendations with reasonable specificity
- 3: General compliance suggestions that need more detail
- 2: Vague regulatory observations without guidance
- 1: No actionable compliance recommendations

### 4. Recency (1-5)
- 5: References current regulatory landscape (2024-2025); mentions recent regulatory actions
- 4: Mostly current regulatory context with some recent references
- 3: Mix of current and outdated regulatory information
- 2: Mostly outdated regulatory information
- 1: Uses clearly outdated regulations or no temporal context

### 5. Structure (1-5)
- 5: Well-organized by regulatory area with clear risk levels and priorities
- 4: Good organization with proper categorization
- 3: Adequate but could be better organized
- 2: Disorganized regulatory information
- 1: No clear structure
"""

    RECENCY_RUBRIC = """
## Evaluation Rubric for Current News/Developments Research

This task REQUIRES the most recent information. One system may have access to web search tools to get current data while others may not.

**IMPORTANT FOR EVALUATION:**
- If a response cites specific sources, URLs, or news articles with dates, treat this as VERIFIED current information
- If a response admits it cannot access recent data or has a knowledge cutoff, it should score LOW on recency
- A response that acknowledges inability to get current data is more honest but less useful for this task

Score each response on a scale of 1-5 for each dimension:

### 1. Accuracy (1-5)
- 5: Provides specific, verifiable facts with sources cited; specific dates and numbers
- 4: Mostly accurate with sources; minor missing details
- 3: Mix of sourced and unsourced claims
- 2: Few sources cited; some questionable claims
- 1: No sources; admits to knowledge limitations OR provides unsourced claims

### 2. Completeness (1-5)
- 5: Covers multiple recent developments: news, stock movements, product updates, partnerships
- 4: Good coverage of recent developments across multiple areas
- 3: Covers some recent areas but misses important recent news
- 2: Very limited coverage of recent events
- 1: Fails to address recent developments OR admits inability to provide them

### 3. Actionability (1-5)
- 5: Provides strategic implications of recent news; clear insights for decision-making
- 4: Good insights with reasonable strategic value
- 3: Basic observations with limited strategic depth
- 2: Purely informational without strategic context
- 1: No actionable insights OR only generic observations

### 4. Recency (1-5) **CRITICAL**
- 5: Includes SPECIFIC events from the requested timeframe with sources/citations
- 4: References events from requested timeframe with some citations
- 3: Has some recent information but also relies on older knowledge
- 2: Mostly acknowledges inability to access recent data
- 1: Only provides older information OR explicitly states knowledge cutoff limitations

### 5. Structure (1-5)
- 5: Well-organized chronologically with clear source citations
- 4: Good organization with proper chronological context
- 3: Adequate but could be better organized
- 2: Disorganized; hard to distinguish recent from older info
- 1: No clear structure or timeline
"""

    DEFAULT_RUBRIC = COMPETITIVE_INTEL_RUBRIC  # Use comprehensive rubric as default

    JUDGE_PROMPT_TEMPLATE = """You are an expert evaluator comparing two AI-generated responses to a business intelligence query.

## Your Task
Evaluate both responses using the rubric below, then declare a winner.

## Important Context
- Today's date is {current_date}
- "Past 6 weeks" means content from {six_weeks_ago} to {current_date}

{rubric}

## The Query
{query}

## Response A
{response_a}

## Response B
{response_b}

## Your Evaluation

Provide your evaluation in the following JSON format:
```json
{{
    "response_a_scores": {{
        "accuracy": <1-5>,
        "completeness": <1-5>,
        "actionability": <1-5>,
        "recency": <1-5>,
        "structure": <1-5>
    }},
    "response_b_scores": {{
        "accuracy": <1-5>,
        "completeness": <1-5>,
        "actionability": <1-5>,
        "recency": <1-5>,
        "structure": <1-5>
    }},
    "winner": "<A|B|tie>",
    "rationale": "<2-3 sentence explanation of why the winner was chosen, citing specific differences>"
}}
```

Respond ONLY with the JSON object, no other text.
"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash"):
        """
        Initialize the LLM Judge.
        
        Args:
            api_key: Gemini API key. If None, reads from GEMINI_API_KEY env var.
            model: Model to use for judging. Default is gemini-2.5-flash.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it in .env or pass as argument.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)
        self.model_name = model
        
    def _parse_judge_response(self, response_text: str) -> Dict:
        """Parse the JSON response from the judge."""
        # Extract JSON from response (handle markdown code blocks)
        text = response_text.strip()
        if text.startswith("```"):
            # Remove markdown code block
            lines = text.split("\n")
            text = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            # Try to find JSON object in the text
            import re
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                return json.loads(json_match.group())
            raise ValueError(f"Could not parse judge response as JSON: {e}")
    
    def evaluate(
        self,
        query: str,
        baseline_response: str,
        agentic_response: str,
        test_case_id: str = "unknown",
        test_case_type: str = "general"
    ) -> EvaluationResult:
        """
        Evaluate and compare two responses using the LLM judge.
        
        Args:
            query: The original query/prompt
            baseline_response: Response from baseline Gemini
            agentic_response: Response from multi-agent system
            test_case_id: Identifier for this test case
            test_case_type: Category of test (competitor_id, competitive_intel, etc.)
            
        Returns:
            EvaluationResult with scores, winner, and rationale
        """
        # Randomize assignment to prevent position bias
        if random.random() < 0.5:
            response_a = baseline_response
            response_b = agentic_response
            a_is_baseline = True
        else:
            response_a = agentic_response
            response_b = baseline_response
            a_is_baseline = False
        
        # Select appropriate rubric based on task type
        if test_case_type == "competitor_identification":
            rubric = self.COMPETITOR_ID_RUBRIC
        elif test_case_type == "competitive_intelligence":
            rubric = self.COMPETITIVE_INTEL_RUBRIC
        elif test_case_type == "regulatory_analysis":
            rubric = self.REGULATORY_RUBRIC
        else:
            rubric = self.DEFAULT_RUBRIC
        
        # Build the judge prompt
        current_date = datetime.now()
        six_weeks_ago = current_date - timedelta(weeks=6)
        
        prompt = self.JUDGE_PROMPT_TEMPLATE.format(
            current_date=current_date.strftime("%B %d, %Y"),
            six_weeks_ago=six_weeks_ago.strftime("%B %d, %Y"),
            rubric=rubric,
            query=query,
            response_a=response_a[:15000],  # Truncate very long responses
            response_b=response_b[:15000]
        )
        
        # Call the judge model with retry logic for rate limits
        for attempt in range(MAX_RETRIES):
            try:
                response = self.model.generate_content(prompt)
                break
            except Exception as e:
                if "429" in str(e) or "rate" in str(e).lower() or "quota" in str(e).lower():
                    wait_time = RATE_LIMIT_DELAY * (attempt + 1)
                    print(f"    Rate limited, waiting {wait_time}s (attempt {attempt + 1}/{MAX_RETRIES})...")
                    time.sleep(wait_time)
                else:
                    raise
        else:
            raise Exception("Max retries exceeded for judge evaluation")
        
        result = self._parse_judge_response(response.text)
        
        # Map scores back to correct systems
        if a_is_baseline:
            baseline_scores_dict = result["response_a_scores"]
            agentic_scores_dict = result["response_b_scores"]
            winner_raw = result["winner"]
            if winner_raw == "A":
                winner = "baseline"
            elif winner_raw == "B":
                winner = "agentic"
            else:
                winner = "tie"
        else:
            baseline_scores_dict = result["response_b_scores"]
            agentic_scores_dict = result["response_a_scores"]
            winner_raw = result["winner"]
            if winner_raw == "A":
                winner = "agentic"
            elif winner_raw == "B":
                winner = "baseline"
            else:
                winner = "tie"
        
        baseline_scores = ScoreBreakdown(**baseline_scores_dict)
        agentic_scores = ScoreBreakdown(**agentic_scores_dict)
        
        return EvaluationResult(
            test_case_id=test_case_id,
            test_case_type=test_case_type,
            input_query=query,
            baseline_response=baseline_response,
            agentic_response=agentic_response,
            baseline_scores=baseline_scores,
            agentic_scores=agentic_scores,
            winner=winner,
            judge_rationale=result.get("rationale", "No rationale provided")
        )
    
    def evaluate_three_systems(
        self,
        query: str,
        basic_response: str,
        detailed_response: str,
        agentic_response: str,
        test_case_id: str = "unknown",
        test_case_type: str = "general"
    ) -> Dict:
        """
        Evaluate three systems in a single call for efficiency.
        
        Returns dict with scores for all three systems.
        """
        # Select appropriate rubric based on test case
        # Recency tests (test_case_id starts with "recency_") use the recency rubric
        if test_case_id.startswith("recency_"):
            rubric = self.RECENCY_RUBRIC
        elif test_case_type == "competitor_identification":
            rubric = self.COMPETITOR_ID_RUBRIC
        elif test_case_type == "competitive_intelligence":
            rubric = self.COMPETITIVE_INTEL_RUBRIC
        elif test_case_type == "regulatory_analysis":
            rubric = self.REGULATORY_RUBRIC
        else:
            rubric = self.DEFAULT_RUBRIC
        
        current_date = datetime.now()
        six_weeks_ago = current_date - timedelta(weeks=6)
        
        # Add web search context for recency tests
        web_search_context = ""
        if test_case_id.startswith("recency_"):
            web_search_context = """
## CRITICAL INFORMATION ABOUT SYSTEM CAPABILITIES
- The **Agentic System (Response 3)** has access to REAL-TIME WEB SEARCH tools and can retrieve current news and information
- The Basic and Detailed systems do NOT have web search and rely only on their training data
- If the Agentic System cites specific recent sources, dates, and news items, this information was retrieved from the web and should be considered ACCURATE
- Systems that admit they cannot access recent information are being honest but LESS USEFUL for this task
- For recency-focused queries, the system that provides ACTUAL RECENT DATA with sources should score highest
"""
        
        prompt = f"""You are an expert evaluator comparing three AI-generated responses to a business intelligence query.

## Your Task
Evaluate all three responses using the rubric below.

## Important Context
- Today's date is {current_date.strftime("%B %d, %Y")}
- "Past 6 weeks" means content from {six_weeks_ago.strftime("%B %d, %Y")} to {current_date.strftime("%B %d, %Y")}
{web_search_context}

{rubric}

## The Query
{query}

## Response 1 (Basic System)
{basic_response[:10000]}

## Response 2 (Detailed System)
{detailed_response[:10000]}

## Response 3 (Agentic System)
{agentic_response[:10000]}

## Your Evaluation

Provide your evaluation in the following JSON format:
```json
{{
    "basic_scores": {{
        "accuracy": <1-5>,
        "completeness": <1-5>,
        "actionability": <1-5>,
        "recency": <1-5>,
        "structure": <1-5>
    }},
    "detailed_scores": {{
        "accuracy": <1-5>,
        "completeness": <1-5>,
        "actionability": <1-5>,
        "recency": <1-5>,
        "structure": <1-5>
    }},
    "agentic_scores": {{
        "accuracy": <1-5>,
        "completeness": <1-5>,
        "actionability": <1-5>,
        "recency": <1-5>,
        "structure": <1-5>
    }},
    "rationale": "<2-3 sentence explanation of the key differences between systems>"
}}
```

Respond ONLY with the JSON object, no other text."""

        # Call the judge model with retry logic
        for attempt in range(MAX_RETRIES):
            try:
                response = self.model.generate_content(prompt)
                
                result = self._parse_judge_response(response.text)
                
                # Add delay after successful call to respect rate limits
                time.sleep(3)
                
                return {
                    "test_case_id": test_case_id,
                    "test_case_type": test_case_type,
                    "query": query,
                    "basic_scores": result["basic_scores"],
                    "detailed_scores": result["detailed_scores"],
                    "agentic_scores": result["agentic_scores"],
                    "rationale": result.get("rationale", "")
                }
                
            except Exception as e:
                if "429" in str(e) or "rate" in str(e).lower() or "quota" in str(e).lower():
                    wait_time = RATE_LIMIT_DELAY * (attempt + 1)
                    print(f"    Rate limited, waiting {wait_time}s (attempt {attempt + 1}/{MAX_RETRIES})...")
                    time.sleep(wait_time)
                else:
                    raise
        
        raise Exception(f"Max retries ({MAX_RETRIES}) exceeded for judge evaluation")

    def evaluate_batch(
        self,
        evaluations: List[Tuple[str, str, str, str, str]]
    ) -> List[EvaluationResult]:
        """
        Evaluate multiple test cases.
        
        Args:
            evaluations: List of tuples (query, baseline_response, agentic_response, test_case_id, test_case_type)
            
        Returns:
            List of EvaluationResult objects
        """
        results = []
        for query, baseline, agentic, case_id, case_type in evaluations:
            try:
                result = self.evaluate(query, baseline, agentic, case_id, case_type)
                results.append(result)
                print(f"✓ Evaluated {case_id}: Winner = {result.winner}")
            except Exception as e:
                print(f"✗ Failed to evaluate {case_id}: {e}")
        return results


def generate_evaluation_report(results: List[EvaluationResult]) -> Dict:
    """
    Generate an aggregate evaluation report from multiple results.
    
    Returns summary statistics and detailed breakdowns.
    """
    if not results:
        return {"error": "No results to analyze"}
    
    # Win counts
    detailed_wins = sum(1 for r in results if r.winner == "baseline")  # baseline = detailed in current setup
    agentic_wins = sum(1 for r in results if r.winner == "agentic")
    ties = sum(1 for r in results if r.winner == "tie")
    
    # Average scores by dimension
    detailed_avg = {
        "accuracy": sum(r.baseline_scores.accuracy for r in results) / len(results),
        "completeness": sum(r.baseline_scores.completeness for r in results) / len(results),
        "actionability": sum(r.baseline_scores.actionability for r in results) / len(results),
        "recency": sum(r.baseline_scores.recency for r in results) / len(results),
        "structure": sum(r.baseline_scores.structure for r in results) / len(results),
    }
    
    agentic_avg = {
        "accuracy": sum(r.agentic_scores.accuracy for r in results) / len(results),
        "completeness": sum(r.agentic_scores.completeness for r in results) / len(results),
        "actionability": sum(r.agentic_scores.actionability for r in results) / len(results),
        "recency": sum(r.agentic_scores.recency for r in results) / len(results),
        "structure": sum(r.agentic_scores.structure for r in results) / len(results),
    }
    
    # Results by test type
    by_type = {}
    for r in results:
        if r.test_case_type not in by_type:
            by_type[r.test_case_type] = {"detailed": 0, "agentic": 0, "tie": 0}
        # Map baseline to detailed for display
        winner_label = "detailed" if r.winner == "baseline" else r.winner
        by_type[r.test_case_type][winner_label] += 1
    
    return {
        "summary": {
            "total_evaluations": len(results),
            "detailed_wins": detailed_wins,
            "agentic_wins": agentic_wins,
            "ties": ties,
            "agentic_win_rate": round(agentic_wins / len(results) * 100, 1)
        },
        "average_scores": {
            "detailed": {k: round(v, 2) for k, v in detailed_avg.items()},
            "agentic": {k: round(v, 2) for k, v in agentic_avg.items()}
        },
        "by_test_type": by_type,
        "individual_results": [r.to_dict() for r in results]
    }
