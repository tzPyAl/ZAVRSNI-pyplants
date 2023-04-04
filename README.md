# pyplants

## Scrapper

- [Tropicopia](http://www.tropicopia.com/house-plant/) contains rich metadata for over 350 house plants
- Using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) we fetch all the meta + image url, and save inside the json file locally
- access [tropicopia - plant](http://www.tropicopia.com/house-plant/detail.np/detail-01.html) to review the available metadata
- support for history. each scrape saved in unique file
- TODO: save scrapped data to db

## Endpoint data from ip

- get local data from ip: city, country, longitude, latitude
- user can hardcode location by city, or lon/lat so weather can be fetched correctly for his plants location
- TODO: save hardcoded values to db

## Weather

- current weather and pollution from OpenWeatherMap API
- data fetched by geolocation from IP (Endpoint data from ip) or by hardcoded city name

## GUI

- navbar, login, register
- routes, auth

## DB

- User, Pots models

## Next step/s

- write tests
- create ci on gh actions
