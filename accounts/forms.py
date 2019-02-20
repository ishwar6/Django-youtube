from django import forms


class OTPForm(forms.Form):
    phone = forms.IntegerField()
    otp = forms.IntegerField()
    password = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
