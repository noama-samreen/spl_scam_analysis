# Copyright 2025 noamasamreen

import requests
import json
import sys
from typing import List, Dict, Optional
import time

class RugCheckAPI:
    def __init__(self):
        self.base_url = "https://api.rugcheck.xyz/v1"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def check_token(self, token_mint: str) -> Optional[Dict]:
        """
        Get token check information for a specific token mint address
        """
        url = f"{self.base_url}/tokens/{token_mint}/report/summary"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error checking token {token_mint}: {str(e)}")
            return None

    def check_tokens_bulk(self, token_addresses: List[str], progress_callback=None) -> Dict[str, Dict]:
        """
        Check multiple tokens and return their results
        """
        results = {}
        total_tokens = len(token_addresses)

        for idx, token_mint in enumerate(token_addresses):
            if progress_callback:
                progress_callback(idx, total_tokens, token_mint)
            else:
                print(f"\nChecking token {idx + 1}/{total_tokens}: {token_mint}")
            
            result = self.check_token(token_mint)
            if result:
                results[token_mint] = result
            
            time.sleep(1)  # Rate limiting

        return results

def load_tokens_from_file(filename: str) -> List[str]:
    """
    Load token addresses from a text file (one address per line)
    """
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def save_results(results: dict, output_file: str):
    """
    Save results to a JSON file
    """
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

def main():
    """
    CLI entry point for the script
    """
    api = RugCheckAPI()
    results = {}

    if len(sys.argv) == 2:
        if sys.argv[1].endswith('.txt'):
            token_addresses = load_tokens_from_file(sys.argv[1])
            results = api.check_tokens_bulk(token_addresses)
        else:
            token_mint = sys.argv[1]
            print(f"\nChecking token: {token_mint}")
            result = api.check_token(token_mint)
            if result:
                results[token_mint] = result
                print(json.dumps(result, indent=2))
    else:
        print("Usage: python rugcheck_api.py <token_address or filename.txt>")
        sys.exit(1)

    if results:
        output_file = "rugcheck_results.json"
        save_results(results, output_file)
        print(f"\nFull results saved to {output_file}")

if __name__ == "__main__":
    main()

