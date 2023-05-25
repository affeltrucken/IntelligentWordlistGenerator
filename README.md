# IntelligentWordlistGenerator
Written by: Aldin Smajlovic

## Description

A *personalized* wordlist generator written in Python that creates wordlists based on the common patterns of humans when creating passwords, based around the keywords of the target. 
&nbsp;

# Guide

## Requirements

- Python 3.10 or above
- colorama
- linkedin-api

## Installation
```
git clone https://github.com/affeltrucken/IntelligentWordlistGenerator
cd IntelligentWordlistGenerator
pip install -r requirements.txt
python main.py
```

## Usage

`python main.py`

From here, you can use the menu

![menu](https://github.com/affeltrucken/IntelligentWordlistGenerator/raw/main/menu.png)

### Options

1. Create a wordlist by entering a set of keywords, such as name, city, country, and birthdate. You can also specify if you want to add leet variations, or special character variations of the password.
2. Create a wordlist from config, which is by default empty
3. Show some tips of keywords you can use when creating your wordlist
4. Print the current configuration of keywords used and password rules set
5. Save the current config to a password_requirements.json and password_keys.json
6. Load a configuration from password_requirements.json, password_keys.json, or both.
7. Create a set of configuration based on a LinkedIn profile, using linkedin-api
8. Edit the current configuration interactively

---
## Known bugs
- As of right now, saving and loading configs seems to be unreliable or it doesn't work at all.
- Colors in the terminal is do not if executed on Windows. To fix this, go to HKEY_CURRENT_USER\Console and add a key called VirtualTerminalLevel with the DWORD value of 1.

## Todo

- [x] Add ability to set password rules
- [x] Use LinkedIn API to get info
- [ ] Use Facebook API to get info
- [ ] Make some functions cleaner

## Legal

DISCLAIMER: This is only for testing and educational purposes and can only be used where strict consent has been given. Do not use this for illegal purposes.
