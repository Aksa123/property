from django.contrib import admin
from .models import Category, Status, Property, Blog, Comment, City
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    def __str__(self):
        return self.name

class StatusAdmin(admin.ModelAdmin):
    def __str__(self):
        return self.name

class PropertyAdmin(SummernoteModelAdmin):
    def __str__(self):
        return self.name

class BlogAdmin(admin.ModelAdmin):
    def __str__(self):
        return self.title

class CommentAdmin(admin.ModelAdmin):
    pass

class CityAdmin(admin.ModelAdmin):
    def __str__(self):
        return self.name

admin.site.register(Category, CategoryAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(City, CityAdmin)