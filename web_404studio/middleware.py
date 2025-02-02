from django.conf import settings
from django.utils import translation
import urllib.request
import json

class LocationBasedLanguageMiddleware:
    def __init__(self, get_response):
        """Initialize middleware with the next response handler"""
        self.get_response = get_response  # Store get_response to call it later

    def __call__(self, request):
        """Process the request and set language based on user IP"""
        ip_address = self.get_client_ip(request)  # Extract IP address

        if not ip_address or ip_address == "127.0.0.1":
            print("Using default language for localhost.")
            country = "Unknown"
        else:
            country = self.get_user_country(ip_address)

        if country in ['Ecuador', 'Mexico', 'Spain']:
            translation.activate('es')
        else:
            translation.activate('en')

        print(f"Detected Country: {country}")
        print(f"Active Language: {translation.get_language()}")

        request.session[settings.LANGUAGE_SESSION_KEY] = translation.get_language()

        response = self.get_response(request)
        translation.deactivate()
        return response

    def get_client_ip(self, request):
        """Extracts the client IP address from request headers"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        print(f"Extracted IP: {ip}")  # Debugging output
        return ip

    def get_user_country(self, ip_address):
        """Fetches the user's country based on IP"""
        try:
            print(f"Fetching country for IP: {ip_address}")
            with urllib.request.urlopen(f"http://ip-api.com/json/{ip_address}") as url:
                data = json.loads(url.read().decode())
                return data.get("country", "Unknown")
        except Exception as e:
            print(f"GeoIP lookup failed: {e}")
            return "Unknown"