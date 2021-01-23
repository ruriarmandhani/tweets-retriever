"""tweets_retriever URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from . import retriever
from . import key

BEARER_TOKEN = key.BEARER_TOKEN
# BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAHTVLwEAAAAA9uTM8wUyJ51%2F5Shl4jJKzrkmMy4%3D0PJnluGD2pPGSjU69WpsvDWIky6WMCpmicwaJKkrQZOu7kI7e4'

def tweets_view(request):
    # username = ['cnbcindonesia', 'KontanNews', 'Bisniscom','detikcom', 'detikfinance']
    username = ['cnbcindonesia','KontanNews', 'Bisniscom','detikcom', 'detikfinance']
    query = retriever.get_query(username, request.POST['input'])
    api_url = retriever.create_url(query)
    tweets = retriever.get_tweets(BEARER_TOKEN,api_url)
    embed_tweets = retriever.embed_tweets(tweets, BEARER_TOKEN)
    # tweets = "tes"
    data = {
        "embed_tweets":embed_tweets
    }
    # print(data)
    return render(request, 'tweets.html', data)

def index(request):
    return render(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('tweets/', tweets_view, name="tweets_view"),
]
