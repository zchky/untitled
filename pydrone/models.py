from django.db import models
from django.utils import timezone
# Create your models here.

class testdata(models.Model):
    time=models.TimeField()
    data=models.IntegerField()

    def __unicode__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.time+self.data

