# Intelligent Wordlist Generator (IWG)

> **A high-performance, targeted password profiling tool designed for authorized security testing.**

**Author:** Aldin Smajlovic  
**Version:** 2.2

## ⚡ Overview

IWG is a context-specific wordlist generator. Unlike brute-force tools that generate random character combinations, IWG profiles a specific human target using OSINT data (names, dates, partners, pets) to generate highly probable password variations.

**Why use this over CUPP?**
* **Performance:** Refactored to use `O(1)` Set lookups and Python Generators. It generates and writes **200,000+ unique passwords in <0.2 seconds**.
* **Localization:** Built-in logic for Swedish character handling (`å`, `ä`, `ö`) and date formats, alongside standard English patterns.
* **Modern Logging:** Features ProjectDiscovery-style CLI output (Info/Warn/Success) for better readability.
* **OSINT Integration:** Includes a module to fetch profile data directly from LinkedIn.

## 🚀 Features

* **Smart Permutations:** Automatically handles Leet speak (`e` -> `3`), special character injection, and case toggling.
* **Pattern Matching:** Appends common patterns (years, birthdates, partner names) based on real-world breach data.
* **Filtering:** Built-in complexity filters (Min/Max length, require numbers/specials) to keep wordlists optimized.
* **State Management:** Save and load target profiles via JSON configurations.
* **LinkedIn Scraper:** Pulls target details (Location, Name, etc.) via the LinkedIn API to auto-populate the profile.

## 📦 Installation

**Requirements:** Python 3.9+

```bash
git clone https://github.com/affeltrucken/IntelligentWordlistGenerator
cd IntelligentWordlistGenerator
pip install -r requirements.txt
```

## 🛠️ Usage

Run the main script to enter the interactive menu:

```bash
python main.py
```

### Interactive Workflow
1.  **Input Target Data:** Enter known details (Name, Nickname, Birthdate, etc.). Press `Enter` to skip unknown fields.
2.  **Configure Rules:** Toggle Leet speak, number appending, or specific Swedish character handling.
3.  **Generate:** The tool will compile a base list and generate variations instantly.

### Example Output

```text
[?] IWG > : 1
[INF] Starting interactive setup mode.
[INF] Press Enter to skip any field.
[?] Firstname: Aldin
[?] Lastname: Smajlovic
[?] Birthdate (YYYY-MM-DD): 2005-09-02
[+] Parsed date: 2005-09-02
[INF] Configuring generation rules...
[?] Enable Leet Speak (e->3)? (y/n) [n]: y
[?] Append Numbers? (y/n) [y]: y
[INF] Loaded 11 base keywords.
[INF] Generating wordlist to file: aldin_135929.txt
[INF] Generated 230000 passwords...
[+] Completed! 230972 passwords saved in 0.16s
```

## ⚙️ Configuration

You can save your current profile configuration to JSON for later use.

* `password_keys.json`: Stores the target's personal data.
* `password_requirements.json`: Stores your generation rules (e.g., "Always use Leet speak", "Max length 12").

## 📋 Todo

- [x] Refactor for O(1) performance (Sets vs Lists)
- [x] Implement ProjectDiscovery-style logging
- [x] Add Swedish character logic
- [x] Integrate LinkedIn API
- [ ] Add STDOUT piping support (for chaining with Hashcat/Hydra)
- [ ] Add "Mentalist" style chain rules

## ⚠️ Legal Disclaimer

**FOR EDUCATIONAL AND AUTHORIZED TESTING PURPOSES ONLY.**

This tool is designed to help security professionals and students understand how poor password habits can be exploited. The author (Aldin Smajlovic) is not responsible for any illegal use of this program. **Do not use this tool against targets for which you do not have explicit, written consent.**
