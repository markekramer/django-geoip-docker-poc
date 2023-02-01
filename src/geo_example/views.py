import ipaddress

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

from contrib.gis.geoip2 import GeoIP2
from contrib.gis.geoip2.resources import City

# Create your views here.

def _get_default_city_obj():
	#set the fallback location from settings in case all heck breaks loose, so we can ALWAYS target the user to SOMEWHERE and make a sale
	default_region = settings.DEFAULT_REGION
	default_country_iso = settings.DEFAULT_COUNTRY_ISO

	#make a mock GEOIP DB query response with our defaults b/c if anything fails we don't want to go to the db again or do some default IP fuckery b/c that'll break for unknown reasons in the future b/c it will be controlled from outside our system
	defaults = { 'country_code': default_country_iso, 'region': default_region }

	return defaults


def index(request):

	#instantiate GeoIP
	g = GeoIP2()

	default_city_obj = _get_default_city_obj()

	#Grab the requestor's IP address -- X_FORWARED_FOR gets priority b/c it'd explictly set on the request
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		http_request_ip = x_forwarded_for.split(',')[0]
	else:
		http_request_ip = request.META.get('REMOTE_ADDR')

	#if the url contains an "ip" parameter, use that. Otherwise fallback to the IP from the request headers
	ip = request.GET.get("ip", http_request_ip)

	#private IPs aren't going to work, so no 192.168 or 10.XX or 172.16-32 ranges -- if running locally or behind a proxy you will not see a public IP address, which is required for geolocation
	try:
		if ipaddress.ip_address(ip).is_private:
			geo_cities = default_city_obj
		else:
			#gotta wrap this in a try except bc if the IP is not in the GeoIP database, it throws an exception
			try:
				geo_cities = g.city(ip)
			except:
				geo_cities = default_city_obj
	except:
		geo_cities = default_city_obj # if a garbage IP address was passed in, just use our default

	

	geolocation = f"IP Address: {ip} | Location: {geo_cities['region']}, {geo_cities['country_code']}"

	return HttpResponse(geolocation)