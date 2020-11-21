from django.contrib import admin
from .models import User, categories, auction_listing, pro_bid, watchlist, comments

# Register your models here.

admin.site.register(User)

admin.site.register(categories)

admin.site.register(auction_listing)

admin.site.register(pro_bid)   

admin.site.register(watchlist)

admin.site.register(comments)