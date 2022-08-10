#!/usr/bin/env python3

__author__ = "Aldin Smajlovic"
__version__ = "1.4"

from json import load, dumps
from colorama import Fore
from time import time
from os import name, path
from datetime import datetime
from linkedin_api import Linkedin
from getpass import getpass
from pprint import pprint


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
  \____/\___|_| |_|\___|_|  \__,_|\__\___/|_| {LIGHT_RED}v{__version__}
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
    "firstname": "",
    "lastname": "",
    "nickname": "",
    "initials": "",
    "birthdate": "",
    "city": "",
    "country": "",
    "pet_name": "",
    "partner_name": "",
    "partner_lastname": "",
    "partner_nickname": "",
    "partner_birthdate": "",
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
f"{CYAN}- Street names\n    {WHITE}Street names/numbers are more common than you might \n    think.\n",
f"{CYAN}- Relatives\n    {WHITE}Some people use close relatives in their password.\n",
f"{CYAN}- months \n    {WHITE}A lot of people use words related to a time of year, \n    like a season.\n",
f"{CYAN}- Games and shows \n    {WHITE}People like to use their favorite games, TV-shows, or \n    characters when creating passwords.\n",
f"{CYAN}- Animals \n    {WHITE}Try to use an animal as a keyword.\n",
f"{CYAN}- Sports teams \n    {WHITE}Football or basketball teams and sports are commonly \n    used.\n",
f"{CYAN}- The platform \n    {WHITE}Keywords related to the platform that the user created \n    an account on might be used.\n",
f"{CYAN}- Artits and bands \n    {WHITE}Try the persons favorite bands/artists.\n",
f"{CYAN}- Company \n    {WHITE}The company the given person works at or something \n    related might be in the password.\n"
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
    "1234567890"]


def clearConsole():
    print("\033[H\033[J", end="")


def yesNoPrompt(prompt, standard):
    while True:
        answer = str(input(f"{prompt}:{YELLOW} ")).lower().strip()
        if not answer:
            answer = standard
        if answer.lower().strip().startswith("y"):
            return True
        if answer.lower().strip().startswith("n"):
            return False


def formatDate(date_string):
    try:
        date = datetime.strptime(date_string, "%Y-%m-%d")
        return date
    except ValueError:
        print(f" {RED}Error while formatting date.")
        return date_string


def inputKeywords():
    print(f"{LIGHT_RED} Press enter to skip a variable.\n\n{WHITE}")
    print(f"{YELLOW} Keywords\n {WHITE}Please enter the keywords you want to use.\n")

    for key, text in zip(keywords.keys(), keyword_text):
        valid_input = False

        while not valid_input:
            inp = input(f"{WHITE}{text}: {YELLOW}")

            if keywords[key] != "" and inp == "" or keywords[key] != [] and inp == "":
                break

            keywords[key] = inp

            if key != ("birthdate" or "partner_birthdate") or keywords[key] == "":
                if key != "other_keywords":
                    break

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
    use_leet = yesNoPrompt(f" {WHITE}Add leet variation (changes \"e\" to \"3\", for example) (y/N)", "n")

    global use_special
    use_special = yesNoPrompt(f" {WHITE}Add special-character variation (changes \"i\" to \"!\", for example) (y/N)", "n")

    global use_numbers
    use_numbers = yesNoPrompt(f" {WHITE}Append common numbers (123, 69, 420 etc...) (Y/n)", "y")

    global use_swedish
    use_swedish = yesNoPrompt(f" {WHITE}Allow Swedish chars (Y/n)", "y")


def inputPasswordRequirements():
    print(f"\n\n {YELLOW}Password requirements")

    global use_requirements
    use_requirements = yesNoPrompt(f"\n {WHITE}Set password rules? (recommended) (Y/n)", "y")

    if use_requirements:
        print()
        while True:
            try:
                global require_min_pass
                global require_max_pass

                global special_required
                global number_required

                require_min_pass = int(input(f" {WHITE}Minimum password length: {YELLOW}"))
                password_requirements["require_min_pass"] = require_min_pass

                require_max_pass = int(input(f" {WHITE}Maximum password length: {YELLOW}"))
                password_requirements["require_max_pass"] = require_max_pass

                number_required = yesNoPrompt(f" {WHITE}Numbers required? (y/N)", "n")
                password_requirements["number_required"] = number_required

                special_required = yesNoPrompt(f" {WHITE}Special characters required? (y/N)", "n")
                password_requirements["special_required"] = special_required

                break
            except ValueError:
                print(f" {RED}Not a valid number.{WHITE}")


def confirmOptions():
    print(f"\n\n {YELLOW}Confirmation")
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
    global valid_birthdate
    global valid_partner_birthdate

    valid_partner_birthdate = False
    valid_birthdate = False

    if isinstance(keywords["birthdate"], datetime):
        global birthdate_year
        global birthdate_month
        global birthdate_day

        birthdate_year = str(keywords["birthdate"].year)
        birthdate_month = str(keywords["birthdate"].month)
        birthdate_day = str(keywords["birthdate"].day)
        valid_birthdate = True

    if isinstance(keywords["partner_birthdate"], datetime):
        global partner_year
        global partner_month
        global partner_day

        partner_year = str(keywords["partner_birthdate"].year)
        partner_month = str(keywords["partner_birthdate"].month)
        partner_day = str(keywords["partner_birthdate"].day)
        valid_partner_birthdate = True


def addKeywordsToList():
    for key, value in keywords.items():
        if not value or key in ["birthdate", "partner_birthdate"]:
            continue
        if isinstance(value, list):
            for keyword in value:
                if keyword in all_keywords_list:
                    continue
                all_keywords_list.append(keyword)
        else:
            all_keywords_list.append(value)
    combo_1 = f"{keywords['firstname']}{keywords['lastname']}"
    combo_2 = f"{keywords['lastname']}{keywords['firstname']}"
    combo_3 = f"{keywords['partner_name']}{keywords['firstname']}"
    combo_4 = f"{keywords['firstname']}{keywords['partner_name']}"
    combo_5 = f"{keywords['partner_lastname']}{keywords['lastname']}"
    combo_6 = f"{keywords['lastname']}{keywords['partner_lastname']}"

    for combo in [combo_1, combo_2, combo_3, combo_4, combo_5, combo_6]:
        if combo not in all_keywords_list:
            all_keywords_list.append(combo)

    print(f"\n{WHITE} Using keys: ", end="")
    if len(all_keywords_list) > 1:
        for key in all_keywords_list:
            print(f"{YELLOW}{key}{',' if key != all_keywords_list[-1] else ''} ", end="")
    else:
        print(f"{YELLOW}{all_keywords_list[0]}", end="")
    print("\n")


def getLinkedInData():
    print(f"\n\n {YELLOW}LinkedIn login (Required for API)")
    email = input(f"\n {WHITE}Enter your LinkedIn email: {YELLOW}")
    password = getpass(f" {WHITE}Enter your LinkedIn password: {YELLOW}")

    print(f"\n {YELLOW}Logging in...\n")
    api = Linkedin(email, password)

    target = input(f" {WHITE}ID or URL of target: {YELLOW}")

    for url in ["https://www.linkedin.com/in/", "https://linkedin.com/", "www.linkedin.com", "linkedin.com", "linkedin.com", "/in", "/"]:
        target = target.strip(url)

    print(f" {WHITE}Using target: {YELLOW}{target}")
    print(f"\n {WHITE}Getting data...")

    data = api.get_profile(target)

    return data

def addLinkedInData(data):
    remove = [
        "geoCountryUrn",
        "geoLocationBackfilled",
        "entityUrn",
        "elt",
        "headline",
        "backgroundPicture",
        "backgroundPictureOriginalImage",
        "profile_id",
        "profile_urn",
        "member_urn",
        "publications",
        "certifications",
        "honors",
        "industryUrn",
        "geoLocation",
        "member_urn",
        "profile_urn",
        "profile_id"
    ]

    profile_keywords = [
        "firstname",
        "lastname",
        "address",
        "locationname",
        "geolocationname",
    ]

    data_lower = {}
    for key, value in data.items():
        data_lower[key.lower()] = value

    data = data_lower

    for key in remove:
        if key in data:
            del data[key]

    pprint(data)

    if yesNoPrompt(" Save data to keywords? (y/N)", "n"):
        for key, value in data.items():
            if key in profile_keywords:
                if key == "locationname":
                    keywords["country"] = value
                elif key == "geolocationname":
                    keywords["city"] = value
                elif key == "address":
                    address = data["address"].split()
                    for value in address:
                        if value not in keywords["other_keywords"]:
                            keywords["other_keywords"].append(value)
                else:
                    keywords[key] = value
        if "birthdate" in data:
            month_int = data["birthdate"]["month"]

            i = 1
            for month, season in months.items():
                if i != int(month_int):
                    i += 1
                    continue
                if month not in all_keywords_list:
                    if month not in keywords["other_keywords"]:
                        keywords["other_keywords"].append(month)
                if season not in all_keywords_list:
                    if season not in keywords["other_keywords"]:
                        keywords["other_keywords"].append(season)
                i += 1 


def createFile():
    global wordlist_file
    global wordlist_name

    overwrite = True
    name = keywords["firstname"]
    time = datetime.now().strftime("%H.%M.%S")

    wordlist_name = f"wordlist_{time}.txt"
    if keywords["firstname"]:
        wordlist_name = f"{name}_{time}.txt"
    if path.exists(wordlist_name):
        overwrite = yesNoPrompt(f"{WHITE}File already exists. This will not overwrite the file, but keep appending \n passwords to it. Continue? (y/N)", "n")

    if not overwrite:
        return
    wordlist_file = open(wordlist_name, "a")


def writeToList(key):
    iters = [
            f"{key}", f"{key}!",
            f"{'!' if key[:0] != '!' else ''}{key}!",
            f"{key}?", f"?{key}?", f"{key}.",
            f".{key}.", f"*{key}*", f"{key}*"]
    for password in iters:
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
    if valid_partner_birthdate:
        write2(key, partner_year)
    if valid_birthdate:
        write2(key, birthdate_year)
    if not use_numbers:
        return
    for num in common_numbers:
        for w in [key, key * 2 if len(key) < 5 else key]:
            writeToList(w + num)
        for w in [num, num * 2 if len(num) < 4 else num]:
            writeToList(w + key)


def write2(key, date):
    for w in [key, reverseString(key)]:
        for f in [str, reverseString]:
            if use_swedish:
                w = replaceChars(key, r_swedish)
            writeToList(w + f(date))
            writeToList(w + lastTwoChars(f(date)))
            writeToList(w + lastTwoChars(f(date)) * 2)


def createWordlist():
    print(f"""
 {CYAN}----------------------------
 {WHITE}Interactive Wordlist Creator
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
    for k in ["birthdate", "partner_birthdate"]:
        temp_keys[k] = str(temp_keys[k]).strip("00:00:00").strip()
    if path.exists(".\\password_keys.json"):
        accept_warning = yesNoPrompt(f"""\n\n{LIGHT_RED} Warning. This will overwrite the current config file(s).
 Continue? (y/N) """, "n")
        if accept_warning:
            config_json = dumps(temp_keys, indent = 4)
            with open ("password_keys.json", "w") as config:
                config.write(config_json)
            rules_json = dumps(password_requirements, indent = 4)
            with open ("password_requirements.json", "w") as rules:
                rules.write(rules_json)
            print(f"{GREEN}\n  Config saved successfully")


def loadConfig():
    global keywords
    if path.exists(".\\password_requirements.json"):
        with open("password_requirements.json", "r", encoding="utf-8") as rules:
            global password_requirements
            password_requirements = load(rules)
            print(f"{GREEN}\n  Password requirements loaded from password_requirements.json.{WHITE}")
    else:
        print(f"{RED}\n  password_requirements.json not found.{WHITE}")
    if path.exists(".\\password_keys.json"):
        with open("password_keys.json", "r", encoding="utf-8") as config:
            keywords = load(config)
            if keywords["birthdate"]:
                keywords["birthdate"] = formatDate(keywords["birthdate"])
            if keywords["partner_birthdate"]:
                keywords["partner_birthdate"] = formatDate(keywords["partner_birthdate"])
            print(f"{GREEN}\n  Password keys loaded from password_keys.json.{WHITE}")
        return
    print(f"{RED}\n  password_keys.json not found.{WHITE}")


def editConfig():
    option = 0
    while option != "c":
        clearConsole()
        printConfig()
        print(f"\n{YELLOW} Enter 'c' to confirm options.")
        option = input(f"{WHITE}\n\n Option: {YELLOW}")
        if option in keywords.keys():
            keywords[option] = input(f"\n {WHITE}Value: ")
            if option in ["partner_birthdate", "birthdate"]:
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
                password_requirements[option] = yesNoPrompt(f" {WHITE}Value (y/n)", "n")
            else:
                password_requirements[option] = input(f" {WHITE}Value: {YELLOW}")
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
    print()
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
            input(f"\n {YELLOW}Press enter when done.")
            main()
        case "4":
            printConfig()
            input(f"\n {YELLOW}Press enter when done.")
            main()
        case "5":
            saveConfig()
        case "6":
            loadConfig()
        case "7":
            addLinkedInData(getLinkedInData())
        case "8":
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
    {CYAN}1{WHITE}) Create wordlist interactively
    {CYAN}2{WHITE}) Create wordlist from config

    {CYAN}3{WHITE}) Show wordlist tips
    {CYAN}4{WHITE}) Show current config

    {CYAN}5{WHITE}) Save config
    {CYAN}6{WHITE}) Load config from file
    {CYAN}7{WHITE}) Load config from LinkedIn 
    {CYAN}8{WHITE}) Edit config

    {LIGHT_RED}99{WHITE}) Exit\n  {CYAN}----------------------{WHITE}\n""")

        option = str(input(f" {WHITE}IWG > "))
        clearConsole()
        checkMenuOption(option)


if __name__ == "__main__":
    main()
