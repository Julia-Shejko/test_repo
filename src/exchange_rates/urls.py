from django.urls import path

from exchange_rates.api import convert

urlpatterns = [
    path("convert/", convert),
]
