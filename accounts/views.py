from django.shortcuts import render, redirect
from .models import PhoneOTP
from .forms import OTPForm, LoginForm
import random
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib.auth import get_user_model, login, logout, authenticate, login
User = get_user_model()


def register(request):
    form = OTPForm()
    return render(request, 'accounts/phone.html', {'form': form})


def send_otp_phone(phone, key):
    otp_key = key
    name = phone

    link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=YOUR_API_KEY&to={phone}&from=YOUR_TEMPLATE&templatename=YOUR_TEMPLATE_NAME&var1={name}&var2={otp_key}'

    #result = requests.get(link, verify=False)


def send_otp_this(request):
    phone = request.GET.get('phone')
    print(phone)
    phone_obj = User.objects.filter(username=phone)
    if phone_obj.exists():
        return JsonResponse({'send': False, 'taken': True})

    key = random.randint(999, 9999)
    print(key)

    phone_obj = PhoneOTP.objects.filter(phone=phone)
    if phone_obj.exists():
        phone_obj = phone_obj.first()
        count = phone_obj.count
        if count < 6:
            phone_obj.count = count + 1
            phone_obj.otp = key
            phone_obj.save()
            send_otp_phone(phone, key)
            return JsonResponse({'send': True})

        else:
            return JsonResponse({'send': False})
    else:

        PhoneOTP.objects.create(
            phone=phone,
            otp=key,
            count=1
        )
        send_otp_phone(phone, key)
        return JsonResponse({'send': True})


def otp_match(request):
    phone = request.GET.get('phone')
    otp_user = request.GET.get('otp')
    print(phone, otp_user)
    if phone and otp_user:
        phone_obj = PhoneOTP.objects.filter(phone=phone)
        if phone_obj.exists():
            phone_obj = phone_obj.first()
            otp_actual = phone_obj.otp
            if int(otp_actual) == int(otp_user):
                return JsonResponse({'match': True})
            else:
                return JsonResponse({'match': False})
        else:
            return JsonResponse({'match': False, 'msg': True})
    else:
        return JsonResponse({'match': False, 'msg': True})


def create(request):
    phone = request.GET.get('phone')
    password = request.GET.get('pass')
    if phone and password:
        user = User.objects.create_user(
            username=phone,
            password=password
        )
        login(request, user)
        return JsonResponse({'create': True})
    else:
        return JsonResponse({'create': False})


def logout_view(request):
    logout(request)
    return redirect('post-show')


def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username', None)
            password = form.cleaned_data.get('password', None)
            if username and password:
                user_obj = authenticate(
                    request, username=username, password=password)
                if user_obj is not None:
                    login(request, user_obj)
                    return redirect('post-show')

    return render(request, 'accounts/login.html', {'form': form})
