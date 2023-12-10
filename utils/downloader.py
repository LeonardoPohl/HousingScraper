from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import requests

# Possible todo: add download and process

def download_file(url):
  with requests.get(url) as r:
    return r


def mt_download(urls: list[str]):
  results = []
  
  with tqdm(total=len(urls)) as pbar:
    with ThreadPoolExecutor(max_workers=len(urls)) as ex:
      futures = [ex.submit(download_file, url) for url in urls]
      for future in as_completed(futures):
        results.append(future.result())
        pbar.update(1)

  return results