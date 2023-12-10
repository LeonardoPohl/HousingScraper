from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup

from .address import Address

TGTBT_THRESHOLD = 13
TINY_ROOM_THRESHOLD = 15

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
  rented: str = ""

  @property 
  def price_per_area(self):
    return self.price / self.area
  
  @property 
  def price_per_room(self):
    return self.price / self.rooms

  @property
  def get_area_per_room(self):
    return self.area / self.rooms
    
  def get_distance_to(self, location):
    pass

  def has_detailed_info(self):
    return self.description != "" or self.address or self.rented != ""

  def is_tgtbt(self, tgtbt_threshold: float = TGTBT_THRESHOLD):
    return self.get_price_per_area < tgtbt_threshold