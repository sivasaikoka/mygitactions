from django import forms

class MyInputForm(forms.Form):
    Given_input = forms.CharField(label="Enter your text here:", max_length=10000)