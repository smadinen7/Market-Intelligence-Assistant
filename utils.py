import streamlit as st
from pypdf import PdfReader
import io
import re
import pandas as pd
from knowledge_graph import CompetitiveKnowledgeGraph

class CentralMemory:
    def __init__(self):
        self.memory = {
            "internal_analysis": {},
            "market_analysis": {},
            "competitive_intelligence": {},
            "current_focus": None
        }
        self.knowledge_graph = CompetitiveKnowledgeGraph()

    def set_focus(self, focus):
        self.memory["current_focus"] = focus

    def get_focus(self):
        return self.memory["current_focus"]

    def update_internal_analysis(self, data):
        self.memory["internal_analysis"].update(data)

    def get_internal_analysis(self):
        return self.memory["internal_analysis"]

    def update_market_analysis(self, data):
        self.memory["market_analysis"].update(data)

    def get_market_analysis(self):
        return self.memory["market_analysis"]

    def update_competitive_intelligence(self, data):
        self.memory["competitive_intelligence"].update(data)

    def get_competitive_intelligence(self):
        return self.memory["competitive_intelligence"]
    
    def get_knowledge_graph(self):
        """Get the knowledge graph instance."""
        return self.knowledge_graph
    
    def get_graph_context_for_query(self, query: str = "") -> str:
        """Generate context from knowledge graph for answering queries."""
        graph = self.knowledge_graph
        
        # Get graph summary
        context = graph.get_graph_summary() + "\n\n"
        
        # Get competitive intelligence data
        comp_intel = self.get_competitive_intelligence()
        user_company = comp_intel.get('user_company', '')
        
        if user_company:
            context += f"\n**User Company: {user_company}**\n"
            
            # Get user company network
            network = graph.get_company_network(user_company)
            if network['competitors']:
                context += f"\nCompetitors: {', '.join(network['competitors'])}\n"
            if network['markets']:
                context += f"Markets: {', '.join(network['markets'])}\n"
            if network['products']:
                context += f"Products: {', '.join(network['products'])}\n"
        
        return context

    def get_chat_context(self):
        focus = self.get_focus()
        if focus == "internal_analysis":
            return self.get_internal_analysis().get("document_content", "")
        elif focus == "market_analysis":
            comp_intel = self.get_competitive_intelligence()
            if comp_intel.get("selected_competitor_analysis"):
                return comp_intel.get("selected_competitor_analysis", "")
            return self.get_market_analysis().get("company_analysis", "")
        return ""

def get_memory():
    if 'central_memory' not in st.session_state:
        st.session_state.central_memory = CentralMemory()
    return st.session_state.central_memory

def process_uploaded_files(uploaded_files):
    """Reads text from uploaded files (PDF, TXT, MD, CSV) and combines them."""
    combined_text = ""
    if uploaded_files:
        for file in uploaded_files:
            try:
                if file.type == "application/pdf":
                    pdf_reader = PdfReader(io.BytesIO(file.getvalue()))
                    for page in pdf_reader.pages:
                        combined_text += page.extract_text() + "\n\n"
                elif file.type == "text/csv" or file.name.lower().endswith('.csv'):
                    # Read CSV and convert to string summary
                    df = pd.read_csv(file)
                    combined_text += f"=== CSV FILE: {file.name} ===\n"
                    combined_text += df.to_string(index=False) + "\n\n"
                else:  # Assumes .txt, .md, etc.
                    combined_text += file.getvalue().decode("utf-8") + "\n\n"
            except Exception as e:
                st.error(f"Error processing file {file.name}: {e}")
    return combined_text

def process_financial_documents(uploaded_files):
    """Reads and processes financial documents with enhanced extraction for financial data, including CSV support."""
    combined_text = ""
    financial_data = {}
    if uploaded_files:
        for file in uploaded_files:
            try:
                if file.type == "application/pdf":
                    pdf_reader = PdfReader(io.BytesIO(file.getvalue()))
                    file_text = ""
                    for page in pdf_reader.pages:
                        file_text += page.extract_text() + "\n\n"
                elif file.type == "text/csv" or file.name.lower().endswith('.csv'):
                    df = pd.read_csv(file)
                    file_text = f"=== CSV FILE: {file.name} ===\n" + df.to_string(index=False) + "\n\n"
                else:  # Assumes .txt, .md, etc.
                    file_text = file.getvalue().decode("utf-8") + "\n\n"
                combined_text += f"=== FILE: {file.name} ===\n{file_text}\n"
                financial_data[file.name] = extract_financial_metrics(file_text)
            except Exception as e:
                st.error(f"Error processing file {file.name}: {e}")
    return combined_text, financial_data

def extract_financial_metrics(text):
    """Extract common financial metrics from text using regex patterns."""
    metrics = {}
    
    # More flexible patterns that look for keywords followed by numbers (with various separators)
    # The number can appear after colons, spaces, newlines, or be on the next line
    patterns = {
        'revenue': r'(?:revenue|total\s+revenue|net\s+sales|total\s+sales)[\s:]*?[\$]?\s*([\d,]+(?:\.\d+)?)\s*(?:million|billion|M|B)?',
        'profit': r'(?:net\s+income|net\s+profit|total\s+profit|earnings)[\s:]*?[\$]?\s*([\d,]+(?:\.\d+)?)\s*(?:million|billion|M|B)?',
        'assets': r'(?:total\s+assets)[\s:]*?[\$]?\s*([\d,]+(?:\.\d+)?)\s*(?:million|billion|M|B)?',
        'debt': r'(?:total\s+debt|long[\s-]?term\s+debt|total\s+liabilities)[\s:]*?[\$]?\s*([\d,]+(?:\.\d+)?)\s*(?:million|billion|M|B)?',
        'cash': r'(?:cash\s+and\s+cash\s+equivalents|total\s+cash|cash\s+position)[\s:]*?[\$]?\s*([\d,]+(?:\.\d+)?)\s*(?:million|billion|M|B)?',
        'equity': r'(?:shareholders[\'\s]+equity|stockholders[\'\s]+equity|total\s+equity)[\s:]*?[\$]?\s*([\d,]+(?:\.\d+)?)\s*(?:million|billion|M|B)?'
    }
    
    for metric, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Clean up and filter valid numeric matches
            cleaned_matches = []
            for m in matches:
                m = m.strip()
                # Only keep if it contains digits
                if m and re.search(r'\d', m):
                    cleaned_matches.append(m)
            if cleaned_matches:
                metrics[metric] = cleaned_matches
    
    return metrics

def validate_company_name(company_name):
    """Basic validation for company names."""
    if not company_name or len(company_name.strip()) < 2:
        return False, "Company name must be at least 2 characters long."
    
    # Remove common company suffixes for processing
    clean_name = re.sub(r'\b(inc|corp|corporation|ltd|llc|co)\b\.?', '', company_name, flags=re.IGNORECASE)
    
    if len(clean_name.strip()) < 2:
        return False, "Please provide a valid company name."
    
    return True, clean_name.strip()

def format_financial_number(value, format_type="auto"):
    """Format financial numbers for display."""
    try:
        num_value = float(value)
        
        if format_type == "currency":
            if abs(num_value) >= 1e9:
                return f"${num_value/1e9:.1f}B"
            elif abs(num_value) >= 1e6:
                return f"${num_value/1e6:.1f}M"
            elif abs(num_value) >= 1e3:
                return f"${num_value/1e3:.1f}K"
            else:
                return f"${num_value:,.2f}"
        
        elif format_type == "percentage":
            return f"{num_value:.2f}%"
        
        else:  # auto format
            if abs(num_value) >= 1e9:
                return f"{num_value/1e9:.1f}B"
            elif abs(num_value) >= 1e6:
                return f"{num_value/1e6:.1f}M"
            elif abs(num_value) >= 1e3:
                return f"{num_value/1e3:.1f}K"
            else:
                return f"{num_value:,.2f}"
    
    except (ValueError, TypeError):
        return str(value)

def safe_rerun():
    """Compatibility helper for Streamlit rerun across versions.

    Tries `st.experimental_rerun()` first, falls back to `st.rerun()` if available.
    If neither exists, sets a session flag so the UI can respond gracefully.
    """
    try:
        import streamlit as st
        if hasattr(st, "experimental_rerun"):
            try:
                st.experimental_rerun()
                return
            except Exception:
                pass
        if hasattr(st, "rerun"):
            try:
                st.rerun()
                return
            except Exception:
                pass
        # Final fallback: toggle a session flag that pages can observe.
        try:
            st.session_state["__rerun_requested__"] = not st.session_state.get("__rerun_requested__", False)
        except Exception:
            # If session state isn't available, do nothing.
            pass
    except Exception:
        # If Streamlit import fails for some reason, silently ignore.
        return
