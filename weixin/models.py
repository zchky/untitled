from django.db import models

from django.utils.timezone import datetime
# Create your models here.
# now = datetime.datetime.utcnow().replace(tzinfo=Hongkong)
import django.utils.timezone

class test_device(models.Model):
    device_id=models.CharField(max_length=30)


    def __str__(self):
        return self.device_id

class test_user(models.Model):
    user=models.CharField(max_length=30)
    user_device_id=models.ManyToManyField(test_device)

    def device(self):
        return "\n".join([p.device_id for p in self.user_device_id.all()])

    # def device_id(self):
    #     return self.user_device_id.device_id()

    def __str__(self):
        return self.user

class test_data(models.Model):
    data_device_id=models.ForeignKey('test_user')
    temperature=models.IntegerField(default=0)
    humidity=models.IntegerField(default=0)
    smoke=models.FloatField(default=0)
    gas=models.FloatField(default=0)
    data=models.DateTimeField(default=django.utils.timezone.now)


    def device(self):
        return self.data_device_id.device()

    def user(self):
        return self.data_device_id.user

# class test_data(models.Model):
#     user = models.CharField(max_length=30)
#     temperature=models.IntegerField(default=0)
#     humidity=models.IntegerField(default=0)
#     smoke=models.FloatField(default=0)
#     burnable_gas=models.FloatField(default=0)
#     data=models.DateTimeField(default=django.utils.timezone.now)
#
#     def __str__(self):
#         return self.user