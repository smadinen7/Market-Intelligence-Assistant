import streamlit as st

st.set_page_config(
    page_title="CEO AI Assistant - Financial Intelligence Platform",
    page_icon="💼",
    layout="wide"
)

# --- Simple styling ---
st.markdown("""
<style>
    .hero-section { 
        padding: 3rem 1rem; 
        text-align: center; 
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class="hero-section">
    <h1>💼 CEO AI Assistant</h1>
    <p>Your AI-powered platform for financial and competitive intelligence</p>
</div>
""", unsafe_allow_html=True)

# --- Navigation Buttons ---
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### Choose your analysis type:")
    st.markdown("")
    
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        if st.button("📄 Internal Analysis", use_container_width=True, help="Analyze your financial documents"):
            st.switch_page("pages/1_Internal_Analysis.py")
        st.caption("Upload and analyze financial documents like 10-K filings, earnings reports, and annual reports.")
    
    with btn_col2:
        if st.button("📈 Market Analysis", use_container_width=True, help="Competitive intelligence and market research"):
            st.switch_page("pages/2_Market_Analysis.py")
        st.caption("Enter your company to identify competitors and get deep competitive intelligence insights.")
