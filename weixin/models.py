from django.db import models

from django.utils.timezone import datetime
# Create your models here.
# now = datetime.datetime.utcnow().replace(tzinfo=Hongkong)

class test_data(models.Model):
    user=models.CharField(max_length=30)
    temperature=models.IntegerField(default=0)
    humidity=models.IntegerField(default=0)
    data=models.DateTimeField(default=datetime.now())

def __str__(self):
    return self.user