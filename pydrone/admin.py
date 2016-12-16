from django.contrib import admin
from .models import testdata
# Register your models here.
class testdataadmin(admin.ModelAdmin):
    list_display = ('time','data')

admin.site.register(testdata,testdataadmin)