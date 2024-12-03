from django import forms

class MyInputForm(forms.Form):
    Given_input = forms.CharField( max_length=10000,min_length=100)