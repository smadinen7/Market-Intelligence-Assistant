# 📘 Market Intelligence Assistant - User Guide

Welcome to the **Market Intelligence Assistant**, your AI-powered platform for competitive analysis and financial insights.

---

## � Table of Contents

1. [Getting Started](#-getting-started)
2. [Market Analysis Module](#-market-analysis)
3. [Internal Analysis Module](#-internal-analysis)
4. [Tips for Best Results](#-tips-for-best-results)
5. [Understanding Recommendations](#-understanding-strategic-recommendations)
6. [Chat Best Practices](#-chat-best-practices)
7. [FAQ](#-frequently-asked-questions)
8. [Technical Documentation](#-technical-documentation)

---

## 🚀 Getting Started

### Accessing the Platform

**Local Development:**
1. Navigate to the project directory
2. Run `streamlit run Home.py`
3. Open `http://localhost:8501` in your browser

**Streamlit Cloud:**
1. Access your deployed app URL (e.g., `https://your-app.streamlit.app`)
2. See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions

### Two Main Modules
- **📈 Market Analysis** - Competitive intelligence and market research
- **📄 Internal Analysis** - Financial document analysis

---

## 📈 Market Analysis

### Step 1: Start a New Analysis
1. Click **"Market Analysis"** in the sidebar
2. Enter your company name (e.g., "Apple", "Tesla", "Microsoft")
3. Click **"🔍 Start Competitive Analysis"**

### Step 2: Review Your Competitors
The AI will automatically identify your top 3 competitors and explain why each is a competitive threat. You'll see:
- Company names with competitive positioning
- Primary areas of overlap
- Key competitive threats

### Step 3: Deep-Dive Analysis
1. Click the **"Analyze"** button next to any competitor
2. Wait for the AI to gather real-time market data (this may take 30-60 seconds)
3. View the comprehensive analysis including:

| Section | What You'll Learn |
|---------|-------------------|
| **Recent Moves** | What the competitor has done in the last 6 weeks |
| **Major Markets** | Where they operate and their market share |
| **Hero Products** | Their key products and competitive positioning |
| **Financial Snapshot** | Revenue, profit, and key financial metrics |
| **Direct Threats** | How they threaten your business |
| **Strategic Recommendations** | Prioritized actions you should take |

### Step 4: Analyze Multiple Competitors
- Return to the **Competitor Identification** tab
- Click **"Analyze"** on additional competitors
- View all analyses in the **Detailed Analysis** tab with separate tabs for each competitor

### Step 5: Ask Follow-Up Questions
Use the chat panel on the right to ask questions like:
- *"What should be our top priority?"*
- *"Tell me more about [specific recommendation]"*
- *"How does their cloud strategy compare to ours?"*
- *"What are the key risks we should address first?"*

---

## 📄 Internal Analysis

### Step 1: Upload Documents
1. Click **"Internal Analysis"** in the sidebar
2. Upload your financial documents:
   - **Supported formats:** PDF, TXT, MD, CSV
   - **Recommended:** 10-K filings, earnings reports, annual reports

### Step 2: View Initial Analysis
After uploading, you'll receive:
- **Quick Summary** with key highlights
- **Financial Health Score** (1-10 scale)
- **Main Strengths** and **Concerns**
- **Investment View** (Positive/Neutral/Negative)

### Step 3: Generate Detailed Reports
In the **Key Metrics** tab:
- Click **"📊 Generate Ratio Analysis"** for financial ratios
- Click **"⚠️ Generate Risk Assessment"** for risk analysis

### Step 4: Ask Questions
Use the chat to ask about your documents:
- *"What are the main revenue drivers?"*
- *"Summarize the key risks mentioned"*
- *"How has profitability changed year-over-year?"*

---

## 💡 Tips for Best Results

### Market Analysis
✅ Use official company names (e.g., "Apple Inc." or "Apple")  
✅ Analyze 2-3 competitors for a comprehensive view  
✅ Ask specific follow-up questions for actionable insights  
✅ Look at **[HIGH PRIORITY]** recommendations first

### Internal Analysis
✅ Upload complete documents for better analysis  
✅ Include multiple years of data when available  
✅ Generate both ratio analysis and risk assessment  
✅ Ask clarifying questions about specific metrics

---

## 🎯 Understanding Strategic Recommendations

Recommendations are tagged with priority levels:

| Priority | Meaning | Action Timeframe |
|----------|---------|------------------|
| **[HIGH PRIORITY]** | Critical for competitive advantage | Immediate (0-3 months) |
| **[MEDIUM PRIORITY]** | Important for long-term positioning | Near-term (3-6 months) |
| **[LOW PRIORITY]** | Nice to have, opportunistic | When resources allow |

Each recommendation includes:
- **Action:** Specific steps to implement
- **Impact:** Expected business benefits

---

## 💬 Chat Best Practices

### Effective Questions
- ✅ *"What is our highest priority action against [Competitor]?"*
- ✅ *"Explain the AI strategy recommendation in more detail"*
- ✅ *"What markets should we focus on?"*
- ✅ *"Compare the financial health of [Competitor A] vs [Competitor B]"*

### The AI Remembers Context
- All competitor analyses are available for reference
- You can ask about any previously analyzed competitor
- The AI connects insights across multiple analyses

---

## 🔄 Starting Fresh

To begin a new analysis session:
1. Click **"🔄 New Analysis"** button in the top-right
2. This clears the current session and lets you start over
3. Previous analyses are not saved between sessions

---

## ❓ Frequently Asked Questions

**Q: How current is the data?**  
A: All market data is fetched in real-time from the web, typically reflecting information from the past few weeks.

**Q: Can I analyze any company?**  
A: Yes, the platform works for public and well-known private companies across all industries.

**Q: How long does an analysis take?**  
A: Competitor identification takes about 30 seconds. Each deep-dive analysis takes 30-60 seconds.

**Q: Is my uploaded data secure?**  
A: Uploaded documents are processed locally and not stored permanently. Session data is cleared when you close the browser.

---

## 📞 Need Help?

If you encounter any issues or have questions:
- Check that you've entered a valid company name
- Try refreshing the page if an analysis seems stuck
- Start a new analysis session if you experience unexpected behavior

---

## 📚 Technical Documentation

For technical setup and customization, refer to:

| Document | Purpose |
|----------|---------|
| [DEPLOYMENT.md](DEPLOYMENT.md) | Deploy to Streamlit Cloud with API keys |
| [LLM_CONFIGURATION.md](LLM_CONFIGURATION.md) | Change LLM providers (Gemini → OpenAI, etc.) |
| [SCALABILITY_GUIDE.md](SCALABILITY_GUIDE.md) | Add new agents, features, and extend functionality |
| [README.md](README.md) | Project overview and local setup |

---

## 🔐 API Keys Required

The application requires the following API keys:

| Key | Purpose | Required |
|-----|---------|----------|
| `GEMINI_API_KEY` | Primary LLM (Gemini 2.5 Flash) | ✅ Yes |
| `GROQ_API_KEY` | Secondary LLM (Llama 3 70B) | ⚠️ Optional |
| `SERPER_API_KEY` | Real-time web search | ⚠️ Optional |

See [DEPLOYMENT.md](DEPLOYMENT.md) for instructions on obtaining and configuring these keys.

---

*Thank you for using Market Intelligence Assistant!*
