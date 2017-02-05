from django.contrib import admin
from .models import testdata
from .models import test1,test2
# Register your models here.
class testdataadmin(admin.ModelAdmin):
    list_display = ('time','data')

class testdataadmin1(admin.ModelAdmin):
    list_display = ['test_1','name']
    # def b(self,obj):
    #     return obj.test_1

admin.site.register(testdata,testdataadmin)
admin.site.register(test1,testdataadmin1)
admin.site.register(test2)