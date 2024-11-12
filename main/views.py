from django.shortcuts import render

def home(request):
    # Define US and Ecuador prices
    us_price = 100
    ec_price = 80

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

