from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

from utils import Entry, Address, mt_download
from .provider import Provider

import json

class ParariusProvider(Provider):
  def __init__(self, query: str):
    self.query: str = query
    self.entries: list(Entry) = []
    self.base_url = "https://www.pararius.com"
  
  def query_entries(self):
    response = requests.get(f"{self.base_url}{self.query}")
    soup = BeautifulSoup(response.content, 'html.parser')

    self.entries = [] 
    page_count = len(soup.find('ul', class_="pagination__list").find_all("li"))
    page_urls = [f"{self.base_url}{self.query}/page-{i}" for i in range(1, page_count)]
    page_results = mt_download(page_urls)

    for response in page_results:
      soup = BeautifulSoup(response.content, 'html.parser')
      for row in soup.select('section.listing-search-item'):
        self.entries.append(self.get_result(row))
  
  def get_result(self, row) -> Entry:
    title = row.find('h2').get_text().strip()
    link = row.find('a', class_='listing-search-item__link')['href']
    location = row.find('div', class_='listing-search-item__sub-title\'').get_text().strip()
    price = row.find('div', class_='listing-search-item__price').get_text().strip()
    area = row.find('li', class_='illustrated-features__item--surface-area').get_text().strip()
    rooms = row.find('li', class_='illustrated-features__item--number-of-rooms').get_text().strip()
    furnished = row.find('li', class_='illustrated-features__item--interior')

    if furnished:
      furnished = furnished.get_text().strip()

    return Entry(
      title = title,
      link = f"{self.base_url}{link}",
      location = location,
      price = int(re.findall(r'\d+', price.replace(',',''))[0]),
      area = int(re.findall(r'\d+', area.replace(',',''))[0]),
      rooms = int(re.findall(r'\d+', rooms)[0]),
      furnished = furnished)

  def get_detailed_results(self):
    responses = mt_download([entry.link for entry in self.entries])
    for i, response in enumerate(responses):
      soup = BeautifulSoup(response.content, 'html.parser')
      contents = json.loads(soup.find("script", type="application/ld+json").get_text().strip())
      self.entries[i].address = Address.from_pararius_dict(contents["address"])

      self.entries[i].description = BeautifulSoup(soup.find("div", class_="listing-detail-description__additional listing-detail-description__additional--collapsed").get_text().strip()).get_text()

      rented = soup.find("span", class_="listing-label listing-label--rented-under-reservation")

      # Ugly code
      if rented:
        rented = rented.get_text().strip()
      else:
        rented = soup.find("span", class_="listing-label listing-label--under-option")
        if rented:
          rented = rented.get_text().strip()

      self.entries[i].rented = rented

    
