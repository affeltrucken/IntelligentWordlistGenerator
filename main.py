#!/usr/bin/env python3

__author__ = "Aldin Smajlovic"
__version__ = "1.0"

import json
from colorama import Fore
from time import time
from os import system, name, path
from datetime import datetime


YELLOW = Fore.LIGHTYELLOW_EX
CYAN = Fore.LIGHTCYAN_EX
WHITE = Fore.LIGHTWHITE_EX
RED = Fore.RED
LIGHT_RED = Fore.LIGHTRED_EX
GREEN = Fore.LIGHTGREEN_EX
MAGNETA = Fore.LIGHTMAGENTA_EX
LOGO = f"""{CYAN}
    _____       _       _ _ _                  _
    \_   \_ __ | |_ ___| | (_) __ _  ___ _ __ | |_
     / /\/ '_ \| __/ _ \ | | |/ _` |/ _ \ '_ \| __|
  /\/ /_ | | | | ||  __/ | | | (_| |  __/ | | | |_
  \____/ |_| |_|\__\___|_|_|_|\__, |\___|_| |_|\__|{WHITE}
  / / /\ \ \___  _ __ __| | (_)___/ |_
  \ \/  \/ / _ \| '__/ _` | | / __| __|
   \  /\  / (_) | | | (_| | | \__ \ |_
    \/{GREEN}__{WHITE}\/ \___/|_|  \__,_|_|_|___/\__|
  {GREEN}  / _ \___ _ __   ___ _ __ __ _| |_ ___  _ __
   / /_\/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
  / /_\\\\  __/ | | |  __/ | | (_| | || (_) | |
  \____/\___|_| |_|\___|_|  \__,_|\__\___/|_| {LIGHT_RED}v1.3
\n\n  {WHITE}Author: {YELLOW}{__author__}{CYAN}\n  {WHITE}Github: {YELLOW}https://github.com/affeltrucken"""

all_keywords_list = []
written_passwords = []
use_leet = True
use_special = True
use_numbers = True
use_swedish = True
use_requirements = False
number_required = False
special_required = False
require_min_pass = 0
require_max_pass = 64

keywords = {
    "name": "",
    "lastname": "",
    "nickname": "",
    "initials": "",
    "birth": "",
    "city": "",
    "country": "",
    "pet_name": "",
    "partner_name": "",
    "partner_lastname": "",
    "partner_nickname": "",
    "partner_birth": "",
    "other_keywords": []
}

r_leet = {
    "o": "0",
    "i": "1",
    "e": "3",
    "a": "4",
    "s": "5"
    }

r_special = {
    "a": "@",
    "i": "!",
    "s": "$",
    # "l": "/",
}


r_swedish = {
    "å": "a",
    "ä": "a",
    "ö": "o"
}

hints = [
f"{CYAN}- Street names\n    {WHITE}Street names/numbers are more common than you might think.\n",
f"{CYAN}- Relatives\n    {WHITE}Some people use close relatives in their password.\n",
f"{CYAN}- months \n    {WHITE}A lot of people use words related to a time of year, \n    like a season.\n",
f"{CYAN}- Games and shows \n    {WHITE}People like to use their favorite games, TV-shows, or \n    characters when creating passwords.\n",
f"{CYAN}- Animals \n    {WHITE}Try to use an animal as a keyword.\n",
f"{CYAN}- Sports teams \n    {WHITE}Football or basketball teams and sports are commonly used.\n",
f"{CYAN}- The platform \n    {WHITE}Keywords related to the platform that the user created \n    an account on might be used.\n",
f"{CYAN}- Artits and bands \n    {WHITE}Try the persons favorite bands/artists.\n",
f"{CYAN}- Company \n    {WHITE}The company the given person works at or something related\n    might be in the password.\n"
]

keyword_text = [
    "Firstname",
    "Lastname",
    "Nickname",
    "Initials",
    "Birthdate (YYYY-MM-DD)",
    "City", "Country",
    "Pet name",
    "Partner firstname",
    "Partner lastname",
    "Partner nickname",
    "Partner birthdate",
    "Other keywords (separated by space)"
]

password_requirements = {
    "use_requirements": use_requirements,
    "require_min_pass": require_min_pass,
    "require_max_pass": require_max_pass,
    "number_required": number_required,
    "special_required": special_required,
    "use_leet": use_leet,
    "use_special": use_special,
    "use_numbers": use_numbers,
    "use_swedish": use_swedish,
}

months = {
    "january": "winter",
    "february": "autumn",
    "mars": "autumn",
    "april": "autumn",
    "may": "summer",
    "june": "summer",
    "july": "summer",
    "august": "spring",
    "september": "spring",
    "october": "spring",
    "november": "winter",
    "december": "winter"
}

common_numbers = [
    "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "10",
    "11", "12", "13","14", "15",
    "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25",
    "69", "99", "111", "222", "333",
    "444", "555", "666", "777", "888",
    "123", "234", "345", "456", "678",
    "007", "123", "314", "321", "369",
    "420", "345", "567", "789", "666",
    "999", "0000", "1010", "1111", "2222",
    "3333", "1212", "1234", "1337", "4321",
    "4444", "5555", "6969", "6666", "7777",
    "8080", "8888", "9999", "12345", "123456",
    "1234567", "12345678", "2000", "2003", "2004",
    "2005", "2006", "2016", "2017", "2018",
    "2019", "2020", "2021", "2022", "2023",
    "1234567890"
]


def clearConsole():
    system("cls" if name == "nt" else "clear")


def yesNoPrompt(prompt, standard):
    while True:
        answer = str(input(prompt + ": ")).lower().strip()
        if not answer:
            answer = standard
        if answer.lower().strip().startswith("y"):
            return True
        if answer.lower().strip().startswith("n"):
            return False


def formatDate(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d")


def inputKeywords():
    print(f"{LIGHT_RED} Press enter to skip a variable.\n{WHITE}")
    print(f"{YELLOW} Keywords\n {WHITE}Please enter the keywords you want to use.\n")

    for key, text in zip(keywords.keys(), keyword_text):
        valid_input = False

        while not valid_input:
            keywords[key] = input(f" {WHITE}{text}: {WHITE}")

            if key != ("birth" or "partner_birth") or keywords[key] == "":
                if key != "other_keywords":
                    valid_input = True

                temp_list = keywords[key].split()
                keywords["other_keywords"] = []

                for extra_key in temp_list:
                    if extra_key in keywords["other_keywords"]:
                        continue
                    keywords["other_keywords"].append(extra_key)

                break

            try:
                keywords[key] = formatDate(keywords[key])
                current = keywords[key]

                i = 1
                for month, season in months.items():
                    if i != int(current.month):
                        i += 1
                        continue
                    if month not in all_keywords_list:
                        all_keywords_list.append(month)
                    if season not in all_keywords_list:
                        all_keywords_list.append(season)
                    i += 1

                break
            except ValueError:
                print(f" {RED}Not a valid date. Use YYYY-MM-DD format or press Enter to skip.{WHITE}\n")


def inputPasswordChoiches():
    print(f"\n\n {YELLOW}Yes/no options")
    print(f"{WHITE} Enter what types of variations of the passwords you want to add.\n")

    global use_leet
    use_leet = yesNoPrompt(f" {WHITE}Add leet variation (changes \"e\" to \"3\", for example) (y/N) ", "n")

    global use_special
    use_special = yesNoPrompt(f" {WHITE}Add special-character variation (changes \"i\" to \"!\", for example) (y/N) ", "n")

    global use_numbers
    use_numbers = yesNoPrompt(f" {WHITE}Append common numbers (123, 69, 420 etc...) (Y/n) ", "y")

    global use_swedish
    use_swedish = yesNoPrompt(f" {WHITE}Allow Swedish chars (Y/n) ", "y")


def inputPasswordRequirements():
    print(f"\n\n {YELLOW}Password requirements\n")

    global require_min_pass
    global require_max_pass

    global special_required
    global number_required

    global use_requirements
    use_requirements = yesNoPrompt(f"\n {WHITE}Set password rules? (recommended) (Y/n) ", "y")

    if use_requirements:
        while True:
            try:
                require_min_pass = int(input(f" Minimum password length: {WHITE}"))
                require_max_pass = int(input(f" Maximum password length: {WHITE}"))

                number_required = yesNoPrompt(" Numbers required? (y/N) ", "n")
                special_required = yesNoPrompt(" Special characters required? (y/N) ", "n")

                break
            except ValueError:
                print(" Not a valid number.")


def confirmOptions():
    print(f"\n\n {YELLOW}Confirmation \n")
    while True:
        options_confirmed = yesNoPrompt(f"{WHITE}\n Confirm all options? (Y/n)", "y")
        if options_confirmed:
            break
        else:
            editConfig()


def replaceChars(word, replacements):
    for char, replacement in replacements.items():
        for c in [char, char.upper()]:
            word = word.replace(char, replacement)
    return word


def checkDates():
    global valid_birth
    global valid_partner_birth
    valid_partner_birth = False
    valid_birth = False
    if isinstance(keywords["birth"], datetime):
        global birth_year
        global birth_month
        global birth_day
        birth_year = str(keywords["birth"].year)
        birth_month = str(keywords["birth"].month)
        birth_day = str(keywords["birth"].day)
        valid_birth = True
    if isinstance(keywords["partner_birth"], datetime):
        global partner_year
        global partner_month
        global partner_day
        partner_year = str(keywords["partner_birth"].year)
        partner_month = str(keywords["partner_birth"].month)
        partner_day = str(keywords["partner_birth"].day)
        valid_partner_birth = True


def addKeywordsToList():
    for key, value in keywords.items():
        if not value or key in ["birth", "partner_birth"]:
            continue
        if isinstance(value, list):
            for keyword in value:
                if keyword in all_keywords_list:
                    continue
                all_keywords_list.append(keyword)
        else:
            all_keywords_list.append(value)
    print(f"\n{WHITE} Using keys: ", end="")
    for key in all_keywords_list:
        print(f"{YELLOW}{key}{',' if key != all_keywords_list[-1] else ''} ", end="")
    print("\n")


def createFile():
    global wordlist_file
    global wordlist_name

    name = keywords["name"]
    time = datetime.now().strftime("%H-%M-%S")

    wordlist_name = f"wordlist_{time}.txt"
    if keywords["name"]:
        wordlist_name = f"{name}_{time}.txt"
    wordlist_file = open(wordlist_name, "a")


def writeToList(key):
    for password in [
                f"{key}", f"{key}!",
                f"{'!' if key[0] != '!' else ''}{key}!",
                f"{key}?", f"?{key}?", f"{key}.",
                f".{key}.", f"*{key}*", f"{key}*"]:
        if password not in written_passwords:
            if use_requirements:
                if number_required:
                    if not any(char.isdigit() for char in password):
                        return
                if special_required:
                    if all((char.isdigit() or char.isalpha) for char in password):
                        return
                if require_max_pass >= len(password) >= require_min_pass:
                    wordlist_file.write(password + "\n")
                    written_passwords.append(password)
            else:
                wordlist_file.write(password + "\n")
                written_passwords.append(password)


def reverseString(string):
    return string[::-1]

def returnString(string):
    return string

def lastTwoChars(string):
    return string[-2:]


def startWrite():
    for key in all_keywords_list:
        for w in [key, key.capitalize(), key.upper(), key.lower(), key * 2 if len(key) <= 5 else key]:
            if not use_swedish:
                w = replaceChars(w, r_swedish)
            write1(w)
            if use_special:
                write1(replaceChars(w, r_special))
            if use_leet:
                w = replaceChars(w, r_leet)
                write1(w)


def write1(key):
    writeToList(key)
    if valid_partner_birth:
        write2(key, partner_year)
    if valid_birth:
        write2(key, birth_year)
    if not use_numbers:
        return
    for num in common_numbers:
        for w in [key, key * 2 if len(key) < 5 else key]:
            writeToList(w + num)
        for w in [num, num * 2 if len(num) < 4 else num]:
            writeToList(w + key)


def write2(key, date):
    for w in [key, reverseString(key)]:
        for f in [returnString, reverseString]:
            if use_swedish:
                w = replaceChars(key, r_swedish)
            writeToList(w + f(date))
            writeToList(w + lastTwoChars(f(date)))
            writeToList(w + lastTwoChars(f(date)) * 2)


def createWordlist():
    print(f"""\n
 {CYAN}----------------------------
 {WHITE}Interactive wordlist creator
 {CYAN}----------------------------
""")
    inputKeywords()
    inputPasswordChoiches()
    inputPasswordRequirements()
    confirmOptions()
    start_time = time()
    checkDates()
    createFile()
    addKeywordsToList()
    print(f"\n {YELLOW}Writing to {wordlist_name}... this may take a while.")
    startWrite()
    print(f"""\n{GREEN} {len(written_passwords)} lines written to {wordlist_name} in {
    round(time() - start_time, 5)
    } seconds\n\n{WHITE}""")
    wordlist_file.close()


def saveConfig():
    temp_keys = keywords
    for k in ["birth", "partner_birth"]:
        temp_keys[k] = str(temp_keys[k]).strip("00:00:00").strip()
    if path.exists(".\\password_keys.json"):
        accept_warning = yesNoPrompt(f"""\n\n{LIGHT_RED} Warning. This will overwrite the current config file(s).
 Continue? (y/N) """, "n")
        if accept_warning:
            config_json = json.dumps(temp_keys, indent = 4)
            with open ("password_keys.json", "w") as config:
                config.write(config_json)
            rules_json = json.dumps(password_requirements, indent = 4)
            with open ("password_requirements.json", "w") as rules:
                rules.write(rules_json)
            print(f"{GREEN}\n  Config saved successfully")


def loadConfig():
    global keywords
    if path.exists(".\\password_requirements.json"):
        with open("password_requirements.json", "r", encoding="utf-8") as rules:
            global password_requirements
            password_requirements = json.load(rules)
            print(f"{GREEN}\n  Password requirements loaded from password_requirements.json.{WHITE}")
    else:
        print(f"{RED}\n  password_requirements.json not found.{WHITE}")
    if path.exists(".\\password_keys.json"):
        with open("password_keys.json", "r", encoding="utf-8") as config:
            keywords = json.load(config)
            if keywords["birth"]:
                keywords["birth"] = formatDate(keywords["birth"])
            if keywords["partner_birth"]:
                keywords["partner_birth"] = formatDate(keywords["partner_birth"])
            print(f"{GREEN}\n  Password keys loaded from password_keys.json.{WHITE}")
        return
    print(f"{RED}\n  password_keys.json not found.{WHITE}")


def editConfig():
    option = 0
    while option != "c":
        clearConsole()
        printConfig()
        print(f"\n{YELLOW} Enter 'c' to confirm options.")
        option = input(f"{WHITE}\n\n Option: ")
        if option in keywords.keys():
            keywords[option] = input(f"{WHITE}\n Value: ")
            if option in ["partner_birth", "birth"]:
                keywords[option] = formatDate(keywords[option])
            if option == "other_keywords":
                temp_list = []
                for k in keywords["other_keywords"].split():
                    if k in temp_list:
                        continue
                    temp_list.append(k)
                keywords["other_keywords"] = temp_list
        if option in password_requirements.keys():
            if isinstance(password_requirements[option], bool):
                password_requirements[option] = yesNoPrompt(" Value (y/n)", "n")
            else:
                password_requirements[option] = input(" Value: ")
    clearConsole()


def printConfig():
    print(f"""
  {CYAN}----------------------
  {WHITE}Keys
  {CYAN}----------------------
    """)
    for key, value in keywords.items():
        if key != "other_keywords":
            print(f"{WHITE}    {key}: {YELLOW}{value}")
        else:
            print(f"    {WHITE}{key}: ", end="")
            for k in keywords["other_keywords"]:
                print(f"{YELLOW}{k}{(',' if k != keywords[key][-1] else '')} ", end="")

    print(f"""
  {CYAN}----------------------
  {WHITE}Password rules
  {CYAN}----------------------
    """)
    for key, value in password_requirements.items():
        if isinstance(value, bool):
            print(f"{WHITE}    {key}: {GREEN if value else RED}{value}")
        else:
            print(f"{WHITE}    {key}: {YELLOW}{value}")
    print("\n")


def writeWordlistFromConfig():
    checkDates()
    start_time = time()
    createFile()
    addKeywordsToList()
    startWrite()
    print(f"""\n{GREEN} {len(written_passwords)} lines written to {wordlist_name} in {
    round(time() - start_time, 5)
    } seconds\n\n{WHITE}""")


def printHints():
    print()
    i = 1
    for hint in hints:
        print(f"  {WHITE}{hint}")
        i += 1


def checkMenuOption(option):
    match option:
        case "1":
            createWordlist()
        case "2":
            writeWordlistFromConfig()
        case "3":
            printHints()
        case "4":
            printConfig()
        case "5":
            saveConfig()
        case "6":
            loadConfig()
        case "7":
            editConfig()
        case "99":
            exit()
        case _:
            print(f"\n  {RED}Invalid option")


def main():
    clearConsole()
    print(LOGO)
    while True:
        print(f"""\n  {CYAN}----------------------{WHITE}
    1) Create wordlist interactively
    2) Create wordlist from config

    3) Show wordlist tips
    4) Show current config

    5) Save config
    6) Load config
    7) Edit config

    99) Exit\n  {CYAN}----------------------{WHITE}\n""")

        option = str(input(f"{WHITE}IWG > "))
        clearConsole()
        checkMenuOption(option)


if __name__ == "__main__":
    main()

# TODO: Import info from facebook/LinkedIn/etc.
