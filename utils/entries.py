from .entry import Entry
from providers import ParariusProvider

class Entries:
  def __init__(self, pararius_query: str = ""):
    self.entries = []

    self.providers = [
      ParariusProvider()
    ]

  def get_all_entries(self):
    self.entries = []

    for provider in self.providers:
      self.entries += provider.query_entries()

    