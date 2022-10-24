from django.contrib import admin

# Register your models here.
from .models import Role, Profile, Users, Watch_List, Stock, Preference, Stocks_list, New, Threshold

admin.site.register(Role)
admin.site.register(Profile)
admin.site.register(Users)
admin.site.register(Watch_List)
admin.site.register(Stock)
admin.site.register(Preference)
admin.site.register(Stocks_list)
admin.site.register(New)
admin.site.register(Threshold)