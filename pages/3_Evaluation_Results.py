"""
Evaluation Results Viewer

Streamlit page to visualize LLM-as-a-Judge evaluation results.
Supports three-system comparison: Basic, Detailed, and Agentic.

NOTE: Access this page with ?show_eval=true in the URL
"""

import os
import json
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from glob import glob

# Check for secret URL parameter to access this page
query_params = st.query_params
has_access = query_params.get("show_eval", "").lower() == "true"

if not has_access:
    st.set_page_config(
        page_title="Page Not Available",
        page_icon="🔒",
        layout="centered"
    )
    st.warning("This page requires special access.")
    st.stop()

# Page config
st.set_page_config(
    page_title="CEO AI Assistant - Evaluation Results",
    page_icon="📊",
    layout="wide"
)

st.title("📊 LLM-as-a-Judge Evaluation Results")
st.markdown("Compare Basic Prompt, Detailed Prompt, and Multi-Agentic System performance")

# Find evaluation result files
eval_dir = os.path.join(os.path.dirname(__file__), "..", "evaluation")
result_files = glob(os.path.join(eval_dir, "evaluation_results_*.json"))
result_files.sort(reverse=True)  # Most recent first

if not result_files:
    st.warning("No evaluation results found. Run an evaluation first:")
    st.code("python -m evaluation.run_evaluation --mode quick", language="bash")
    st.stop()

# Select result file
selected_file = st.selectbox(
    "Select Evaluation Run",
    options=result_files,
    format_func=lambda x: os.path.basename(x).replace("evaluation_results_", "").replace(".json", "")
)

# Load results
with open(selected_file) as f:
    results = json.load(f)

summary = results.get("summary", {})
avg_scores = results.get("average_scores", {})
individual = results.get("individual_results", [])

# Detect if this is a three-system or two-system result
is_three_system = "basic" in avg_scores or any("basic_scores" in r for r in individual)

# Define dimensions (excluding 'total')
DIMENSIONS = ["accuracy", "completeness", "actionability", "recency", "structure"]

def calc_total(scores_dict):
    """Calculate total from scores, using 'total' field if present, otherwise sum dimensions only."""
    if not scores_dict:
        return 0
    if "total" in scores_dict:
        return scores_dict["total"]
    return sum(scores_dict.get(d, 0) for d in DIMENSIONS)

# ============================================================================
# SUMMARY METRICS
# ============================================================================

st.header("📈 Summary")

if is_three_system:
    # Three-system layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tests", summary.get("total_evaluations", len(individual)))
    
    # Get average scores
    basic_avg = avg_scores.get("basic", {})
    detailed_avg = avg_scores.get("detailed", {})
    agentic_avg = avg_scores.get("agentic", {})
    
    # Calculate totals using helper function
    basic_total = calc_total(basic_avg)
    detailed_total = calc_total(detailed_avg)
    agentic_total = calc_total(agentic_avg)
    
    with col2:
        st.metric(
            "Basic Prompt Avg",
            f"{basic_total:.1f}/25",
            delta=None
        )
    
    with col3:
        st.metric(
            "Detailed Prompt Avg",
            f"{detailed_total:.1f}/25",
            delta=f"{detailed_total - basic_total:+.1f} vs Basic Prompt" if detailed_total != basic_total else None
        )
    
    with col4:
        st.metric(
            "Multi-Agentic Avg",
            f"{agentic_total:.1f}/25",
            delta=f"{agentic_total - detailed_total:+.1f} vs Detailed Prompt" if agentic_total != detailed_total else None,
            delta_color="normal"
        )
    
    # Winner highlight
    winner = "Multi-Agentic System" if agentic_total >= detailed_total and agentic_total >= basic_total else \
             ("Detailed Prompt" if detailed_total >= basic_total else "Basic Prompt")
    st.success(f"🏆 **Best Performing System: {winner}** with average score of {max(basic_total, detailed_total, agentic_total):.1f}/25")

else:
    # Two-system layout (legacy)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Tests", summary.get("total_evaluations", 0))
    
    with col2:
        st.metric("Baseline Wins", summary.get("baseline_wins", 0))
    
    with col3:
        st.metric("Agentic Wins", summary.get("agentic_wins", 0))
    
    with col4:
        st.metric("Ties", summary.get("ties", 0))
    
    with col5:
        win_rate = summary.get("agentic_win_rate", 0)
        st.metric(
            "Agentic Win Rate",
            f"{win_rate}%",
            delta=f"{win_rate - 50:.1f}% vs random" if win_rate != 50 else None
        )

# ============================================================================
# SCORE COMPARISON CHARTS
# ============================================================================

st.header("📊 Score Comparison by Dimension")

if is_three_system:
    basic_scores = avg_scores.get("basic", {})
    detailed_scores = avg_scores.get("detailed", {})
    agentic_scores = avg_scores.get("agentic", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Radar chart for three systems
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=[basic_scores.get(d, 0) for d in DIMENSIONS],
            theta=[d.title() for d in DIMENSIONS],
            fill='toself',
            name='Basic Prompt',
            line_color='#FF6B6B'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=[detailed_scores.get(d, 0) for d in DIMENSIONS],
            theta=[d.title() for d in DIMENSIONS],
            fill='toself',
            name='Detailed Prompt',
            line_color='#FFE66D'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=[agentic_scores.get(d, 0) for d in DIMENSIONS],
            theta=[d.title() for d in DIMENSIONS],
            fill='toself',
            name='Multi-Agentic',
            line_color='#4ECDC4'
        ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=True,
            title="Average Scores by Dimension (1-5 scale)"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        # Bar comparison for three systems
        score_data = []
        for dim in DIMENSIONS:
            score_data.append({
                "Dimension": dim.title(),
                "Basic Prompt": basic_scores.get(dim, 0),
                "Detailed Prompt": detailed_scores.get(dim, 0),
                "Multi-Agentic": agentic_scores.get(dim, 0)
            })
        
        df_scores = pd.DataFrame(score_data)
        
        fig_scores = px.bar(
            df_scores,
            x="Dimension",
            y=["Basic Prompt", "Detailed Prompt", "Multi-Agentic"],
            title="Score Comparison by Dimension",
            barmode="group",
            color_discrete_map={
                "Basic Prompt": "#FF6B6B",
                "Detailed Prompt": "#FFE66D",
                "Multi-Agentic": "#4ECDC4"
            }
        )
        fig_scores.update_layout(yaxis_range=[0, 5])
        st.plotly_chart(fig_scores, use_container_width=True)
    
    # Score comparison table
    st.subheader("Score Summary Table")
    
    table_data = []
    for dim in DIMENSIONS:
        b = basic_scores.get(dim, 0)
        d = detailed_scores.get(dim, 0)
        a = agentic_scores.get(dim, 0)
        best = max(b, d, a)
        winner = "Basic Prompt" if b == best else ("Detailed Prompt" if d == best else "Multi-Agentic")
        
        table_data.append({
            "Dimension": dim.title(),
            "Basic Prompt": f"{b:.2f}",
            "Detailed Prompt": f"{d:.2f}",
            "Multi-Agentic": f"{a:.2f}",
            "Best": f"🏆 {winner}"
        })
    
    # Add totals
    b_total = calc_total(basic_scores)
    d_total = calc_total(detailed_scores)
    a_total = calc_total(agentic_scores)
    best_total = max(b_total, d_total, a_total)
    winner_total = "Basic Prompt" if b_total == best_total else ("Detailed Prompt" if d_total == best_total else "Multi-Agentic")
    
    table_data.append({
        "Dimension": "**TOTAL**",
        "Basic Prompt": f"**{b_total:.2f}**",
        "Detailed Prompt": f"**{d_total:.2f}**",
        "Multi-Agentic": f"**{a_total:.2f}**",
        "Best": f"🏆 **{winner_total}**"
    })
    
    df_table = pd.DataFrame(table_data)
    st.dataframe(df_table, use_container_width=True, hide_index=True)

else:
    # Two-system charts (legacy)
    baseline_scores = avg_scores.get("baseline", {})
    agentic_scores = avg_scores.get("agentic", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=[baseline_scores.get(d, 0) for d in DIMENSIONS],
            theta=[d.title() for d in DIMENSIONS],
            fill='toself',
            name='Baseline Gemini',
            line_color='#FF6B6B'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=[agentic_scores.get(d, 0) for d in DIMENSIONS],
            theta=[d.title() for d in DIMENSIONS],
            fill='toself',
            name='Agentic (CrewAI)',
            line_color='#4ECDC4'
        ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=True,
            title="Average Scores by Dimension (1-5 scale)"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        score_data = []
        for dim in DIMENSIONS:
            score_data.append({
                "Dimension": dim.title(),
                "Baseline": baseline_scores.get(dim, 0),
                "Agentic": agentic_scores.get(dim, 0)
            })
        
        df_scores = pd.DataFrame(score_data)
        
        fig_scores = px.bar(
            df_scores,
            x="Dimension",
            y=["Baseline", "Agentic"],
            title="Score Comparison",
            barmode="group",
            color_discrete_map={
                "Baseline": "#FF6B6B",
                "Agentic": "#4ECDC4"
            }
        )
        fig_scores.update_layout(yaxis_range=[0, 5])
        st.plotly_chart(fig_scores, use_container_width=True)

# ============================================================================
# INDIVIDUAL TEST RESULTS
# ============================================================================

st.header("📋 Individual Test Results")

if individual:
    if is_three_system:
        # Three-system results table
        results_data = []
        for r in individual:
            b_scores = r.get("basic_scores", {})
            d_scores = r.get("detailed_scores", {})
            a_scores = r.get("agentic_scores", {})
            
            b_total = calc_total(b_scores)
            d_total = calc_total(d_scores)
            a_total = calc_total(a_scores)
            
            best = max(b_total, d_total, a_total)
            winner = "Basic Prompt" if b_total == best else ("Detailed Prompt" if d_total == best else "Multi-Agentic")
            
            results_data.append({
                "Test ID": r.get("test_case_id", ""),
                "Type": r.get("test_case_type", "").replace("_", " ").title(),
                "Basic Prompt": f"{b_total:.0f}/25",
                "Detailed Prompt": f"{d_total:.0f}/25",
                "Multi-Agentic": f"{a_total:.0f}/25",
                "Winner": f"🏆 {winner}",
            })
        
        df_results = pd.DataFrame(results_data)
        st.dataframe(df_results, use_container_width=True, hide_index=True)
        
        # Test-by-test chart
        st.subheader("Score Progression by Test")
        
        chart_data = []
        for r in individual:
            b_scores = r.get("basic_scores", {})
            d_scores = r.get("detailed_scores", {})
            a_scores = r.get("agentic_scores", {})
            
            test_id = r.get("test_case_id", "")
            chart_data.append({"Test": test_id, "System": "Basic Prompt", "Score": calc_total(b_scores)})
            chart_data.append({"Test": test_id, "System": "Detailed Prompt", "Score": calc_total(d_scores)})
            chart_data.append({"Test": test_id, "System": "Multi-Agentic", "Score": calc_total(a_scores)})
        
        df_chart = pd.DataFrame(chart_data)
        fig_line = px.line(
            df_chart,
            x="Test",
            y="Score",
            color="System",
            markers=True,
            title="Scores by Test Case",
            color_discrete_map={
                "Basic Prompt": "#FF6B6B",
                "Detailed Prompt": "#FFE66D",
                "Multi-Agentic": "#4ECDC4"
            }
        )
        fig_line.update_layout(yaxis_range=[0, 25])
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Detailed view expander
        st.subheader("Detailed Results")
        
        for r in individual:
            b_scores = r.get("basic_scores", {})
            d_scores = r.get("detailed_scores", {})
            a_scores = r.get("agentic_scores", {})
            
            b_total = calc_total(b_scores)
            d_total = calc_total(d_scores)
            a_total = calc_total(a_scores)
            best = max(b_total, d_total, a_total)
            winner = "Basic Prompt" if b_total == best else ("Detailed Prompt" if d_total == best else "Multi-Agentic")
            
            with st.expander(f"{r.get('test_case_id')} - 🏆 {winner} ({a_total:.0f}/25 Multi-Agentic)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Query:**")
                    st.info(r.get("query", r.get("input_query", "N/A")))
                    
                    st.markdown("**Judge Rationale:**")
                    st.write(r.get("rationale", r.get("judge_rationale", "N/A")))
                
                with col2:
                    st.markdown("**Score Breakdown:**")
                    
                    score_compare = pd.DataFrame({
                        "Dimension": [d.title() for d in DIMENSIONS],
                        "Basic Prompt": [b_scores.get(d, 0) for d in DIMENSIONS],
                        "Detailed Prompt": [d_scores.get(d, 0) for d in DIMENSIONS],
                        "Multi-Agentic": [a_scores.get(d, 0) for d in DIMENSIONS]
                    })
                    st.dataframe(score_compare, use_container_width=True, hide_index=True)
                
                # Show responses in tabs
                tab1, tab2, tab3 = st.tabs(["Basic Prompt Response", "Detailed Prompt Response", "Multi-Agentic Response"])
                
                with tab1:
                    st.markdown(r.get("basic_response", "N/A")[:3000])
                    if len(r.get("basic_response", "")) > 3000:
                        st.caption("(Response truncated for display)")
                
                with tab2:
                    st.markdown(r.get("detailed_response", "N/A")[:3000])
                    if len(r.get("detailed_response", "")) > 3000:
                        st.caption("(Response truncated for display)")
                
                with tab3:
                    st.markdown(r.get("agentic_response", "N/A")[:3000])
                    if len(r.get("agentic_response", "")) > 3000:
                        st.caption("(Response truncated for display)")
    
    else:
        # Two-system results (legacy)
        results_data = []
        for r in individual:
            b_scores = r.get("baseline_scores", {})
            a_scores = r.get("agentic_scores", {})
            
            results_data.append({
                "Test ID": r.get("test_case_id", ""),
                "Type": r.get("test_case_type", "").replace("_", " ").title(),
                "Winner": r.get("winner", "").upper(),
                "Baseline Total": calc_total(b_scores),
                "Agentic Total": calc_total(a_scores),
                "Rationale": r.get("judge_rationale", "")[:100] + "..."
            })
        
        df_results = pd.DataFrame(results_data)
        df_results["Winner"] = df_results["Winner"].apply(
            lambda x: f"🟢 {x}" if x == "AGENTIC" else (f"🔴 {x}" if x == "BASELINE" else f"⚪ {x}")
        )
        
        st.dataframe(df_results, use_container_width=True, hide_index=True)

# ============================================================================
# SYSTEM COMPARISON SUMMARY
# ============================================================================

if is_three_system:
    st.header("🔍 System Comparison Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📝 Basic Prompt")
        st.markdown("""
        **Architecture:** Simple prompts to Gemini
        
        **Strengths:**
        - Fast response times
        - Low complexity
        - Consistent output
        
        **Weaknesses:**
        - No web search capability
        - Limited to training data
        - Less structured outputs
        """)
    
    with col2:
        st.markdown("### 📋 Detailed Prompt")
        st.markdown("""
        **Architecture:** Structured prompts with guidelines
        
        **Strengths:**
        - Better formatting
        - More comprehensive coverage
        - Clear organization
        
        **Weaknesses:**
        - No web search capability
        - Limited to training data
        - May over-structure simple tasks
        """)
    
    with col3:
        st.markdown("### 🤖 Multi-Agentic System")
        st.markdown("""
        **Architecture:** Multi-agent CrewAI with web search
        
        **Strengths:**
        - Real-time web search
        - Specialized agents
        - Current information
        
        **Weaknesses:**
        - Higher latency
        - More complex
        - Depends on search quality
        """)

# ============================================================================
# RUN NEW EVALUATION
# ============================================================================

st.header("🚀 Run New Evaluation")

st.markdown("""
Run a new evaluation from the command line:

```bash
# Quick evaluation (5 tests, ~8 min)
python -m evaluation.run_evaluation --mode quick

# Full evaluation (all tests, ~30 min)
python -m evaluation.run_evaluation --mode full

# Single test
python -m evaluation.run_evaluation --mode single --test-id recency_001
```
""")

# Refresh button
if st.button("🔄 Refresh Results"):
    st.rerun()
