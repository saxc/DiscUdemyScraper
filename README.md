# DiscUdemyScraper
The script allows you to access free [Udemy](https://www.udemy.com/) courses listed on [DiscUdemy](https://www.discudemy.com/).

## Useing
- Call `python DiscUdemyScraper.py`to start the script.
- Choose your preferred language
- The scraper works page by page on [DiscUdemy](https://www.discudemy.com/)
- Courses that are not on the blacklist will open in the browser.

## Blacklist
- Courses that you already have or don't want can be added to the `blacklist.txt` file so that the URL won't open.
- The blocked courses are marked with an ❌ in the CLI.
- The CLI output of opened courses (✅) can be copied to the blacklist to prevent them from being opened again.

## Settings
- The behavior can be adjusted in the code within the settings section.

```py
# === Settings ===
show_blacklist_files = True
auto_add_to_blacklist = False
blacklist_file_name = "blacklist.txt"
# ================
```

## Demo
![](demo.gif)