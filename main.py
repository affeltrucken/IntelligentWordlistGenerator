#!/usr/bin/env python3

__author__ = "Aldin Smajlovic"
__version__ = "2.2-fixed-logic"

import json
import os
import time
import sys
from datetime import datetime
from typing import Dict, List, Set, Any, Generator
from getpass import getpass
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# --- Configuration & Constants ---
C_INF = Fore.BLUE           # Info
C_WRN = Fore.YELLOW         # Warning
C_ERR = Fore.RED            # Error
C_SUC = Fore.GREEN          # Success
C_TXT = Fore.LIGHTWHITE_EX  # Text
C_RST = Style.RESET_ALL

LOGO = f"""{Fore.CYAN}
    _____       _       _                      _
    \_   \_ __ | |_ ___| | (_) __ _  ___ _ __ | |_
     / /\/ '_ \| __/ _ \ | | |/ _` |/ _ \ '_ \| __|
  /\/ /_ | | | | ||  __/ | | | (_| |  __/ | | | |_
  \____/ |_| |_|\__\___|_|_|_|\__, |\___|_| |_|\__|{Fore.WHITE}
  / / /\ \ \___  _ __ __| | (_)___/ |_
  \ \/  \/ / _ \| '__/ _` | | / __| __|
   \  /\  / (_) | | | (_| | | \__ \ |_
    \/{Fore.GREEN}__{Fore.WHITE}\/ \___/|_|  \__,_|_|_|___/\__|
  {Fore.GREEN}  / _ \___ _ __    ___ _ __ __ _| |_ ___  _ __
   / /_\/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
  / /_\\\\  __/ | | |  __/ | | (_| | || (_) | |
  \____/\___|_| |_|\___|_|  \__,_|\__\___/|_| {Fore.LIGHTRED_EX}v{__version__}
\n  {Fore.WHITE}Author: {Fore.YELLOW}{__author__}
"""

LEET_MAP = {"o": "0", "i": "1", "e": "3", "a": "4", "s": "5"}
SPECIAL_MAP = {"a": "@", "i": "!", "s": "$"}
SWEDISH_MAP = {"å": "a", "ä": "a", "ö": "o"}

# RESTORED: The full number list
COMMON_NUMBERS = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25", "69", "99", "111", "222", "333",
    "444", "555", "666", "777", "888", "123", "234", "345", "456", "678",
    "007", "314", "321", "369", "420", "567", "789", "999", "0000",
    "1010", "1111", "2222", "3333", "1212", "1234", "1337", "4321",
    "4444", "5555", "6969", "6666", "7777", "8080", "8888", "9999",
    "12345", "123456", "1234567", "12345678", "2000", "2003", "2004",
    "2005", "2006", "2016", "2017", "2018", "2019", "2020", "2021",
    "2022", "2023", "2024", "1234567890"
]

class Log:
    @staticmethod
    def info(msg: str): sys.stderr.write(f"{C_INF}[INF]{C_RST} {msg}\n")
    @staticmethod
    def warning(msg: str): sys.stderr.write(f"{C_WRN}[WRN]{C_RST} {msg}\n")
    @staticmethod
    def error(msg: str): sys.stderr.write(f"{C_ERR}[ERR]{C_RST} {msg}\n")
    @staticmethod
    def success(msg: str): sys.stderr.write(f"{C_SUC}[+]{C_RST} {msg}\n")
    @staticmethod
    def debug(msg: str): sys.stderr.write(f"{Fore.LIGHTBLACK_EX}[DBG]{C_RST} {msg}\n")
    @staticmethod
    def input(prompt: str, default: str = "") -> str:
        d_str = f" [{default}]" if default else ""
        sys.stderr.write(f"{C_INF}[?]{C_RST} {prompt}{d_str}: ")
        try:
            val = input()
            return val.strip() if val.strip() else default
        except KeyboardInterrupt:
            sys.stderr.write("\n")
            Log.error("User aborted.")
            sys.exit(0)

class WordlistGenerator:
    def __init__(self):
        self.keywords: Dict[str, Any] = {
            "firstname": "", "lastname": "", "nickname": "", "initials": "",
            "birthdate": "", "partner_birthdate": "", "city": "", "country": "", 
            "partner_name": "", "other_keywords": []
        }
        self.config: Dict[str, Any] = {
            "use_leet": True, "use_special": True, "use_numbers": True,
            "use_swedish": True, "use_requirements": True,
            "require_min_pass": 0, "require_max_pass": 64,
            "number_required": False, "special_required": False
        }
        self.base_keywords_list: List[str] = []

    def clear_console(self):
        print("\033[H\033[J", end="")

    def _replace_chars(self, word: str, replacements: Dict[str, str]) -> str:
        for char, replacement in replacements.items():
            word = word.replace(char, replacement).replace(char.upper(), replacement)
        return word

    def input_keywords(self):
        Log.info("Starting interactive setup mode.")
        Log.info("Press Enter to skip any field.")
        
        labels = [
            ("firstname", "Firstname"), ("lastname", "Lastname"), 
            ("nickname", "Nickname"), ("birthdate", "Birthdate (YYYY-MM-DD)"),
            ("city", "City"), ("partner_name", "Partner Name"),
            ("partner_birthdate", "Partner Birthdate (YYYY-MM-DD)"),
            ("other_keywords", "Other Keywords (space separated)")
        ]

        for key, text in labels:
            val = Log.input(text)
            
            if key == "other_keywords" and val:
                self.keywords["other_keywords"] = val.split()
            elif key in ["birthdate", "partner_birthdate"] and val:
                try:
                    self.keywords[key] = datetime.strptime(val, "%Y-%m-%d")
                    Log.success(f"Parsed date: {self.keywords[key].date()}")
                except ValueError:
                    Log.error("Invalid date format. Skipping.")
            elif val:
                self.keywords[key] = val

    def input_config(self):
        Log.info("Configuring generation rules...")
        c = self.config
        c["use_leet"] = Log.input("Enable Leet Speak (e->3)? (y/n)", "n").lower().startswith('y')
        c["use_numbers"] = Log.input("Append Numbers? (y/n)", "y").lower().startswith('y')
        c["use_swedish"] = Log.input("Keep Swedish Chars? (y/n)", "y").lower().startswith('y')
        
        if Log.input("Set complexity requirements? (y/n)", "y").lower().startswith('y'):
            c["use_requirements"] = True
            try:
                c["require_min_pass"] = int(Log.input("Min Length", "0"))
                c["require_max_pass"] = int(Log.input("Max Length", "64"))
                c["number_required"] = Log.input("Require Numbers? (y/n)", "n").lower().startswith('y')
                c["special_required"] = Log.input("Require Special Chars? (y/n)", "n").lower().startswith('y')
            except ValueError:
                Log.warning("Invalid number. Using defaults.")
        else:
            c["use_requirements"] = False

    def compile_base_list(self):
        self.base_keywords_list = []
        k = self.keywords
        
        # Add basic strings
        for key, val in k.items():
            if isinstance(val, str) and val:
                self.base_keywords_list.append(val)
            elif isinstance(val, list):
                self.base_keywords_list.extend(val)

        # Add combinations
        if k['firstname'] and k['lastname']:
            self.base_keywords_list.append(f"{k['firstname']}{k['lastname']}")
            self.base_keywords_list.append(f"{k['lastname']}{k['firstname']}")
            self.base_keywords_list.append(f"{k['firstname']}.{k['lastname']}")
        
        if k['partner_name'] and k['firstname']:
             self.base_keywords_list.append(f"{k['firstname']}{k['partner_name']}")
             self.base_keywords_list.append(f"{k['partner_name']}{k['firstname']}")

        Log.info(f"Loaded {len(self.base_keywords_list)} base keywords.")

    def _apply_suffixes(self, word: str) -> Generator[str, None, None]:
        """RESTORED: Applies !, ?, ., * logic from original writeToList"""
        # Original: [key, key!, !key!, key?, ?key?, key., .key., *key*, key*]
        
        # 1. The word itself
        yield word
        
        # 2. Basic suffixes
        for s in ["!", "?", ".", "*"]:
            yield f"{word}{s}"
            
        # 3. Wrapping (e.g., *word*, ?word?)
        for s in ["!", "?", ".", "*"]:
            yield f"{s}{word}{s}"
            
        # 4. Double suffixes (common in passwords)
        yield f"{word}123" if "123" not in word else word # Safety check
        yield f"{word}!"
        yield f"{word}!!"

    def _generate_variations(self, word: str) -> Generator[str, None, None]:
        """Generates Case, Leet, and Special variations"""
        forms = [word, word.lower(), word.upper(), word.capitalize()]
        
        # Original logic: Double up short words
        if len(word) < 5:
            forms.append(word * 2)

        for w in forms:
            # Swedish handling
            if not self.config["use_swedish"]:
                w = self._replace_chars(w, SWEDISH_MAP)
            yield w
            
            if self.config["use_leet"]: 
                yield self._replace_chars(w, LEET_MAP)
            
            if self.config["use_special"]:
                yield self._replace_chars(w, SPECIAL_MAP)

    def generate_all_passwords(self) -> Generator[str, None, None]:
        """
        The Master Pipeline:
        Base -> Variations -> (Append Date/Num) -> Suffixes -> Final
        """
        for key in self.base_keywords_list:
            
            # Step 1: Get all casing/leet variations of the keyword
            variations = list(self._generate_variations(key))
            
            for variant in variations:
                
                # List of candidates to apply suffixes to
                candidates = [variant]
                
                # Step 2: Append Numbers (RESTORED FULL LOGIC)
                if self.config["use_numbers"]:
                    for num in COMMON_NUMBERS:
                        candidates.append(f"{variant}{num}")
                        candidates.append(f"{variant}_{num}")
                        # Logic for num + variant
                        candidates.append(f"{num}{variant}")
                        if len(variant) < 5:
                            candidates.append(f"{variant*2}{num}")

                # Step 3: Append Dates (RESTORED)
                for date_key in ["birthdate", "partner_birthdate"]:
                    if isinstance(self.keywords[date_key], datetime):
                        year = str(self.keywords[date_key].year)
                        short_year = year[-2:]
                        
                        candidates.append(f"{variant}{year}")
                        candidates.append(f"{variant}{short_year}")
                        candidates.append(f"{variant}_{year}")
                
                # Step 4: Apply Suffixes to ALL candidates and Yield
                # This ensures "Aldin123" also gets "Aldin123!"
                for candidate in candidates:
                    for final_pass in self._apply_suffixes(candidate):
                        yield final_pass

    def save_wordlist(self):
        name = self.keywords.get("firstname") or "wordlist"
        filename = f"{name}_{datetime.now().strftime('%H%M%S')}.txt"
        
        Log.info(f"Generating wordlist to file: {filename}")
        
        start_time = time.time()
        unique_hashes = set()
        count = 0
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for password in self.generate_all_passwords():
                    
                    # Requirements Check
                    if self.config["use_requirements"]:
                        if len(password) < self.config["require_min_pass"]: continue
                        if len(password) > self.config["require_max_pass"]: continue
                        if self.config["number_required"] and not any(c.isdigit() for c in password): continue
                        if self.config["special_required"] and password.isalnum(): continue
                    
                    if password not in unique_hashes:
                        unique_hashes.add(password)
                        f.write(password + "\n")
                        count += 1
                        
                        if count % 5000 == 0:
                            sys.stderr.write(f"\r{C_INF}[INF]{C_RST} Generated {count} passwords...")
                            
            sys.stderr.write("\n")
            duration = round(time.time() - start_time, 2)
            Log.success(f"Completed! {count} passwords saved in {duration}s")
            
        except IOError as e:
            Log.error(f"File write error: {e}")

    def run(self):
        self.clear_console()
        print(LOGO)
        
        while True:
            print(f"\n{C_TXT}Select Option:{C_RST}")
            print(f"1. Interactive Mode")
            print(f"2. Exit")
            
            opt = Log.input("IWG > ")
            
            if opt == "1":
                self.input_keywords()
                self.input_config()
                self.compile_base_list()
                self.save_wordlist()
            elif opt == "2":
                Log.info("Exiting...")
                sys.exit()
            else:
                Log.error("Invalid option")

if __name__ == "__main__":
    app = WordlistGenerator()
    app.run()
