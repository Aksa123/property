from django.contrib import admin
from django.urls import path, include
from . import views
from . import views_class
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('test/', views.test, name='test'),
    path('about/', views_class.About.as_view(), name='about'),
    path('contact-us/', views_class.ContactUs.as_view(), name='contact-us'),

    # Admin start
    path('admin/', views.admin, name='admin'),
    path('admin/user/', views.admin_user, name='admin_user'),
    path('admin/user/add/', views.admin_add_user, name='admin_add_user'),
    path('admin/user/edit/<int:id>/', views.admin_edit_user, name='admin_edit_user'),
    path('admin/categories/', views.admin_category, name='admin_category'),
    path('admin/categories/add/', views.admin_add_category, name='admin_add_category'),
    path('admin/categories/edit/<int:id>/', views.admin_edit_category, name='admin_edit_category'),
    path('admin/status/', views.admin_status, name='admin_status'),
    path('admin/status/add/', views.admin_add_status, name='admin_add_status'),
    path('admin/status/edit/<int:id>/', views.admin_edit_status, name='admin_edit_status'),
    path('admin/cities/', views.admin_city, name='admin_city'),
    path('admin/cities/add/', views.admin_add_city, name='admin_add_city'),
    path('admin/cities/edit/<int:id>/', views.admin_edit_city, name='admin_edit_city'),
    path('admin/properties/', views.admin_property, name='admin_property'),
    path('admin/properties/add/', views.admin_add_property, name='admin_add_property'),
    path('admin/properties/edit/<int:id>/', views.admin_edit_property, name='admin_edit_property'),
    path('admin/delete_item/', views.admin_delete_item, name='admin_delete_item'),
    path('admin/blog/', views.admin_blog, name='admin_blog'),
    path('admin/blog/add/', views.admin_add_blog, name='admin_add_blog'),
    path('admin/blog/edit/<int:id>/', views.admin_edit_blog, name='admin_edit_blog'),
    path('admin/review/', views.admin_review, name='admin_review'),
    path('admin/review/add/', views.admin_add_review, name='admin_add_review'),
    path('admin/review/edit/<int:id>/', views.admin_edit_review, name='admin_edit_review'),
    path('admin/about/', views.admin_about, name='admin_about'),
    path('admin/about/add/', views.admin_add_about, name='admin_add_about'),
    path('admin/about/edit/<int:id>/', views.admin_edit_about, name='admin_edit_about'),
    # Admin end

    path('login/', views_class.Login.as_view(), name='user_login'),
    path('logout/', views_class.Logout.as_view(), name='user_logout'),
    path('register/', views_class.Register.as_view(), name='user_register'),

    path('', views.home, name='home'),
    path('property/<int:id>/', views.property_detail, name='property_detail'),
    path('browse', views.browse, name='browse'),
    path('browse/page/<int:page>/', views.browse, name='browse'),
    path('browse2', views.browse2, name='browse2'),
    path('browse/city/<int:city_id>-<str:city_name>/page/<int:page>/', views.browse_city, name='browse_city'),
    path('browse/category/<int:category_id>-<str:category_name>/page/<int:page>/', views.browse_category, name='browse_category'),
    path('browse/search/', views.browse_search, name='browse_search'),
    path('browse/search/<str:search>=<str:text>/<int:page>/', views.browse_search_result, name='browse_search_result'),

    path('blogs/', views.blog, name='blog'),
    path('blogs/<int:page>/', views.blog, name='blog'),
    path('blogs/detail/<int:id>/', views.blog_detail, name='blog_detail'),
    path('blogs/comment/', views.comment, name='comment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
