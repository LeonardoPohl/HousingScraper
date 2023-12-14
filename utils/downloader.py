from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import requests
from typing import Callable
import json

def download_file(url):
  headers = {
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", 
      "Accept-Encoding": "gzip, deflate, br", 
      "Accept-Language": "en-US,en;q=0.5", 
      "Dnt": "1", 
      "Host": "httpbin.org", 
      "Sec-Fetch-Dest": "document", 
      "Sec-Fetch-Mode": "navigate", 
      "Sec-Fetch-Site": "cross-site", 
      "Sec-Fetch-User": "?1", 
      "Sec-Gpc": "1", 
      "Upgrade-Insecure-Requests": "1", 
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0", 
      "X-Amzn-Trace-Id": "Root=1-657b40f0-60b9292261869faa719dbf6d"
  }

  with requests.get(url) as r:
    return r


def mt_download(urls: list[str], func: Callable = None):
  results = []
  
  if len(urls) == 0:
    return

  with tqdm(total=len(urls)) as pbar:
    with ThreadPoolExecutor(max_workers=len(urls)) as ex:
      futures = {ex.submit(download_file, url):i for i, url in enumerate(urls)}

      for i, future in enumerate(as_completed(futures)):
        col = futures[future]
        if func:
          func(col, future.result())
        results.append(future.result())
        pbar.update(1)

  return results