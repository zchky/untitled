from django import forms
from .models import Post,MyModel
#forms.py
from markdownx.fields import MarkdownxFormField

class MyForm(forms.Form):
    myfield = MarkdownxFormField()

class PostForm(forms.ModelForm):
    class Meta:
        model= Post
        fields=('title','Archive','markdown')


class UploadFileForm(forms.Form):
    # title=forms.CharField(max_length=50)
    file=forms.FileField()

class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))