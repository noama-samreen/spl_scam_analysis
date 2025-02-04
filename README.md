# RugCheck Token Analyzer

A Streamlit application that interfaces with the RugCheck API to analyze Solana tokens for potential security risks and detailed information.

## Features

- Single token analysis
- Bulk token analysis via file upload
- Detailed token information including:
  - Security score
  - Risk assessment
  - Market information
  - Token metadata
  - Verification status
  - Top holders
  - And more...

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/rugcheck-analyzer.git
cd rugcheck-analyzer
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
streamlit run app.py
```

## Usage

### Single Token Analysis
1. Enter a Solana token mint address in the input field
2. Click "Check Token"
3. View the results and download them if needed

### Bulk Token Analysis
1. Prepare a text file with one token mint address per line
2. Upload the file using the file uploader
3. Click "Check Tokens"
4. View the results and download them if needed

## API Reference

This application uses the RugCheck API (https://api.rugcheck.xyz/v1). The main endpoint used is:
- `/tokens/{mint}/report/summary` - Generate a report summary for given token mint


