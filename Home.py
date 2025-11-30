import streamlit as st
from utils import get_memory, validate_company_name
from crewai import Crew, Process
from financial_agents import FinancialAgents
from financial_tasks import FinancialTasks
from datetime import datetime
import uuid
import re

st.set_page_config(
    page_title="CEO AI Assistant - Financial Intelligence Platform",
    page_icon="",
    layout="wide"
)

# --- SESSION STATE INITIALIZATION ---
memory = get_memory()

# Initialize market session structures so Market Analysis page finds them
if "market_sessions" not in st.session_state:
    st.session_state.market_sessions = {}
if "current_market_session_id" not in st.session_state:
    st.session_state.current_market_session_id = None

# Helper: parse competitor names from AI output
def _parse_competitors(competitor_text):
    pattern = r'\*\*Competitor \d+:\s*([^*\n]+?)\*\*'
    matches = re.findall(pattern, competitor_text)
    if matches:
        return [m.strip() for m in matches[:3]]
    # fallback: split on newlines and take first 3 non-empty lines
    lines = [l.strip() for l in competitor_text.splitlines() if l.strip()]
    return lines[:3]

# Instantiate agents/tasks factory
financial_agents = FinancialAgents()
financial_tasks = FinancialTasks()

# --- Custom CSS for styling ---
st.markdown("""
<style>
    .hero-section {
        padding: 4rem 2rem;
        text-align: center;
    }
    .hero-section h1 {
        font-size: 3.5rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .hero-section p {
        font-size: 1.25rem;
        color: #4A5568;
        max-width: 600px;
        margin: 1rem auto;
    }
    .cta-button {
        display: inline-block;
        padding: 0.8rem 2rem;
        background-color: #4299E1;
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 1rem;
    }
    .section {
        padding: 3rem 2rem;
    }
    .feature-card {
        background-color: #F7FAFC;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #E2E8F0;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }
    .feature-item {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .feature-item h3 {
        color: #1A202C;
    }
    .workflow-flow {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    .flow-step {
        background-color: #E2E8F0;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        white-space: nowrap;
    }
    .flow-arrow {
        font-size: 1.5rem;
        color: #4A5568;
    }
</style>
""", unsafe_allow_html=True)

# --- Main Content Area ---
# --- Hero Section ---
with st.container():
    st.markdown("""
    <div class="hero-section">
        <h1>💼 CEO AI Assistant</h1>
        <p>Your intelligent financial analysis companion. Get comprehensive insights from company research, financial documents, and data analysis powered by advanced AI agents.</p>
    </div>
    """, unsafe_allow_html=True)
    # --- Quick Start: Set your company and jump to Competitive Analysis ---
    with st.container():
        st.subheader("Start: Enter your company")
        cols = st.columns([3, 1])
        with cols[0]:
            with st.form(key="company_form"):
                home_company_input = st.text_input(
                    "Company Name",
                    placeholder="e.g., Apple Inc., Tesla, Microsoft",
                    help="Enter your company name to pre-load competitor analysis"
                )
                submitted = st.form_submit_button("Enter")

        with cols[1]:
            # Navigate to Market Analysis page; only available after a session is created
            if st.button("Competitive Analysis", use_container_width=True, type="primary"):
                if st.session_state.get("current_market_session_id"):
                    st.switch_page("pages/2_Market_Analysis.py")
                else:
                    st.error("Please enter a company name and press Enter to start analysis before navigating to Competitive Analysis.")

        # If the user submitted the form, start competitor identification on the backend
        if submitted and home_company_input:
            is_valid, clean_name = validate_company_name(home_company_input)
            if not is_valid:
                st.error("Please enter a valid company name.")
            else:
                session_id = str(uuid.uuid4())
                st.session_state.current_market_session_id = session_id
                initial_message = "Welcome to Competitive Intelligence! Identifying top competitors..."
                conversation_state = "identifying_competitors"
                st.session_state.market_sessions[session_id] = {
                    "title": f"Competitive Intelligence - {home_company_input}",
                    "session_type": "competitive",
                    "messages": [{"role": "assistant", "content": initial_message}],
                    "conversation_state": conversation_state,
                    "analysis_data": {},
                    "chat_history": [],
                    "user_company": home_company_input,
                    "competitors": [],
                    "selected_competitor": None,
                    "competitor_analyses": {},
                    "analysis_results": {},
                    "quick_metrics": {}
                }

                try:
                    with st.spinner(f"Identifying top competitors for {home_company_input}..."):
                        competitor_agent = financial_agents.competitor_identification_agent()
                        competitor_task = financial_tasks.identify_competitors_task(competitor_agent, home_company_input)
                        crew = Crew(agents=[competitor_agent], tasks=[competitor_task], process=Process.sequential)
                        competitor_analysis = crew.kickoff().raw

                        competitors = _parse_competitors(competitor_analysis or "")

                        # populate knowledge graph
                        kg = memory.get_knowledge_graph()
                        kg.add_company(home_company_input, {'is_user_company': True})
                        for competitor in competitors:
                            kg.add_company(competitor, {'is_competitor': True})
                            kg.add_relationship(home_company_input, competitor, 'competes_with', {
                                'identified_at': datetime.now().isoformat()
                            })

                        st.session_state.market_sessions[session_id]["competitors"] = competitors
                        st.session_state.market_sessions[session_id]["analysis_data"]["competitor_identification"] = competitor_analysis
                        st.session_state.market_sessions[session_id]["conversation_state"] = "competitors_identified"
                        st.session_state.market_sessions[session_id]["messages"].append({
                            "role": "assistant",
                            "content": f"I've identified the top {len(competitors)} competitors for {home_company_input}:\n\n{competitor_analysis}\n\nGo to 'Market Analysis' to select a competitor for detailed analysis."
                        })
                        memory.update_competitive_intelligence({
                            "user_company": home_company_input,
                            "competitors": competitors,
                            "competitor_identification": competitor_analysis
                        })

                        st.success(f"Started competitor identification for {home_company_input}. Click 'Competitive Analysis' to go to Market Analysis.")
                except Exception as e:
                    st.error(f"Error identifying competitors: {e}")
                    # keep existing home content visible
                    pass
    # (Removed redundant quick-navigation buttons; use the 'Competitive Analysis' button above)

st.markdown("---")

# --- Core Features Section ---
with st.container():
    st.header("Comprehensive Financial Intelligence")
    st.markdown("""
    CEO AI Assistant provides enterprise-grade financial analysis tools powered by advanced AI agents.
    """)
    
    # Financial Analysis Capabilities
    st.subheader("📊 Financial Analysis Capabilities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📄 Document Analysis**
        - Upload PDF financial reports (10-K, 10-Q, annual reports)
        - Process CSV financial data and spreadsheets
        - Extract key metrics automatically
        - Generate comprehensive analysis reports
        """)
        
        st.markdown("""
        **🏢 Company Research**
        - Research any public company by name
        - Fundamental analysis and valuation
        - Industry comparisons and benchmarking
        - Investment recommendations with rationale
        """)
    
    with col2:
        st.markdown("""
        **📈 Advanced Analytics**
        - Financial ratio calculations and interpretation
        - Risk assessment across multiple categories
        - Trend analysis and forecasting
        - Portfolio optimization insights
        """)
        
        st.markdown("""
        **💬 AI-Powered Insights**
        - Interactive chat with financial context
        - Ask follow-up questions about analysis
        - Get explanations in plain language
        - Export professional reports
        """)

    # Workflow demonstration
    st.subheader("🔄 How It Works")
    st.markdown("""
    <div class="workflow-flow">
        <div class="flow-step">Upload Documents or Enter Company</div>
        <div class="flow-arrow">→</div>
        <div class="flow-step">AI Analyzes Data</div>
        <div class="flow-arrow">→</div>
        <div class="flow-step">Interactive Dashboard</div>
        <div class="flow-arrow">→</div>
        <div class="flow-step">Export Reports</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- Why Choose CEO AI Assistant ---
with st.container():
    st.header("Why Choose CEO AI Assistant")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🤖 Multi-Agent AI Architecture")
        st.write("Powered by specialized AI agents including Financial Document Analyzers, Investment Advisors, Risk Assessment Specialists, and Market Comparison Analysts working together for comprehensive insights.")
    with col2:
        st.subheader(" Professional-Grade Analysis")
        st.write("Enterprise-level financial analysis capabilities including ratio analysis, risk assessment, peer comparisons, and investment recommendations typically found in expensive financial software.")
    
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("🔄 Multi-Format Support")
        st.write("Process PDFs, CSV files, and text documents simultaneously. Upload annual reports alongside financial spreadsheets for the most comprehensive analysis possible.")
    with col4:
        st.subheader("💼 Executive-Ready Reports")
        st.write("Generate professional reports and presentations ready for board meetings, investor presentations, or strategic planning sessions with downloadable formats.")

st.divider()

# --- Final CTA Section ---
with st.container():
    st.markdown("""
    <div class="hero-section">
        <h2>Ready to Make Smarter Financial Decisions?</h2>
        <p>Transform complex financial data into actionable insights. Let CEO AI Assistant analyze companies, assess risks, and provide investment recommendations with the power of advanced AI.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Internal Analysis Now", use_container_width=True, type="primary"):
            st.switch_page("pages/1_Internal_Analysis.py")
    with col2:
        if st.button("📈 Market Analysis Now", use_container_width=True, type="secondary"):
            st.switch_page("pages/2_Market_Analysis.py")
