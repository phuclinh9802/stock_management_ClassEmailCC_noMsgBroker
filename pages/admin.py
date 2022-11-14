from django.contrib import admin

# Register your models here.
from .models import Profile, Stock, Threshold, WatchList, StockNew


admin.site.register(Profile)
admin.site.register(Stock)
admin.site.register(Threshold)
admin.site.register(WatchList)
admin.site.register(StockNew)