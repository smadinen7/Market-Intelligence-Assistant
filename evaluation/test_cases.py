"""
Test Cases for LLM-as-a-Judge Evaluation

This module defines standardized test cases for comparing
the baseline Gemini against the multi-agent CrewAI system.
"""

from dataclasses import dataclass
from typing import Optional, List
from enum import Enum


class TestCaseType(Enum):
    """Categories of test cases."""
    COMPETITOR_IDENTIFICATION = "competitor_identification"
    COMPETITIVE_INTELLIGENCE = "competitive_intelligence"
    FINANCIAL_ANALYSIS = "financial_analysis"
    RATIO_ANALYSIS = "ratio_analysis"
    RISK_ASSESSMENT = "risk_assessment"
    CHAT_QUESTION = "chat_question"
    COMPANY_RESEARCH = "company_research"
    REGULATORY_ANALYSIS = "regulatory_analysis"


@dataclass
class TestCase:
    """A single test case for evaluation."""
    id: str
    type: TestCaseType
    name: str
    description: str
    
    # Input parameters
    company_name: Optional[str] = None
    competitor_name: Optional[str] = None
    document_content: Optional[str] = None
    question: Optional[str] = None
    context: Optional[str] = None
    
    # Expected elements (for human reference, not automated checking)
    expected_elements: Optional[List[str]] = None
    
    def get_query_description(self) -> str:
        """Get a human-readable description of what's being tested."""
        if self.type == TestCaseType.COMPETITOR_IDENTIFICATION:
            return f"Identify top 3 competitors for {self.company_name}"
        elif self.type == TestCaseType.COMPETITIVE_INTELLIGENCE:
            return f"Competitive intelligence: {self.competitor_name} vs {self.company_name}"
        elif self.type == TestCaseType.FINANCIAL_ANALYSIS:
            return f"Financial analysis of document ({len(self.document_content or '')} chars)"
        elif self.type == TestCaseType.RATIO_ANALYSIS:
            return f"Financial ratio analysis"
        elif self.type == TestCaseType.RISK_ASSESSMENT:
            return f"Risk assessment"
        elif self.type == TestCaseType.CHAT_QUESTION:
            return f"Question: {self.question[:100]}..."
        elif self.type == TestCaseType.COMPANY_RESEARCH:
            return f"Research company: {self.company_name}"
        elif self.type == TestCaseType.REGULATORY_ANALYSIS:
            return f"Regulatory analysis for: {self.company_name}"
        return self.description


# ============================================================================
# COMPETITOR IDENTIFICATION TEST CASES
# ============================================================================

COMPETITOR_ID_CASES = [
    TestCase(
        id="comp_id_001",
        type=TestCaseType.COMPETITOR_IDENTIFICATION,
        name="Apple Competitors",
        description="Identify Apple's top competitors across hardware and services",
        company_name="Apple",
        expected_elements=["Samsung", "Microsoft", "Google", "market overlap", "threat"]
    ),
    TestCase(
        id="comp_id_002",
        type=TestCaseType.COMPETITOR_IDENTIFICATION,
        name="Tesla Competitors",
        description="Identify Tesla's top competitors in EV and energy",
        company_name="Tesla",
        expected_elements=["BYD", "Rivian", "Ford", "GM", "market share"]
    ),
    TestCase(
        id="comp_id_003",
        type=TestCaseType.COMPETITOR_IDENTIFICATION,
        name="Microsoft Competitors",
        description="Identify Microsoft's top competitors across cloud and software",
        company_name="Microsoft",
        expected_elements=["Amazon", "Google", "Salesforce", "cloud", "enterprise"]
    ),
    TestCase(
        id="comp_id_004",
        type=TestCaseType.COMPETITOR_IDENTIFICATION,
        name="Netflix Competitors",
        description="Identify Netflix's top competitors in streaming",
        company_name="Netflix",
        expected_elements=["Disney+", "Amazon Prime", "HBO Max", "streaming", "content"]
    ),
    TestCase(
        id="comp_id_005",
        type=TestCaseType.COMPETITOR_IDENTIFICATION,
        name="NVIDIA Competitors",
        description="Identify NVIDIA's top competitors in AI/GPU",
        company_name="NVIDIA",
        expected_elements=["AMD", "Intel", "AI chips", "data center"]
    ),
]

# ============================================================================
# COMPETITIVE INTELLIGENCE TEST CASES
# ============================================================================

COMPETITIVE_INTEL_CASES = [
    TestCase(
        id="comp_intel_001",
        type=TestCaseType.COMPETITIVE_INTELLIGENCE,
        name="Apple vs Samsung",
        description="Competitive intelligence on Samsung from Apple's perspective",
        company_name="Apple",
        competitor_name="Samsung",
        expected_elements=[
            "Recent Moves", "Major Markets", "Hero Products",
            "Financial Snapshot", "Direct Threats", "Strategic Recommendations"
        ]
    ),
    TestCase(
        id="comp_intel_002",
        type=TestCaseType.COMPETITIVE_INTELLIGENCE,
        name="Tesla vs BYD",
        description="Competitive intelligence on BYD from Tesla's perspective",
        company_name="Tesla",
        competitor_name="BYD",
        expected_elements=[
            "Recent Moves", "China market", "EV sales",
            "price comparison", "Strategic Recommendations"
        ]
    ),
    TestCase(
        id="comp_intel_003",
        type=TestCaseType.COMPETITIVE_INTELLIGENCE,
        name="Microsoft vs Amazon",
        description="Competitive intelligence on Amazon/AWS from Microsoft's perspective",
        company_name="Microsoft",
        competitor_name="Amazon",
        expected_elements=[
            "AWS", "Azure", "cloud market share",
            "AI services", "Strategic Recommendations"
        ]
    ),
    TestCase(
        id="comp_intel_004",
        type=TestCaseType.COMPETITIVE_INTELLIGENCE,
        name="Coca-Cola vs PepsiCo",
        description="Competitive intelligence on PepsiCo from Coca-Cola's perspective",
        company_name="Coca-Cola",
        competitor_name="PepsiCo",
        expected_elements=[
            "beverage", "snacks", "market share",
            "distribution", "Strategic Recommendations"
        ]
    ),
    TestCase(
        id="comp_intel_005",
        type=TestCaseType.COMPETITIVE_INTELLIGENCE,
        name="NVIDIA vs AMD",
        description="Competitive intelligence on AMD from NVIDIA's perspective",
        company_name="NVIDIA",
        competitor_name="AMD",
        expected_elements=[
            "GPU", "AI chips", "data center",
            "gaming", "Strategic Recommendations"
        ]
    ),
]

# ============================================================================
# FINANCIAL ANALYSIS TEST CASES
# ============================================================================

# Sample financial data for testing - TechCorp (synthetic)
SAMPLE_FINANCIAL_DATA_1 = """
Company: TechCorp Inc.
Fiscal Year 2024 Financial Summary

INCOME STATEMENT:
- Revenue: $45.2 billion (up 12% YoY)
- Cost of Revenue: $28.1 billion
- Gross Profit: $17.1 billion
- Operating Expenses: $8.5 billion
- Operating Income: $8.6 billion
- Net Income: $7.2 billion

BALANCE SHEET:
- Total Assets: $82.4 billion
- Current Assets: $31.2 billion
- Cash & Equivalents: $15.8 billion
- Inventory: $4.2 billion
- Accounts Receivable: $6.8 billion
- Total Liabilities: $35.6 billion
- Current Liabilities: $18.2 billion
- Long-term Debt: $12.4 billion
- Shareholders' Equity: $46.8 billion

CASH FLOW:
- Operating Cash Flow: $12.4 billion
- Capital Expenditures: $3.2 billion
- Free Cash Flow: $9.2 billion

KEY RATIOS:
- P/E Ratio: 24.5
- Market Cap: $176.4 billion
"""

# Microsoft FY2024 10K Summary (extracted from actual filing)
MICROSOFT_10K_FY2024 = """
Company: Microsoft Corporation
Fiscal Year 2024 (ended June 30, 2024) - Form 10-K Summary

OVERVIEW:
Microsoft is a technology company committed to making digital technology and artificial intelligence 
available broadly and responsibly, with a mission to empower every person and organization on the planet.

KEY HIGHLIGHTS FY2024 vs FY2023:
- Microsoft Cloud revenue increased 23% to $137.4 billion
- Office Commercial products and cloud services revenue increased 14% (Office 365 Commercial +16%)
- Office Consumer products and cloud services revenue increased 4% (82.5 million Microsoft 365 subscribers)
- LinkedIn revenue increased 9%
- Dynamics products and cloud services revenue increased 19% (Dynamics 365 +24%)
- Server products and cloud services revenue increased 22% (Azure +30%)
- Windows revenue increased 8% (Windows OEM +7%, Windows Commercial +11%)
- Devices revenue decreased 15%
- Xbox content and services revenue increased 50% (including 44 points from Activision Blizzard acquisition)
- Search and news advertising revenue (ex-TAC) increased 12%
- Operating income increased $20.9 billion or 24% across all segments

MAJOR ACQUISITION:
On October 13, 2023, Microsoft completed its acquisition of Activision Blizzard for $75.4 billion in cash.
Activision Blizzard is now part of the More Personal Computing segment.

SEGMENT PERFORMANCE - Productivity and Business Processes:
- Revenue increased $8.5 billion or 12%
- Operating income increased $6.4 billion or 19%
- Gross margin increased $6.5 billion or 12% driven by Office 365 Commercial

SEGMENT PERFORMANCE - Intelligent Cloud:
- Revenue increased $17.5 billion or 20%
- Server products and cloud services revenue increased $17.8 billion or 22%
- Azure and other cloud services revenue grew 30% driven by consumption-based services

TAX MATTERS:
The company is currently under IRS audit for tax years 2004-2013. The IRS is seeking an additional 
tax payment of $28.9 billion plus penalties and interest, primarily related to intercompany transfer pricing.

RISK FACTORS:
- Intense competition across all markets
- Cybersecurity threats and data breaches
- Regulatory compliance (antitrust, privacy, AI governance)
- Intellectual property risks
- ESG and sustainability requirements
"""

SAMPLE_FINANCIAL_DATA_2 = """
Company: RetailMax Corp
Q3 2024 Earnings Report

Revenue: $12.8 billion (vs $11.2B prior year)
Same-store sales growth: +4.2%
E-commerce revenue: $3.1 billion (+28% YoY)

Gross Margin: 28.4% (down from 29.1%)
Operating Margin: 6.2%
Net Income: $412 million

Balance Sheet Highlights:
- Inventory: $5.8 billion (inventory days: 68)
- Accounts Payable: $4.2 billion
- Long-term Debt: $8.4 billion
- Cash: $1.2 billion

Guidance: Expecting Q4 revenue of $15-16 billion
Challenges: Supply chain costs, wage inflation
"""

FINANCIAL_ANALYSIS_CASES = [
    TestCase(
        id="fin_analysis_001",
        type=TestCaseType.FINANCIAL_ANALYSIS,
        name="Microsoft FY24 10K Analysis",
        description="Analyze Microsoft's FY2024 annual report (10-K)",
        document_content=MICROSOFT_10K_FY2024,
        expected_elements=[
            "cloud growth", "Azure", "AI", "Activision acquisition",
            "segment performance", "risks", "Investment Perspective"
        ]
    ),
    TestCase(
        id="fin_analysis_002",
        type=TestCaseType.FINANCIAL_ANALYSIS,
        name="TechCorp Analysis",
        description="Analyze tech company annual financials",
        document_content=SAMPLE_FINANCIAL_DATA_1,
        expected_elements=[
            "Executive Summary", "revenue growth", "margins",
            "cash flow", "Investment Perspective"
        ]
    ),
    TestCase(
        id="fin_analysis_003",
        type=TestCaseType.FINANCIAL_ANALYSIS,
        name="RetailMax Quarterly",
        description="Analyze retail company quarterly earnings",
        document_content=SAMPLE_FINANCIAL_DATA_2,
        expected_elements=[
            "same-store sales", "e-commerce growth", "margin pressure",
            "guidance", "risks"
        ]
    ),
]

# ============================================================================
# RATIO ANALYSIS TEST CASES
# ============================================================================

RATIO_ANALYSIS_CASES = [
    TestCase(
        id="ratio_001",
        type=TestCaseType.RATIO_ANALYSIS,
        name="TechCorp Ratios",
        description="Calculate financial ratios for tech company",
        document_content=SAMPLE_FINANCIAL_DATA_1,
        expected_elements=[
            "Current Ratio", "Quick Ratio", "ROE", "ROA",
            "Debt-to-Equity", "interpretation"
        ]
    ),
    TestCase(
        id="ratio_002",
        type=TestCaseType.RATIO_ANALYSIS,
        name="Microsoft Margin Analysis",
        description="Analyze profitability metrics from Microsoft 10K",
        document_content=MICROSOFT_10K_FY2024,
        expected_elements=[
            "operating margin", "growth rates", "segment profitability",
            "cloud economics", "interpretation"
        ]
    ),
]

# ============================================================================
# CHAT QUESTION TEST CASES
# ============================================================================

SAMPLE_ANALYSIS_CONTEXT = """
=== Analysis of Samsung ===
TopLine: Samsung remains Apple's primary hardware competitor with $234B revenue.

## Recent Moves (last 6 weeks)
- Launched Galaxy S24 Ultra with enhanced AI features in November 2025
- Announced $15B investment in Texas chip fab expansion
- Partnership with Google on next-gen foldable displays

## Financial Snapshot
- FY2024 Revenue: $234.1 billion
- Operating Profit: $28.4 billion
- Smartphone market share: 19.2% globally

## Strategic Recommendations for Apple
- **[HIGH PRIORITY]** Accelerate foldable iPhone development
  **Action:** Fast-track R&D on foldable display technology
  **Impact:** Counter Samsung's 3-year lead in foldables market

- **[MEDIUM PRIORITY]** Expand manufacturing in India
  **Action:** Increase iPhone production capacity in India to 25%
  **Impact:** Reduce supply chain risk and compete on price in emerging markets
"""

CHAT_QUESTION_CASES = [
    TestCase(
        id="chat_001",
        type=TestCaseType.CHAT_QUESTION,
        name="Priority Recommendation",
        description="Ask about top priority recommendation",
        question="What should we do first?",
        context=SAMPLE_ANALYSIS_CONTEXT,
        expected_elements=["HIGH PRIORITY", "foldable", "action", "implementation"]
    ),
    TestCase(
        id="chat_002",
        type=TestCaseType.CHAT_QUESTION,
        name="Specific Threat",
        description="Ask about specific competitive threat",
        question="How is Samsung's AI chip investment threatening us?",
        context=SAMPLE_ANALYSIS_CONTEXT,
        expected_elements=["chip", "investment", "competitive", "response"]
    ),
    TestCase(
        id="chat_003",
        type=TestCaseType.CHAT_QUESTION,
        name="Implementation Question",
        description="Ask how to implement a recommendation",
        question="How should we accelerate our foldable development?",
        context=SAMPLE_ANALYSIS_CONTEXT,
        expected_elements=["R&D", "timeline", "partnerships", "steps"]
    ),
]

# ============================================================================
# COMPANY RESEARCH TEST CASES
# ============================================================================

COMPANY_RESEARCH_CASES = [
    TestCase(
        id="research_001",
        type=TestCaseType.COMPANY_RESEARCH,
        name="Research NVIDIA",
        description="Comprehensive research on NVIDIA",
        company_name="NVIDIA",
        expected_elements=[
            "AI chips", "data center", "gaming",
            "revenue growth", "competitive position"
        ]
    ),
    TestCase(
        id="research_002",
        type=TestCaseType.COMPANY_RESEARCH,
        name="Research Spotify",
        description="Comprehensive research on Spotify",
        company_name="Spotify",
        expected_elements=[
            "streaming", "podcasts", "subscribers",
            "profitability", "competition"
        ]
    ),
]

# ============================================================================
# REGULATORY ANALYSIS TEST CASES
# ============================================================================

REGULATORY_ANALYSIS_CASES = [
    TestCase(
        id="reg_001",
        type=TestCaseType.REGULATORY_ANALYSIS,
        name="Apple Regulatory",
        description="Analyze regulatory risks and compliance for Apple",
        company_name="Apple",
        expected_elements=[
            "antitrust", "App Store", "privacy", "EU regulations",
            "compliance risks", "cross-border"
        ]
    ),
    TestCase(
        id="reg_002",
        type=TestCaseType.REGULATORY_ANALYSIS,
        name="Meta Regulatory",
        description="Analyze regulatory risks and compliance for Meta",
        company_name="Meta",
        expected_elements=[
            "privacy", "GDPR", "antitrust", "content moderation",
            "FTC", "data protection"
        ]
    ),
    TestCase(
        id="reg_003",
        type=TestCaseType.REGULATORY_ANALYSIS,
        name="Tesla Regulatory",
        description="Analyze regulatory risks and compliance for Tesla",
        company_name="Tesla",
        expected_elements=[
            "autonomous driving", "NHTSA", "safety recalls",
            "emissions credits", "manufacturing regulations"
        ]
    ),
]

# ============================================================================
# RECENCY-FOCUSED TEST CASES (require web search for current info)
# ============================================================================

RECENCY_TEST_CASES = [
    TestCase(
        id="recency_001",
        type=TestCaseType.COMPANY_RESEARCH,
        name="NVIDIA Recent News",
        description="Research NVIDIA's most recent news and announcements from the past 2 weeks",
        company_name="NVIDIA",
        question="What are NVIDIA's most significant announcements and news from the past 2 weeks (late November - December 2025)? Include specific dates, product launches, partnerships, and stock movements.",
        expected_elements=[
            "specific dates", "recent announcements", "stock price",
            "AI developments", "December 2025"
        ]
    ),
    TestCase(
        id="recency_002",
        type=TestCaseType.COMPANY_RESEARCH,
        name="Tesla Recent Developments",
        description="Research Tesla's latest news and developments from December 2025",
        company_name="Tesla",
        question="What are Tesla's most recent news, stock movements, and announcements from December 2025? Include Cybertruck updates, FSD progress, and any regulatory news.",
        expected_elements=[
            "December 2025", "stock price", "Cybertruck",
            "FSD updates", "recent events"
        ]
    ),
    TestCase(
        id="recency_003",
        type=TestCaseType.COMPANY_RESEARCH,
        name="OpenAI Recent News",
        description="Research OpenAI's latest announcements and developments",
        company_name="OpenAI",
        question="What are OpenAI's most recent announcements from November-December 2025? Include any new model releases, partnerships, valuation updates, and leadership news.",
        expected_elements=[
            "GPT updates", "recent releases", "valuation",
            "December 2025", "Sam Altman"
        ]
    ),
]

# ============================================================================
# AGGREGATE TEST CASES
# ============================================================================

TEST_CASES = {
    "competitor_identification": COMPETITOR_ID_CASES,
    "competitive_intelligence": COMPETITIVE_INTEL_CASES,
    "financial_analysis": FINANCIAL_ANALYSIS_CASES,
    "ratio_analysis": RATIO_ANALYSIS_CASES,
    "chat_question": CHAT_QUESTION_CASES,
    "company_research": COMPANY_RESEARCH_CASES,
    "regulatory_analysis": REGULATORY_ANALYSIS_CASES,
    "recency_test": RECENCY_TEST_CASES,
}

# Quick access to all test cases as a flat list
ALL_TEST_CASES: List[TestCase] = []
for category_cases in TEST_CASES.values():
    ALL_TEST_CASES.extend(category_cases)


def get_test_cases_by_type(test_type: TestCaseType) -> List[TestCase]:
    """Get all test cases of a specific type."""
    return [tc for tc in ALL_TEST_CASES if tc.type == test_type]


def get_quick_evaluation_set() -> List[TestCase]:
    """Get a minimal set of test cases for quick evaluation - focused on recency."""
    return [
        RECENCY_TEST_CASES[0],  # NVIDIA recent news (requires web search)
        RECENCY_TEST_CASES[1],  # Tesla recent developments (requires web search)
        RECENCY_TEST_CASES[2],  # OpenAI recent news (requires web search)
        COMPETITIVE_INTEL_CASES[0],  # Apple vs Samsung (benefits from web search)
        REGULATORY_ANALYSIS_CASES[0],  # Apple Regulatory (benefits from web search)
    ]


def get_full_evaluation_set() -> List[TestCase]:
    """Get all test cases for comprehensive evaluation."""
    return ALL_TEST_CASES
