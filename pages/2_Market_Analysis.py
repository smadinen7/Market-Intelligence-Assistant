import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew, Process
from financial_agents import FinancialAgents
from financial_tasks import FinancialTasks
from utils import validate_company_name, get_memory
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="CEO AI Assistant - Market Analysis", page_icon="📈", layout="wide")

memory = get_memory()
memory.set_focus("market_analysis")

st.markdown("""
<style>
    .centered-cell .stButton > button {
        margin: 0 auto;
        display: block;
    }
    .analysis-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        background-color: #fafafa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
    .metric-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        margin: 20px 0;
    }
    .metric-item {
        text-align: center;
        margin: 10px;
        padding: 15px;
        background-color: #f0f2f6;
        border-radius: 8px;
        min-width: 120px;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "market_sessions" not in st.session_state:
    st.session_state.market_sessions = {}
if "current_market_session_id" not in st.session_state:
    st.session_state.current_market_session_id = None
if "editing_market_session_id" not in st.session_state:
    st.session_state.editing_market_session_id = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- HELPER FUNCTIONS ---
def get_current_market_session():
    if st.session_state.current_market_session_id:
        return st.session_state.market_sessions.get(st.session_state.current_market_session_id)
    return None

def new_market_session():
    session_id = str(uuid.uuid4())
    st.session_state.current_market_session_id = session_id
    
    initial_message = "Welcome to CEO AI Assistant! Enter a company name to get started with comprehensive company research and analysis."
    conversation_state = "awaiting_company"
    title = "Company Research Session"
    
    st.session_state.market_sessions[session_id] = {
        "title": title,
        "session_type": "company",
        "messages": [{"role": "assistant", "content": initial_message}],
        "conversation_state": conversation_state,
        "analysis_data": {},
        "chat_history": [],
        "company_name": "",
        "analysis_results": {},
        "quick_metrics": {}
    }
    st.session_state.editing_market_session_id = None

# --- AGENT & TASK DEFINITIONS ---
financial_agents = FinancialAgents()
financial_tasks = FinancialTasks()

# --- SIDEBAR: SESSION MANAGEMENT ---
with st.sidebar:
    st.title("📈 Market Analysis")
    st.markdown("Competitor and Market Intelligence")

    if st.button("🏢 Research Company", use_container_width=True, type="primary"):
        new_market_session()
        st.rerun()

# --- MAIN LAYOUT ---
main_col, chat_col = st.columns([2, 1])

with main_col:
    session = get_current_market_session()

    if not session:
        st.info("Start a new market analysis session from the sidebar to begin your AI-powered analysis.")
    else:
        st.title("📈 Market Analysis")

        analysis_tab, metrics_tab = st.tabs(["📊 Analysis", "📈 Key Metrics"])

        with analysis_tab:
            st.header("Market Analysis Workspace")
            
            # Progress indicator
            state = session.get("conversation_state", "start")
            if state in ["awaiting_company"]:
                progress_value = 0.2
            elif state in ["researching_company"]:
                progress_value = 0.6
            elif state in ["analysis__complete"]:
                progress_value = 1.0
            else:
                progress_value = 0.4
            
            st.progress(progress_value)
            
            # Display conversation messages
            for message in session.get("messages", []):
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Handle different conversation states
            if state == "awaiting_company":
                company_input = st.text_input(
                    "Enter Company Name", 
                    placeholder="e.g., Apple Inc., Microsoft, Tesla",
                    help="Enter the full company name or ticker symbol"
                )
                
                if st.button("🔍 Analyze Company") and company_input:
                    is_valid, clean_name = validate_company_name(company_input)
                    if is_valid:
                        with st.spinner(f"Researching {company_input}..."):
                            try:
                                session["company_name"] = company_input
                                session["messages"].append({"role": "user", "content": f"Analyze {company_input}"})
                                
                                # Company research
                                researcher_agent = financial_agents.company_research_agent()
                                research_task = financial_tasks.research_company_task(researcher_agent, company_input)
                                crew = Crew(agents=[researcher_agent], tasks=[research_task], process=Process.sequential)
                                company_analysis = crew.kickoff().raw
                                
                                session["analysis_data"]["company_analysis"] = company_analysis
                                memory.update_market_analysis({"company_analysis": company_analysis, "company_name": company_input})
                                session["messages"].append({"role": "assistant", "content": f"Research complete for {company_input}!\n\n{company_analysis}\n\nYou can now explore detailed metrics, ask specific questions, or request additional analysis."})
                                session["conversation_state"] = "analysis_complete"
                                session["title"] = f"Company Analysis - {company_input}"
                                
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error researching company: {e}")
                    else:
                        st.error("Please enter a valid company name.")

            elif state == "analysis_complete":
                st.success("✅ Analysis complete! Use the tabs above to explore detailed insights, metrics, and AI chat.")

        with metrics_tab:
            st.header("📈 Key Financial Metrics")
            
            if session.get("analysis_data"):
                # Generate detailed ratio analysis
                if st.button("📊 Generate Ratio Analysis", use_container_width=True):
                    with st.spinner("Calculating financial ratios..."):
                        try:
                            ratio_agent = financial_agents.financial_ratio_analyst_agent()
                            
                            analysis_input = session["analysis_data"].get("company_analysis", "")
                            
                            ratio_task = financial_tasks.calculate_financial_ratios_task(ratio_agent, analysis_input)
                            crew = Crew(agents=[ratio_agent], tasks=[ratio_task], process=Process.sequential)
                            ratio_analysis = crew.kickoff().raw
                            
                            session["analysis_data"]["ratio_analysis"] = ratio_analysis
                            memory.update_market_analysis({"ratio_analysis": ratio_analysis})
                            st.success("Ratio analysis complete!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error generating ratio analysis: {e}")

                # Display generated analyses
                if "ratio_analysis" in session["analysis_data"]:
                    with st.expander("📊 Financial Ratio Analysis", expanded=True):
                        st.markdown(session["analysis_data"]["ratio_analysis"])

            else:
                st.info("Complete an analysis first to view financial metrics.")

with chat_col:
    st.header("💬 AI Financial Analyst Chat")

    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about the analysis..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing your question..."):
                try:
                    # Get AI response
                    context = memory.get_chat_context()
                    chat_agent = financial_agents.company_research_agent()
                    chat_task = financial_tasks.financial_chat_response_task(chat_agent, prompt, context)
                    crew = Crew(agents=[chat_agent], tasks=[chat_task], process=Process.sequential)
                    response = crew.kickoff().raw
                    
                    st.markdown(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {e}"
                    st.markdown(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
