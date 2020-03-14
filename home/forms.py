from django import forms
from .models import City, Status, Category, Review
from django.utils import timezone
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class UserForm(forms.Form):
    role_options = [ ('admin','Admin'), ('user','User'), ('owner','Property Owner') ]
    name = forms.CharField(label='Your name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Phone number', max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(label="Role", choices=role_options, widget=forms.RadioSelect)
    image = forms.ImageField(label="Avatar", widget=forms.FileInput(attrs={'class': "form-control-file"}))


class UserEditForm(forms.Form):
    role_options = [ ('admin','Admin'), ('user','User'), ('owner','Property Owner') ]
    name = forms.CharField(label='Your name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Phone number', max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(label="Role", choices=role_options, widget=forms.RadioSelect)
    image = forms.ImageField(label="Avatar", widget=forms.FileInput(attrs={'class': "form-control-file"}))


class CategoryForm(forms.Form):
    name = forms.CharField(label="Category name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    home_text = forms.CharField(label="Home text", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

class StatusForm(forms.Form):
    name = forms.CharField(label="Category name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

class CityForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    number_of_listing = forms.IntegerField(label="Number of listings", min_value=0, max_value=1000, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(label="Image", widget=forms.FileInput(attrs={'class': "form-control-file"}))

class PropertyForm(forms.Form):
    city_options = []
    cities = City.objects.all()
    for c in cities:
        city_options.append((c.id, c.name))

    status_options = []
    status = Status.objects.all()
    for s in status:
        status_options.append((s.id, s.name))

    category_options = []
    categories = Category.objects.all()
    for cat in categories:
        category_options.append((cat.id, cat.name))

    boolean_options = [(True, "Yes"), (False, "No")]
    
    name = forms.CharField(label="Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(label="Avatar", widget=forms.FileInput(attrs={'class': "form-control-file"}))
    image = forms.ImageField(label="Images", widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': "form-control-file"}))
    address = forms.CharField(label="Address", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.ChoiceField(label="City", choices=city_options, widget=forms.Select(attrs={'class': 'form-control'}))
    price = forms.DecimalField(label="Price", min_value=0.00, max_value=100000.00, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(label="Status", choices=status_options, widget=forms.Select(attrs={'class': 'form-control'}))
    area = forms.IntegerField(label="Area", min_value=0, max_value=10000, widget=forms.NumberInput(attrs={'class': 'form-control', 'value': 36}))
    garage = forms.ChoiceField(label="Has a garage?", choices=boolean_options, widget=forms.RadioSelect(attrs={'checked': "checked"}))
    bathroom = forms.IntegerField(label="Bathrooms", min_value=0, max_value=10000, widget=forms.NumberInput(attrs={'class': 'form-control', 'value': 1}))
    bedroom = forms.IntegerField(label="Bedrooms", min_value=0, max_value=10000, widget=forms.NumberInput(attrs={'class': 'form-control', 'value': 1}))
    category = forms.ChoiceField(label="Category", choices=category_options, widget=forms.Select(attrs={'class': 'form-control'}))
    founded_date = forms.DateField(label="Founded date", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    description = forms.CharField(label="Description", widget=SummernoteWidget())
    google_map = forms.CharField(label="Google map", max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control', 'value': '-7.782889,110.3648873'}))
    featured = forms.ChoiceField(label="Featured", choices=boolean_options, widget=forms.RadioSelect(attrs={'checked': "checked"})) # ONLY the last option ("No") is checked by default


class BlogForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(label='Avatar', widget=forms.FileInput(attrs={'class': "form-control-file"}))
    content = forms.CharField(label="Content", widget=SummernoteWidget())


class ReviewForm(forms.Form):
    star = forms.IntegerField(label="Star", min_value=0, max_value=5, widget=forms.NumberInput(attrs={'class': 'form-control', 'value': 1}))
    content = forms.CharField(label="Write your review", widget=forms.Textarea(attrs={'class': 'form-control'}))
    career = forms.CharField(label="May we know your career position?", widget=forms.TextInput(attrs={'class': 'form-control'}))



class AboutForm(forms.Form):
    review_options = []
    reviews = Review.objects.all()
    for rev in reviews:
        review_options.append((rev.id, rev.preview()))

    about_us = forms.CharField(label="About us", widget=SummernoteWidget())
    image = forms.ImageField(label="Image", widget=forms.FileInput(attrs={'class': "form-control-file"}))
    our_quality = forms.CharField(label="Our quality", widget=SummernoteWidget())
    selected_review = forms.ChoiceField(label="Selected reviews", choices=review_options, widget=forms.Select(attrs={'class': 'form-control'}))
    

class ContactMailForm(forms.Form):
    name = forms.CharField(label="Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control", "required":""}))
    email = forms.EmailField(label="Email", max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "type": "email", "required":""}))
    content = forms.CharField(label="Message", widget=forms.Textarea(attrs={"class": "form-control", "required":""}))