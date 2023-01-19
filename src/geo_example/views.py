import ipaddress

from django.shortcuts import render
from django.http import HttpResponse

from contrib.gis.geoip2 import GeoIP2



# Create your views here.
def index(request):

	#instantiate GeoIP
	g = GeoIP2()

	#this should be moved to the SETTINGS file
	default_ip_location = '86.19.240.14' #defaulting it to a rando Leeds UK IP adresss -- it's what we use arbtitratilly in our product  
	
	#Grab the requestor's IP address -- X_FORWARED_FOR gets priority b/c it'd explictly set on the request
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		http_request_ip = x_forwarded_for.split(',')[0]
	else:
		http_request_ip = request.META.get('REMOTE_ADDR')

	#if the url contains an "ip" parameter, use that. Otherwise fallback to the IP from the request headers
	ip = request.GET.get("ip", http_request_ip)

	#private IPs aren't going to work so no 192.168 or 10.XX or 172.16-32 ranges -- if running locally or behind a proxy you will not see a public IP address, which is required for geolocation
	try:
		if ipaddress.ip_address(ip).is_private:
			ip = default_ip_location
	except:
		ip = default_ip_location # if a garbage IP address was passed in, just use our default

	#gotta wrap this in a try except bc if the IP is not in the GeoIP database, it throws an exception
	try:
		geo_cities = g.city(ip)
	except:
		geo_cities = g.city(default_ip_location)

	geolocation = f"IP Address: {ip} | Location: {geo_cities['city']}, {geo_cities['region']}, {geo_cities['country_code']}"

	return HttpResponse(geolocation)