from django.http import request, HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from .models import UserProfile

class LoginRoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.admin_permission = ['admin', 'admin_user', 'admin_add_user', 'admin_edit_user', 'admin_category', 'admin_add_category', 'admin_edit_category', 'admin_status', 'admin_add_status', 'admin_edit_status', 'admin_city', 'admin_add_city', 'admin_edit_city', 'admin_property', 'admin_add_property', 'admin_edit_property', 'admin_delete_item', 'admin_blog', 'admin_add_blog', 'admin_edit_blog', 'admin_review', 'admin_add_review', 'admin_edit_review', 'admin_about', 'admin_add_about', 'admin_edit_about']
        self.owner_permission = ['admin', 'admin_property', 'admin_add_property', 'admin_edit_property', 'admin_user', 'admin_edit_user', 'admin_delete_item', 'admin_review', 'admin_add_review', 'admin_edit_review']
        self.user_permission = ['admin', 'admin_user', 'admin_edit_user', 'admin_delete_item', 'admin_review', 'admin_add_review', 'admin_edit_review']

    def process_view(self, request, view, args, kwargs):
        path = resolve(request.path).url_name
        if path is not None and path[:5] == 'admin':
            if request.user.is_authenticated:
                user_id = request.user.id
                role = UserProfile.objects.get(user_id=user_id).role
                if path in self.admin_permission and role == 'admin':
                    kwargs['role'] = role
                    return None
                elif path in self.owner_permission and role == 'owner':
                    kwargs['role'] = role
                    kwargs['user_id'] = user_id
                    return None
                elif path in self.user_permission and role == 'user':
                    kwargs['role'] = role
                    kwargs['user_id'] = user_id
                    return None
                else:
                    return HttpResponse("Wrong role!")
            else:
                return HttpResponseRedirect(reverse('user_login'))


    def __call__(self, request):
        # Code before the view is called.

        response = self.get_response(request)
        # Code after the view is called.
        
        
       
        return response




class test:
    def __init__(self, get_response):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs ):
        view_kwargs['name'] =  'pratyaksa'        # give parameter to view !!!
        view_kwargs['view_name'] = view_func.__name__
        return None

    def __call__(self, request):
        # Code before the view is called.
        response = self.get_response(request)
        # Code after the view is called.
       
        return response