from django.contrib import admin
from django.urls import path, include

from main import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.home, name='home'),
    path('portfolio/', main_views.portfolio, name='portfolio'),
    path('development_packages/', main_views.development_packages, name='development_packages'),
    path('hosting_plans/', main_views.hosting_plans, name='hosting_plans'),
    path('contact/', main_views.contact, name='contact'),
    path('links/', main_views.links, name='links'),
]
