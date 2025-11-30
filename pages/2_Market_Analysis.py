import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew, Process
from financial_agents import FinancialAgents
from financial_tasks import FinancialTasks
from utils import validate_company_name, get_memory
import uuid
import json
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
    
    initial_message = "Welcome to Competitive Intelligence! Enter your company name to identify and analyze your top competitors."
    conversation_state = "awaiting_user_company"
    title = "Competitive Intelligence Session"
    
    st.session_state.market_sessions[session_id] = {
        "title": title,
        "session_type": "competitive",
        "messages": [{"role": "assistant", "content": initial_message}],
        "conversation_state": conversation_state,
        "analysis_data": {},
        "chat_history": [],
        "user_company": "",
        "competitors": [],
        "selected_competitor": None,
        "competitor_analyses": {},
        "analysis_results": {},
        "quick_metrics": {}
    }
    st.session_state.editing_market_session_id = None

def parse_competitors(competitor_text):
    """Parse competitor names from the structured AI response."""
    import re
    competitors = []
    
    # Try to find competitors in the format: **Competitor N: [Company Name]**
    pattern = r'\*\*Competitor \d+:\s*([^*\n]+?)\*\*'
    matches = re.findall(pattern, competitor_text)
    
    if matches:
        competitors = [match.strip() for match in matches[:3]]
    
    return competitors

# --- AGENT & TASK DEFINITIONS ---
financial_agents = FinancialAgents()
financial_tasks = FinancialTasks()


def run_competitor_identification(session):
    """Run competitor identification for a session that was created on the Home page.
    This function performs the same identification flow as the UI button, but is
    safe to call on page load so the work starts as soon as the user submitted on Home.
    """
    user_company = session.get("user_company")
    if not user_company:
        return

    try:
        competitor_agent = financial_agents.competitor_identification_agent()
        competitor_task = financial_tasks.identify_competitors_task(competitor_agent, user_company)
        crew = Crew(agents=[competitor_agent], tasks=[competitor_task], process=Process.sequential)
        competitor_analysis = crew.kickoff().raw

        # Parse competitor names using existing helper
        competitors = parse_competitors(competitor_analysis)

        # populate knowledge graph
        kg = memory.get_knowledge_graph()
        kg.add_company(user_company, {'is_user_company': True})
        for competitor in competitors:
            kg.add_company(competitor, {'is_competitor': True})
            kg.add_relationship(user_company, competitor, 'competes_with', {
                'identified_at': datetime.now().isoformat()
            })

        session['competitors'] = competitors
        session['analysis_data']['competitor_identification'] = competitor_analysis
        session['conversation_state'] = 'competitors_identified'
        session['messages'].append({
            'role': 'assistant',
            'content': f"I've identified the top {len(competitors)} competitors for {user_company}:\n\n{competitor_analysis}\n\nClick on a competitor below to get detailed competitive intelligence."
        })

        memory.update_competitive_intelligence({
            'user_company': user_company,
            'competitors': competitors,
            'competitor_identification': competitor_analysis
        })

        # refresh the page to show new state
        st.rerun()
    except Exception as e:
        # Surface error to UI and keep session in identifying state
        st.error(f"Error identifying competitors: {e}")
        session['conversation_state'] = 'awaiting_user_company'
        return

# --- SIDEBAR: SESSION MANAGEMENT ---
with st.sidebar:
    st.title("📈 Competitive Intelligence")
    st.markdown("Analyze Your Competition")

    if st.button("🔍 New Competitive Analysis", use_container_width=True, type="primary"):
        new_market_session()
        st.rerun()
    
    # Show user company and competitors if available
    session = get_current_market_session()

    # If this session was created on Home and marked as identifying, start identification now
    if session and session.get('conversation_state') == 'identifying_competitors' and not session.get('competitors'):
        run_competitor_identification(session)
    if session and session.get("user_company"):
        st.divider()
        st.subheader("Your Company")
        st.write(f"**{session['user_company']}**")
        
        if session.get("competitors"):
            st.subheader("Identified Competitors")
            for idx, comp in enumerate(session["competitors"], 1):
                st.write(f"{idx}. {comp}")

# --- MAIN LAYOUT ---
main_col, chat_col = st.columns([2, 1])

with main_col:
    session = get_current_market_session()

    if not session:
        st.info("Start a new competitive intelligence session from the sidebar to identify and analyze your competitors.")
    else:
        st.title("🎯 Competitive Intelligence")

        analysis_tab, competitor_tab = st.tabs(["📊 Competitor Identification", "🔍 Detailed Analysis"])

        with analysis_tab:
            st.header("Competitive Landscape Analysis")
            
            # Progress indicator
            state = session.get("conversation_state", "start")
            if state == "awaiting_user_company":
                progress_value = 0.25
            elif state == "identifying_competitors":
                progress_value = 0.5
            elif state == "competitors_identified":
                progress_value = 0.75
            elif state == "competitor_selected":
                progress_value = 1.0
            else:
                progress_value = 0.1
            
            st.progress(progress_value)
            
            # Display conversation messages
            for message in session.get("messages", []):
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # State 1: Awaiting user's company
            if state == "awaiting_user_company":
                user_company_input = st.text_input(
                    "What company are you working for?", 
                    placeholder="e.g., Apple Inc., Tesla, Microsoft",
                    help="Enter your company name to identify your top competitors"
                )
                
                if st.button("🔍 Identify Competitors") and user_company_input:
                    is_valid, clean_name = validate_company_name(user_company_input)
                    if is_valid:
                        with st.spinner(f"Identifying top competitors for {user_company_input}..."):
                            try:
                                session["user_company"] = user_company_input
                                session["messages"].append({"role": "user", "content": f"My company: {user_company_input}"})
                                session["conversation_state"] = "identifying_competitors"
                                
                                # Identify competitors
                                competitor_agent = financial_agents.competitor_identification_agent()
                                competitor_task = financial_tasks.identify_competitors_task(competitor_agent, user_company_input)
                                crew = Crew(agents=[competitor_agent], tasks=[competitor_task], process=Process.sequential)
                                competitor_analysis = crew.kickoff().raw
                                
                                # Parse competitor names
                                competitors = parse_competitors(competitor_analysis)
                                
                                # Build knowledge graph - add user company and competitors
                                kg = memory.get_knowledge_graph()
                                kg.add_company(user_company_input, {'is_user_company': True})
                                for competitor in competitors:
                                    kg.add_company(competitor, {'is_competitor': True})
                                    kg.add_relationship(user_company_input, competitor, 'competes_with', {
                                        'identified_at': datetime.now().isoformat()
                                    })
                                
                                session["competitors"] = competitors
                                session["analysis_data"]["competitor_identification"] = competitor_analysis
                                memory.update_competitive_intelligence({
                                    "user_company": user_company_input,
                                    "competitors": competitors,
                                    "competitor_identification": competitor_analysis
                                })
                                
                                session["messages"].append({
                                    "role": "assistant", 
                                    "content": f"I've identified the top 3 competitors for {user_company_input}:\n\n{competitor_analysis}\n\nClick on a competitor below to get detailed competitive intelligence."
                                })
                                session["conversation_state"] = "competitors_identified"
                                session["title"] = f"Competitive Intelligence - {user_company_input}"
                                
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error identifying competitors: {e}")
                                session["conversation_state"] = "awaiting_user_company"
                    else:
                        st.error("Please enter a valid company name.")

            # State 2: Competitors identified - show selection
            elif state == "competitors_identified":
                st.success("✅ Top 3 competitors identified!")
                st.subheader("Select a competitor to analyze:")
                
                if session.get("competitors"):
                    cols = st.columns(3)
                    for idx, competitor in enumerate(session["competitors"]):
                        with cols[idx]:
                            st.markdown(f"### {competitor}")
                            if st.button(f"Analyze {competitor}", key=f"competitor_{idx}", use_container_width=True):
                                session["selected_competitor"] = competitor
                                session["conversation_state"] = "analyzing_competitor"
                                st.rerun()
                else:
                    st.warning("No competitors were identified. Please try again.")

            # State 3: Analyzing selected competitor
            elif state == "analyzing_competitor":
                selected_competitor = session.get("selected_competitor")
                if selected_competitor:
                    # Initialize progress and status containers
                    progress_container = st.empty()
                    status_container = st.empty()
                    debug_container = st.empty()  # For debugging information
                    progress_container.progress(0)
                    
                    try:
                        # Step 1: Competitive intelligence analysis
                        status_container.info("📊 Step 1/3: Gathering competitive intelligence...")
                        progress_container.progress(0.15)
                        
                        # Debug info
                        debug_container.code(f"""Debug Info:
User Company: {session.get('user_company')}
Selected Competitor: {selected_competitor}
Analysis State: Starting competitive intelligence analysis""")
                        
                        intel_agent = financial_agents.competitive_intelligence_agent()
                        intel_task = financial_tasks.competitive_intelligence_task(
                            intel_agent, 
                            session["user_company"], 
                            selected_competitor
                        )
                        
                        # Use smaller crew for initial analysis
                        crew = Crew(
                            agents=[intel_agent], 
                            tasks=[intel_task], 
                            process=Process.sequential,
                            verbose=True  # Enable verbose mode for debugging
                        )
                        
                        debug_container.code("Attempting competitive analysis...")
                        competitive_analysis = crew.kickoff()
                        
                        if not competitive_analysis:
                            debug_container.error("Crew kickoff returned None")
                            raise Exception("Analysis failed - no response from crew")
                        
                        if not hasattr(competitive_analysis, 'raw'):
                            debug_container.error(f"Unexpected response format: {type(competitive_analysis)}")
                            raise Exception("Analysis failed - invalid response format")
                        
                        if not competitive_analysis.raw:
                            debug_container.error("Empty response from analysis")
                            raise Exception("Analysis failed - empty response")
                        
                        competitive_analysis = competitive_analysis.raw
                        debug_container.code(f"Analysis successful. Response length: {len(competitive_analysis)}")
                        progress_container.progress(0.35)
                        
                        # Step 2: Extract entities and populate knowledge graph
                        status_container.info("🔍 Step 2/3: Extracting key information...")
                        
                        # Break analysis into smaller chunks for better reliability
                        chunk_size = 2000
                        chunks = [competitive_analysis[i:i + chunk_size] for i in range(0, len(competitive_analysis), chunk_size)]
                        all_entities = []
                        
                        # Calculate progress step for each chunk
                        chunk_progress_step = 0.4 / len(chunks)
                        current_progress = 0.35
                        
                        for i, chunk in enumerate(chunks, 1):
                            status_container.info(f"🔍 Step 2/3: Processing chunk {i} of {len(chunks)}...")
                            extraction_agent = financial_agents.knowledge_graph_analyst_agent()
                            extraction_task = financial_tasks.entity_extraction_task(
                                extraction_agent,
                                chunk,
                                session["user_company"],
                                selected_competitor
                            )
                            extraction_crew = Crew(
                                agents=[extraction_agent], 
                                tasks=[extraction_task], 
                                process=Process.sequential
                            )
                            chunk_result = extraction_crew.kickoff()
                            if chunk_result and chunk_result.raw:
                                all_entities.append(chunk_result.raw)
                            
                            # Update progress
                            current_progress += chunk_progress_step
                            progress_container.progress(current_progress)
                        
                        # Step 3: Knowledge Graph Updates
                        status_container.info("🌐 Step 3/3: Building knowledge graph...")
                        progress_container.progress(0.8)
                        
                        extracted_entities = "\n".join(all_entities)
                        if not extracted_entities:
                            raise Exception("No entities were extracted from the analysis")
                        
                        # Update knowledge graph
                        kg = memory.get_knowledge_graph()
                        kg.parse_entity_extraction(
                            extracted_entities,
                            session["user_company"],
                            selected_competitor
                        )
                        
                        progress_container.progress(0.9)
                        
                        # Update session and memory
                        session["competitor_analyses"][selected_competitor] = competitive_analysis
                        session["analysis_data"]["current_competitor_analysis"] = competitive_analysis
                        session["analysis_data"]["extracted_entities"] = extracted_entities
                        
                        memory.update_competitive_intelligence({
                            "selected_competitor": selected_competitor,
                            "selected_competitor_analysis": competitive_analysis,
                            "extracted_entities": extracted_entities
                        })
                        
                        # Add message to chat with improved formatting
                        session["messages"].append({
                            "role": "assistant",
                            "content": f"""## Competitive Intelligence Report: {selected_competitor}

{competitive_analysis}

*Analysis completed successfully. View detailed information in the 'Detailed Analysis' tab.*"""
                        })
                        
                        # Update state and display completion
                        session["conversation_state"] = "competitor_selected"
                        progress_container.progress(1.0)
                        status_container.success("✅ Analysis completed successfully!")
                        
                        # Short delay for UI update
                        import time
                        time.sleep(1)
                        
                        # Clean up and refresh
                        progress_container.empty()
                        status_container.empty()
                        st.rerun()
                    
                    except Exception as e:
                        # Log error for debugging
                        import traceback
                        print(f"Competitor analysis error: {str(e)}")
                        print(traceback.format_exc())
                        
                        # Clear progress indicators and show error
                        progress_container.empty()
                        status_container.error(f"❌ Error analyzing competitor: {str(e)}")
                        session["conversation_state"] = "competitors_identified"
                        st.rerun()

            # State 4: Analysis complete
            elif state == "competitor_selected":
                st.success("✅ Competitive analysis complete!")
                
                # Option to analyze another competitor
                st.subheader("Analyze another competitor:")
                remaining_competitors = [c for c in session.get("competitors", []) if c != session.get("selected_competitor")]
                
                if remaining_competitors:
                    cols = st.columns(len(remaining_competitors))
                    for idx, competitor in enumerate(remaining_competitors):
                        with cols[idx]:
                            if st.button(f"Analyze {competitor}", key=f"remaining_competitor_{idx}", use_container_width=True):
                                session["selected_competitor"] = competitor
                                session["conversation_state"] = "analyzing_competitor"
                                st.rerun()

        with competitor_tab:
            st.header("🔍 Detailed Competitive Intelligence")
            
            if session.get("competitor_analyses"):
                # Show knowledge graph visualization
                with st.expander("🌐 Knowledge Graph Visualization", expanded=False):
                    kg = memory.get_knowledge_graph()
                    
                    # Only show visualization if there are nodes
                    if kg.graph.number_of_nodes() > 0:
                        try:
                            fig = kg.visualize_graph()
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as e:
                            st.warning(f"Could not generate visualization: {e}")
                    else:
                        st.info("No entities in knowledge graph yet.")
                    
                    st.divider()
                    st.markdown(kg.get_graph_summary())
                    
                    # Show graph statistics
                    stats = kg.export_graph_data()['stats']
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Companies", stats['companies'])
                    with col2:
                        st.metric("Products", stats['products'])
                    with col3:
                        st.metric("Markets", stats['markets'])
                    with col4:
                        st.metric("Relationships", stats['total_edges'])
                
                # Show tabs for each analyzed competitor
                analyzed_competitors = list(session["competitor_analyses"].keys())
                
                if len(analyzed_competitors) == 1:
                    st.markdown(session["competitor_analyses"][analyzed_competitors[0]])
                else:
                    competitor_tabs = st.tabs(analyzed_competitors)
                    for idx, competitor in enumerate(analyzed_competitors):
                        with competitor_tabs[idx]:
                            st.markdown(session["competitor_analyses"][competitor])
            else:
                st.info("Select and analyze a competitor from the 'Competitor Identification' tab to view detailed intelligence here.")

with chat_col:
    st.header("💬 Competitive Intelligence Chat")

    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # Chat input
    if prompt := st.chat_input("Ask about competitive analysis..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consulting with expert analysts..."):
                try:
                    # Get necessary context with timeout
                    try:
                        with st.spinner("Retrieving context..."):
                            graph_context = memory.get_graph_context_for_query(prompt)
                            chat_context = memory.get_chat_context()
                    except Exception as e:
                        st.error("Error retrieving context. Using available information.")
                        graph_context = ""
                        chat_context = ""
                    
                    # Initialize council members with timeouts
                    agents = {
                        "Competitive Analysis": financial_agents.competitive_intelligence_agent(),
                        "Market Comparison": financial_agents.market_comparison_agent(),
                        "Risk Assessment": financial_agents.risk_assessment_agent(),
                        "Knowledge Graph": financial_agents.knowledge_graph_analyst_agent()
                    }
                    
                    # Initialize agents
                    primary_agent = financial_agents.competitive_intelligence_agent()
                    online_agent = financial_agents.online_research_agent()
                    tasks = []
                    
                    # Create main task with context from knowledge graph
                    main_task = financial_tasks.financial_chat_response_task(
                        agent=primary_agent,
                        user_question=prompt,
                        context=f"""Knowledge Graph Context:\n{graph_context}\n\nChat History:\n{chat_context}"""
                    )
                    tasks.append(main_task)
                    
                    # Add online research task to gather additional information
                    online_task = financial_tasks.online_research_task(
                        agent=online_agent,
                        query=prompt,
                        company_name=session.get("user_company", ""),
                        context=chat_context
                    )
                    tasks.append(online_task)
                    
                    # Get metrics from knowledge graph for additional context
                    kg = memory.get_knowledge_graph()
                    metrics = {}
                    try:
                        stats = kg.export_graph_data()
                        metrics = {
                            "companies": stats.get('companies', 0),
                            "markets": stats.get('markets', 0),
                            "products": stats.get('products', 0),
                            "relationships": stats.get('total_edges', 0)
                        }
                    except Exception as e:
                        print(f"Error getting metrics: {str(e)}")
                        metrics = {
                            "companies": 0,
                            "markets": 0,
                            "products": 0,
                            "relationships": 0
                        }
                    
                    # Add market comparison task if relevant metrics exist
                    if metrics["companies"] > 0:
                        comparison_agent = financial_agents.market_comparison_agent()
                        comparison_task = financial_tasks.peer_comparison_task(
                            agent=comparison_agent,
                            company_name=session.get("user_company", ""),
                            industry="",  # Will be inferred from knowledge graph
                            key_metrics=json.dumps(metrics)
                        )
                        tasks.append(comparison_task)
                    
                    # Run all tasks with the crew
                    crew = Crew(
                        agents=[primary_agent, online_agent, financial_agents.market_comparison_agent()],
                        tasks=tasks,
                        process=Process.sequential
                    )
                    
                    crew_result = crew.kickoff()
                    if crew_result and crew_result.raw:
                        response = crew_result.raw
                    else:
                        # Fallback to simple online research if crew fails
                        fallback_crew = Crew(
                            agents=[online_agent],
                            tasks=[online_task],
                            process=Process.sequential
                        )
                        fallback_result = fallback_crew.kickoff()
                        response = fallback_result.raw if fallback_result else "I apologize, but I couldn't generate a complete analysis. Please try rephrasing your question."
                    
                    st.markdown(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {e}"
                    st.markdown(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
