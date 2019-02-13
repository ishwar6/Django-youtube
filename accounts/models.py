from django.db import models
from django.core.validators import RegexValidator


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone = models.CharField(
        validators=[phone_regex], max_length=17, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of otp sent')
    logged = models.BooleanField(
        default=False, help_text='If otp verification got successful')
    forgot = models.BooleanField(
        default=False, help_text='only true for forgot password')
    forgot_logged = models.BooleanField(
        default=False, help_text='Only true if validdate otp forgot get successful')

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)
