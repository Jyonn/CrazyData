"""CrazyData URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from SmartDjango import Analyse
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path, include
from django.views.generic import RedirectView


@Analyse.r()
def view_handler(r):
    return render(r, 'index.html')


def wx_view(*args):
    return HttpResponse('4388663213378584851')


urlpatterns = [
    path('v1', include('CrazyData.api_urls')),
    path('hall/<path:pid>', view_handler),
    path('tencent12290086912027340533.txt', wx_view),
]
