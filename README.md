# Smart-Wordlist-Generator

                                          #Smart Wordlist Generator

A Python-based, intelligent wordlist generator designed for **authorized security testing, penetration testing, and fuzzing**. 

Instead of using generic, massive wordlists, this tool scrapes a target organization's public-facing website, extracts meaningful terminology, and applies smart mutations to generate highly targeted, high-probability wordlists.

##  Ethical Disclaimer
> **FOR EDUCATIONAL AND AUTHORIZED USE ONLY.**  
> This tool is intended for security professionals and researchers conducting authorized penetration tests or security assessments. Do not use this tool against any website or system without explicit, written permission from the owner. Unauthorized access or testing is illegal.

##  Features
- **Intelligent Scraping**: Uses `BeautifulSoup` to extract visible text while ignoring scripts, styles, and navigation boilerplate.
- **Noise Filtering**: Automatically removes common English stop words and short, meaningless strings.
- **Smart Mutations**: Generates password-style variations (e.g., capitalization, appending recent years like 2024-2026, adding common special characters, and basic leet-speak).
- **CLI Interface**: Easy to use with `argparse`, making it scriptable and automation-friendly.
- **Clean Output**: Sorts the final wordlist by length and alphabetically for optimal use with tools like `Hydra`, `Hashcat`, or `Burp Suite`.

##  Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/smart-wordlist-gen.git
   cd smart-wordlist-gen
2.Create a virtual environment (recommended):
  ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3.Install dependencies:


