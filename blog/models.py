from django.db import models
from django.utils import timezone
from markdownx.models import MarkdownxField

class MyModel(models.Model):

    myfield = MarkdownxField()

class MyModel_text(models.Model):
    mytext=models.TextField()

class Archive(models.Model):
    Archive_name=models.CharField(max_length=40,default="others")

    def __str__(self):
        return self.Archive_name

# Create your models here.
class Post(models.Model):
    author=models.ForeignKey('auth.User')
    Archive=models.ForeignKey(Archive)
    title=models.CharField(max_length=200)
    markdown=MarkdownxField()
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now)
    published_date=models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.publish_date=timezone.now()
        self.save()

    def __str__(self):
        return self.title

