from django.db import models
from django.utils import timezone
# Create your models here.

class testdata(models.Model):
    time=models.TimeField()
    data=models.IntegerField()

    def __unicode__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.time+self.data

class test1(models.Model):
    test_1=models.ForeignKey(testdata)
    name=models.CharField(max_length=30,default='NA')

    # def a(self):
    #     return self.test_1.data

class test2(models.Model):
    test_2=models.ForeignKey(test1)
