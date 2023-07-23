import random
import time
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import csv
import random
from datetime import date, timedelta
from selenium.webdriver.chrome.options import Options
import pandas
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# test

def get_prices(cities, dates):
    options = Options()
    df = pandas.read_csv('whatismybrowser-user-agent-database.csv')
    # chrome_options.add_argument(f"--user-agent={my_user_agent}")
    agent_id = random.randint(1, len(df))
    my_user_agent = df['user_agent'][agent_id]
    options.add_argument(f"--user-agent={my_user_agent}")
    options.add_argument("disable-infobars")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])

    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    # options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # driver = webdriver.Chrome(options=options)

    # for city in cities:
    #    header = ['start date', 'end date', 'fly out company', 'fly out duration', 'fly back company','fly back duration', 'cost']
    #    filename = f"flights_{city}.csv"
    #    file = open(filename, 'w')
    #    writer = csv.writer(file)
    #    writer.writerow(header)

    # for date in dates:
    # startdate = '2023-09-01'
    startdate = date.split("/")[0].strip()
    # enddate = '2023-09-04'
    enddate = date.split("/")[1].strip()
    print(f"checking for {city} at {date}")
    driver = webdriver.Chrome(options=options)
    url = f"https://www.kayak.com/flights/TLV-{city}/{startdate}/{enddate}/2adults?sort=price_a"
    # print(url)
    driver.get(url)
    sleep_time = random.randint(5, 10)
    sleep(sleep_time)
    # driver.quit()
    flights = driver.find_elements(By.CLASS_NAME, 'nrc6-inner')
    # print(len(flights))
    try:
        elementHTML = flights[0].get_attribute('outerHTML')
    except:
        sleep(30)

    else:
        elementSoup = BeautifulSoup(elementHTML, 'html.parser')
        temp_price = elementSoup.find('div', {'class': 'nrc6-price-section'})
        price = temp_price.find('div', {'class': 'f8F1-price-text'}).text.split('$')[1]
        # print(price.text)
        companies = elementSoup.find("div", {'class': 'J0g6-operator-text'})
        if companies:
            # print(companies.text)
            pass
        temp_flights = elementSoup.find_all('li', {'class': 'hJSA-item'})
        # flights = temp_flights.find_all('div', {'class': 'c3J0r-container'})
        # for flight in flights:
        # for flight in temp_flights:
        # print(flight)
        out_carrier = temp_flights[0].findNext('div', {'class': 'c_cgF c_cgF-mod-variant-default'}).text
        out_time = temp_flights[0].findNext('div', {'class': 'vmXl vmXl-mod-variant-large'}).text
        in_carrier = temp_flights[1].findNext('div', {'class': 'c_cgF c_cgF-mod-variant-default'}).text
        in_time = temp_flights[1].findNext('div', {'class': 'vmXl vmXl-mod-variant-large'}).text
        # print(f"flight from {startdate} until {enddate}")
        # print(f"fly out with {out_carrier} for {out_time} and back with {in_carrier} for {in_time} cost:{price} ")
        # header = ['start date', 'end date', 'fly out company', 'fly out duration', 'fly back company', 'fly back duration',

        row = [startdate, enddate, out_carrier, out_time, in_carrier, in_time, price]
        if row:
            # print(row)
            # driver.close()
            return row
        else:
            row = [0, 0, 0, 0, 0, 0, 0]
            return row


# print((temp_flights))
dates = []
sdate = date(2024, 1, 1)  # start date
edate = date(2024, 4, 30)  # end date
delta = edate - sdate
for day in range(delta.days + 1):
    day_obj = sdate + timedelta(days=day)
    if day_obj.weekday() == 3:  # Thursday
        sunday = day_obj + timedelta(days=3)
        # print(day_obj, day_obj.weekday())
        # print(sunday, sunday.weekday())
        # print(type(day_obj))
        # get_prices(str(day_obj.strftime("%Y-%m-%d")).strip(), str(sunday.strftime("%Y-%m-%d")).strip())
        startday = day_obj.strftime("%Y-%m-%d").strip()
        endday = sunday.strftime("%Y-%m-%d").strip()
        # print (type (startday))
        date_range = f"{startday}/{endday}"
        dates.append(date_range)
        # get_prices(date_range)


# thursdays = [(sdate + timedelta(days=d)).strftime('%A %Y-%m-%d') for d in range(0, (edate - sdate).days + 1)
# if (sdate + timedelta(days=d)).weekday() == 3]
def user_agent():
    df = pandas.read_csv('whatismybrowser-user-agent-database.csv')
    # chrome_options.add_argument(f"--user-agent={my_user_agent}")
    agent_id = random.randint(1, len(df))
    my_user_agent = df['user_agent'][agent_id]
    print(my_user_agent)


# print(dates)
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print(current_time)

header = ['start date', 'end date', 'fly out company', 'fly out duration', 'fly back company', 'fly back duration',
          'cost']

# for date in dates:
# row =
cities = ['TBS', 'IST', 'VIE', 'PAR', 'ROM', 'MIL', 'BUD', 'KRK', 'BER', 'AMS', 'CDG', 'PRG', 'LON']
# get_prices(cities, dates)
for city in cities:
    filename = f"flights_{city}.csv"
    file = open(filename, 'w')
    writer = csv.writer(file)
    writer.writerow(header)
    for date in dates:
        row = get_prices(city, date)
        print(row)
        if row:
            writer.writerow(row)
    file.close()
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print(current_time)
