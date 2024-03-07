# Houseing Scraper

Finding housing is a pain, especially with the lack of filters. This webscraper gets all new postings off of a given list of providers (for now only pararius but they can be extended as a provider subclass).

## The way it works

1. Create a list of providers and target URL, e.g. with pararius one url for each location
2. Each registered provider will dynamically retrieve all pages based and scrape the entries opening each one for additional information
3. Each site is also stored for later viewing
4. The entries are then filtered based on more criteria
5. The ones that are left after filtering are then opened in the default browser.

## How to use it

1. Clone this repository
2. Explore the Analysis notebook or run the headless mode
3. Adapt the Providers as wanted
4. Adapt the filters