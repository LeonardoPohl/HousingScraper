from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup

from .address import Address

@dataclass
class Entry:
  title: str = ""
  link: int = 0
  location: str = 0
  price: int = 0
  area: int = 0
  rooms: int = 0
  furnished: str = ""

  # Detailed
  description: str = ""
  address: Address = None