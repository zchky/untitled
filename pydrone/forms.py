from django import forms


class AddForm(forms.Form):
    a = forms.TimeField(required=False)
    b = forms.TimeField(required=False)