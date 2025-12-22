# 🔧 LLM Configuration Guide

This guide explains how to change the LLM providers used in the Market Intelligence Assistant.

---

## 📋 Table of Contents

1. [Current LLM Setup](#-current-llm-setup)
2. [Supported LLM Providers](#-supported-llm-providers)
3. [Changing the Primary LLM](#-changing-the-primary-llm)
4. [Changing the Secondary LLM](#-changing-the-secondary-llm)
5. [Using OpenAI](#-using-openai)
6. [Using Anthropic Claude](#-using-anthropic-claude)
7. [Using Local Models](#-using-local-models-ollama)
8. [Configuration Examples](#-configuration-examples)

---

## 🏗️ Current LLM Setup

The application currently uses:

| LLM | Model | Purpose | File |
|-----|-------|---------|------|
| **Primary** | Gemini 2.5 Flash | All agents (11 of 12) | `financial_agents.py` |
| **Secondary** | Llama 3 70B (Groq) | Market Comparison Agent | `financial_agents.py` |

---

## 🤖 Supported LLM Providers

CrewAI supports these LLM providers out of the box:

| Provider | Model Examples | API Key Required |
|----------|----------------|------------------|
| **Google Gemini** | `gemini/gemini-2.5-flash`, `gemini/gemini-pro` | `GEMINI_API_KEY` |
| **OpenAI** | `gpt-4o`, `gpt-4-turbo`, `gpt-3.5-turbo` | `OPENAI_API_KEY` |
| **Anthropic** | `claude-3-5-sonnet-20241022`, `claude-3-opus` | `ANTHROPIC_API_KEY` |
| **Groq** | `groq/llama3-70b-8192`, `groq/mixtral-8x7b` | `GROQ_API_KEY` |
| **Ollama** | `ollama/llama3`, `ollama/mistral` | None (local) |
| **Azure OpenAI** | Custom deployment names | `AZURE_OPENAI_API_KEY` |

---

## 🔄 Changing the Primary LLM

### Step 1: Open `financial_agents.py`

Locate the LLM configuration section (around line 53-75):

```python
# Define the LLMs
gemini_llm = LLM(
    api_key=gemini_api_key,
    model="gemini/gemini-2.5-flash"
)
```

### Step 2: Change the Model

Replace with your preferred model:

```python
# Example: Switch to OpenAI GPT-4o
primary_llm = LLM(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o"
)
```

### Step 3: Update All Agent References

Find all instances of `llm=gemini_llm` and replace with `llm=primary_llm`:

```python
# Before
def financial_document_analyzer_agent(self):
    return Agent(
        role='Financial Document Analyzer',
        ...
        llm=gemini_llm,  # <-- Change this
        ...
    )

# After
def financial_document_analyzer_agent(self):
    return Agent(
        role='Financial Document Analyzer',
        ...
        llm=primary_llm,  # <-- New LLM
        ...
    )
```

### Step 4: Add API Key

Add the new API key to your `.env` file:

```env
OPENAI_API_KEY=sk-...
```

And update the key retrieval:

```python
openai_api_key = get_api_key("OPENAI_API_KEY")
```

---

## ⚡ Changing the Secondary LLM

The secondary LLM (currently Groq) is used for the Market Comparison Agent:

```python
# Current configuration (around line 70)
groq_llm = LLM(
    api_key=groq_api_key,
    model="groq/llama3-70b-8192"
)
```

To change it:

```python
# Example: Use Anthropic Claude for market comparison
secondary_llm = LLM(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-3-5-sonnet-20241022"
)
```

Then update `market_comparison_agent`:

```python
def market_comparison_agent(self):
    return Agent(
        role='Market Comparison Analyst',
        ...
        llm=secondary_llm,  # Changed from groq_llm
        ...
    )
```

---

## 🟢 Using OpenAI

### Configuration

```python
from crewai import Agent, LLM
import os

# Get API key
openai_api_key = get_api_key("OPENAI_API_KEY")

# Define OpenAI LLM
openai_llm = LLM(
    api_key=openai_api_key,
    model="gpt-4o"  # or "gpt-4-turbo", "gpt-3.5-turbo"
)
```

### Available Models

| Model | Best For | Cost |
|-------|----------|------|
| `gpt-4o` | Best quality, multimodal | $$$ |
| `gpt-4-turbo` | Long context, good quality | $$ |
| `gpt-3.5-turbo` | Fast, economical | $ |

### Environment Variable

```env
OPENAI_API_KEY=sk-proj-...
```

---

## 🟣 Using Anthropic Claude

### Configuration

```python
from crewai import Agent, LLM
import os

# Get API key
anthropic_api_key = get_api_key("ANTHROPIC_API_KEY")

# Define Claude LLM
claude_llm = LLM(
    api_key=anthropic_api_key,
    model="claude-3-5-sonnet-20241022"
)
```

### Available Models

| Model | Best For | Cost |
|-------|----------|------|
| `claude-3-5-sonnet-20241022` | Best balance of speed/quality | $$ |
| `claude-3-opus-20240229` | Highest capability | $$$ |
| `claude-3-haiku-20240307` | Fastest, most economical | $ |

### Environment Variable

```env
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 🖥️ Using Local Models (Ollama)

### Prerequisites

1. Install [Ollama](https://ollama.ai/)
2. Pull a model: `ollama pull llama3`

### Configuration

```python
from crewai import Agent, LLM

# No API key needed for local models
ollama_llm = LLM(
    model="ollama/llama3"
)
```

### Available Local Models

| Model | Size | Quality |
|-------|------|---------|
| `ollama/llama3` | 8B | Good |
| `ollama/llama3:70b` | 70B | Excellent |
| `ollama/mistral` | 7B | Good |
| `ollama/mixtral` | 8x7B | Very Good |
| `ollama/codellama` | 7B | Good for code |

### Running Ollama

```bash
# Start Ollama server
ollama serve

# In another terminal, run your app
streamlit run Home.py
```

---

## 📝 Configuration Examples

### Example 1: All OpenAI

```python
# financial_agents.py

openai_api_key = get_api_key("OPENAI_API_KEY")

primary_llm = LLM(
    api_key=openai_api_key,
    model="gpt-4o"
)

secondary_llm = LLM(
    api_key=openai_api_key,
    model="gpt-3.5-turbo"  # Faster for simple tasks
)
```

### Example 2: Gemini + Claude Mix

```python
# financial_agents.py

gemini_api_key = get_api_key("GEMINI_API_KEY")
anthropic_api_key = get_api_key("ANTHROPIC_API_KEY")

# Gemini for most agents (cost-effective)
primary_llm = LLM(
    api_key=gemini_api_key,
    model="gemini/gemini-2.5-flash"
)

# Claude for strategic synthesis (highest quality)
strategy_llm = LLM(
    api_key=anthropic_api_key,
    model="claude-3-5-sonnet-20241022"
)
```

### Example 3: Local Development (Free)

```python
# financial_agents.py

# All local, no API costs
primary_llm = LLM(model="ollama/llama3")
secondary_llm = LLM(model="ollama/mistral")
```

---

## ⚠️ Important Considerations

### Cost Comparison

| Provider | Cost per 1M tokens (approx) |
|----------|----------------------------|
| Gemini 2.5 Flash | $0.075 |
| GPT-4o | $5.00 |
| Claude 3.5 Sonnet | $3.00 |
| Groq (Llama 3 70B) | $0.59 |
| Ollama (local) | Free |

### Rate Limits

- **Gemini:** 60 requests/minute (free tier)
- **OpenAI:** Varies by plan
- **Anthropic:** Varies by plan
- **Groq:** 30 requests/minute (free tier)

### Quality vs Speed Trade-offs

| Priority | Recommended Setup |
|----------|-------------------|
| **Best Quality** | GPT-4o or Claude 3 Opus |
| **Best Speed** | Groq (Llama 3) or Gemini Flash |
| **Best Cost** | Gemini Flash or Ollama (local) |
| **Balanced** | Gemini Flash + Groq (current setup) |

---

## 🔄 Quick Switch Template

Copy this template to quickly switch all agents to a new LLM:

```python
# At the top of financial_agents.py, after imports

# ============ LLM CONFIGURATION ============
# Change these values to switch LLM providers

PRIMARY_MODEL = "gemini/gemini-2.5-flash"  # Main agents
SECONDARY_MODEL = "groq/llama3-70b-8192"   # Market comparison

# API Keys
primary_api_key = get_api_key("GEMINI_API_KEY")
secondary_api_key = get_api_key("GROQ_API_KEY")

# Initialize LLMs
primary_llm = LLM(api_key=primary_api_key, model=PRIMARY_MODEL)
secondary_llm = LLM(api_key=secondary_api_key, model=SECONDARY_MODEL)
# ============================================
```

Then change just the model strings and API key names to switch providers.

---

## 📞 Need Help?

- Check [CrewAI LLM Documentation](https://docs.crewai.com/concepts/llms)
- Verify API keys are valid
- Check rate limits if getting errors
