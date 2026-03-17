import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import time

# Configure page
st.set_page_config(
    page_title="AI Financial Analyzer",
    page_icon="📊",
    layout="wide"
)

# API endpoint (update if deployed elsewhere)
API_URL = "http://localhost:8000"

# Title and description
st.title("📊 AI Financial Analyzer")
st.markdown("""
Upload financial documents (10-K, annual reports) and ask questions about them using AI.
""")

# Initialize session state
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'current_doc' not in st.session_state:
    st.session_state.current_doc = None

# Sidebar
with st.sidebar:
    st.header("📁 Document Management")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload PDF Documents",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload financial reports (max 10MB each)"
    )
    
    # Process uploaded files
    if uploaded_files:
        for file in uploaded_files:
            if file.name not in st.session_state.documents:
                with st.spinner(f"Processing {file.name}..."):
                    # Send to backend
                    files = {"file": (file.name, file.getvalue(), "application/pdf")}
                    try:
                        response = requests.post(f"{API_URL}/upload", files=files)
                        if response.status_code == 200:
                            st.success(f"✅ {file.name} processed")
                            st.session_state.documents.append(file.name)
                            st.session_state.current_doc = file.name
                        else:
                            st.error(f"❌ {file.name}: {response.text}")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
    
    # Document selector
    if st.session_state.documents:
        st.divider()
        st.subheader("Select Document")
        selected_doc = st.selectbox(
            "Choose a document to analyze",
            st.session_state.documents,
            index=0 if st.session_state.current_doc else 0
        )
        st.session_state.current_doc = selected_doc
    
    # API status
    st.divider()
    st.subheader("System Status")
    try:
        response = requests.get(API_URL, timeout=2)
        if response.status_code == 200:
            st.success("✅ Backend connected")
        else:
            st.error("❌ Backend error")
    except:
        st.error("❌ Backend not reachable")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🔍 Ask Questions")
    
    # Question input
    question = st.text_area(
        "Enter your question about the financial document:",
        placeholder="e.g., What was the revenue in 2023? What are the total assets?",
        height=100
    )
    
    # Ask button
    if st.button("Ask Question", type="primary", use_container_width=True):
        if not st.session_state.current_doc:
            st.warning("Please upload a document first")
        elif not question:
            st.warning("Please enter a question")
        else:
            with st.spinner("Analyzing document..."):
                try:
                    response = requests.post(
                        f"{API_URL}/query",
                        params={"question": question}
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.success("Answer:")
                        st.markdown(f"> {result['answer']}")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
    
    # Example questions
    with st.expander("📝 Example Questions"):
        st.markdown("""
        - What was the total revenue for the fiscal year?
        - What is the net income?
        - What are the total assets?
        - How much did R&D spending increase?
        - What are the key risks mentioned?
        """)

with col2:
    st.header("📈 Financial Metrics")
    
    # Extract metrics button
    if st.button("Extract Key Metrics", use_container_width=True):
        if not st.session_state.current_doc:
            st.warning("Upload a document first")
        else:
            with st.spinner("Extracting metrics..."):
                try:
                    response = requests.post(f"{API_URL}/extract")
                    if response.status_code == 200:
                        metrics = response.json()["metrics"]
                        
                        # Display metrics in a nice format
                        metric_data = {
                            "Metric": list(metrics.keys()),
                            "Value": list(metrics.values())
                        }
                        df = pd.DataFrame(metric_data)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.error("Failed to extract metrics")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
    
    st.divider()
    
    # Sample dashboard
    st.subheader("📊 Trend Analysis")
    
    # Sample data (replace with real data from your document)
    sample_data = pd.DataFrame({
        "Year": ["2021", "2022", "2023"],
        "Revenue": [100, 150, 200],
        "Net Income": [20, 35, 50]
    })
    
    # Create plot
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(sample_data["Year"], sample_data["Revenue"], marker='o', label="Revenue")
    ax.plot(sample_data["Year"], sample_data["Net Income"], marker='s', label="Net Income")
    ax.set_xlabel("Year")
    ax.set_ylabel("Amount ($M)")
    ax.set_title("Financial Trends (Sample Data)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        AI Financial Analyzer | Built with LangChain, FastAPI, and Streamlit
    </div>
    """,
    unsafe_allow_html=True
)