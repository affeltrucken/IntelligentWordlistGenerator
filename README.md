# IntelligentWordlistGenerator
A *personalized* wordlist generator written in Python that creates wordlists based on the common patterns of humans when creating passwords. 


## Help

## Important

The wordlist generation can sometimes be *veeery* slow. It can take up to an hour (unfortunately) if you specify a lot of keywords and use all possible password variations. Feel free to contribute if you think you could make it faster.

### Requirements

- Python 3.10 or above
- colorama
- linkedin-api

### Usage

`python3 main.py`

From here, you can use the menu

![menu](https://github.com/affeltrucken/IntelligentWordlistGenerator/raw/main/menu.png)

### Options

1. Create a wordlist by entering a set of keywords, such as name, city, country, and birthdate. You can also specify if you want to add leet variations, or special character variations of the password.
2. Create a wordlist from config, which is by default empty
3. Show some tips of keywords you can use when creating your wordlist
4. Print the current configuration of keywords used and password rules set
5. Save the current config to a password_requirements.json and password_keys.json
6. Load a configuration from password_requirements.json, password_keys.json, or both.
7. Edit the current configuration interactively

---

### Todo

- [x] Add ability to set password rules
- [x] Use LinkedIn API to get info
- [ ] Use Facebook API to get info
- [ ] Clean up some functions

## Legal

I, the author, am not responsible for **ANY** damage caused by this software. Please use responsibly.
