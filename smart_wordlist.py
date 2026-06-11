
"""
Smart Wordlist Generator
A tool for generating targeted wordlists from website content for authorized security testing.
"""

import argparse
import re
import sys
from typing import List, Set
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# Common English stop words to filter out noise
STOP_WORDS = {
    'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 
    'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 
    'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'she', 'use', 
    'her', 'way', 'many', 'will', 'with', 'this', 'that', 'from', 'they', 'have'
}

def fetch_website_content(url: str) -> str:
    """Fetches HTML content from a given URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[-] Error fetching URL: {e}")
        sys.exit(1)

def extract_and_clean_text(html_content: str) -> Set[str]:
    """Extracts text from HTML, cleans it, and returns a set of unique words."""
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Remove script and style elements
    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.decompose()
    
    # Get text and convert to lowercase
    text = soup.get_text(separator=' ', strip=True).lower()
    
    # Extract words using regex (alphanumeric only)
    words = re.findall(r'\b[a-z0-9]{3,}\b', text)
    
    # Filter out stop words and common short noise
    cleaned_words = {word for word in words if word not in STOP_WORDS and len(word) >= 3}
    return cleaned_words

def generate_smart_mutations(words: Set[str], domain_name: str) -> Set[str]:
    """Generates smart password-style mutations from base words."""
    mutations = set()
    current_year = "2026"
    recent_years = ["2024", "2025", "2026"]
    special_chars = ["!", "@", "#", "123", "2026"]
    
    # Add domain name itself as a base word
    words.add(domain_name)

    for word in words:
        # Base variations
        mutations.add(word)
        mutations.add(word.capitalize())
        mutations.add(word.upper())
        
        # Year appendages
        for year in recent_years:
            mutations.add(f"{word}{year}")
            mutations.add(f"{word.capitalize()}{year}")
            
        # Special character appendages
        for char in special_chars:
            mutations.add(f"{word}{char}")
            mutations.add(f"{word.capitalize()}{char}")
            
        # Leet speak basics (optional, keeps it smart but not bloated)
        leet_word = word.replace('a', '4').replace('e', '3').replace('i', '1').replace('o', '0')
        mutations.add(leet_word)
        mutations.add(f"{leet_word}{current_year}")

    return mutations

def save_wordlist(wordlist: Set[str], output_file: str):
    """Saves the generated wordlist to a file."""
    try:
        # Sort by length, then alphabetically for better readability
        sorted_list = sorted(list(wordlist), key=lambda x: (len(x), x))
        with open(output_file, "w", encoding="utf-8") as f:
            for word in sorted_list:
                f.write(f"{word}\n")
        print(f"[+] Successfully saved {len(sorted_list)} words to '{output_file}'")
    except IOError as e:
        print(f"[-] Error saving file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Smart Wordlist Generator for Authorized Security Testing",
        epilog="Example: python smart_wordlist.py -u https://example.com -o wordlist.txt -m"
    )
    parser.add_argument("-u", "--url", required=True, help="Target URL to scrape")
    parser.add_argument("-o", "--output", default="wordlist.txt", help="Output file name (default: wordlist.txt)")
    parser.add_argument("-m", "--mutate", action="store_true", help="Enable smart password mutations")
    
    args = parser.parse_args()

    # Validate URL
    if not args.url.startswith(("http://", "https://")):
        print("[-] Invalid URL. Must start with http:// or https://")
        sys.exit(1)

    print(f"[*] Fetching content from: {args.url}")
    html_content = fetch_website_content(args.url)
    
    print("[*] Extracting and cleaning text...")
    base_words = extract_and_clean_text(html_content)
    print(f"[*] Found {len(base_words)} unique base words.")

    final_wordlist = base_words
    if args.mutate:
        print("[*] Generating smart mutations...")
        # Extract domain name without TLD for better mutations (e.g., "example" from "example.com")
        domain = urlparse(args.url).netloc.split('.')[0]
        final_wordlist = generate_smart_mutations(base_words, domain)
        print(f"[*] Generated {len(final_wordlist)} mutated words.")

    save_wordlist(final_wordlist, args.output)
    print("[+] Done!")

if __name__ == "__main__":
    main()