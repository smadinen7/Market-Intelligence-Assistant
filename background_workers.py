import os
import json
from datetime import datetime

def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def run_company_research(session_id: str, company_name: str, workspace_path: str):
    """Run company research using local agent factories and save results to a job file.

    This runs in a separate process (ProcessPoolExecutor) so it must import modules
    locally and avoid relying on Streamlit state.
    """
    # Import inside function so worker process can load modules independently
    try:
        from financial_agents import FinancialAgents
        from financial_tasks import FinancialTasks
        from utils import get_memory
        from crewai import Crew, Process
    except Exception as e:
        # If imports fail, write an error job file
        job_dir = os.path.join(workspace_path, ".jobs")
        _ensure_dir(job_dir)
        job_file = os.path.join(job_dir, f"{session_id}.json")
        json.dump({"status": "error", "error": str(e), "ts": datetime.now().isoformat()}, open(job_file, "w"))
        return

    job_dir = os.path.join(workspace_path, ".jobs")
    _ensure_dir(job_dir)
    job_file = os.path.join(job_dir, f"{session_id}.json")

    try:
        memory = get_memory()
        financial_agents = FinancialAgents()
        financial_tasks = FinancialTasks()

        expert_outputs = []

        # Company research
        research_agent = financial_agents.company_research_agent()
        research_task = financial_tasks.research_company_task(research_agent, company_name)
        research_crew = Crew(agents=[research_agent], tasks=[research_task], process=Process.sequential)
        research_result = research_crew.kickoff()
        if research_result and getattr(research_result, 'raw', None):
            expert_outputs.append(research_result.raw)

        # Online research
        online_agent = financial_agents.online_research_agent()
        online_task = financial_tasks.online_research_task(online_agent, query=company_name, company_name=company_name)
        online_crew = Crew(agents=[online_agent], tasks=[online_task], process=Process.sequential)
        online_result = online_crew.kickoff()
        if online_result and getattr(online_result, 'raw', None):
            expert_outputs.append(online_result.raw)

        # Trend analysis
        trend_agent = financial_agents.financial_trend_analyst_agent()
        trend_task = financial_tasks.trend_analysis_task(trend_agent, historical_data=company_name)
        trend_crew = Crew(agents=[trend_agent], tasks=[trend_task], process=Process.sequential)
        trend_result = trend_crew.kickoff()
        if trend_result and getattr(trend_result, 'raw', None):
            expert_outputs.append(trend_result.raw)

        # Quick financial summary
        summary_agent = financial_agents.financial_trend_analyst_agent()
        summary_task = financial_tasks.quick_financial_summary_task(summary_agent, company_name)
        summary_crew = Crew(agents=[summary_agent], tasks=[summary_task], process=Process.sequential)
        summary_result = summary_crew.kickoff()
        if summary_result and getattr(summary_result, 'raw', None):
            expert_outputs.append(summary_result.raw)

        # Investment advisor
        advisor_agent = financial_agents.investment_advisor_agent()
        analysis_summary = research_result.raw if (research_result and getattr(research_result, 'raw', None)) else company_name
        advisor_task = financial_tasks.investment_recommendation_task(advisor_agent, analysis_summary)
        advisor_crew = Crew(agents=[advisor_agent], tasks=[advisor_task], process=Process.sequential)
        advisor_result = advisor_crew.kickoff()
        if advisor_result and getattr(advisor_result, 'raw', None):
            expert_outputs.append(advisor_result.raw)

        # Synthesize using the dedicated company insights synthesis agent if available
        synth_output = None
        try:
            synth_agent = financial_agents.company_insights_synthesis_agent()
            expert_join = "\n\n---\n\n".join(expert_outputs)
            synth_task = financial_tasks.strategy_synthesis_task(
                synth_agent,
                query=f"List up to 10 concise, actionable insights for {company_name} for an executive (each 1-2 short bullets).",
                expert_responses=expert_join
            )
            synth_crew = Crew(agents=[synth_agent], tasks=[synth_task], process=Process.sequential)
            synth_result = synth_crew.kickoff()
            if synth_result and getattr(synth_result, 'raw', None):
                synth_output = synth_result.raw
        except Exception:
            synth_output = None

        # Save job file
        payload = {
            "status": "done",
            "ts": datetime.now().isoformat(),
            "expert_outputs": expert_outputs,
            "synth_output": synth_output
        }
        with open(job_file, "w") as f:
            json.dump(payload, f)

        # Optionally update knowledge graph (best-effort)
        try:
            kg = memory.get_knowledge_graph()
            kg.add_company(company_name, {"insights_generated_at": datetime.now().isoformat()})
        except Exception:
            pass

    except Exception as e:
        with open(job_file, "w") as f:
            json.dump({"status": "error", "error": str(e), "ts": datetime.now().isoformat()}, f)
