#!/usr/bin/env python
import os
from string import Template
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROME_OPTIONS = Options()
CHROME_OPTIONS.add_argument('--headless')
CHROME_OPTIONS.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
DRIVER = webdriver.Chrome(executable_path=os.path.abspath('chromedriver'), chrome_options=CHROME_OPTIONS)
ROOMS = [14531512, 19278160, 19292873]
ROOMURL = Template('https://www.airbnb.co.uk/rooms/$roomId')

def getListingName(soup):
    return soup.find('div', {'id': 'listing_name'}).text


def getDetails(soup):
    details_div = soup.find('div', {'id': 'details'}).findAll('strong')
    key_values = [x.parent.text for x in details_div
                  if x.parent.name == 'div'
                  and ':' in x.parent.text]

    details_values = {}
    for kvp in key_values:
        split_values = kvp.split(': ')
        details_values[split_values[0]] = split_values[1]
    return details_values


def getAmenities(soup):
    amenities = set()
    for span in soup.find('div', {'class': 'amenities'}).findAll('span'):
        if 'Amenities' not in span.text and 'More' not in span.text:
            amenities.add(span.text)
    return ', '.join(amenities)


def fetchRoom(room):
    DRIVER.get(ROOMURL.substitute(roomId=room))
    soup = BeautifulSoup(DRIVER.page_source, 'html.parser')

    name = getListingName(soup)
    details = getDetails(soup)
    amenities = getAmenities(soup)

    print
    print room
    print name
    print 'Type: ' + details['Room type']
    print 'Bedrooms: ' + details['Bedrooms']
    print 'Bathrooms: ' + details['Bathrooms']
    print 'Amenities: ' + amenities
    print


for roomId in ROOMS:
    fetchRoom(roomId)

DRIVER.close()
