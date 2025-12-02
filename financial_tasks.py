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
                description=f"""Answer the user's question briefly and directly.

Question: {user_question}
Context: {context}

Rules for response (strict):
1. Provide a one-line top summary (1 sentence) followed by up to 3 short bullets if needed.
2. Do NOT use phrases like: "according to", "based on", "the data shows", or any meta-commentary about sources or process.
3. Use present-tense, declarative statements. Keep each bullet under ~18 words.
4. If the answer requires numbers or metrics, present only the most essential figures (no long tables).
5. If information is not available locally, run online checks and then answer; if still missing, reply: "Information not available."

Format: 1-line summary + up to 3 bullets. Total answer should be short — suitable for a CEO to read in 10 seconds.""",
                expected_output="Very short, direct answer (1 line + up to 3 bullets).",
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
            description=f"""Identify the top 3 direct competitors of {company_name}.

            Research and identify the 3 biggest direct competitors based on:
            1. Industry overlap and market segment
            2. Product/service similarity
            3. Market share and competitive positioning
            4. Geographic presence
            5. Revenue scale and company size

            IMPORTANT: For reliable downstream parsing, return ONLY a JSON array containing
            the competitor names (strings) and nothing else. The JSON array must contain
            up to 3 company names (strings). Do NOT include any explanatory text, headings,
            or other content outside the JSON array.

            Examples (valid outputs):
            ["Company A", "Company B", "Company C"]
            ["Company A"]

            Company to analyze: {company_name}""",
            expected_output='A JSON array (e.g., ["Company A","Company B","Company C"]) containing up to 3 company names only.',
            agent=agent
        )

    def competitive_intelligence_task(self, agent, user_company, competitor_company):
            # Produce a concise, executive-ready competitor analysis focused on recent moves, markets, hero products,
            # financial snapshot, and explicit threats to the user's company. The output MUST be short, to-the-point,
            # and formatted as Markdown headings so the UI can render sections clearly.
            return Task(
                description=f"""Produce a concise, executive-ready competitor analysis for {competitor_company} vs {user_company}.

    STRICT OUTPUT RULES (MUST FOLLOW):
    1. Output MUST start with a single line beginning with exactly: `TopLine:` (first non-empty line).
    2. Use ONLY the following Markdown sections in this order. Do NOT add, remove, or rename headings:
       - TopLine: One-line summary (1 sentence)
       - ## Recent Moves (last 6 weeks)
       - ## Major Markets
       - ## Hero Products & Focus
       - ## Financial Snapshot (key figures)
       - ## Direct Threats to {user_company}
    3. Do NOT include any preamble, planning text, chain-of-thought, process notes, or meta-commentary. Provide no explanations of method.
    4. Keep content extremely concise: bullets only where requested; adhere to limits (Recent Moves up to 6 bullets; Major Markets 3-6 items; Hero Products up to 3 short lines; Financial Snapshot up to 5 short metric lines; Direct Threats up to 6 bullets).
    5. If information unavailable, use exact phrases: `Not available` (for metrics) or `No recent public news (last 6 weeks)` (for Recent Moves).
    6. Do not include source citations, URLs, or parenthetical provenance. Do not include JSON or wrappers — plain Markdown only.
    7. Output nothing else. If you cannot produce the required sections, respond with exactly: `Information not available`.

    Notes for the agent:
    1. Use the knowledge graph and stored analysis first, then perform online checks (news and filings) to update Recent Moves.
    2. Restrict Recent Moves to the last ~6 weeks only.
    3. When citing financials, prefer official filings (10-K/10-Q) or company releases; if exact figures are not found, use `Not available`.

    User's Company: {user_company}
    Competitor: {competitor_company}""",
                expected_output="Markdown with the exact required headings (TopLine then the listed H2s) and concise bullets.",
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
                description=f"""Research the query online and provide concise, up-to-date findings.

Query: {query}
Company Context: {company_name}
Additional Context: {context}

Instructions:
1. Prioritize news and developments from the LAST 6 WEEKS. If none, explicitly say: "No recent public news (last 6 weeks)".
2. Focus on short, factual bullets. Output must be concise — executives only.
3. If researching a company, return sections (Markdown headings):
    - Recent News (last 6 weeks): up to 6 bullets
    - Immediate Market Impact: 1-3 bullets
    - Quick Financial Signals (if available): 1-3 bullets or "Not available"
4. Do NOT include source citations or meta-commentary. Use present-tense declarative bullets.

Format: Markdown headings and short bullets. Keep total output under ~150 words where possible.""",
                expected_output="Concise, news-focused markdown summary (last 6 weeks prioritized).",
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
