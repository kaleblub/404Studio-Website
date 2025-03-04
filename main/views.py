from django.shortcuts import render, redirect
from django.urls import reverse

from django.utils import translation

def home(request):
    # Define US and Ecuador prices
    us_price = 100
    ec_price = 80
    language = request.COOKIES.get('django_language', 'en')
    translation.activate(language)
    print(translation.get_language())

    # Select price based on the location set in the session
    # if request.session.get('country') == 'US':
    #     price = us_price
    # else:
    #     price = ec_price

    # context = {
    #     'price': price,
    #     'currency': request.session.get('currency', 'USD'),
    # }
    return render(request, 'main/home.html')

def portfolio(request):
    return render(request, 'main/portfolio.html')

def contact(request):
    return render(request, 'main/contact.html')

def development_packages(request):
    return render(request, 'main/development_packages.html')

def hosting_plans(request):
    return render(request, 'main/hosting_plans.html')

def links(request):
    return render(request, 'main/links-page.html')

def set_language(request, language):
    print(f"Language selected: {language}")

    redirect_url = reverse('home')
	# print(f"Redirect to: {response.url}")

    response = redirect(redirect_url)
    response.set_cookie('django_language', language)
    return response