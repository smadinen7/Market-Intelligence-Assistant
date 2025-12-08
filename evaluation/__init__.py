# LLM-as-a-Judge Evaluation Framework
# Compares Basic, Detailed, and Agentic (multi-agent) systems

from .llm_judge import LLMJudge, EvaluationResult
from .baseline_gemini import BasicGemini
from .detailed_gemini import DetailedGemini
from .agentic_system import AgenticSystem
from .test_cases import TEST_CASES, TestCase
from .run_evaluation import run_full_evaluation

__all__ = [
    "LLMJudge",
    "EvaluationResult", 
    "BasicGemini",
    "DetailedGemini",
    "AgenticSystem",
    "TEST_CASES",
    "TestCase",
    "run_full_evaluation"
]
