"""
Definition of urls for stockmarketservice.
"""

from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import RedirectView
from app import forms, views
from rest_framework import routers

favicon_view = RedirectView.as_view(url='/static/app/favicon.ico', permanent=True)

urlpatterns = [
    path('app\favicon\.ico', favicon_view),
    path('',            views.home, name='home'),
    path('about/',      views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/',      LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/',       admin.site.urls),
    path('stockmarket/', views.DailyPricesView.as_view(), name='stockmarket'),
    path('signup/',      views.SignUpViewSet.as_view({'get': 'list'}), name='signup'),
    path('api-auth/',    include('rest_framework.urls', namespace='rest_framework'))
]
