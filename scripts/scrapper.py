SCRAPPING_BASE_URL = "http://www.tropicopia.com/house-plant/detail.np/detail-"
import requests
#import logging as logger
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
import json

id = 0

def scrapper(start=1, end=365): # todo: could make this dynamic, to loop until 404
    plants = []
    for id in range(start, end+1):
        if id < 10 : id = "0" + str(id)
        feed_url = SCRAPPING_BASE_URL + str(id) + ".html"
        ask_for_scrape = _get_html_content(feed_url)
        if isinstance(ask_for_scrape, int):
            print("Can not access the URL, status", ask_for_scrape)
        else:
            plants.append(ask_for_scrape)
    # save the data locally once the scrapping is done. will save empty file if fails
    event_id = datetime.now().strftime("_%d.%m.%Y-%H:%M:%S")
    file_name = _get_domain_from_url(SCRAPPING_BASE_URL) + event_id + ".json"
    Path("./scrapped_data").mkdir(parents=True, exist_ok=True)
    with open(f"./scrapped_data/{file_name}", "w") as new_file:
        json.dump(plants, new_file, indent=4)

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
        return _soup_tropicopia_house_plant(html_content=html_response.content)

def _soup_tropicopia_house_plant(html_content):
    global id
    soup = BeautifulSoup(html_content, "html.parser")
    abstract = soup.find_all('p', attrs={'class' : 'ar12D'})
    id += 1
    plant = {'id':id}
    key_bool = True
    key = ""
    value = ""
    for tag in abstract:
        cleared_tag = tag.getText().replace("\t", "").replace("\n", "")
        if key_bool: # ako je key na redu
            key = cleared_tag[:-2].replace(" ","_") # svaki key ima zadnja dva chara " :"
        else:
            if cleared_tag.find(":") > 0: # provjeravamo da li postoji value. ako ima ':' onda je key, pogledaj predhodni komentar
                key = cleared_tag[:-2].replace(" ","_") # spremi za iduci key, ali nemoj ga gledat. sto znaci da je iduci cleared_tag moguci value
                cleared_tag = "None"
                key_bool = not key_bool
            value = cleared_tag
            #logger.DEBUG("Found key, writing {key}: {value} to plant", key=key, value=value)
            value = value.lower() if value else value
            plant[key.lower()] = value
        key_bool = not key_bool
    #logger.DEBUG("No more keys on this plant...")
    plant.popitem() # remove comments
    # scrape plant image url
    image = ""
    for img in soup.findAll('img', alt=True):
        image = img # we want last one
    plant["image_url"] = "http://www.tropicopia.com/house-plant/" + image["src"][3:]
    return plant

if __name__ == "__main__":
    scrapper()
