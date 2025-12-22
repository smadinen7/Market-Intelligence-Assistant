# 🚀 Deploying Market Intelligence Assistant to Streamlit Cloud

This guide covers deploying the application to Streamlit Cloud and configuring API keys.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [API Keys Setup](#-api-keys-setup)
3. [Deployment Steps](#-deployment-steps)
4. [Configuring Secrets](#-configuring-secrets)
5. [Troubleshooting](#-troubleshooting)
6. [Local Development](#-local-development)

---

## Prerequisites

- A GitHub account
- Your project pushed to a GitHub repository
- API keys (see below)

---

## 🔑 API Keys Setup

### Required Keys

| Key | Provider | Purpose | Get It Here |
|-----|----------|---------|-------------|
| `GEMINI_API_KEY` | Google | Primary LLM (Gemini 2.5 Flash) | [Google AI Studio](https://aistudio.google.com/apikey) |
| `GROQ_API_KEY` | Groq | Fast inference (Llama 3 70B) | [Groq Console](https://console.groq.com/keys) |
| `SERPER_API_KEY` | Serper | Real-time web search | [Serper.dev](https://serper.dev/) |

### Obtaining API Keys

#### 1. Gemini API Key (Required)
1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key and save it securely

#### 2. Groq API Key (Recommended)
1. Go to [Groq Console](https://console.groq.com/keys)
2. Sign up or log in
3. Navigate to **API Keys** section
4. Click **"Create API Key"**
5. Copy and save the key

#### 3. Serper API Key (Recommended for Real-Time Data)
1. Go to [Serper.dev](https://serper.dev/)
2. Sign up for an account
3. Navigate to your dashboard
4. Copy your API key (free tier: 2,500 queries/month)

---

## 📤 Deployment Steps

### Step 1: Push to GitHub

Ensure your latest code is pushed to your GitHub repository:

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Click **"New app"**
3. Connect your GitHub account if not already connected
4. Select:
   - **Repository:** Your repository name
   - **Branch:** `main`
   - **Main file path:** `Home.py`
5. Click **"Deploy!"**

### Step 3: Wait for Build

- The initial build takes 2-5 minutes
- The app will show errors until you configure secrets (next step)

---

## 🔐 Configuring Secrets

### Adding API Keys to Streamlit Cloud

1. On your app's dashboard in Streamlit Cloud, click the **⋮** menu (three dots)
2. Select **"Settings"**
3. Go to the **"Secrets"** tab
4. Paste your API keys in TOML format:

```toml
# Required - Primary LLM
GEMINI_API_KEY = "your_gemini_api_key_here"

# Recommended - Fast inference for market comparison
GROQ_API_KEY = "your_groq_api_key_here"

# Recommended - Real-time web search
SERPER_API_KEY = "your_serper_api_key_here"
```

5. Click **"Save"**
6. The app will automatically restart

### Secrets Format Example

```toml
GEMINI_API_KEY = "AIzaSyC..."
GROQ_API_KEY = "gsk_..."
SERPER_API_KEY = "abc123..."
```

> ⚠️ **Important:** Do NOT include quotes around the entire line, only around the value.

---

## 🔧 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| **"Module not found"** | Check that all dependencies are in `requirements.txt` |
| **"GEMINI_API_KEY not found"** | Verify secrets are saved correctly (exact variable names) |
| **App crashes on start** | Check logs in Streamlit Cloud dashboard |
| **Web search not working** | Add `SERPER_API_KEY` to secrets |
| **Slow responses** | Add `GROQ_API_KEY` for faster market comparison |

### Viewing Logs

1. Go to your app dashboard on Streamlit Cloud
2. Click **"Manage app"** (bottom right)
3. Select **"Logs"** to view application logs

### Restarting the App

1. Click **"Manage app"**
2. Select **"Reboot app"**

---

## 💻 Local Development

### Setup for Local Testing

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Market-Intelligence-Assistant
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```

5. **Add your API keys to `.env`:**
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   ```

6. **Run the application:**
   ```bash
   streamlit run Home.py
   ```

7. **Access at:** `http://localhost:8501`

---

## 🔄 Updating the Deployment

When you push changes to your GitHub repository:

1. Streamlit Cloud automatically detects changes
2. The app rebuilds and redeploys
3. No manual action required

To force a rebuild:
1. Go to app settings
2. Click **"Reboot app"**

---

## 📊 Resource Limits (Free Tier)

Streamlit Cloud free tier limits:
- **Apps:** Up to 3 public apps
- **Resources:** 1 GB RAM
- **Sleep:** Apps sleep after 7 days of inactivity

For higher limits, consider Streamlit Cloud Teams or self-hosting.

---

## 📞 Support

If you encounter issues:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review Streamlit Cloud logs
3. Verify all API keys are valid and have quota remaining
