# pyplants

## Scrapper ✅

- [Tropicopia](http://www.tropicopia.com/house-plant/) contains rich metadata for over 350 house plants
- Using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) we fetch all the meta + image url, and save inside the json file locally
- access [tropicopia - plant](http://www.tropicopia.com/house-plant/detail.np/detail-01.html) to review the available metadata
- support for history. each scrape saved in unique file

## Endpoint data from ip ✅

- get local data from ip: city, country, longitude, latitude using `ipapi`
- user can hardcode location by city, or lon/lat so weather can be fetched correctly for his plants location

## Weather ✅

- current weather and pollution from `OpenWeatherMap API`
- data fetched by geolocation from IP (Endpoint data from ip) or by hardcoded city name

## GUI ✅

- `Flask`, `jinja2`, `FlaskForm`, `Pillow`, `json2html`
- `bootstrap`, `html`, `css`
- navbar, layout, login, register
- error pages (404, 403, 500)

### Pots ✅

- responsive home page with add pot option
- pagination

### Pot 🚧

- pot has name, image, status, location, lon, lat
- location is proposed from the ip.address, but can be manually entered
- we use API -explained in weather- to find the city
- when we confirm the city, we extract lon/lat for weather data
- pot now has tabs: basic info, weather and pollution, which consumes fetched weather data
- CRUD
- you can connect plant to pot. idea is to know which plant is in the pot, so you can use plant's meta to create alarms and notifications.
- to connect plant, you can use scrapped db, which will automaticlly fill the meta, or manually enter the plant.
- it's possible to edit plant, but no need for delete.

### Plants ✅

- search scrapped plants db
- search is posible by keyword in common_name key
- not key sensitive
- responsive result of first filter match

### Profil ✅

- auth, remember me
- user has name, email, password and image
- CRUD
- if user changes the profile picture, old one is deleted
- profile picture is formated to 125x125px
- user email and password reset

## DB ✅

- `SQLAlchemy`
- hashed password with `secrets`
- User model (id, username, email, password, image_file)
- Pots models (id, name, pot_image, date_created, status, location, lon, lat, user_id)

## Next step/s 🚧 🚧 🚧

- deploy, custom domain, https
- write tests
- create ci on gh actions

## To define 🤔

- IoT via API. create one or use free.
- create alarms between plant meta and pot iot -> pots hardcode statuses, and show status content and icon
- data visualization
