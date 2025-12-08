from crewai import Task

class FinancialTasks:
    
    def analyze_financial_document_task(self, agent, document_content, analysis_focus="comprehensive"):
        return Task(
            description=f"""Analyze the provided financial document and extract key insights.
            Focus: {analysis_focus}
            
            Please provide a comprehensive analysis including:
            1. **Executive Summary** - Key highlights and overall financial health
            2. **Key Financial Metrics** - Revenue, profit margins, cash flow, debt levels
            3. **Financial Ratios** - Liquidity, profitability, efficiency, and leverage ratios
            4. **Trends Analysis** - Year-over-year changes and multi-year trends
            5. **Strengths & Opportunities** - What the company is doing well
            6. **Risks & Concerns** - Areas of concern or potential red flags
            7. **Investment Perspective** - Overall assessment for potential investors
            
            DOCUMENT CONTENT:
            {document_content}""",
            expected_output="A structured financial analysis report with clear sections and actionable insights.",
            agent=agent
        )

    def research_company_task(self, agent, company_name, analysis_type="fundamental"):
        return Task(
            description=f"""Research and analyze the company: {company_name}
            Analysis Type: {analysis_type}
            
            Provide a comprehensive company analysis including:
            1. **Company Overview** - Business model, industry, key products/services
            2. **Financial Performance** - Recent financial results and key metrics
            3. **Competitive Position** - Market share, competitive advantages
            4. **Management & Governance** - Leadership team and corporate governance
            5. **Growth Prospects** - Future opportunities and strategic initiatives
            6. **Risk Factors** - Key risks and challenges facing the company
            7. **Valuation Assessment** - Current valuation metrics and fair value analysis
            8. **Investment Recommendation** - Buy/Hold/Sell recommendation with rationale
            
            Note: Base your analysis on publicly available information and financial data.
            """,
            expected_output="A detailed company research report with investment recommendation.",
            agent=agent
        )

    def calculate_financial_ratios_task(self, agent, financial_data):
        return Task(
            description=f"""Calculate and analyze key financial ratios from the provided financial data.
            
            Calculate the following ratios and provide interpretation:
            
            **Liquidity Ratios:**
            - Current Ratio
            - Quick Ratio
            - Cash Ratio
            
            **Profitability Ratios:**
            - Gross Profit Margin
            - Operating Profit Margin
            - Net Profit Margin
            - Return on Assets (ROA)
            - Return on Equity (ROE)
            
            **Efficiency Ratios:**
            - Asset Turnover
            - Inventory Turnover
            - Accounts Receivable Turnover
            
            **Leverage Ratios:**
            - Debt-to-Equity Ratio
            - Debt-to-Assets Ratio
            - Interest Coverage Ratio
            
            For each ratio, provide:
            1. The calculated value
            2. What it means (interpretation)
            3. Whether it's good/concerning compared to industry standards
            
            FINANCIAL DATA:
            {financial_data}""",
            expected_output="A comprehensive ratio analysis with calculations, interpretations, and assessments.",
            agent=agent
        )

    def investment_recommendation_task(self, agent, analysis_summary, risk_tolerance="moderate"):
        return Task(
            description=f"""Based on the financial analysis provided, generate an investment recommendation.
            
            Risk Tolerance: {risk_tolerance}
            
            Provide:
            1. **Investment Rating** - Strong Buy/Buy/Hold/Sell/Strong Sell
            2. **Price Target** - If applicable, provide a fair value estimate
            3. **Investment Thesis** - Key reasons supporting the recommendation
            4. **Risk Assessment** - Key risks to consider
            5. **Time Horizon** - Recommended holding period
            6. **Portfolio Allocation** - Suggested position sizing based on risk tolerance
            7. **Monitoring Points** - Key metrics/events to watch
            
            ANALYSIS SUMMARY:
            {analysis_summary}""",
            expected_output="A clear investment recommendation with detailed rationale and risk considerations.",
            agent=agent
        )

    def trend_analysis_task(self, agent, historical_data, period="3-year"):
        return Task(
            description=f"""Analyze financial trends over the specified period: {period}
            
            Identify and analyze:
            1. **Revenue Trends** - Growth patterns, seasonality, cyclicality
            2. **Profitability Trends** - Margin expansion/contraction patterns
            3. **Cash Flow Trends** - Operating cash flow consistency and growth
            4. **Balance Sheet Trends** - Asset quality, debt levels, working capital
            5. **Key Performance Indicators** - Trend analysis of relevant KPIs
            6. **Anomalies & Inflection Points** - Significant changes or unusual patterns
            7. **Forward-Looking Indicators** - Trends that suggest future performance
            
            HISTORICAL DATA:
            {historical_data}""",
            expected_output="A detailed trend analysis with insights about trajectory and future implications.",
            agent=agent
        )

    def risk_assessment_task(self, agent, company_analysis, market_conditions="current"):
        return Task(
            description=f"""Conduct a comprehensive risk assessment based on the company analysis.
            
            Market Conditions: {market_conditions}
            
            Assess the following risk categories:
            
            **Financial Risks:**
            - Liquidity risk
            - Credit risk
            - Leverage risk
            
            **Operational Risks:**
            - Business model risks
            - Competitive risks
            - Management risks
            
            **Market Risks:**
            - Industry cyclicality
            - Economic sensitivity
            - Regulatory risks
            
            **Strategic Risks:**
            - Technology disruption
            - Market disruption
            - Execution risks
            
            For each risk category:
            1. Risk level (Low/Medium/High)
            2. Impact assessment
            3. Likelihood assessment
            4. Mitigation factors
            5. Monitoring indicators
            
            COMPANY ANALYSIS:
            {company_analysis}""",
            expected_output="A comprehensive risk assessment with risk ratings and mitigation strategies.",
            agent=agent
        )

    def peer_comparison_task(self, agent, company_name, industry, key_metrics):
        return Task(
            description=f"""Compare {company_name} against industry peers and benchmarks.
            
            Industry: {industry}
            
            Provide comparative analysis on:
            1. **Financial Performance Comparison** - Key metrics vs peers
            2. **Valuation Comparison** - P/E, P/B, EV/EBITDA vs industry
            3. **Growth Comparison** - Revenue and earnings growth vs peers
            4. **Profitability Comparison** - Margins and returns vs industry average
            5. **Efficiency Comparison** - Operational efficiency metrics
            6. **Risk Profile Comparison** - Risk metrics vs peer group
            7. **Market Position** - Market share and competitive positioning
            8. **Relative Ranking** - Overall ranking within peer group
            
            KEY METRICS:
            {key_metrics}""",
            expected_output="A detailed peer comparison analysis with relative rankings and competitive insights.",
            agent=agent
        )

    def financial_chat_response_task(self, agent, user_question, context=""):
          return Task(
                description=f"""Answer the user's question thoroughly and directly.

Question: {user_question}

This is the context you're working with (includes prior competitor analyses and strategic recommendations):
{context}

IMPORTANT CONTEXT UNDERSTANDING:
- The context contains COMPETITOR ANALYSES with sections like "Strategic Recommendations for [Company]"
- Strategic Recommendations are SUGGESTIONS for actions the user's company SHOULD take - they are NOT real products or announcements
- If the user asks about a recommendation (e.g., "Tesla Lite", "affordable model", etc.), explain HOW to implement it, don't search for it as if it exists
- Distinguish between: (1) Real competitor moves/products to research online, (2) Recommendations that are strategic suggestions

QUESTION INTERPRETATION:
- If user asks "what should we do first" or "first thing" or "priority" or "most important action" - they want the TOP PRIORITY RECOMMENDATION from the Strategic Recommendations section, NOT information about the first competitor
- If user asks about a specific competitor by name, provide info about that competitor
- If user asks "what", "how", "why" about a strategy/recommendation - provide implementation guidance
- "First", "most important", "priority", "start with" = asking for prioritized recommendations, NOT the first competitor in the list

CRITICAL OUTPUT FORMAT RULES (VIOLATING THESE IS A FAILURE):
1. Your FIRST CHARACTER must be the start of the actual answer. NO exceptions.
2. FORBIDDEN phrases at the start: "The user", "I need to", "I will", "I should", "Let me", "This is", "The question", "Looking at", "Based on", "According to", "The relevant", "I'll structure"
3. FORBIDDEN anywhere: "Thought:", "Thinking:", "chain-of-thought", any meta-commentary about your reasoning
4. START with a direct statement answering the question. Example: "Reinforcing privacy as a competitive advantage requires..."
5. If the question is about a RECOMMENDATION, provide detailed implementation guidance - do NOT search for it as news.
6. Provide a comprehensive response: 1-2 line summary + 5-8 detailed bullets with implementation steps.
7. Use present-tense, declarative statements. Be actionable and specific.

WRONG OUTPUT EXAMPLE (DO NOT DO THIS):
"The user is asking for... I need to elaborate... The relevant section..."

CORRECT OUTPUT EXAMPLE:
"Reinforcing privacy as a competitive advantage requires a multi-faceted approach:
- Launch comprehensive marketing campaigns emphasizing on-device AI processing
- Develop clear privacy certifications for all AI features
..."

Your response must be ONLY the final answer with no preamble or reasoning.""",
                expected_output="Direct answer starting with the actual content. NO 'The user is asking', NO 'I need to', NO reasoning shown. Just the answer.",
                agent=agent
          )

    def quick_financial_summary_task(self, agent, company_or_document):
        return Task(
            description=f"""Provide a quick financial summary and key insights.
            
            Generate a concise but comprehensive summary including:
            1. **Key Highlights** (3-5 bullet points)
            2. **Financial Health Score** (1-10 with explanation)
            3. **Main Strengths** (top 3)
            4. **Main Concerns** (top 3)
            5. **Quick Investment View** (Positive/Neutral/Negative with brief rationale)
            
            INPUT:
            {company_or_document}""",
            expected_output="A concise financial summary with key insights and quick assessment.",
            agent=agent
        )

    def identify_competitors_task(self, agent, company_name):
        return Task(
            description=f"""Identify the top 3 direct competitors of {company_name} and explain WHY each is a competitor.

            IMPORTANT: Use the web search tool to find current 2024/2025 competitive landscape data.
            Search for "{company_name} competitors 2024" or "{company_name} competitive analysis 2025".

            Research and identify the 3 biggest direct competitors based on:
            1. Industry overlap and market segment
            2. Product/service similarity
            3. Market share and competitive positioning
            4. Geographic presence
            5. Revenue scale and company size

            FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:
            
            First, output a JSON array with just the competitor names on its own line:
            ["Competitor1", "Competitor2", "Competitor3"]
            
            Then provide a brief explanation for each competitor:
            
            ## Why These Are Key Competitors
            
            **1. [Competitor Name]**
            - Primary overlap: [main area of competition]
            - Key threat: [why they threaten {company_name}]
            
            **2. [Competitor Name]**
            - Primary overlap: [main area of competition]
            - Key threat: [why they threaten {company_name}]
            
            **3. [Competitor Name]**
            - Primary overlap: [main area of competition]
            - Key threat: [why they threaten {company_name}]

            Company to analyze: {company_name}""",
            expected_output='A JSON array followed by a "Why These Are Key Competitors" section explaining each competitor.',
            agent=agent
        )

    def competitive_intelligence_task(self, agent, user_company, competitor_company):
            # Produce a comprehensive, executive-ready competitor analysis focused on recent moves, markets, hero products,
            # financial snapshot, threats, and strategic recommendations. The output should be detailed yet structured,
            # and formatted as Markdown headings so the UI can render sections clearly.
            return Task(
                description=f"""Produce a comprehensive, executive-ready competitor analysis for {competitor_company} vs {user_company}.

    IMPORTANT: You MUST use the web search tool to get CURRENT 2024/2025 data. Do NOT rely on training data.
    - Search for "{competitor_company} Q3 2024 earnings" or "{competitor_company} 2024 annual report" for financials
    - Search for "{competitor_company} news December 2025" or "{competitor_company} latest news" for recent moves
    - The current date is December 2025 - all data should be from 2024 or 2025, NOT 2023 or earlier

    STRICT OUTPUT RULES (MUST FOLLOW):
    1. Output MUST start with a single line beginning with exactly: `TopLine:` (first non-empty line).
    2. Use ONLY the following Markdown sections in this order. Do NOT add, remove, or rename headings:
       - TopLine: One-line summary (1 sentence)
       - ## Recent Moves (last 6 weeks)
       - ## Major Markets
       - ## Hero Products & Focus
       - ## Financial Snapshot (key figures)
       - ## Direct Threats to {user_company}
       - ## Strategic Recommendations for {user_company}
    3. Do NOT include any preamble, planning text, chain-of-thought, process notes, or meta-commentary. Provide no explanations of method.
    4. Provide detailed content with specific facts and figures. Content limits:
       - Recent Moves: 6-10 bullets with specific details (dates, amounts, partner names where available)
       - Major Markets: 4-8 items with market size or share data if available
       - Hero Products: 4-6 lines covering key products/services with brief competitive positioning
       - Financial Snapshot: 6-8 metric lines including revenue, profit, growth rates, market cap (use FY2024 or latest available - NOT 2023)
       - Direct Threats: 6-10 bullets explaining specific competitive threats with impact assessment
       - Strategic Recommendations: 6-8 actionable recommendations with priority levels
    5. If current 2024/2025 information unavailable after searching, use exact phrases: `Not available` (for metrics) or `No recent public news (last 6 weeks)` (for Recent Moves).
    6. Do not include source citations, URLs, or parenthetical provenance. Do not include JSON or wrappers — plain Markdown only.
    7. Output nothing else. If you cannot produce the required sections, respond with exactly: `Information not available`.

    For Strategic Recommendations:
    - Each recommendation must be a specific, actionable item {user_company} can implement
    - Base recommendations on {competitor_company}'s recent moves and strengths
    - Focus on: defensive moves, offensive opportunities, areas to invest, partnerships to consider
    - Format EACH recommendation as a bullet with this EXACT structure:
      * **Brief title** **[HIGH PRIORITY]** or **[MEDIUM PRIORITY]** or **[LOW PRIORITY]**
      
      **Action:** What to do and how to do it
      
      **Impact:** Expected business impact and benefits
    - IMPORTANT: Put title first, then priority level in brackets. Put Action and Impact on separate lines

    CRITICAL: Use web search tool FIRST before answering. Do NOT use 2023 data - search for 2024/2025 figures.
    IMPORTANT: Be thorough and detailed. Executives want comprehensive intelligence, not just summaries.

    User's Company: {user_company}
    Competitor: {competitor_company}""",
                expected_output="Detailed Markdown with the exact required headings (TopLine, Recent Moves, Major Markets, Hero Products, Financial Snapshot, Direct Threats, Strategic Recommendations) and comprehensive bullets with specific facts. All financial data must be from 2024 or latest available.",
                agent=agent
            )

    def regulatory_concerns_task(self, agent, user_company, competitor_company, strategic_recommendations, industry_context):
        return Task(
            description=f"""Quickly identify TOP 3 regulatory concerns for {user_company} in the {industry_context}.

Strategic Recommendations:
{strategic_recommendations}

IMPORTANT: Output ONLY the formatted regulatory summary below. Do NOT include any reasoning, thoughts, planning, or process notes.

Provide a CONCISE regulatory summary in this EXACT format:

## Regulatory & Compliance Concerns

### Key Industry Regulations
- List 2-3 most critical regulations (e.g., antitrust, data privacy, sector rules)
- Mention relevant regulatory bodies (FTC, SEC, FDA, etc.)

### Top Compliance Risks
- Identify 2-3 main regulatory risks from the strategic recommendations
- Format: **Risk** | **Severity** (HIGH/MEDIUM/LOW) | **Quick Mitigation**

### Cross-Border Considerations
- Note any major export controls, data localization, or trade restrictions
- State "None identified" if not applicable

Keep each section to 2-4 concise bullet points. Focus on ACTIONABLE, HIGH-IMPACT concerns only.
Output MUST start with "## Regulatory & Compliance Concerns" - nothing before it.""",
            expected_output="Concise Markdown regulatory summary with 3 sections, focusing on top 2-3 concerns per section. Must start with heading, no preamble or reasoning.",
            agent=agent
        )

    def knowledge_graph_query_task(self, agent, query, graph_context):
        return Task(
            description=f"""Given this competitive intelligence query:

            {query}

            And this competitive data:
            {graph_context}

            Your task:
            1. Analyze the data directly related to the query
            2. Extract only the most relevant facts and relationships
            3. Provide a clear, factual answer
            4. Use simple, declarative statements
            5. Focus specifically on answering the query asked
            
            Format: Provide your response as direct statements without any meta-commentary or analysis framing.""",
            expected_output="Direct factual answer to the query without any meta-analysis.",
            agent=agent
        )

    def strategy_synthesis_task(self, agent, query, expert_responses):
        return Task(
            description=f"""You are a Chief Strategy Officer answering this question:

            {query}

            You have these expert inputs:
            {expert_responses}

            Provide a direct answer that:
            1. Directly addresses the user's question
            2. Synthesizes the most relevant expert insights
            3. Uses concrete, factual statements
            4. Stays focused on the specific question asked
            5. Avoids meta-commentary about analysis or synthesis
            
            Important: Do not mention the experts or the analysis process. Simply provide the answer as if you are directly responding to the question based on your knowledge.""",
            expected_output="Direct answer incorporating expert insights without meta-commentary.",
            agent=agent
        )

    def online_research_task(self, agent, query, company_name="", context=""):
        return Task(
                description=f"""Research the query online and provide detailed, up-to-date findings.

Query: {query}
Company Context: {company_name}
Additional Context: {context}

Instructions:
1. Prioritize news and developments from the LAST 6 WEEKS. If none, explicitly say: "No recent public news (last 6 weeks)".
2. Provide comprehensive, factual bullets with specific details (dates, figures, names).
3. If researching a company, return sections (Markdown headings):
    - Recent News (last 6 weeks): 6-10 bullets with specific details
    - Immediate Market Impact: 3-5 bullets explaining implications
    - Quick Financial Signals (if available): 3-5 bullets with specific numbers or "Not available"
    - Key Takeaways: 2-3 bullets summarizing most important points
4. Do NOT include source citations or meta-commentary. Use present-tense declarative bullets.
5. Include specific numbers, percentages, and dates where available.

Format: Markdown headings and detailed bullets. Aim for comprehensive coverage while staying factual.""",
                expected_output="Detailed, news-focused markdown summary with specific facts and figures (last 6 weeks prioritized).",
                agent=agent
          )

    def entity_extraction_task(self, agent, analysis_text, user_company, competitor_company):
        return Task(
            description=f"""Extract structured entities and relationships from the competitive intelligence analysis.

Extract and structure:

COMPANIES:
- Identify all mentioned companies and provide short attributes (size, public/private, HQ country).

PRODUCTS:
- List products/services mentioned for {user_company} and {competitor_company} (product name: brief category).

MARKETS:
- Identify market segments and geographies mentioned (short list).

PEOPLE:
- Extract named executives and their roles, if mentioned (Name: Role, Company).

RELATIONSHIPS:
- Provide concise relationship lines (e.g., "CompanyA -> competes_with -> CompanyB: direct cloud offering overlap").

STRATEGIC_EVENTS:
- List recent strategic events referenced in the analysis (launches, acquisitions, partnerships) as short bullets.

Format the response so it is machine-parseable: use section headings in ALL CAPS (COMPANIES, PRODUCTS, MARKETS, PEOPLE, RELATIONSHIPS, STRATEGIC_EVENTS) with short bullets under each.
""",
            expected_output="Structured extraction of entities and relationships in a parseable format.",
            agent=agent
        )
