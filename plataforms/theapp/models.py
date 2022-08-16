from cgitb import text
from re import T
from django.db import models

# Create your models here.

class Universe(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Group(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=64, blank=True)
    username = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField()
    description = models.CharField(max_length=64, blank=True)
    location = models.CharField(max_length=64, blank=True, null=True)
    pinned_tweet_id = models.BigIntegerField(blank=True, null=True)
    profile_image_url = models.CharField(max_length=64, blank=True)
    url = models.CharField(max_length=64, blank=True)
    verified = models.BooleanField()
    universe = models.ForeignKey(Universe, on_delete=models.DO_NOTHING, blank=True, related_name="universes")
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, blank=True, related_name="groups")
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, related_name="categories")
    
    def __str__(self):
        return f"{self.name} {self.username} {self.universe} {self.group} {self.category}"
class Tweet(models.Model):
    tweet_id=models.BigIntegerField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    created_at = models.DateTimeField()
    text = models.CharField(max_length=280)
    like_count = models.IntegerField()
    retweet_count = models.IntegerField()
    reply_count = models.IntegerField()
    quote_count = models.IntegerField()
    social_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.author} says: {self.created_at} {self.text}: Likes: {self.like_count} | Retweets: {self.retweet_count} | Replies: {self.reply_count} | Quotes: {self.quote_count}"