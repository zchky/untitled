from django.db import models

from django.utils.timezone import datetime
# Create your models here.
# now = datetime.datetime.utcnow().replace(tzinfo=Hongkong)
import django.utils.timezone

class device(models.Model):
    device_id=models.CharField(max_length=30,unique=True)



    def __str__(self):
        return self.device_id

class user(models.Model):
    user=models.CharField(max_length=30,unique=True)

    def __str__(self):
        return self.user

class UserAndDevice(models.Model):
    UAD_user=models.ForeignKey(user)
    UAD_device_id=models.ForeignKey(device)

    # def device(self):
        # return "\n".join([p.device_id for p in self.user_device_id.all()])

    class Meta:
        unique_together = ('UAD_user', 'UAD_device_id',)

    # def device_id(self):
    #     return self.user_device_id.device_id()

    def __str__(self):
        return self.UAD_user.user

class data(models.Model):
    data_device_id=models.ForeignKey('device')
    temperature=models.IntegerField(default=0)
    humidity=models.IntegerField(default=0)
    smoke=models.FloatField(default=0)
    gas=models.FloatField(default=0)
    data=models.DateTimeField(default=django.utils.timezone.now)


    def device(self):
        return self.data_device_id.device_id


