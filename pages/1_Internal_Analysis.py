import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew, Process
from financial_agents import FinancialAgents
from financial_tasks import FinancialTasks
from utils import process_financial_documents, get_memory
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="CEO AI Assistant - Internal Analysis", page_icon="📄", layout="wide")

memory = get_memory()
memory.set_focus("internal_analysis")

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
if "internal_session" not in st.session_state:
    st.session_state.internal_session = None

# --- HELPER FUNCTIONS ---
def get_current_internal_session():
    return st.session_state.internal_session

def new_internal_session():
    """Create a new internal analysis session (replaces any existing one)."""
    st.session_state.internal_session = {
        "id": str(uuid.uuid4()),
        "title": "Document Analysis Session",
        "session_type": "document",
        "messages": [],
        "conversation_state": "awaiting_document",
        "analysis_data": {},
        "chat_history": [],  # Per-session chat history
        "document_content": "",
        "analysis_results": {},
        "quick_metrics": {}
    }
    return st.session_state.internal_session

def reset_session():
    """Reset the current session to start fresh."""
    st.session_state.internal_session = None

# --- AGENT & TASK DEFINITIONS ---
financial_agents = FinancialAgents()
financial_tasks = FinancialTasks()

# --- MAIN LAYOUT ---
session = get_current_internal_session()

# If no session exists, show the welcome/upload interface
if not session:
    st.title("📄 Internal Analysis")
    st.markdown("---")
    
    st.header("Upload financial documents to get started")
    st.markdown("Upload 10-K filings, earnings reports, annual reports, or other financial documents for AI-powered analysis.")
    
    uploaded_files = st.file_uploader(
        "Upload Financial Documents", 
        type=['pdf', 'txt', 'md', 'csv'],
        accept_multiple_files=True,
        help="Upload annual reports, 10-K filings, earnings reports, CSVs, or other financial documents"
    )
    
    if uploaded_files:
        if st.button("🔍 Start Analysis", use_container_width=True):
            # Create session
            session = new_internal_session()
            
            with st.spinner("Processing financial documents..."):
                try:
                    document_content, extracted_metrics = process_financial_documents(uploaded_files)
                    session["document_content"] = document_content
                    session["analysis_data"]["extracted_metrics"] = extracted_metrics
                    memory.update_internal_analysis({"document_content": document_content})
                    
                    # Quick analysis
                    analyzer_agent = financial_agents.financial_document_analyzer_agent()
                    quick_task = financial_tasks.quick_financial_summary_task(analyzer_agent, document_content)
                    crew = Crew(agents=[analyzer_agent], tasks=[quick_task], process=Process.sequential)
                    quick_summary = crew.kickoff().raw
                    
                    session["messages"].append({"role": "user", "content": f"Uploaded {len(uploaded_files)} financial document(s)."})
                    session["messages"].append({"role": "assistant", "content": f"Documents processed successfully! Here's a quick summary:\n\n{quick_summary}\n\nYou can now ask questions about the analysis or request specific types of analysis from the tabs above."})
                    session["conversation_state"] = "analysis_complete"
                    session["analysis_data"]["quick_summary"] = quick_summary
                    memory.update_internal_analysis({"quick_summary": quick_summary})
                    
                    # Update session title
                    file_names = [f.name for f in uploaded_files]
                    session["title"] = f"Analysis: {file_names[0]}" + (f" (+{len(file_names)-1} more)" if len(file_names) > 1 else "")
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Error processing documents: {e}")
                    reset_session()

else:
    # Session exists - show the full analysis interface
    main_col, chat_col = st.columns([2, 1])

    with main_col:
        # Header with title and reset button
        header_col1, header_col2 = st.columns([3, 1])
        with header_col1:
            st.title("📄 Internal Analysis")
            st.caption(f"**{session.get('title', 'Document Analysis')}**")
        with header_col2:
            if st.button("🔄 New Analysis", use_container_width=True):
                reset_session()
                st.rerun()

        analysis_tab, metrics_tab = st.tabs(["📊 Analysis", "📈 Key Metrics"])

        with analysis_tab:
            state = session.get("conversation_state", "start")
            
            # Display conversation messages
            for message in session.get("messages", []):
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if state == "analysis_complete":
                st.success("✅ Analysis complete! Use the tabs above to explore detailed insights, metrics, and AI chat.")

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
                                
                                analysis_input = session.get("document_content", "")
                                
                                ratio_task = financial_tasks.calculate_financial_ratios_task(ratio_agent, analysis_input)
                                crew = Crew(agents=[ratio_agent], tasks=[ratio_task], process=Process.sequential)
                                ratio_analysis = crew.kickoff().raw
                                
                                session["analysis_data"]["ratio_analysis"] = ratio_analysis
                                memory.update_internal_analysis({"ratio_analysis": ratio_analysis})
                                st.success("Ratio analysis complete!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error generating ratio analysis: {e}")

                with col2:
                    if st.button("⚠️ Generate Risk Assessment", use_container_width=True):
                        with st.spinner("Assessing risks..."):
                            try:
                                risk_agent = financial_agents.risk_assessment_agent()
                                
                                analysis_input = session.get("document_content", "")
                                
                                risk_task = financial_tasks.risk_assessment_task(risk_agent, analysis_input)
                                crew = Crew(agents=[risk_agent], tasks=[risk_task], process=Process.sequential)
                                risk_analysis = crew.kickoff().raw
                                
                                session["analysis_data"]["risk_analysis"] = risk_analysis
                                memory.update_internal_analysis({"risk_analysis": risk_analysis})
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

    with chat_col:
        st.header("💬 AI Chat")
        
        # Use per-session chat history
        chat_history = session.get("chat_history", [])

        # Display chat history
        for chat in chat_history:
            with st.chat_message(chat["role"]):
                st.markdown(chat["content"])

        # Chat input
        if prompt := st.chat_input("Ask a question about the analysis..."):
            chat_history.append({"role": "user", "content": prompt})
            session["chat_history"] = chat_history
            
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Analyzing your question..."):
                    try:
                        # Get AI response
                        context = memory.get_chat_context()
                        chat_agent = financial_agents.financial_document_analyzer_agent()
                        chat_task = financial_tasks.financial_chat_response_task(chat_agent, prompt, context)
                        crew = Crew(agents=[chat_agent], tasks=[chat_task], process=Process.sequential)
                        response = crew.kickoff().raw
                        
                        st.markdown(response)
                        chat_history.append({"role": "assistant", "content": response})
                        session["chat_history"] = chat_history
                    except Exception as e:
                        error_msg = f"Sorry, I encountered an error: {e}"
                        st.markdown(error_msg)
                        chat_history.append({"role": "assistant", "content": error_msg})
                        session["chat_history"] = chat_history
