

import streamlit as st
import os
from utils import get_memory, validate_company_name, safe_rerun
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

if "market_sessions" not in st.session_state:
    st.session_state.market_sessions = {}
if "current_market_session_id" not in st.session_state:
    st.session_state.current_market_session_id = None

# If a company was set earlier in this run, restore the active session id when possible
if "current_user_company" in st.session_state and not st.session_state.get("current_market_session_id"):
    # try to find an existing session for that company
    for sid, sess in st.session_state.market_sessions.items():
        try:
            if sess.get("user_company") == st.session_state.get("current_user_company"):
                st.session_state.current_market_session_id = sid
                break
        except Exception:
            continue

# Helper: parse competitor names from AI output
def _parse_competitors(competitor_text):
    pattern = r'\*\*Competitor \d+:\s*([^*\n]+?)\*\*'
    matches = re.findall(pattern, competitor_text or "")
    if matches:
        return [m.strip() for m in matches[:3]]
    # fallback: split on newlines and take first 3 non-empty lines
    lines = [l.strip() for l in (competitor_text or "").splitlines() if l.strip()]
    return lines[:3]




# Instantiate agents/tasks factory
financial_agents = FinancialAgents()
financial_tasks = FinancialTasks()

# --- Simple styling ---
st.markdown("""
<style>
    .hero-section { padding: 2rem 1rem; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- Hero / Company entry ---
with st.container():
    st.markdown("""
    <div class="hero-section">
        <h1>💼 CEO AI Assistant</h1>
        <p>Enter your company to bootstrap a tailored analysis session.</p>
    </div>
    """, unsafe_allow_html=True)

# Main company form and results area
current_session_id = st.session_state.get("current_market_session_id")

if current_session_id:
    # Lock to existing company
    session = st.session_state.market_sessions.get(current_session_id, {})
    user_company = session.get("user_company")
    # Show the company prominently as a title and keep the small caption
    st.title(f"Company: {user_company}")
    st.caption("This app instance is configured for a single company for this session.")

    # Show synthesized company insights if available
    insights = session.get("company_insights")
    if insights:
        st.markdown("**Top Actionable Insights**")
        st.markdown(insights)

    if st.button("Go to Competitive Analysis", use_container_width=True):
        st.switch_page("pages/2_Market_Analysis.py")

else:
    # Show form to enter company (only when no session exists)
    st.header("Start: Enter your company")
    with st.form(key="company_form"):
        company_input = st.text_input(
            "Company Name",
            placeholder="e.g., Apple Inc., Tesla, Microsoft",
        )
        submitted = st.form_submit_button("Enter")

    if submitted:
        if not company_input:
            st.error("Please enter a company name.")
        else:
            is_valid, clean_name = validate_company_name(company_input)
            if not is_valid:
                st.error("Please enter a valid company name.")
            else:
                # Create session
                session_id = str(uuid.uuid4())
                st.session_state.current_market_session_id = session_id
                st.session_state.market_sessions[session_id] = {
                    "title": f"Competitive Intelligence - {company_input}",
                    "session_type": "competitive",
                    "messages": [],
                    "conversation_state": "identifying_competitors",
                    "analysis_data": {},
                    "chat_history": [],
                    "user_company": company_input,
                    "competitors": [],
                    "selected_competitor": None,
                    "competitor_analyses": {},
                    "analysis_results": {},
                    "quick_metrics": {},
                    "company_insights": None
                }
                # Remember company at top-level so the app keeps focus on this company for the run
                st.session_state["current_user_company"] = company_input

                # Add the user company to the knowledge graph (no competitor identification here).
                try:
                    kg = memory.get_knowledge_graph()
                    kg.add_company(company_input, {"is_user_company": True})
                except Exception:
                    pass

                # Synchronously run the company insights synthesis agent so the Home page
                # displays actionable insights immediately (no background jobs).
                try:
                    synth_agent = financial_agents.company_insights_synthesis_agent()
                    # Provide a concise prompt asking for actionable insights; no expert inputs available yet.
                    synth_task = financial_tasks.strategy_synthesis_task(
                        synth_agent,
                        f"Provide the top 10 actionable insights for the CEO of {company_input}. Keep entries short and numbered.",
                        expert_responses=""  # no expert outputs yet; synthesis should rely on KG and agent knowledge
                    )
                    crew = Crew(agents=[synth_agent], tasks=[synth_task], process=Process.sequential)
                    synth_output = crew.kickoff().raw
                    if not synth_output:
                        synth_output = "No insights returned. Try again or visit Competitive Analysis for deeper research."
                    st.session_state.market_sessions[session_id]["company_insights"] = synth_output
                    st.success("Actionable insights generated.")
                    # Force a UI refresh so the new insights appear below the form
                    safe_rerun()
                except Exception as e:
                    st.error(f"Error generating actionable insights: {e}")
