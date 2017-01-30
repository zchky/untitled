from django.contrib import admin
# from .models import test_data,test_device,test_user
# Register your models here.
from .models  import test_data,test_device,test_user

class test_devices_dis(admin.ModelAdmin):
    list_display = ('device_id',)

class test_user_dis(admin.ModelAdmin):
    list_display = ['device','user']

class test_data_dis(admin.ModelAdmin):
    list_display = ['device','user','temperature','humidity']



admin.site.register(test_device)
admin.site.register(test_user,test_user_dis)
admin.site.register(test_data,test_data_dis)