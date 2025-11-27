#!/usr/bin/env python3

import requests
import webbrowser
from bs4 import BeautifulSoup

# === Settings ===
show_blacklist_files = True
auto_add_to_blacklist = False
blacklist_file_name = "blacklist.txt"
# ================

def main():
    urls = {
        'de': 'https://www.discudemy.com/language/german/',
        'en': 'https://www.discudemy.com/language/english/',
        'es': 'https://www.discudemy.com/language/spanish/'
    }

    available_languages = ', '.join(urls.keys())
    language = input(f"Select a language, default is en ({available_languages}): ").strip().lower()

    if language not in urls:
        language = "en"

    blacklist = get_blacklist()
    counter = 1

    while True:
        current_url = f"{urls[language]}{counter}"

        print("use URL: " + current_url)
        links = scrap(current_url)

        for link in links:
            if on_blacklist(link, blacklist):
                if show_blacklist_files == True:
                    print("❌ " + link)
            else:
                print("✅ " + link)
                webbrowser.open(link)
                if auto_add_to_blacklist == True:
                    append_line_on_blacklist(link)

        more = input("Press return for more courses: ")

        if more == '':
            counter += 1
        else:
            print("Script terminate.")
            break


def scrap(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # collect card links
    card_links = []
    for a_tag in soup.find_all('a', class_='card-header'):
        if 'href' in a_tag.attrs:
            card_links.append(a_tag['href'])

    # collect sub_side_links
    sub_side_links = []
    for link in card_links:
        response = requests.get(link)
        soup_inner = BeautifulSoup(response.content, 'html.parser')

        take_course_tag = soup_inner.find('a', string=lambda s: s and 'Take Course' in s)
        if take_course_tag and 'href' in take_course_tag.attrs:
            sub_side_links.append(take_course_tag['href'])

    # collect udemy links
    udemy_links = []
    for course_link in sub_side_links:
        response = requests.get(course_link)
        soup_final = BeautifulSoup(response.content, 'html.parser')

        target_tag = soup_final.find('a', string=lambda s: s and 'https' in s)
        if target_tag and 'href' in target_tag.attrs:
            udemy_links.append(target_tag['href'])

    return udemy_links


def on_blacklist(url, blacklist):
    base_url = url.split('?')[0].rstrip('/')
    return base_url in blacklist


def get_blacklist():
    try:
        with open(blacklist_file_name, 'r') as datei:
            blacklist = datei.read().splitlines()
            return [url.lstrip('✅ ').split('?')[0].rstrip('/') for url in blacklist]
    except FileNotFoundError:
        print(f"File was not found: {blacklist_file_name}")
        return []
    except Exception as e:
        print(f"An error has occurred: {e}")
        return []


def append_line_on_blacklist(line: str):
    if not line.endswith("\n"):
        line = line + "\n"

    with open(blacklist_file_name, "a", encoding="utf-8") as f:
        f.write(line)


main()