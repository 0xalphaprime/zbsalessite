import os
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage, get_connection
from django.core import mail
from django.conf import settings
from django.contrib import auth
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator


# Create your views here.

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }


        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Password too short")
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(str(user.pk).encode())

                
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
                email_subject = "Activate Your Account"
                activate_url = "http://"+domain+link
                email_body = "Hi "+user.username+ "Please use this link to verify your account\n"+activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email, 'apaino@primesurgicalusa.com'],
                    reply_to=[settings.DEFAULT_FROM_EMAIL],
                )
                email.send(fail_silently=False)
                messages.success(request, "Account Successfully Created")
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')
        '''
        messages.success(request, "Success")
        messages.warning(request, "Warning")
        messages.info(request, "Info")
        messages.error(request, "Error")
        return render(request, "authentication/register.html")
        '''


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]

        if not validate_email(email):
            return JsonResponse({"email_error":"email is invalid"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error":"existing account with this email"}, status=409)
        return JsonResponse({"email_valid": True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]

        if not str(username).isalnum():
            return JsonResponse({"username_error":"username should only contain alphanumeric characters"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error":"username is taken. please select another."}, status=409)
        return JsonResponse({"username_valid": True})


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')