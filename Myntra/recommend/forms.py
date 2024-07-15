from django import forms

class SizeForm(forms.Form):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    chest = forms.FloatField(required=False)
    waist = forms.FloatField(required=False)
    hips = forms.FloatField(required=False)
    height_shoulder = forms.FloatField(required=False)
    height_hips = forms.FloatField(required=False)
