# Image Scraper

Simple python module for scraping images from the web, created for AI development.

## Features

* scrape images from google.com and duckduckgo.com
* search duplicated and eliminate them.
* allow to create complex databases from the engine top search of supplied keyword.
* use tor network with firefox for scraping. (optional)

## Basic Usage

```
>> python imageCrawler.py -k cats dogs
>> Select by number the queries to ignore:
>> ( 0 ) cats
>> ( 1 ) cats with hats
>> 1
>> Start with cats download 4000 at engines\cats
>> 100%
>> Select by number the queries to ignore:
>> ( 0 ) dogs
>> ( 1 ) dogs with hats
>> 1
>> Start with cats download 4000 at engines\dogs
>> 100%
>> Searching duplicated...
>> END
```

### Results:

    \engines
        \cats
            \ keys.json
            \ +4000 images files
        \dogs
            \ keys.json
            \ +4000 images files

## Installing

### (1) Install.

* [Firefox](https://www.mozilla.org/en-US/firefox/new/)
* [TorBrowser](https://www.torproject.org/) (OPTIONAL).

### (2) Download and add to path.

#### geckodriver combability [check](https://stackoverflow.com/questions/45329528/which-firefox-browser-versions-supported-for-given-geckodriver-version) 

* [geckodriver](https://github.com/mozilla/geckodriver/releases)

### (3) Run this command.
```
pip install engineCrawler
```