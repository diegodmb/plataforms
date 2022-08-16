#from telnetlib import theNULL
#from itertools import groupby
#from xmlrpc.client import _HostType

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import tweepy
import csv
from .models import User, Tweet, Universe, Category, Group
from django.db.models import Sum, Count, Max, Min
import json
from datetime import datetime, date, timedelta
# Create your views here.


    
def index(request):
    uni = Universe.objects.get(name='Sports')
    data=Tweet.objects.filter(author__universe=uni).aggregate(cant=Count('tweet_id'), likes=Sum('like_count'), 
        retweets=Sum('retweet_count'), reply=Sum('reply_count'), quotes=Sum('quote_count'), 
        sv=Sum('social_value') )

    context = {}
    context['data']= data
    return render(request, "index.html", context)

def universe(request, uni):
    #client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAPuHdAEAAAAAo4K7xznaF3T9jvlr6zOsrywol4o%3DbpIDYVl7v1qhpJ5YjFCvCz4pGXjcjpYuJkXm1QwV0aYRKnYJPW')
    uni = Universe.objects.get(name=uni)
    context = {}
    #Universe
    context['uni']= uni
    #Data General
    data=Tweet.objects.filter(author__universe=uni).aggregate(cant=Count('tweet_id'), likes=Sum('like_count'), 
        retweets=Sum('retweet_count'), reply=Sum('reply_count'), quotes=Sum('quote_count'), sv=Sum('social_value') )
    context['data']= data
    #Grupos  General
    data=Tweet.objects.filter(author__universe=uni).values('author__group__name').annotate(cant=Count('tweet_id'), likes=Sum('like_count'), 
        retweets=Sum('retweet_count'), reply=Sum('reply_count'), quotes=Sum('quote_count'), sv=Sum('social_value')).order_by('-sv')
    context['groups']= data
    # Users Rank
    data=Tweet.objects.filter(author__universe=uni).values('author__group__name', 'author__category__name',
        'author__profile_image_url', 'author__name', 'author__username').annotate(cant=Count('tweet_id'), likes=Sum('like_count'), 
        retweets=Sum('retweet_count'), reply=Sum('reply_count'), quotes=Sum('quote_count'), sv=Sum('social_value')).order_by('-sv')
    
    context['users']= data

    return render(request, "universe.html", context)

def filter(request):
    data = json.load(request)['data']
    fecha = datetime.today()
    universo = data['universo']
    periodo = data['periodo']
    category = data['informe']

    context = {}
    #Universe
    context['uni']= uni


    uni = Universe.objects.get(name=universo)
    
    if periodo == 'hoy':
        ini = fecha
    elif periodo == 'semana':
        s = fecha - timedelta(days=fecha.weekday())
        sem = s.date()
        ini = sem


    #Data General
    data=Tweet.objects.filter(author__universe=uni).aggregate(cant=Count('tweet_id'), likes=Sum('like_count'), 
        retweets=Sum('retweet_count'), reply=Sum('reply_count'), quotes=Sum('quote_count'), sv=Sum('social_value') )
    context['data']= data
    #Grupos  General
    data=Tweet.objects.filter(author__universe=uni).values('author__group__name').annotate(cant=Count('tweet_id'), likes=Sum('like_count'), 
        retweets=Sum('retweet_count'), reply=Sum('reply_count'), quotes=Sum('quote_count'), sv=Sum('social_value')).order_by('-sv')
    context['groups']= data
    # Users Rank
    data=Tweet.objects.filter(author__universe=uni).values('author__group__name', 'author__category__name',
        'author__profile_image_url', 'author__name', 'author__username').annotate(cant=Count('tweet_id'), likes=Sum('like_count'), 
        retweets=Sum('retweet_count'), reply=Sum('reply_count'), quotes=Sum('quote_count'), sv=Sum('social_value')).order_by('-sv')
    context['users']= data
    return JsonResponse(context, safe=False) 

def update(request):
    client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAPuHdAEAAAAAo4K7xznaF3T9jvlr6zOsrywol4o%3DbpIDYVl7v1qhpJ5YjFCvCz4pGXjcjpYuJkXm1QwV0aYRKnYJPW')
    file = open('C:\\Users\\diego\Documents\\Dev\\pltfrms\\plataforms\\plataforms\\theapp\\db.csv', encoding='utf-8-sig')
    reader = csv.reader(file)
    username=[]
    group=[]
    category = []
    universe=[]
    for row in reader:
        username.append(row[1])
        group.append(row[3])
        category.append(row[4])
        universe.append(row[2])

    usrnmstr=str(username).replace(" ","").replace("'", "").replace("'", "")
    usrnmstr=usrnmstr[1:-1]
    response = client.get_users(usernames=usrnmstr, user_fields=["profile_image_url", "created_at", "description","location","pinned_tweet_id",
        "url","verified"])
    for user in response.data:
        count=0
        for usn in username:
            if usn == user.username:
                grupo = Group.objects.get_or_create(name=group[count])
                grupo=Group.objects.get(name=group[count])
                cat = Category.objects.get_or_create(name=category[count])
                cat = Category.objects.get(name=category[count])
                uni = Universe.objects.get_or_create(name=universe[count])
                uni = Universe.objects.get(name=universe[count])
                break
            count +=1

        updated_values = {"name": user.name, "username": user.username, "created_at": user.created_at, "description": user.description, "pinned_tweet_id": user.pinned_tweet_id, 
            "profile_image_url": user.profile_image_url, "url": user.url, 
            "verified": user.verified, "location": user.location, "universe": uni, "group": grupo, "category": cat}
        obj, created = User.objects.update_or_create(user_id=user.id, defaults=updated_values)
        
        query = 'from:'+usn +' -is:retweet'
        print(query)
        tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at', 'public_metrics', 'attachments', 'geo'], 
        user_fields=['profile_image_url'], expansions=['author_id'] ,max_results=100)        
        if tweets.data is not None:
            for tweet in tweets.data:
                author=User.objects.get(user_id=tweet.author_id)
                print(tweet.text)
                sv = tweet.public_metrics['like_count'] + tweet.public_metrics['reply_count']*2+tweet.public_metrics['retweet_count']*2.5+tweet.public_metrics['quote_count']*3
                tw_updated_values = {"author": author, "created_at": tweet.created_at, "text": tweet.text, 
                    "like_count": tweet.public_metrics['like_count'], "retweet_count": tweet.public_metrics['retweet_count'], 
                    "reply_count": tweet.public_metrics['reply_count'], "quote_count": tweet.public_metrics['quote_count'],
                    "social_value": sv}
                obj, created = Tweet.objects.update_or_create(tweet_id=tweet.id, defaults=tw_updated_values)
        #http= "<p>"+user.name+" | " +uni.name+" | " +cat.name+" | " +grupo.name +" | ACTUALIZADO<p>"
        #return HttpResponse(http)
    context = {}
    context['usr']=response.data
    context['tweets']=tweets.data
    return render(request, "update.html", context)