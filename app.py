import streamlit as st
import json
import time
from rugcheck_api import RugCheckAPI

def main():
    st.set_page_config(
        page_title="SPL Token RugCheck",
        page_icon="🔍",
        layout="wide"
    )

    st.title("🔍 SPL Token RugCheck")
    st.markdown("""
    This app allows you to analyze Solana tokens using the RugCheck API.
    Enter a token mint address or upload a file with multiple addresses.
    """)

    # Initialize API
    api = RugCheckAPI()

    # Create two columns for input methods
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Single Token Check")
        token_address = st.text_input("Enter Token Mint Address")
        check_single = st.button("Check Token")

    with col2:
        st.subheader("Bulk Token Check")
        uploaded_file = st.file_uploader("Upload a text file with token addresses (one per line)", type=['txt'])
        check_bulk = st.button("Check Tokens")

    if check_single and token_address:
        with st.spinner(f"Analyzing token {token_address}..."):
            result = api.check_token(token_address)
            
            if result:
                st.json(result)
                
                # Add download button for the result
                st.download_button(
                    label="Download Result",
                    data=json.dumps(result, indent=2),
                    file_name=f"rugcheck_{token_address}.json",
                    mime="application/json"
                )
            else:
                st.error("Failed to fetch token information")

    elif check_bulk and uploaded_file is not None:
        # Read token addresses from file
        token_addresses = [line.decode().strip() for line in uploaded_file.readlines() if line.decode().strip()]
        
        # Create progress tracking elements
        progress_bar = st.progress(0)
        status_text = st.empty()

        def update_progress(current_idx, total, current_token):
            """Callback function to update Streamlit progress indicators"""
            progress_bar.progress((current_idx + 1) / total)
            status_text.text(f"Checking token {current_idx + 1}/{total}: {current_token}")

        with st.spinner("Analyzing tokens..."):
            results = api.check_tokens_bulk(token_addresses, progress_callback=update_progress)

            if results:
                st.json(results)
                
                # Add download button for all results
                st.download_button(
                    label="Download All Results",
                    data=json.dumps(results, indent=2),
                    file_name="rugcheck_results.json",
                    mime="application/json"
                )
                
                status_text.text("Analysis complete!")
            else:
                st.error("No valid results found")

if __name__ == "__main__":
    main() 