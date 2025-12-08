# LLM-as-a-Judge Evaluation Framework

This evaluation framework compares the performance of a **baseline Gemini model** against the **multi-agent CrewAI system** using an impartial LLM judge.

## Overview

The evaluation uses a "blind" comparison approach:
1. Both systems receive the same query/task
2. Responses are anonymized as "Response A" and "Response B" (randomly assigned)
3. A judge LLM (Gemini 1.5 Pro) scores both on 5 dimensions
4. Winner is declared based on total scores

## Evaluation Dimensions

Each response is scored 1-5 on:

| Dimension | Description |
|-----------|-------------|
| **Accuracy** | Factual correctness, no hallucinations |
| **Completeness** | All required sections present with adequate detail |
| **Actionability** | Specific, implementable recommendations |
| **Recency** | Uses data from past 6 weeks (Oct-Dec 2025) |
| **Structure** | Proper formatting with required headings |

## Test Case Categories

| Category | # Tests | Description |
|----------|---------|-------------|
| Competitor Identification | 5 | Identify top 3 competitors for major companies |
| Competitive Intelligence | 5 | Deep-dive competitor analysis |
| Financial Analysis | 2 | Analyze financial documents |
| Ratio Analysis | 1 | Calculate and interpret financial ratios |
| Chat Questions | 3 | Answer questions based on analysis context |
| Company Research | 2 | Comprehensive company research |

## Usage

### Quick Evaluation (4 tests, ~5 minutes)

```bash
cd Market-Intelligence-Assistant
python -m evaluation.run_evaluation --mode quick
```

### Full Evaluation (18 tests, ~30 minutes)

```bash
python -m evaluation.run_evaluation --mode full
```

### Single Test

```bash
python -m evaluation.run_evaluation --mode single --test-id comp_intel_001
```

### By Category

```bash
python -m evaluation.run_evaluation --category competitive_intelligence
```

### Options

| Flag | Description |
|------|-------------|
| `--mode` | `quick` (4 tests), `full` (all), or `single` |
| `--test-id` | Specific test ID for single mode |
| `--category` | Filter to one test category |
| `--output` | Custom output filename |
| `--quiet` | Reduce console output |

## Output

Results are saved as JSON in the `evaluation/` directory:

```json
{
  "summary": {
    "total_evaluations": 4,
    "baseline_wins": 1,
    "agentic_wins": 3,
    "ties": 0,
    "agentic_win_rate": 75.0
  },
  "average_scores": {
    "baseline": {"accuracy": 3.5, "completeness": 3.0, ...},
    "agentic": {"accuracy": 4.25, "completeness": 4.5, ...}
  },
  "by_test_type": {...},
  "individual_results": [...]
}
```

## Programmatic Usage

```python
from evaluation import (
    LLMJudge, BaselineGemini, AgenticSystem,
    get_quick_evaluation_set, run_full_evaluation
)

# Run full evaluation
report = run_full_evaluation()
print(f"Agentic win rate: {report['summary']['agentic_win_rate']}%")

# Or run individual comparisons
baseline = BaselineGemini()
agentic = AgenticSystem()
judge = LLMJudge()

baseline_response = baseline.identify_competitors("Apple")
agentic_response = agentic.identify_competitors("Apple")

result = judge.evaluate(
    query="Identify top 3 competitors for Apple",
    baseline_response=baseline_response,
    agentic_response=agentic_response
)
print(f"Winner: {result.winner}")
```

## File Structure

```
evaluation/
├── __init__.py           # Package exports
├── llm_judge.py          # LLM Judge with scoring rubric
├── baseline_gemini.py    # Simple Gemini wrapper (baseline)
├── agentic_system.py     # CrewAI multi-agent wrapper
├── test_cases.py         # Standardized test cases
├── run_evaluation.py     # CLI runner script
└── README.md             # This file
```

## Adding Custom Test Cases

Edit `test_cases.py` to add new test cases:

```python
TestCase(
    id="comp_intel_custom",
    type=TestCaseType.COMPETITIVE_INTELLIGENCE,
    name="Custom Analysis",
    description="My custom competitive intelligence test",
    company_name="MyCompany",
    competitor_name="TheirCompany",
    expected_elements=["Recent Moves", "Strategic Recommendations"]
)
```

## Expected Results

Based on the system design, the **agentic system should outperform** baseline on:
- **Recency**: Uses Serper web search for real-time data
- **Completeness**: Structured prompts enforce all sections
- **Actionability**: Explicit Action/Impact formatting in recommendations
- **Structure**: Strict output rules with required headings

The baseline may be competitive on:
- **Accuracy**: Both use the same underlying Gemini model
- Simple queries where agent orchestration adds little value
