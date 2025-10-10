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
            description=f"""Answer the user's financial analysis question based on the provided context.
            
            User Question: {user_question}
            
            Provide a helpful, accurate, and well-structured response that:
            1. Directly addresses the user's question
            2. Uses the provided context/analysis when relevant
            3. Explains financial concepts in clear, understandable terms
            4. Provides actionable insights when appropriate
            5. Suggests follow-up questions or analysis if helpful
            
            Context (if available):
            {context}""",
            expected_output="A helpful and informative response to the user's financial question.",
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