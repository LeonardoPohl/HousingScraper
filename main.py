from providers import ParariusProvider
from utils import Entry

def get_pararius_entries():
  pp = ParariusProvider()
  pp.query_entries()
  pp.get_detailed_results()
  return pp.entries

def filter_entries(entries: list[Entry]):
  
  tgtbt_filter = lambda entry: entry.getPricePerArea > TGTBT_AREA_PRICE_THRESHOLD
  df = df[df['Price per area'] > tgtbt_area_price_threshold]
  df = df[df['Area per room'] > tiny_room_threshold]
  df = df[~df["description"].str.contains('permit', case=False)]
  df = df[df["rented"].isnull()]

if __name__ == "__main__":
  entries = []
  entries += get_pararius_entries()


