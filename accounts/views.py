from django.shortcuts import render, redirect
from .models import PhoneOTP
from .forms import OTPForm
import random
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def validate_phone(request):
    phone = request.GET.get('phone', None)
    data = {
        'is_taken': False
    }
    data['phone'] = phone,
    print('working')

    if data['is_taken']:
        data['error_message'] = 'This Phone Number already exists.',
    else:
        request.session['phone'] = phone
        send_activation(request, phone)

    return redirect('accounts:check-otp')


@csrf_exempt
def register_new(request):
    # if request.user.is_authenticated:
    #     return redirect('account:profile')
    form = OTPForm()
    return render(request, 'accounts/phone.html', {'form': form})


@csrf_exempt
def send_activation(request, phone):
    phone = request.session.get('phone', '6666')
    key = random.randint(1, 999999)
    previous = PhoneOTP.objects.filter(phone=phone)
    if previous.exists():
        previous.first().delete()

    PhoneOTP.objects.create(
        phone=phone,
        otp=key
    )
    print('step 1')
    request.session['key'] = key

    phone = str(phone)
    key = str(key)
    # link = 'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=26183928-e9fe-11e7-a328-0200cd936042&to=' + \
    #     phone+'&from=HTadka&templatename=Firstlogin&var1='+key
    print(key)
    # result = requests.get(link)
    # end = len(result.text)
    # return result.ok
    return True


@csrf_exempt
def send_otp(request):

    if request.method == 'POST':
        token = 0
        phone = request.session.get('phone', '6666')
        otp_given_ = PhoneOTP.objects.filter(phone=phone)
        print(otp_given_)
        if otp_given_.exists():
            otp_given = otp_given_.first()
            token = otp_given.match
        print(token)
        form = PhoneOTP(request.POST or None)
        if form.is_valid():
            if token == 1:
                print('here token is 0ne')
                return redirect('account:set-password')
        else:
            if token:
                del request.session['token']
            return redirect('account:register')
    else:
        form = PhoneOTP()
    return render(request, 'accounts/phone.html', {'form': form})


@csrf_exempt
def validate_otp(request):
    phone = request.session.get('phone', '6666')
    otp = int(request.GET.get('otp', None))
    otp_given_ = PhoneOTP.objects.filter(phone=phone)
    if otp_given_.exists():
        otp_given = otp_given_.first().otp

    data = {
        'matches': False
    }
    if otp == otp_given:
        otp_given_ = PhoneOTP.objects.filter(phone=phone)
        if otp_given_.exists():
            otp_given = otp_given_.first()
            otp_given.match = 1
            otp_given.save()
            print('saved 2', otp_given)
        data = {
            'matches': True
        }
    if not data['matches']:
        data['error_message'] = 'This otp is not valid.',
    print(data)
    return JsonResponse(data)
