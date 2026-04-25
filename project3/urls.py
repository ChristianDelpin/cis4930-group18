"""
URL configuration for project2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    0. Add an import:  from my_app import views
    1. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    0. Add an import:  from other_app.views import Home
    1. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    0. Import the include() function: from django.urls import include, path
    1. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from pathlib import Path
from . import views

BASE_DIR = Path(__file__).resolve().parent.parent

urlpatterns = [
    path('admin/', admin.site.urls), # can delete later
    path('', views.home, name='home'),
    path('project0/', views.project1, name='project1'),
    re_path(r'^project0/figures/(?P<path>.*)$', serve, {'document_root': BASE_DIR / 'project1' / 'figures'}),

    path('currency_list/', views.CurrencyListView.as_view(), name='currency-list'),
    path('currency/<str:code>/', views.currency_countries, name='currency-countries'),
    path('country_list/', views.CountryListView.as_view(), name='country-list'),
    #adding the extra credit search bar
    path("search/", views.search, name="search")   
]
