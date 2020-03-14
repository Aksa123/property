from django.http import request, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from .models import ContactMail
from .forms import ContactMailForm


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

