from django import forms


class OTPForm(forms.Form):
    phone = forms.IntegerField()
    otp = forms.IntegerField()
