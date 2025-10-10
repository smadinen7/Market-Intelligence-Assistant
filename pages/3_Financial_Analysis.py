import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew, Process
from financial_agents import FinancialAgents
from financial_tasks import FinancialTasks
from utils import process_financial_documents, validate_company_name, format_financial_number
import uuid
import re
from datetime import datetime

# Load environment variables
load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="CEO AI Assistant - Financial Analysis", page_icon="�", layout="wide")

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
if "financial_sessions" not in st.session_state:
    st.session_state.financial_sessions = {}
if "current_financial_session_id" not in st.session_state:
    st.session_state.current_financial_session_id = None
if "editing_financial_session_id" not in st.session_state:
    st.session_state.editing_financial_session_id = None
if "active_financial_tab" not in st.session_state:
    st.session_state.active_financial_tab = "📊 Analysis"

# --- HELPER FUNCTIONS ---
def get_current_financial_session():
    if st.session_state.current_financial_session_id:
        return st.session_state.financial_sessions.get(st.session_state.current_financial_session_id)
    return None

def new_financial_session(session_type="document"):
    session_id = str(uuid.uuid4())
    st.session_state.current_financial_session_id = session_id
    
    if session_type == "document":
        initial_message = "Welcome to CEO AI Assistant! Upload a financial document (annual report, 10-K, earnings report) to get started with comprehensive analysis."
        conversation_state = "awaiting_document"
        title = "Document Analysis Session"
    else:  # company research
        initial_message = "Welcome to CEO AI Assistant! Enter a company name to get started with comprehensive company research and analysis."
        conversation_state = "awaiting_company"
        title = "Company Research Session"
    
    st.session_state.financial_sessions[session_id] = {
        "title": title,
        "session_type": session_type,
        "messages": [{"role": "assistant", "content": initial_message}],
        "conversation_state": conversation_state,
        "analysis_data": {},
        "chat_history": [],
        "document_content": "",
        "company_name": "",
        "analysis_results": {},
        "quick_metrics": {}
    }
    st.session_state.editing_financial_session_id = None

def create_mock_financial_session():
    """Creates a pre-populated financial session for testing purposes."""
    session_id = str(uuid.uuid4())
    st.session_state.current_financial_session_id = session_id
    st.session_state.financial_sessions[session_id] = {
        "title": "Mock Financial Analysis - Apple Inc.",
        "session_type": "company",
        "messages": [{"role": "assistant", "content": "Mock financial analysis session loaded for Apple Inc."}],
        "conversation_state": "analysis_complete",
        "analysis_data": {
            "company_overview": "Apple Inc. is a multinational technology company...",
            "financial_health": "Strong financial position with excellent liquidity...",
            "key_metrics": {
                "revenue": "394.3B",
                "net_income": "99.8B", 
                "total_assets": "352.8B",
                "cash": "29.0B"
            }
        },
        "chat_history": [],
        "document_content": "",
        "company_name": "Apple Inc.",
        "analysis_results": {
            "investment_rating": "Buy",
            "financial_health_score": 9.2,
            "key_strengths": ["Strong brand", "Excellent margins", "Solid balance sheet"],
            "key_risks": ["Regulatory scrutiny", "Market saturation", "Dependence on iPhone"]
        },
        "quick_metrics": {
            "P/E Ratio": "28.5",
            "ROE": "147.4%",
            "Debt/Equity": "1.73",
            "Current Ratio": "0.94"
        }
    }
    st.session_state.editing_financial_session_id = None
    st.toast("Mock financial session created successfully!")
    st.rerun()

# --- AGENT & TASK DEFINITIONS ---
financial_agents = FinancialAgents()
financial_tasks = FinancialTasks()

# --- SIDEBAR: SESSION MANAGEMENT ---
with st.sidebar:
    st.title("� CEO AI Assistant")
    st.markdown("Financial Intelligence Platform")

    if st.button("📄 Analyze Document", use_container_width=True, type="primary"):
        new_financial_session("document")
        st.rerun()

    if st.button("🏢 Research Company", use_container_width=True, type="secondary"):
        new_financial_session("company")
        st.rerun()
    
    if st.button("🧪 Load Test Session", use_container_width=True):
        create_mock_financial_session()

    st.divider()
    if st.session_state.financial_sessions:
        st.subheader("📜 Session History")
        for session_id, session_data in reversed(list(st.session_state.financial_sessions.items())):
            is_active = (session_id == st.session_state.current_financial_session_id)
            label = f"**▶ {session_data['title']}**" if is_active else session_data['title']
            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
            with col1:
                if st.button(label, key=f"load_fin_{session_id}", use_container_width=True):
                    st.session_state.current_financial_session_id = session_id
                    st.session_state.editing_financial_session_id = None
                    st.session_state.active_financial_tab = "📊 Analysis"
                    st.rerun()
            with col2.container(border=False):
                if st.button("✏️", key=f"start_edit_fin_{session_id}", use_container_width=True):
                    st.session_state.editing_financial_session_id = session_id
                    st.rerun()
            with col3.container(border=False):
                if st.button("🗑️", key=f"delete_fin_{session_id}", use_container_width=True):
                    del st.session_state.financial_sessions[session_id]
                    if st.session_state.current_financial_session_id == session_id:
                        st.session_state.current_financial_session_id = None
                    st.rerun()

            if st.session_state.editing_financial_session_id == session_id:
                new_title = st.text_input("New title", value=session_data["title"], key=f"edit_fin_{session_id}", label_visibility="collapsed")
                if new_title != session_data["title"]:
                    st.session_state.financial_sessions[session_id]["title"] = new_title
                    st.session_state.editing_financial_session_id = None
                    st.rerun()

# --- MAIN CONTENT AREA ---
session = get_current_financial_session()

if not session:
    st.info("Start a new financial analysis session from the sidebar to begin your AI-powered analysis.")
else:
    st.title("💼 CEO AI Assistant - Financial Intelligence")

    analysis_tab, metrics_tab, chat_tab, reports_tab = st.tabs(["📊 Analysis", "📈 Key Metrics", "💬 AI Chat", "📋 Reports"])

    with analysis_tab:
        st.header("Financial Analysis Workspace")
        
        # Progress indicator
        state = session.get("conversation_state", "start")
        if state in ["awaiting_document", "awaiting_company"]:
            progress_value = 0.2
        elif state in ["processing_document", "researching_company"]:
            progress_value = 0.6
        elif state in ["analysis_complete"]:
            progress_value = 1.0
        else:
            progress_value = 0.4
        
        st.progress(progress_value)
        
        # Display conversation messages
        for message in session.get("messages", []):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Handle different conversation states
        if state == "awaiting_document":
            uploaded_files = st.file_uploader(
                "Upload Financial Documents", 
                type=['pdf', 'txt', 'md', 'csv'],  # Added 'csv' support
                accept_multiple_files=True,
                help="Upload annual reports, 10-K filings, earnings reports, CSVs, or other financial documents"
            )
            
            if uploaded_files:
                with st.spinner("Processing financial documents..."):
                    try:
                        document_content, extracted_metrics = process_financial_documents(uploaded_files)
                        session["document_content"] = document_content
                        session["analysis_data"]["extracted_metrics"] = extracted_metrics
                        
                        # Quick analysis
                        analyzer_agent = financial_agents.financial_document_analyzer_agent()
                        quick_task = financial_tasks.quick_financial_summary_task(analyzer_agent, document_content)
                        crew = Crew(agents=[analyzer_agent], tasks=[quick_task], process=Process.sequential)
                        quick_summary = crew.kickoff().raw
                        
                        session["messages"].append({"role": "user", "content": f"Uploaded {len(uploaded_files)} financial document(s)."})
                        session["messages"].append({"role": "assistant", "content": f"Documents processed successfully! Here's a quick summary:\n\n{quick_summary}\n\nYou can now ask questions about the analysis or request specific types of analysis from the other tabs."})
                        session["conversation_state"] = "analysis_complete"
                        session["analysis_data"]["quick_summary"] = quick_summary
                        
                        # Update session title
                        file_names = [f.name for f in uploaded_files]
                        session["title"] = f"Document Analysis - {file_names[0]}" + (f" (+{len(file_names)-1} more)" if len(file_names) > 1 else "")
                        
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error processing documents: {e}")

        elif state == "awaiting_company":
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
            
            # Display quick summary if available
            if "quick_summary" in session["analysis_data"]:
                with st.expander("📋 Quick Summary", expanded=True):
                    st.markdown(session["analysis_data"]["quick_summary"])

    with metrics_tab:
        st.header("📈 Key Financial Metrics")
        
        if session.get("analysis_data"):
            # Display metrics based on session type
            if session.get("session_type") == "document" and "extracted_metrics" in session["analysis_data"]:
                st.subheader("Extracted Metrics from Documents")
                
                metrics = session["analysis_data"]["extracted_metrics"]
                if metrics:
                    for file_name, file_metrics in metrics.items():
                        with st.expander(f"📄 {file_name}"):
                            if file_metrics:
                                cols = st.columns(3)
                                col_idx = 0
                                for metric_name, values in file_metrics.items():
                                    with cols[col_idx % 3]:
                                        st.metric(
                                            label=metric_name.replace('_', ' ').title(),
                                            value=values[0] if values else "N/A"
                                        )
                                    col_idx += 1
                            else:
                                st.info("No financial metrics detected in this document.")
                else:
                    st.info("No financial metrics were extracted from the uploaded documents.")
            
            # Generate detailed ratio analysis
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("📊 Generate Ratio Analysis", use_container_width=True):
                    with st.spinner("Calculating financial ratios..."):
                        try:
                            ratio_agent = financial_agents.financial_ratio_analyst_agent()
                            
                            # Use document content or company analysis as input
                            analysis_input = session["analysis_data"].get("company_analysis", "") or session.get("document_content", "")
                            
                            ratio_task = financial_tasks.calculate_financial_ratios_task(ratio_agent, analysis_input)
                            crew = Crew(agents=[ratio_agent], tasks=[ratio_task], process=Process.sequential)
                            ratio_analysis = crew.kickoff().raw
                            
                            session["analysis_data"]["ratio_analysis"] = ratio_analysis
                            st.success("Ratio analysis complete!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error generating ratio analysis: {e}")

            with col2:
                if st.button("⚠️ Generate Risk Assessment", use_container_width=True):
                    with st.spinner("Assessing risks..."):
                        try:
                            risk_agent = financial_agents.risk_assessment_agent()
                            
                            analysis_input = session["analysis_data"].get("company_analysis", "") or session.get("document_content", "")
                            
                            risk_task = financial_tasks.risk_assessment_task(risk_agent, analysis_input)
                            crew = Crew(agents=[risk_agent], tasks=[risk_task], process=Process.sequential)
                            risk_analysis = crew.kickoff().raw
                            
                            session["analysis_data"]["risk_analysis"] = risk_analysis
                            st.success("Risk assessment complete!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error generating risk assessment: {e}")

            # Display generated analyses
            if "ratio_analysis" in session["analysis_data"]:
                with st.expander("📊 Financial Ratio Analysis", expanded=True):
                    st.markdown(session["analysis_data"]["ratio_analysis"])

            if "risk_analysis" in session["analysis_data"]:
                with st.expander("⚠️ Risk Assessment", expanded=True):
                    st.markdown(session["analysis_data"]["risk_analysis"])

        else:
            st.info("Complete an analysis first to view financial metrics.")

    with chat_tab:
        st.header("💬 AI Financial Analyst Chat")
        
        if session.get("conversation_state") == "analysis_complete":
            # Display chat history
            for chat in session.get("chat_history", []):
                with st.chat_message(chat["role"]):
                    st.markdown(chat["content"])

            # Chat input
            if prompt := st.chat_input("Ask about the financial analysis..."):
                session["chat_history"].append({"role": "user", "content": prompt})
                
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner("Analyzing your question..."):
                        try:
                            # Prepare context from analysis data
                            context = ""
                            if "company_analysis" in session["analysis_data"]:
                                context += f"Company Analysis:\n{session['analysis_data']['company_analysis']}\n\n"
                            if "quick_summary" in session["analysis_data"]:
                                context += f"Summary:\n{session['analysis_data']['quick_summary']}\n\n"
                            if "ratio_analysis" in session["analysis_data"]:
                                context += f"Ratio Analysis:\n{session['analysis_data']['ratio_analysis']}\n\n"
                            if session.get("document_content"):
                                context += f"Document Content (excerpt):\n{session['document_content'][:2000]}...\n\n"

                            # Get AI response
                            chat_agent = financial_agents.financial_document_analyzer_agent()
                            chat_task = financial_tasks.financial_chat_response_task(chat_agent, prompt, context)
                            crew = Crew(agents=[chat_agent], tasks=[chat_task], process=Process.sequential)
                            response = crew.kickoff().raw
                            
                            st.markdown(response)
                            session["chat_history"].append({"role": "assistant", "content": response})
                        except Exception as e:
                            error_msg = f"Sorry, I encountered an error: {e}"
                            st.markdown(error_msg)
                            session["chat_history"].append({"role": "assistant", "content": error_msg})
        else:
            st.info("Complete a financial analysis first to start chatting with the AI analyst.")

    with reports_tab:
        st.header("📋 Analysis Reports")
        
        if session.get("conversation_state") == "analysis_complete":
            # Generate investment recommendation
            if st.button("💡 Generate Investment Recommendation", use_container_width=True):
                with st.spinner("Generating investment recommendation..."):
                    try:
                        advisor_agent = financial_agents.investment_advisor_agent()
                        
                        # Prepare analysis summary
                        analysis_summary = ""
                        if "company_analysis" in session["analysis_data"]:
                            analysis_summary += session["analysis_data"]["company_analysis"]
                        if "ratio_analysis" in session["analysis_data"]:
                            analysis_summary += f"\n\nRatio Analysis:\n{session['analysis_data']['ratio_analysis']}"
                        
                        investment_task = financial_tasks.investment_recommendation_task(advisor_agent, analysis_summary)
                        crew = Crew(agents=[advisor_agent], tasks=[investment_task], process=Process.sequential)
                        investment_rec = crew.kickoff().raw
                        
                        session["analysis_data"]["investment_recommendation"] = investment_rec
                        st.success("Investment recommendation generated!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error generating investment recommendation: {e}")

            # Display reports
            if "investment_recommendation" in session["analysis_data"]:
                st.subheader("💡 Investment Recommendation")
                st.markdown(f"""
                    <div class="analysis-card">
                        {session["analysis_data"]["investment_recommendation"]}
                    </div>
                """, unsafe_allow_html=True)

            # Download options
            st.subheader("📥 Export Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if "company_analysis" in session["analysis_data"] or session.get("document_content"):
                    report_content = f"""
# Financial Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Analysis Summary
{session["analysis_data"].get("company_analysis", "") or session["analysis_data"].get("quick_summary", "")}

## Ratio Analysis
{session["analysis_data"].get("ratio_analysis", "Not generated")}

## Risk Assessment  
{session["analysis_data"].get("risk_analysis", "Not generated")}

## Investment Recommendation
{session["analysis_data"].get("investment_recommendation", "Not generated")}
"""
                    st.download_button(
                        "📄 Download Full Report",
                        data=report_content,
                        file_name=f"financial_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

            with col2:
                if session.get("chat_history"):
                    chat_export = "\n".join([f"{msg['role'].upper()}: {msg['content']}\n" for msg in session["chat_history"]])
                    st.download_button(
                        "💬 Download Chat History", 
                        data=chat_export,
                        file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

        else:
            st.info("Complete a financial analysis first to generate reports.")