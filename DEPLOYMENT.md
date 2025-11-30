# Deploying CEO AI Assistant to Streamlit Cloud

This guide will help you deploy your application to Streamlit Cloud and configure the necessary API keys.

## Prerequisites
- A GitHub account.
- Your project pushed to a GitHub repository.
- Your `GEMINI_API_KEY` and `GROQ_API_KEY`.

## Steps

### 1. Push to GitHub
Ensure your latest code is pushed to your GitHub repository.
```bash
git add .
git commit -m "Prepare for deployment"
git push
```

### 2. Deploy on Streamlit Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **New app**.
3.  Select your repository, branch (usually `main`), and the main file path (`Home.py`).
4.  Click **Deploy!**.

### 3. Configure Secrets (API Keys)
Your app will likely fail to start initially because it's missing the API keys. You need to add them as "Secrets".

1.  On your app's dashboard in Streamlit Cloud, click the **Settings** menu (three dots in the top right) -> **Settings**.
2.  Go to the **Secrets** tab.
3.  Paste your API keys in the TOML format shown below:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
GROQ_API_KEY = "your_groq_api_key_here"
```

4.  Click **Save**.

### 4. Reboot
After saving the secrets, your app should automatically restart. If not, you can manually reboot it from the menu.

## Troubleshooting
- **Module not found**: Ensure all your dependencies are listed in `requirements.txt`.
- **Key errors**: Double-check that the variable names in Secrets match exactly (`GEMINI_API_KEY`, `GROQ_API_KEY`).
