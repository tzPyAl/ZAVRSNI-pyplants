# pyplants

## Scrapper ✅

- [Tropicopia](http://www.tropicopia.com/house-plant/) contains rich metadata for over 350 house plants
- Using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) we fetch all the meta + image url, and save inside the json file locally
- access [tropicopia - plant](http://www.tropicopia.com/house-plant/detail.np/detail-01.html) to review the available metadata
- support for history. each scrape saved in unique file

## Endpoint data from ip ✅

- get local data from ip: city, country, longitude, latitude
- user can hardcode location by city, or lon/lat so weather can be fetched correctly for his plants location

## Weather ✅

- current weather and pollution from OpenWeatherMap API
- data fetched by geolocation from IP (Endpoint data from ip) or by hardcoded city name

## GUI 🚧

- Flask, jinja2, FlaskForm
- bootstrap, html, css
- navbar, login, register

### Pots 🚧

- responsive home page

### Pot 🚧

- pot has name, image, and status
- CRUD

### Profil 🚧

- auth, remember me
- user has name, email, password and image
- CRUD
- if user changes the profile picture, old one is deleted
- profile picture is formated to 125x125px

## DB ✅

- MySQL with SQLAlchemy
- User, Pots models

## Next step/s 🚧 🚧 🚧

- pots hardcode statuses, and show status content and icon
- paginate the home page
- user email and password reset
- deploy, custom domain, https
- embed the weather and ip/location data
- write tests
- create ci on gh actions

## To define 🤔

- local iot data
- data visualization
- embed the scrapped data
