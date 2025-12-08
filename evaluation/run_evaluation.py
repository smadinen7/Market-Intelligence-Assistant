#!/usr/bin/env python3
"""
Evaluation Runner

Main script to run the LLM-as-a-Judge evaluation comparing
baseline Gemini against the multi-agent CrewAI system.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import List, Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from evaluation.llm_judge import LLMJudge, EvaluationResult, generate_evaluation_report
from evaluation.baseline_gemini import BasicGemini
from evaluation.detailed_gemini import DetailedGemini
from evaluation.agentic_system import AgenticSystem
from evaluation.test_cases import (
    TestCase, TestCaseType, ALL_TEST_CASES,
    get_quick_evaluation_set, get_full_evaluation_set
)


def run_single_test(
    test_case: TestCase,
    basic: BasicGemini,
    detailed: DetailedGemini,
    agentic: AgenticSystem,
    judge: LLMJudge,
    verbose: bool = True
) -> Optional[dict]:
    """
    Run a single test case through all three systems.
    Returns dict with responses and evaluations from all three systems.
    
    Returns dict with all three responses and comparison results, or None if error occurred.
    """
    if verbose:
        print(f"\n{'='*60}")
        print(f"Running: {test_case.id} - {test_case.name}")
        print(f"Type: {test_case.type.value}")
        print(f"{'='*60}")
    
    try:
        import time
        SYSTEM_DELAY = 20  # Delay between system calls to avoid Gemini rate limits (increased for free tier)
        
        # Generate responses from all three systems
        if test_case.type == TestCaseType.COMPETITOR_IDENTIFICATION:
            if verbose:
                print(f"  → Basic: Identifying competitors for {test_case.company_name}...")
            basic_response = basic.identify_competitors(test_case.company_name)
            time.sleep(SYSTEM_DELAY)
            
            if verbose:
                print(f"  → Detailed: Identifying competitors for {test_case.company_name}...")
            detailed_response = detailed.identify_competitors(test_case.company_name)
            time.sleep(SYSTEM_DELAY)
            
            if verbose:
                print(f"  → Agentic: Identifying competitors for {test_case.company_name}...")
            agentic_response = agentic.identify_competitors(test_case.company_name)
            
            query = f"Identify the top 3 direct competitors of {test_case.company_name}"
            
        elif test_case.type == TestCaseType.COMPETITIVE_INTELLIGENCE:
            if verbose:
                print(f"  → Basic: Generating intel on {test_case.competitor_name}...")
            basic_response = basic.competitive_intelligence(
                test_case.company_name, test_case.competitor_name
            )
            time.sleep(SYSTEM_DELAY)
            
            if verbose:
                print(f"  → Detailed: Generating intel on {test_case.competitor_name}...")
            detailed_response = detailed.competitive_intelligence(
                test_case.company_name, test_case.competitor_name
            )
            time.sleep(SYSTEM_DELAY)
            
            if verbose:
                print(f"  → Agentic: Generating intel on {test_case.competitor_name}...")
            agentic_response = agentic.competitive_intelligence(
                test_case.company_name, test_case.competitor_name
            )
            
            query = f"Provide competitive intelligence on {test_case.competitor_name} from {test_case.company_name}'s perspective"
            
        elif test_case.type == TestCaseType.FINANCIAL_ANALYSIS:
            if verbose:
                print(f"  → Basic: Analyzing financial document...")
            basic_response = basic.analyze_financial_document(test_case.document_content)
            time.sleep(SYSTEM_DELAY)
            
            if verbose:
                print(f"  → Detailed: Analyzing financial document...")
            detailed_response = detailed.analyze_financial_document(test_case.document_content)
            time.sleep(SYSTEM_DELAY)
            
            if verbose:
                print(f"  → Agentic: Analyzing financial document...")
            agentic_response = agentic.analyze_financial_document(test_case.document_content)
            
            query = f"Analyze this financial document and extract key insights"
            
        elif test_case.type == TestCaseType.RATIO_ANALYSIS:
            if verbose:
                print(f"  → Basic: Calculating financial ratios...")
            basic_response = basic.calculate_financial_ratios(test_case.document_content)
            time.sleep(SYSTEM_DELAY)
            
            if verbose:
                print(f"  → Detailed: Calculating financial ratios...")
            detailed_response = detailed.calculate_financial_ratios(test_case.document_content)
            time.sleep(SYSTEM_DELAY)
            
            if verbose:
                print(f"  → Agentic: Calculating financial ratios...")
            agentic_response = agentic.calculate_financial_ratios(test_case.document_content)
            
            query = f"Calculate and analyze key financial ratios from this data"
            
        elif test_case.type == TestCaseType.CHAT_QUESTION:
            if verbose:
                print(f"  → Basic: Answering question...")
            basic_response = basic.answer_question(test_case.question, test_case.context)
            time.sleep(SYSTEM_DELAY)
            
            if verbose:
                print(f"  → Detailed: Answering question...")
            detailed_response = detailed.answer_question(test_case.question, test_case.context)
            time.sleep(SYSTEM_DELAY)
            
            if verbose:
                print(f"  → Agentic: Answering question...")
            agentic_response = agentic.answer_question(test_case.question, test_case.context)
            
            query = test_case.question
            
        elif test_case.type == TestCaseType.COMPANY_RESEARCH:
            # Use specific question if provided (for recency tests), otherwise general research
            specific_question = test_case.question if test_case.question else None
            
            if verbose:
                if specific_question:
                    print(f"  → Basic: Researching {test_case.company_name} (specific query)...")
                else:
                    print(f"  → Basic: Researching {test_case.company_name}...")
            basic_response = basic.research_company(test_case.company_name, specific_question)
            time.sleep(SYSTEM_DELAY)
            
            if verbose:
                if specific_question:
                    print(f"  → Detailed: Researching {test_case.company_name} (specific query)...")
                else:
                    print(f"  → Detailed: Researching {test_case.company_name}...")
            detailed_response = detailed.research_company(test_case.company_name, specific_question)
            time.sleep(SYSTEM_DELAY)
            
            if verbose:
                if specific_question:
                    print(f"  → Agentic: Researching {test_case.company_name} (specific query)...")
                else:
                    print(f"  → Agentic: Researching {test_case.company_name}...")
            agentic_response = agentic.research_company(test_case.company_name, specific_question)
            
            query = specific_question if specific_question else f"Provide comprehensive research on {test_case.company_name}"
            
        elif test_case.type == TestCaseType.REGULATORY_ANALYSIS:
            if verbose:
                print(f"  → Basic: Analyzing regulations for {test_case.company_name}...")
            basic_response = basic.regulatory_analysis(test_case.company_name)
            time.sleep(SYSTEM_DELAY)
            
            if verbose:
                print(f"  → Detailed: Analyzing regulations for {test_case.company_name}...")
            detailed_response = detailed.regulatory_analysis(test_case.company_name)
            time.sleep(SYSTEM_DELAY)
            
            if verbose:
                print(f"  → Agentic: Analyzing regulations for {test_case.company_name}...")
            agentic_response = agentic.regulatory_analysis(test_case.company_name)
            
            query = f"Analyze regulatory risks and compliance requirements for {test_case.company_name}"
            
        else:
            print(f"  ✗ Unknown test case type: {test_case.type}")
            return None
        
        # Evaluate all three systems with judge (single call for efficiency)
        if verbose:
            print(f"  → Judge: Evaluating all three systems...")
        
        result = judge.evaluate_three_systems(
            query=query,
            basic_response=basic_response,
            detailed_response=detailed_response,
            agentic_response=agentic_response,
            test_case_id=test_case.id,
            test_case_type=test_case.type.value
        )
        
        # Add the full responses to the result
        result["basic_response"] = basic_response
        result["detailed_response"] = detailed_response
        result["agentic_response"] = agentic_response
        
        if verbose:
            basic_total = sum(result["basic_scores"].values())
            detailed_total = sum(result["detailed_scores"].values())
            agentic_total = sum(result["agentic_scores"].values())
            print(f"  ✓ Scores:")
            print(f"    Basic:    {basic_total}/25 (avg: {basic_total/5:.1f})")
            print(f"    Detailed: {detailed_total}/25 (avg: {detailed_total/5:.1f})")
            print(f"    Agentic:  {agentic_total}/25 (avg: {agentic_total/5:.1f})")
        
        return result
        
    except Exception as e:
        print(f"  ✗ Error running test case {test_case.id}: {e}")
        import traceback
        traceback.print_exc()
        return None


def run_full_evaluation(
    test_cases: Optional[List[TestCase]] = None,
    output_file: Optional[str] = None,
    verbose: bool = True
) -> dict:
    """
    Run full evaluation across all specified test cases.
    
    Args:
        test_cases: List of test cases to run. If None, uses quick evaluation set.
        output_file: Path to save JSON results. If None, uses timestamped default.
        verbose: Print progress to console.
        
    Returns:
        Evaluation report dictionary with summary and individual results.
    """
    if test_cases is None:
        test_cases = get_quick_evaluation_set()
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"evaluation_results_{timestamp}.json"
    
    print("\n" + "="*70)
    print("LLM-as-a-Judge Evaluation: Basic vs Detailed vs Agentic")
    print("Comparing all three systems with comprehensive scoring")
    print("="*70)
    print(f"Test cases to run: {len(test_cases)}")
    print(f"Output file: {output_file}")
    print("="*70)
    
    # Initialize systems
    print("\nInitializing systems...")
    basic = BasicGemini()
    detailed = DetailedGemini()
    agentic = AgenticSystem()
    judge = LLMJudge()
    print("  ✓ Basic Gemini initialized")
    print("  ✓ Detailed Gemini initialized")
    print("  ✓ Agentic System initialized")
    print("  ✓ LLM Judge initialized")
    
    # Run evaluations with rate limiting
    results: List[EvaluationResult] = []
    
    import time
    DELAY_BETWEEN_TESTS = 45  # seconds to wait between test cases (increased for Gemini free tier)
    
    for i, test_case in enumerate(test_cases):
        print(f"\n[{i+1}/{len(test_cases)}]", end="")
        result = run_single_test(test_case, basic, detailed, agentic, judge, verbose)
        if result:
            results.append(result)
        
        # Rate limiting delay between tests (except for last one)
        if i < len(test_cases) - 1:
            print(f"\n  ⏳ Waiting {DELAY_BETWEEN_TESTS}s to avoid rate limits...")
            time.sleep(DELAY_BETWEEN_TESTS)
    
    # Generate report
    print("\n" + "="*70)
    print("Generating Evaluation Report...")
    print("="*70)
    
    # Calculate aggregate statistics for three systems
    report = generate_three_system_report(results)
    
    # Print summary
    summary = report.get("summary", {})
    print(f"\n📊 EVALUATION SUMMARY")
    print(f"   Total Evaluations: {summary.get('total_evaluations', 0)}")
    
    print(f"\n📈 AVERAGE SCORES (All Three Systems)")
    avg_scores = report.get("average_scores", {})
    basic_avg = avg_scores.get("basic", {})
    detailed_avg = avg_scores.get("detailed", {})
    agentic_avg = avg_scores.get("agentic", {})
    
    print(f"   {'Dimension':<15} {'Basic':>10} {'Detailed':>10} {'Agentic':>10}")
    print(f"   {'-'*15} {'-'*10} {'-'*10} {'-'*10}")
    for dim in ["accuracy", "completeness", "actionability", "recency", "structure"]:
        b_score = basic_avg.get(dim, 0)
        d_score = detailed_avg.get(dim, 0)
        a_score = agentic_avg.get(dim, 0)
        print(f"   {dim:<15} {b_score:>10.2f} {d_score:>10.2f} {a_score:>10.2f}")
    
    print(f"\n   {'TOTAL AVERAGE':<15} {basic_avg.get('total', 0):>10.2f} {detailed_avg.get('total', 0):>10.2f} {agentic_avg.get('total', 0):>10.2f}")
    
    # Save results
    output_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "evaluation",
        output_file
    )
    
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_path}")
    
    return report


def generate_three_system_report(results: List[dict]) -> dict:
    """
    Generate evaluation report for three systems.
    
    Args:
        results: List of evaluation result dictionaries from run_single_test
        
    Returns:
        Report dictionary with summary and averages for all three systems
    """
    if not results:
        return {
            "summary": {"total_evaluations": 0},
            "average_scores": {"basic": {}, "detailed": {}, "agentic": {}},
            "individual_results": []
        }
    
    # Calculate average scores for each system
    basic_totals = {"accuracy": 0, "completeness": 0, "actionability": 0, "recency": 0, "structure": 0, "total": 0}
    detailed_totals = {"accuracy": 0, "completeness": 0, "actionability": 0, "recency": 0, "structure": 0, "total": 0}
    agentic_totals = {"accuracy": 0, "completeness": 0, "actionability": 0, "recency": 0, "structure": 0, "total": 0}
    
    # Filter out None results (failed test cases)
    valid_results = [r for r in results if r is not None]
    
    if not valid_results:
        print("\n⚠️  Warning: No valid test results to generate report")
        return {
            "summary": {
                "total_evaluations": 0,
                "timestamp": datetime.now().isoformat(),
                "error": "All test cases failed"
            },
            "average_scores": {},
            "individual_results": []
        }
    
    for result in valid_results:
        basic_scores = result["basic_scores"]
        detailed_scores = result["detailed_scores"]
        agentic_scores = result["agentic_scores"]
        
        for dim in ["accuracy", "completeness", "actionability", "recency", "structure"]:
            basic_totals[dim] += basic_scores[dim]
            detailed_totals[dim] += detailed_scores[dim]
            agentic_totals[dim] += agentic_scores[dim]
        
        # Calculate totals from individual dimensions
        basic_totals["total"] += sum(basic_scores[dim] for dim in ["accuracy", "completeness", "actionability", "recency", "structure"])
        detailed_totals["total"] += sum(detailed_scores[dim] for dim in ["accuracy", "completeness", "actionability", "recency", "structure"])
        agentic_totals["total"] += sum(agentic_scores[dim] for dim in ["accuracy", "completeness", "actionability", "recency", "structure"])
    
    n = len(valid_results)
    basic_avg = {dim: round(basic_totals[dim] / n, 2) for dim in basic_totals}
    detailed_avg = {dim: round(detailed_totals[dim] / n, 2) for dim in detailed_totals}
    agentic_avg = {dim: round(agentic_totals[dim] / n, 2) for dim in agentic_totals}
    
    # Include both valid and failed results for transparency
    failed_count = len(results) - len(valid_results)
    
    return {
        "summary": {
            "total_evaluations": n,
            "total_tests_run": len(results),
            "failed_tests": failed_count,
            "timestamp": datetime.now().isoformat()
        },
        "average_scores": {
            "basic": basic_avg,
            "detailed": detailed_avg,
            "agentic": agentic_avg
        },
        "individual_results": results
    }


def main():
    """CLI entry point for evaluation runner."""
    parser = argparse.ArgumentParser(
        description="Run LLM-as-a-Judge evaluation comparing Basic vs Detailed vs Agentic systems"
    )
    parser.add_argument(
        "--mode",
        choices=["quick", "full", "single"],
        default="quick",
        help="Evaluation mode: quick (4 tests), full (all tests), single (one test)"
    )
    parser.add_argument(
        "--test-id",
        type=str,
        help="Test case ID for single mode (e.g., comp_id_001)"
    )
    parser.add_argument(
        "--category",
        choices=[
            "competitor_identification",
            "competitive_intelligence",
            "financial_analysis",
            "ratio_analysis",
            "chat_question",
            "company_research"
        ],
        help="Run only tests in this category"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file name for results JSON"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce output verbosity"
    )
    
    args = parser.parse_args()
    
    # Determine test cases to run
    if args.mode == "single":
        if not args.test_id:
            print("Error: --test-id required for single mode")
            sys.exit(1)
        test_cases = [tc for tc in ALL_TEST_CASES if tc.id == args.test_id]
        if not test_cases:
            print(f"Error: Test case '{args.test_id}' not found")
            sys.exit(1)
    elif args.mode == "full":
        test_cases = get_full_evaluation_set()
    else:  # quick
        test_cases = get_quick_evaluation_set()
    
    # Filter by category if specified
    if args.category:
        type_map = {
            "competitor_identification": TestCaseType.COMPETITOR_IDENTIFICATION,
            "competitive_intelligence": TestCaseType.COMPETITIVE_INTELLIGENCE,
            "financial_analysis": TestCaseType.FINANCIAL_ANALYSIS,
            "ratio_analysis": TestCaseType.RATIO_ANALYSIS,
            "chat_question": TestCaseType.CHAT_QUESTION,
            "company_research": TestCaseType.COMPANY_RESEARCH,
        }
        target_type = type_map.get(args.category)
        test_cases = [tc for tc in test_cases if tc.type == target_type]
    
    # Run evaluation
    run_full_evaluation(
        test_cases=test_cases,
        output_file=args.output,
        verbose=not args.quiet
    )


if __name__ == "__main__":
    main()
