from bs4 import BeautifulSoup
from datetime import datetime
import requests
import cloudscraper
from fake_useragent import UserAgent
from collections import defaultdict
from menu_item import MenuItem

def scrape():
    dining_halls = [
        "bursley",
        "east-quad",
        "markley",
        "mosher-jordan",
        "north-quad",
        "south-quad",
        "twigs-at-oxford"
    ]
    prin = True
    for dining_hall in dining_halls:
        menu = get_menu(dining_hall)
        print("GETTING BREAKFAST")
        if(prin):
            print(menu['breakfast'])
        prin = False

    return

def get_menu(hall):
    scraper = cloudscraper.create_scraper()
    user_agent = UserAgent().random
    today = datetime.now()
    today_formatted = today.strftime("%Y-%m-%d")
    date = '2026-03-16' 
    url = f"https://dining.umich.edu/menus-locations/dining-halls/{hall}/?menuDate={today_formatted}"
    
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://dining.umich.edu/menus-locations/dining-halls/",
    }

    try:
        # 4. Use scraper instead of requests
        response = scraper.get(url, headers=headers)
        response.raise_for_status() 
    except Exception as error:
        return f"Error connecting to U-M server: {error}"

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # menu = {
    #     "breakfast": [],
    #     "lunch": [],
    #     "dinner": []
    # }
    menu = defaultdict(dict)
    menu_data = defaultdict(dict)
    all_food_items = defaultdict(dict)
    # stations = {
    #     "hot-cereal" : [],
    #     "toast" : [],
    #     "mbakery" : [],
    #     "soup" : [],
    #     "signature-maize" : [],
    #     "signature-blue" : [],
    #     "24-carrots" : [],
    # } 
    
    
    food_items_container = soup.find('div', id='mdining-items')
    meals_divided = food_items_container.find_all(['h3', 'div'], class_=['courses', ''])
    for i in range (0,2):
        
        what_meal = meals_divided[2*i].get_text(strip=True)
        courses_list = meals_divided[1+ 2*i].find('ul')
        courses = courses_list.find_all('li', recursive=False)
        for course in courses:
            if not course.find('h4'):
                continue
            print(courses)
            print(i)
            station = course.find('h4').get_text(strip =True)
            meals_container = course.find('ul')
            meals = meals_container.find_all('li', recursive=False)
            for meal in meals:
                name = meal.find('h5').find('span').get_text(strip = True)
                all_food_items[station] = (MenuItem(what_meal, name, station))
        menu[what_meal] = (all_food_items)
#.
    

        # for item in items:
        #     name = item.get_text(strip=True)
        #     if name:
    # else:
    #     menu[meal] = ["No menu found or Hall closed"]

    return menu

scrape()
# '''
# 1. Cloud-Native Serverless Functions (FaaS)
# Instead of a full server, you use a single function (like your Python scraper) that "wakes up" on a schedule.

# Options: AWS Lambda + Amazon EventBridge, Google Cloud Functions + Cloud Scheduler, or Azure Functions.

# How it works: You write the code and set a "trigger" in the cloud provider's console. The cloud provider handles the infrastructure.

# Pros: Extremely cheap (often free within the free tier), highly scalable, and demonstrates knowledge of major cloud platforms.

# Cons: Slightly more complex setup (IAM roles, permissions).

# 2. Always-On Virtual Private Server (VPS)
# You rent a small slice of a server (a "droplet" or "instance").

# Options: DigitalOcean, Linode, AWS EC2, or Google Compute Engine.

# How it works: You use a tool called Crontab (the industry-standard Linux task scheduler). You add a line to a configuration file that tells the server: "Run python3 scraper.py every day at 6:00 AM."

# Pros: Complete control over the environment. You can run databases and multiple scripts on one machine.

# Cons: Not free (usually $4–$5/month), and you are responsible for server security and updates.

# 3. PaaS "Background Workers"
# Platforms that simplify deployment often have built-in "cron" features.

# Options: Render (Cron Jobs), Railway (Scheduled Jobs), or Heroku (Heroku Scheduler).

# How it works: You connect your GitHub repo, and in the dashboard, you simply define the command and the frequency.

# Pros: The easiest to set up. It integrates directly with your existing server/API.

# Cons: Free tiers are more limited compared to GitHub Actions or AWS Lambda.
# You will need: pip install curl_cffi beautifulsoup4
# from curl_cffi import requests
# from bs4 import BeautifulSoup
# import json

# def scrape_all_halls():
#     dining_halls = [
#         "bursley", "east-quad", "markley", 
#         "mosher-jordan", "north-quad", "south-quad"
#     ]

#     all_data = {}
#     for hall in dining_halls:
#         print(f"Scraping {hall}...")
#         menu = get_menu(hall)
#         all_data[hall] = menu
    
#     # This is what you will eventually send to DynamoDB
#     return all_data

# def get_menu(hall):
#     # Use f-string to ensure NO spaces in the URL
#     url = f"https://dining.umich.edu/menus-locations/dining-halls/{hall}/"
    
#     try:
#         # 'impersonate' is the key: it mimics a real Chrome browser handshake
#         # which is much more effective than just changing the User-Agent
#         response = requests.get(url, impersonate="chrome120", timeout=10)
#         response.raise_for_status()
#     except Exception as e:
#         return {"error": f"Connection failed: {e}"}

#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # U-M uses specific IDs for meal periods
#     meal_periods = ["breakfast", "lunch", "dinner"]
#     menu_data = {}

#     for meal in meal_periods:
#         # Find the div section for that specific meal
#         meal_section = soup.find('div', id=meal)
#         items_list = []
        
#         if meal_section:
#             # U-M often puts the dish name inside an <a> tag inside the 'item-name' div
#             items = meal_section.find_all('div', class_='item-name')
#             for item in items:
#                 name = item.get_text(strip=True)
#                 if name:
#                     items_list.append(name)
        
#         menu_data[meal] = items_list if items_list else ["Closed or No Data"]

#     return menu_data

# # Run it
# if __name__ == "__main__":
#     results = scrape_all_halls()
#     print(json.dumps(results, indent=2))