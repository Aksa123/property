from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.utils import timezone
from house.settings import STATICFILES_DIRS, MEDIA_URL

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    home_text = models.CharField(max_length=100, default="Add a simple text for homepage!")
    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    number_of_listing = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="city", blank=True, default=None)
    def __str__(self):
        return self.name
    def image_source(self):
        return self.image.name
    def absolute_url(self):
        return self.image.url
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    image = models.ImageField(upload_to="user", blank=True, default=None)
    role = models.CharField(max_length=10, default='user')
    def absolute_url(self):
        if self.image:
            return self.image.url
        else:
            return None

class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    address =  models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    area = models.PositiveIntegerField()
    garage = models.BooleanField(default=False)
    bathroom = models.PositiveIntegerField(default=0)
    bedroom = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    founded_date = models.DateField(default=timezone.now)
    description = models.TextField()
    avatar = models.ImageField(upload_to="property")
    google_map = models.TextField(blank=True, default=None)
    order = models.PositiveIntegerField(default=0, blank=True)
    featured = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    def absolute_url(self):
        return self.avatar.url
    def floor_map_source(self):
        return self.floor_map.path
    def listing_age(self):
        d1 = datetime.strptime(str(date.today()), "%Y-%m-%d")
        d2 = datetime.strptime(str(self.founded_date), "%Y-%m-%d")
        difference = abs((d2 - d1).days)
        return difference
    def founded_dateformat(self):
        return self.founded_date.strftime("%d %b, %Y")

class PropertyImage(models.Model):
    prop =  models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, default=None)
    image = models.ImageField(upload_to="property", blank=True, default=None)
    def __str__(self):
        return self.prop.name
    def absolute_url(self):
        return self.image.url

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='blog', blank=True, default=None)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    def absolute_url(self):
        return self.avatar.url

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    parent = models.PositiveIntegerField(default=0)
    main = models.PositiveIntegerField(default=0)
    def dateformat(self):
        return self.date.strftime("%d %b %Y, %H:%M")


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.TextField()
    career = models.CharField(max_length=50)
    star = models.PositiveIntegerField(default=5)
    def preview(self):
        return str(self.content[:20].strip() + "...")


class About(models.Model):
    about_us = models.TextField()
    our_quality = models.TextField()
    image = models.ImageField(upload_to="about")
    selected_review = models.ManyToManyField(Review)
    def preview(self):
        return str(self.about_us[:20].strip() + "...")


class ContactMail(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    content = models.TextField()