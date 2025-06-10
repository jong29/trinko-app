from django.urls import path
from . import views

app_name = 'etf_screener'

urlpatterns = [
    path('', views.etf_screener, name='etf_screener'),
]
