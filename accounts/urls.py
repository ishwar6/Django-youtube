from django.conf.urls import url, include
from .views import (
    send_otp_this, otp_match, register, create
)

app_name = 'accounts'
urlpatterns = [
    url(r'^start/$', register, name='register'),

    url(r'^ajax/new/$', send_otp_this, name='new'),

    url(r'^ajax/match/$', otp_match, name='match'),
    url(r'^ajax/create/$', create, name='create'),
    # url(r'^ajax/validate_otp/reset/$',
    #     validate_otp_reset, name='validate-otp-reset'),
    # url(r'^ajax/validate_phone/reset/$',
    #     validate_phone_reset, name='validate-phone-reset'),


]
