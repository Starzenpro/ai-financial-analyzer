import re
from typing import Dict, Optional

def extract_financials(text: str) -> Dict[str, Optional[str]]:
    """
    Extract key financial metrics from text using regex patterns
    """
    patterns = {
        "revenue": [
            r"revenue[:\s]*\$?([\d,]+(?:\.\d+)?)\s*(?:million|billion)?",
            r"total\s+revenue[:\s]*\$?([\d,]+(?:\.\d+)?)",
            r"sales[:\s]*\$?([\d,]+(?:\.\d+)?)"
        ],
        "net_income": [
            r"net\s+income[:\s]*\$?([\d,]+(?:\.\d+)?)",
            r"net\s+earnings[:\s]*\$?([\d,]+(?:\.\d+)?)"
        ],
        "total_assets": [
            r"total\s+assets[:\s]*\$?([\d,]+(?:\.\d+)?)",
            r"assets[:\s]*\$?([\d,]+(?:\.\d+)?)"
        ],
        "eps": [
            r"earnings\s+per\s+share[:\s]*\$?([\d,]+(?:\.\d+)?)",
            r"EPS[:\s]*\$?([\d,]+(?:\.\d+)?)"
        ]
    }
    
    results = {}
    
    for metric, pattern_list in patterns.items():
        for pattern in pattern_list:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Clean up the number (remove commas)
                value = match.group(1).replace(',', '')
                results[metric] = value
                break
    
    return results