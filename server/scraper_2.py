# from bs4 import BeautifulSoup
# from datetime import datetime
# from collections import defaultdict
# import cloudscraper
# from fake_useragent import UserAgent


# def get_menu(hall):
#     scraper = cloudscraper.create_scraper()
#     today = datetime.now().strftime("%Y-%m-%d")
#     url = f"https://dining.umich.edu/menus-locations/dining-halls/{hall}/?menuDate={today}"

#     headers = {
#         "User-Agent": UserAgent().random,
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#         "Accept-Language": "en-US,en;q=0.9",
#         "Referer": "https://dining.umich.edu/menus-locations/dining-halls/",
#     }

#     try:
#         response = scraper.get(url, headers=headers)
#         response.raise_for_status()
#     except Exception as e:
#         return f"Error: {e}"

#     soup = BeautifulSoup(response.text, 'html.parser')

#     meal_map = {0: 'breakfast', 1: 'lunch', 2: 'dinner'}
#     menu = {}

#     # The menu is inside #mdining-items, split into 3 .courses divs (one per meal)
#     mdining_items = soup.find('div', id='mdining-items')
#     if not mdining_items:
#         return "Could not find menu container."

#     courses_divs = mdining_items.find_all('div', class_='courses')

#     for i, courses_div in enumerate(courses_divs[:3]):
#         meal_name = meal_map[i]
#         station_data = defaultdict(list)

#         # Each station is an <li> inside <ul class="courses_wrapper">
#         wrapper = courses_div.find('ul', class_='courses_wrapper')
#         if not wrapper:
#             continue

#         for station_li in wrapper.find_all('li', recursive=False):
#             h4 = station_li.find('h4')
#             if not h4:
#                 continue

#             station = h4.get_text(strip=True)

#             # Food items: <li> tags inside <ul class="items"> that contain an <h5>
#             items_ul = station_li.find('ul', class_='items')
#             if not items_ul:
#                 continue

#             for item_li in items_ul.find_all('li'):
#                 h5 = item_li.find('h5')
#                 if not h5:
#                     continue
#                 span = h5.find('span', class_='item-name')
#                 if not span:
#                     continue
#                 name = span.get_text(strip=True)
#                 station_data[station].append(name)

#         menu[meal_name] = station_data

#     return menu


# def print_menu(menu):
#     for meal in ['breakfast', 'lunch', 'dinner']:
#         print(f"\n{'='*40}")
#         print(f"  {meal.upper()}")
#         print(f"{'='*40}")

#         station_data = menu.get(meal, {})
#         if not station_data:
#             print("  (No data)")
#             continue

#         for station, items in station_data.items():
#             print(f"\n  [{station}]")
#             for item in items:
#                 print(f"    - {item}")


# if __name__ == "__main__":
#     print("Fetching Bursley menu...")
#     menu = get_menu("bursley")

#     if isinstance(menu, str):
#         print(menu)
#     else:
#         print_menu(menu)


import requests
from bs4 import BeautifulSoup
import json

def scrape_umich_sports():
    url = "https://events.umich.edu/list?filter=alltypes%3A20"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        events = []

        # Find all event containers based on your screenshot
        event_divs = soup.find_all('div', class_='event-listing-grid')

        for item in event_divs:
            # 1. Extract Title and Link
            title_tag = item.find('div', class_='event-title').find('a')
            title = title_tag.get_text(strip=True)
            link = "https://events.umich.edu" + title_tag['href']

            # 2. Extract DateTime from the <time> tag
            time_tag = item.find('time', class_='time-banner')
            event_datetime = time_tag['datetime'] if time_tag else "N/A"
            readable_time = time_tag.get_text(strip=True) if time_tag else "N/A"

            # 3. Extract Location (usually inside event-details <ul>)
            details = item.find('ul', class_='event-details')
            location = "TBD"
            if details:
                # Often the first or second <li> in the details list
                loc_li = details.find('li')
                if loc_li:
                    location = loc_li.get_text(strip=True)

            events.append({
                "title": title,
                "link": link,
                "datetime": event_datetime,
                "time_display": readable_time,
                "location": location
            })

        return events

    except Exception as e:
        print(f"Error scraping: {e}")
        return []

# Run it
if __name__ == "__main__":
    sports_data = scrape_umich_sports()
    print(json.dumps(sports_data, indent=2))