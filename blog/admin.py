from django.contrib import admin
from .models import Post,MyModel_text,Archive
# Register your models here.

admin.site.register(Post)
admin.site.register(MyModel_text)
admin.site.register(Archive)