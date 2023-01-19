# # django-geoip-docker-poc
1. Ensure you have docker desktop installed.
2. Create empty `.env` file in project root folder.
3. Run `docker-compose up -d` to start your dev environment.
4. Run `docker-compose down` to stop your dev environment.

*Here's what's inside:*
* A Docker image demonstrating how to install the GeoIP C library that prevents GeoIP lookups from being fat and slow, and a copy of the GeoCityLite DB. You'll want to replace the DB with the latest.
* A requirements.txt that shows everything you need on the python side to run GeoIP and Django
* A copy of the GeoDjango GEOIP module in contrib.gis.geoip -- this is useful if you are running Django, don't want to use the base GEOIP python module and wire it up to Django, and don't need all of GeoDjango.
* A view in the Django app "geo_example" that accepts a parameter called “ip” which is a full IPv4 address, or looks at the HTTP_X_FORWARDED_FOR IP, or the IP address of the HTTP client in that order, and returns the geo information for that IP. The view also has some IP validation that should get refactored and encapsulated as its own function.
* A settings file in our “geo” project that sets 3 variables. GEOIP_PATH & GEOIP_CITY define the path and name of the file of where the GeoCityLite DB lives on this system used in contrib.gis.geoip. DEFAULT_IP is used in the view to keep things DRY.

Example Requests:
* http://localhost:8000/?ip=98.47.108.185 << passing in an IP as a parameter
* curl -H “X-Forwarded-For: 98.47.108.185” http://localhost:8000/ << a curl example that sets HTTP_X_FORWARDED_FOR
*  http://localhost:8000/ << uses the HTTP client ’s IP address. If you are running locally or behind a proxy, it’ll return whatever is set to default in the settings file (Leeds, ENG, GB is what comes out of the box with our example)