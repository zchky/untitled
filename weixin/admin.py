from django.contrib import admin
# from .models import test_data,test_device,test_user
# Register your models here.
from .models  import data,user,device,UserAndDevice


class test_user_dis(admin.ModelAdmin):
    list_display = ['UAD_user','UAD_device_id']

class test_data_dis(admin.ModelAdmin):
    list_display = ['device','temperature','humidity']



admin.site.register(device)
admin.site.register(user)
admin.site.register(UserAndDevice,test_user_dis)
admin.site.register(data,test_data_dis)