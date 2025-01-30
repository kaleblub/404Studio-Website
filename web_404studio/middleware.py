from django.conf import settings
from django.utils import translation
from django.contrib.gis.geoip2 import GeoIP2

class LocationBasedLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = self.get_client_ip(request)
        country = self.get_user_country(ip_address)

        print(f"Detected IP: {ip_address}, Country: {country}")

        if country in ['Ecuador', 'Mexico', 'Spain']:
            translation.activate('es')
        else:
            translation.activate('en')

        request.session[settings.LANGUAGE_SESSION_KEY] = translation.get_language()

        response = self.get_response(request)
        translation.deactivate()
        return response

    def get_client_ip(self, request):
        """Extracts the client IP address from the request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_user_country(self, ip_address):
        """Uses Django's GeoIP2 to determine the country of the given IP"""
        try:
            g = GeoIP2()
            return g.country(ip_address)['country_name']
        except Exception as e:
            print(f"GeoIP lookup failed: {e}")
            return "Unknown"