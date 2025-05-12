import streamlit as st
from src.backend.config.config import init_config
from src.frontend.pages.dashboard import show_dashboard
from src.frontend.pages.analysis import show_analysis_tools

def main():
    st.set_page_config(layout="wide", page_title="Dataset Analyzer")
    
    # Initialize configuration
    init_config()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Analysis Tools"])
    
    if page == "Dashboard":
        show_dashboard()
    else:
        show_analysis_tools()

if __name__ == "__main__":
    main()

