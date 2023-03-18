SCRAPPING_BASE_URL = "http://www.tropicopia.com/house-plant/detail.np/detail-"
import requests
#import logging as logger
from bs4 import BeautifulSoup
from pathlib import Path
import json

def scrapper(start=1, end=356): # todo: could make this dynamic, to loop until 404
    plants = []
    for id in range(start, end+1):
        # build URL
        if id < 10 : id = "0" + str(id)
        feed_url = SCRAPPING_BASE_URL + str(id) + ".html"
        #logger.DEBUG("Trying to scrape: {url}", url=str(feed_url))
        ask_for_scrape = _get_html_content(feed_url)
        if isinstance(ask_for_scrape, int):
            print("Can not access the URL, status", ask_for_scrape)
        else:
            plants.append(ask_for_scrape)
    # save only at the end
    file_name = _get_domain_from_url(SCRAPPING_BASE_URL) + ".json"
    Path("./scrapped_data").mkdir(parents=True, exist_ok=True)
    try:
        file_exists = open(f"./scrapped_data/{file_name}", "r")
    except FileNotFoundError:
        print("Saving data...")
        file = open(f"./scrapped_data/{file_name}", "w")
        json.dump(plants, file, indent=4)
        file.close()
    else:
        file_exists.close()
        print(f"File {file_name} already exists. Manually delete if you want to refresh data")

def _get_domain_from_url(url=SCRAPPING_BASE_URL):
    prefix = url.index(".") + 1
    domain = url[prefix:]
    sufix = len(domain) - domain.index("/")
    domain = domain[:-sufix].replace(".", "-")
    return domain

def _get_html_content(url):
    print("Scrapping...", url)
    html_response = requests.get(url)

    if html_response.status_code != 200:
        return html_response.status_code
    else:
        #logger.DEBUG("Successful fetch from {url}, returned Status {st}", url=url, st=html_response.status_code)
        return _soup_the_plant(html_content=html_response.content)

def _soup_the_plant(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    abstract = soup.find_all('p', attrs={'class' : 'ar12D'})

    plant = {}
    # create a list from all avilable metadata
    key_bool = True
    key = ""
    value = ""
    for tag in abstract:
        tmp = tag.getText().replace("\t", "").replace("\n", "")

        if key_bool: # ako je key na redu
            key = tmp[:-2]
        else:
            if tmp.find(":") > 0: # ako ima ':' onda je key
                key = tmp[:-2] # spremi za iduci key, ali nemoj ga gledat. sto znaci da je iduci tmp moguci value
                tmp = None
                key_bool = not key_bool

            value = tmp
            #logger.DEBUG("Found key, writing {key}: {value} to plant", key=key, value=value)
            plant[key] = value
        key_bool = not key_bool
    #logger.DEBUG("No more keys on this plant...")
    # scrape plant image url
    image = ""
    for img in soup.findAll('img', alt=True):
        image = img # we want last one
    plant["image_url"] = "http://www.tropicopia.com/house-plant/" + image["src"][3:]
    return plant


scrapper()
