from django.contrib import admin

# Register your models here.
from .models import Universe, Group, Category, User, Tweet

admin.site.register(Universe)
admin.site.register(Group)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Tweet)