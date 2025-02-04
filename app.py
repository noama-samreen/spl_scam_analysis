import streamlit as st
import json
import time
from rugcheck_api import RugCheckAPI

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'batch_results' not in st.session_state:
    st.session_state.batch_results = None

# Page config
st.set_page_config(
    page_title="SPL Token RugCheck",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main {
    padding: 2rem;
}
.stButton>button {
    width: 100%;
    background-color: #7047EB;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    margin: 1rem 0;
}
.stButton>button:hover {
    background-color: #5835c4;
}
.json-output {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    font-family: monospace;
    white-space: pre-wrap;
    font-size: 0.85rem;
}
.output-container {
    margin: 2rem 0;
    padding: 1rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
}
.header-container {
    text-align: center;
    padding: 2rem 0;
}
.stProgress > div > div > div {
    background-color: #7047EB;
}
.metric-container {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("🔍 SPL Token RugCheck")
st.markdown("This app allows you to analyze Solana tokens using the RugCheck API. Enter a token mint address or upload a file with multiple addresses.")

# Initialize API
api = RugCheckAPI()

# Create tabs
tab1, tab2 = st.tabs(["Single Token", "Batch Process"])

with tab1:
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        token_address = st.text_input("Enter token address", placeholder="Enter Solana token address...")
    with col2:
        analyze_button = st.button("Analyze Token", key="single_analyze")
    with col3:
        if st.button("Reset", key="reset_single"):
            st.session_state.analysis_results = None
            token_address = ""
            st.experimental_rerun()

    if analyze_button and token_address:
        with st.spinner("Analyzing token..."):
            result = api.check_token(token_address)
            if result:
                st.session_state.analysis_results = result
            else:
                st.error("Failed to fetch token information")

    # Display results if they exist
    if st.session_state.analysis_results:
        result_dict = st.session_state.analysis_results

        # Display key metrics in columns
        if 'score' in result_dict:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Security Score", result_dict.get('score', 'N/A'))
            with col2:
                st.metric("Rugged Status", "Yes" if result_dict.get('rugged', False) else "No")

        # Display full results
        with st.expander("View Raw Data"):
            st.json(result_dict)

        # Download button
        st.download_button(
            "Download JSON",
            data=json.dumps(result_dict, indent=2),
            file_name=f"rugcheck_{token_address}.json",
            mime="application/json"
        )

with tab2:
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader(
            "Upload a text file with one token address per line",
            type="txt",
            help="File should contain one Solana token address per line"
        )
    with col2:
        if st.button("Reset", key="reset_batch"):
            st.session_state.batch_results = None
            uploaded_file = None
            st.experimental_rerun()

    if uploaded_file:
        addresses = [line.decode().strip() for line in uploaded_file if line.decode().strip()]
        st.info(f"Found {len(addresses)} addresses in file")

        if st.button("Process Batch", key="batch_process"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            def update_progress(current_idx, total, current_token):
                progress_bar.progress((current_idx + 1) / total)
                status_text.text(f"Checking token {current_idx + 1}/{total}: {current_token}")

            with st.spinner("Analyzing tokens..."):
                results = api.check_tokens_bulk(addresses, progress_callback=update_progress)
                if results:
                    st.session_state.batch_results = results
                    st.success(f"Successfully processed {len(results)} tokens")
                else:
                    st.error("No valid results found")

    # Display batch results if they exist
    if st.session_state.batch_results:
        results = st.session_state.batch_results
        
        # Display results
        with st.expander("View Raw Data"):
            st.json(results)

        # Create CSV data
        csv_data = "address,score,rugged\n"
        for address, result in results.items():
            csv_data += f"{address},{result.get('score', 'N/A')},{result.get('rugged', 'N/A')}\n"

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "Download JSON",
                data=json.dumps(results, indent=2),
                file_name="rugcheck_results.json",
                mime="application/json"
            )
        with col2:
            st.download_button(
                "Download CSV",
                data=csv_data,
                file_name="rugcheck_results.csv",
                mime="text/csv"
            )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    SPL Token RugCheck | 
    <a href='https://github.com/yourusername/rugcheck-analyzer' target='_blank'>GitHub</a>
</div>
""", unsafe_allow_html=True) 
