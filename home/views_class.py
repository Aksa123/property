from django.http import request, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import ContactMail, UserProfile
from django.contrib.auth.models import User
from .forms import ContactMailForm, UserForm


class Register(View):
    template_name = 'home/register.html'
    form = UserForm
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        role = request.POST['role']
        password = request.POST['password']
        avatar = request.FILES['avatar']
        user = User.objects.filter(username=name) | User.objects.filter(email=email)
        if len(user) > 0:
            return HttpResponse("account already exist !")
        else:
            new_user = User.objects.create_user(username=name, email=email, password=password)
            new_profile = UserProfile(user=new_user, phone=phone, role=role, image=avatar)
            new_profile.save()
            return HttpResponseRedirect(reverse('home'))


class Login(View):
    template_name = 'home/login.html'
    def get(self, request):
        return render(request, 'home/login.html')
    def post(self, request):
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(username=name, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('admin_user'))
        else:
            return HttpResponse("Username & password don't match !?")

class Logout(View):
    template_name = 'home/login.html'
    def get(self, request):
        return HttpResponseRedirect(reverse('user_login'))
    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))


class About(View):
    template_name = 'home/about.html'
    def get(self, request):
        return render(self.request, self.template_name)

class ContactUs(View):
    template_name = 'home/contact.html'
    form = ContactMailForm
    def get(self, request):
        return render(request, self.template_name, context={"form":self.form()})
    def post(self, request):
        input_form = self.form(request.POST)
        if input_form.is_valid():
            name = input_form.cleaned_data['name']
            email = input_form.cleaned_data['email']
            content = input_form.cleaned_data['content']
            new_mail = ContactMail(name=name, email=email, content=content)
            new_mail.save()
            return JsonResponse({"status": "Your message has been submitted!"})
        else:
            return JsonResponse({"status": "FUCK! Something's wrong!"})

