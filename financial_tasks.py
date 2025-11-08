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
            description=f"""Answer this question directly:

{user_question}

Context:
{context}

Response Rules:
1. State facts directly without phrases like:
   - "Based on the analysis..."
   - "According to the knowledge graph..."
   - "The data shows..."
   - "I can see that..."
   
2. Never mention:
   - The analysis process
   - Data sources
   - The knowledge graph
   - How you got the information
   
3. Instead of:
   "According to the knowledge graph, Apple and Microsoft compete in the software market"
   Say:
   "Apple and Microsoft compete in the software market"

4. If information is missing, simply state:
   "This information is not available" or "This data is not found"

Always write in present tense, declarative statements.""",
            expected_output="Direct factual statements without meta-references.",
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
            
            For each competitor, provide:
            - Company name
            - Brief description (1-2 sentences)
            - Why they are a direct competitor
            - Approximate market position/size
            
            IMPORTANT: Return the results in a structured format with clear competitor names 
            that can be easily parsed. Use this exact format:
            
            **Competitor 1: [Company Name]**
            Description: [Brief description]
            Competitive Overlap: [Why they compete]
            Market Position: [Position/size]
            
            **Competitor 2: [Company Name]**
            ...
            
            **Competitor 3: [Company Name]**
            ...
            
            Company to analyze: {company_name}""",
            expected_output="A list of the top 3 direct competitors with structured information about each.",
            agent=agent
        )

    def competitive_intelligence_task(self, agent, user_company, competitor_company):
        return Task(
            description=f"""Provide comprehensive competitive intelligence analysis comparing {competitor_company} against {user_company}.
            
            Deliver a detailed competitive analysis including:
            
            1. **Company Overview**
               - Brief background of {competitor_company}
               - Business model and key products/services
               - Market position and scale
            
            2. **Recent Strategic Moves** (Past 6-12 months)
               - Major product launches or updates
               - Acquisitions or partnerships
               - Market expansion initiatives
               - Strategic pivots or changes
               - Recent funding or investment rounds
            
            3. **Market Position & Competitive Strategy**
               - Current market share (if available)
               - Competitive advantages and differentiators
               - Target market and customer segments
               - Pricing strategy
               - Distribution channels
            
            4. **Threats to {user_company}**
               - Direct competitive threats
               - Areas where they outperform {user_company}
               - Emerging capabilities that could disrupt
               - Customer segments they're winning
               - Strategic initiatives that pose risks
            
            5. **Financial Comparison**
               - Revenue comparison (if available)
               - Profitability metrics
               - Growth rates
               - Valuation (for public companies)
               - Financial health indicators
               - Investment in R&D/Innovation
            
            6. **Strengths vs Weaknesses**
               - Key competitive strengths of {competitor_company}
               - Notable weaknesses or vulnerabilities
               - Areas where {user_company} has advantages
            
            7. **Strategic Recommendations**
               - How {user_company} should respond
               - Opportunities to exploit competitor weaknesses
               - Defensive strategies needed
               - Areas requiring urgent attention
            
            User's Company: {user_company}
            Competitor Being Analyzed: {competitor_company}""",
            expected_output="A comprehensive competitive intelligence report with actionable insights and strategic recommendations.",
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
            description=f"""Research the following query online:

{query}

Company Context: {company_name}
Additional Context: {context}

Instructions:
1. Focus on finding current, factual information from reliable sources
2. If researching a company, prioritize:
   - Recent news and developments
   - Market position and competitive landscape
   - Financial performance and metrics
   - Products and services
   - Strategic initiatives

3. Present information in these categories:
   - Key Facts: Direct, verifiable information
   - Market Context: Industry trends and market position
   - Competitive Insights: Relative position and competitive dynamics
   - Recent Developments: Latest news and changes (within last 6 months)

Format your response as direct statements without referencing sources or analysis process.""",
            expected_output="Current, factual information presented directly without meta-commentary.",
            agent=agent
        )

    def entity_extraction_task(self, agent, analysis_text, user_company, competitor_company):
        return Task(
            description=f"""Extract structured entities and relationships from the competitive intelligence analysis.
            
            Extract and structure:
            
            **Companies:**
            - Identify all mentioned companies
            - Note their attributes (size, revenue, market position, etc.)
            
            **Products/Services:**
            - List products mentioned for {user_company}
            - List products mentioned for {competitor_company}
            - Note product categories and market segments
            
            **Markets/Industries:**
            - Identify all markets and industry segments mentioned
            - Note market size, growth, and characteristics
            
            **Key People:**
            - Extract names of executives, founders, key personnel
            - Note their roles and companies
            
            **Relationships:**
            - Competitive relationships (who competes with whom)
            - Market relationships (which companies operate in which markets)
            - Product relationships (which company produces which products)
            - Partnership relationships (collaborations, acquisitions)
            
            **Strategic Events:**
            - Recent moves, launches, acquisitions
            - Market entries or exits
            - Strategic partnerships
            
            Format your response as structured data that can be easily parsed:
            
            COMPANIES:
            - [Company Name]: [attributes]
            
            PRODUCTS:
            - [Product Name]: company=[Company], category=[Category]
            
            MARKETS:
            - [Market Name]: [attributes]
            
            PEOPLE:
            - [Person Name]: company=[Company], role=[Role]
            
            RELATIONSHIPS:
            - [Entity1] -> [Relationship Type] -> [Entity2]: [description]
            
            Analysis Text:
            {analysis_text}""",
            expected_output="Structured extraction of entities and relationships in a parseable format.",
            agent=agent
        )
