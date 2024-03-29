# pyplants

## Scrapper ✅

- [Tropicopia](http://www.tropicopia.com/house-plant/) contains rich metadata for over 350 house plants
- Using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) we fetch all the meta + image url, and save inside the json file locally
- access [tropicopia - plant](http://www.tropicopia.com/house-plant/detail.np/detail-01.html) to review the available metadata
- support for history. each scrape saved in unique file

## Endpoint data from ip ✅

- get local data from ip: city, country, longitude, latitude using `ipapi`
- user can hardcode location by city, or lon/lat, so that weather can be fetched correctly for his plants location

## Weather ✅

- current weather and pollution from `OpenWeatherMap API`
- data fetched by geolocation from IP (Endpoint data from ip) or by hardcoded city name

## GUI ✅

- `Flask`, `jinja2`, `FlaskForm`, `Pillow`, `json2table`
- `bootstrap`, `html`, `css`
- navbar, layout, login, register
- error pages (404, 403, 500)

### Pots ✅

- responsive home page with add pot option, top nav bar, active user's pots with image, status and location
- pagination, hardcoded to 6 per page

### Pot ✅

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
- you can see full plants scrap in UI, it will just pretty print last scrapped json file

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

### IoT and Data generator

- dummy IoT generator: temp, humidity, pH and salt levels
- option for careless owner, will generate more reading outside the "green" scope
- data visualization: chart + table, will show errors for readings outside the "green" scope
- there is no embedded dummy generator CTA in UI, you need to refresh to pot profile page to regenerate IoT data

### PyPlant Status

- we use different status id to rise a error/status icons
- since dummy data will regenerate on each pot profile page refresh, we don't show status on home page
- status icons are hosted in pyplant/static/status_icon
- here are all statuses:

| Status Id | Status                    |
| --------- | ------------------------- |
| 0         | OK!                       |
| 1         | Temp low                  |
| 2         | Temp high                 |
| 3         | Moisture low              |
| 4         | Temp low + Moisture low   |
| 5         | Temp high + Moisture low  |
| 6         | Moisture high             |
| 7         | Temp low + Moisture high  |
| 8         | Temp high + Moisture high |

---

## IoT API microservice

- IoT is standalone microservice. (here)[https://github.com/tzPyAl/iot-be-pyplant]
- not used in project though, IoT data is generated by custom dummy generator

## Next step/s 🚧 🚧 🚧

that's all folks!
