from django.shortcuts import render
from django.urls import reverse
from django.http import request, HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Property, City, UserProfile, Category, Status, City, PropertyImage, Blog, Review, About, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import UserForm, CategoryForm, StatusForm, CityForm, PropertyForm, UserEditForm, BlogForm, ReviewForm, AboutForm
from django.utils.decorators import decorator_from_middleware, decorator_from_middleware_with_args
from .middleware import LoginRoleMiddleware
from django.core.paginator import Paginator
from django.core import serializers

# Create your views here.

def test(request):
    name = "default name"
    level = 0
    if "name" in request.GET and "level" in request.GET:
        name = request.GET['name']
        level = request.GET['level']
    return HttpResponse(str("name: " + name + ", level: " + str(level)))


def register(request):

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        role = request.POST['role']
        password = request.POST['password']
        avatar = request.FILES['avatar']
        user = User.objects.filter(username=name) | User.objects.filter(email=email)
        if len(user) > 0:
            return HttpResponse("account alrady exist !")
        else:
            new_user = User.objects.create_user(username=name, email=email, password=password)
            new_profile = UserProfile(user=new_user, phone=phone, role=role, image=avatar)
            new_profile.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        
        return render(request, 'home/register.html')



def user_login(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(username=name, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('admin_user'))
        else:
            return HttpResponse("Username & password don't match !?")
    else:
        return render(request, 'home/login.html')


def user_logout(request):
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('user_login'))


def admin(request, **kwargs):
    if request.user.is_authenticated:        
        return render(request, 'home/admin_home.html')
    else:
        # return HttpResponseRedirect(reverse('user_login'))
        return HttpResponse("not logged in")



def admin_user(request, **kwargs):
    if kwargs['role'] == 'admin':
        users = User.objects.all()
    else:
        user_id = kwargs['user_id']
        users = User.objects.filter(id=user_id)
    return render(request, 'home/admin_user.html', context={'users': users})


def admin_add_user(request, **kwargs):
    if request.method == "POST":
        input_form = UserForm(request.POST, request.FILES) # add request.FILES if contains files or images
        if input_form.is_valid():
            name = input_form.cleaned_data['name']
            phone = input_form.cleaned_data['phone']
            email = input_form.cleaned_data['email']
            password = input_form.cleaned_data['password']
            image = input_form.cleaned_data['image']
            role = input_form.cleaned_data['role']

            user = User.objects.create_user(username=name, email=email, password=password)
            profile = UserProfile(user=user, phone=phone, role=role, image=image)
            profile.save()
            return HttpResponseRedirect(reverse('admin_user'))
        else:
            return render(request, 'home/admin_user.html', context={
            'form': input_form
            })
    else:
        form = UserForm()
        title = "Create New User"
        url = 'admin_add_user'
        return render(request, 'home/admin_add_item.html', context={'form': form, 'title': title, 'url': url })


def admin_edit_user(request, id, **kwargs):
    if kwargs['role'] == 'admin':
        user = User.objects.get(pk=id)
    else:
        if kwargs['user_id'] == id:
            user = User.objects.get(pk=id)
        else:
            return HttpResponse("Permission denied!")
    try:
        profile = UserProfile.objects.get(user=id)
    except:
        # create new profile if not exist
        profile = UserProfile(user=user, phone="", role="", image=None )
        profile.save()
    if request.method == "POST":
        input_form = UserEditForm(request.POST, request.FILES)
        if input_form.is_valid():
            new_name = input_form.cleaned_data['name']
            new_email = input_form.cleaned_data['email']
            new_phone = input_form.cleaned_data['phone']
            new_image = input_form.cleaned_data['image']
            new_role = input_form.cleaned_data['role']
            user.username = new_name
            user.email = new_email
            user.save()
            profile.phone = new_phone
            profile.role = new_role
            profile.image = new_image
            profile.save()
        else:
            title = "Edit user"
            url = "admin_edit_user"
            return render(request, 'home/admin_edit_item.html', context={'form': input_form, 'id': id, 'title': title, 'url': url })
        return HttpResponseRedirect(reverse('admin_user'))
    else:
        data = {'name': user.username, 'email': user.email, 'phone': profile.phone, 'role': profile.role, 'image': profile.image}
        form = UserEditForm(data)
        title = "Edit user"
        url = "admin_edit_user"
        return render(request, 'home/admin_edit_item.html', context={'form': form, 'id': id, 'title': title, 'url': url})


def admin_category(request, **kwargs):
    categories = Category.objects.all()
    return render(request, 'home/admin_category.html', context={'categories': categories })


def admin_add_category(request, **kwargs):
    if request.method == "POST":
        input_form =  CategoryForm(request.POST)
        if input_form.is_valid():
            name = input_form.cleaned_data['name']
            home_text = input_form.cleaned_data['home_text']
            category = Category(name=name, home_text=home_text)
            category.save()
            return HttpResponseRedirect(reverse('admin_category'))
    else:
        form = CategoryForm()
        title = 'Create new category'
        url = 'admin_add_category'
        return render(request, 'home/admin_add_item.html', context={'form': form, 'title': title, 'url': url })


def admin_edit_category(request, id, **kwargs):
    category = Category.objects.get(pk=id)
    if request.method == "POST":
        input_form = CategoryForm(request.POST)
        if input_form.is_valid():
            new_name = input_form.cleaned_data['name']
            new_home_text = input_form.cleaned_data['home_text']
            category.name = new_name
            category.home_text = new_home_text
            category.save()
            return HttpResponseRedirect(reverse('admin_category'))
        else:
            title = "Edit category"
            url = "admin_edit_category"
            return render(request, 'home/admin_edit_item.html', context={'form': input_form, 'id': id, 'title': title, 'url': url })
    else:
        data = { 'name': category.name, 'home_text': category.home_text }
        form = CategoryForm(data)
        title = "Edit category"
        url = "admin_edit_category"
        return render(request, 'home/admin_edit_item.html', context={'form': form, 'id': id, 'title': title, 'url': url })



def admin_status(request, **kwargs):
    status = Status.objects.all()
    return render(request, 'home/admin_status.html', context={'status': status })


def admin_add_status(request, **kwargs):
    if request.method == "POST":
        input_form = StatusForm(request.POST)
        if input_form.is_valid():
            name = input_form.cleaned_data['name']
            status = Status(name=name)
            status.save()   
        return HttpResponseRedirect(reverse('admin_status'))
    else:
        form = StatusForm()
        title = 'Create new status'
        url = 'admin_add_status'
        return render(request, 'home/admin_add_item.html', context={'form': form, 'title': title, 'url': url })


def admin_edit_status(request, id, **kwargs):
    status = Status.objects.get(pk=id)
    if request.method == "POST":
        input_form = StatusForm(request.POST)
        if input_form.is_valid():
            new_name = input_form.cleaned_data['name']
            status.name = new_name
            status.save()
            return HttpResponseRedirect(reverse('admin_status'))
        else:
            title = "Edit status"
            url = "admin_edit_status"
            return render(request, 'home/admin_edit_item.html', context={'form': input_form, "id": id, 'title': title, 'url': url})
    else:
        data = { 'name': status.name }
        form = StatusForm(data)
        title = "Edit status"
        url = "admin_edit_status"
        return render(request, 'home/admin_edit_item.html', context={'form': form, "id": id, 'title': title, 'url': url})


def admin_city(request, **kwargs):
    cities = City.objects.all()
    return render(request, 'home/admin_city.html', context={'cities': cities })


def admin_add_city(request, **kwargs):
    if request.method == "POST":
        input_form = CityForm(request.POST, request.FILES)
        if input_form.is_valid():
            name = input_form.cleaned_data['name']
            listing = input_form.cleaned_data['number_of_listing']
            image = input_form.cleaned_data['image']
            city = City(name=name, number_of_listing=listing, image=image)
            city.save()
        return HttpResponseRedirect(reverse('admin_city'))
    else:
        form = CityForm()
        title = 'Create new city'
        url = 'admin_add_city'
        return render(request, 'home/admin_add_item.html', context={'form': form, 'title': title, 'url': url })


def admin_edit_city(request, id, **kwargs):
    city = City.objects.get(pk=id)
    if request.method == "POST":
        input_form = CityForm(request.POST, request.FILES)
        if input_form.is_valid():
            new_name = input_form.cleaned_data['name']
            new_listing = input_form.cleaned_data['number_of_listing']
            new_image = input_form.cleaned_data['image']
            city.name = new_name
            city.number_of_listing = new_listing
            city.image = new_image
            city.save()
            return HttpResponseRedirect(reverse('admin_city'))
        else:
            title = "Edit city"
            url = "admin_edit_city"
            return render(request, 'home/admin_edit_item.html', context={'form': input_form, 'id': id, 'title': title, 'url': url})
    else:
        data = {
            'name': city.name,
            'number_of_listing': city.number_of_listing,
            'image': city.absolute_url()
        }
        form = CityForm(data)
        title = "Edit city"
        url = "admin_edit_city"
        return render(request, 'home/admin_edit_item.html', context={'form': form, 'id': id, 'title': title, 'url': url})


def admin_property(request, **kwargs):
    if kwargs['role'] == 'admin':
        properties = Property.objects.all()
    else:
        user_id = kwargs['user_id']
        properties = Property.objects.filter(user_id=user_id)
    return render(request, 'home/admin_property.html', context={'properties': properties})


def admin_add_property(request, **kwargs):
    if request.method == "POST":
        input_form = PropertyForm(request.POST, request.FILES)
        if input_form.is_valid():
            user = request.user
            name = input_form.cleaned_data['name']
            address = input_form.cleaned_data['address']
            city = input_form.cleaned_data['city']
            price = input_form.cleaned_data['price']
            status = input_form.cleaned_data['status']
            area = input_form.cleaned_data['area']
            garage = input_form.cleaned_data['garage']
            bedroom = input_form.cleaned_data['bedroom']
            bathroom = input_form.cleaned_data['bathroom']
            category = input_form.cleaned_data['category']
            founded_date = input_form.cleaned_data['founded_date']
            avatar = input_form.cleaned_data['avatar']
            description = input_form.cleaned_data['description']
            google_map = input_form.cleaned_data['google_map']
            featured = input_form.cleaned_data['featured']
            image = request.FILES.getlist('image')
            
            city_obj = City.objects.get(pk=city)
            city_obj.number_of_listing += 1
            city_obj.save()

            status_obj = Status.objects.get(pk=status)
            category_obj = Category.objects.get(pk=category)

            prop = Property(user=user, name=name, address=address, city=city_obj, price=price, status=status_obj, area=area, garage=garage, bedroom=bedroom, bathroom=bathroom, category=category_obj, founded_date=founded_date, avatar=avatar, description=description, google_map=google_map, featured=featured)
            prop.save()

            for i in image:
                prop_image = PropertyImage(prop=prop, image=i)
                prop_image.save()

            return HttpResponseRedirect(reverse('admin_property'))
        else:
            title = 'Create new property'
            url = 'admin_add_property'
            return render(request, 'home/admin_add_item.html', context={'form': input_form, 'title': title, 'url': url })
    else:
        form = PropertyForm()
        title = 'Create new property'
        url = 'admin_add_property'
        return render(request, 'home/admin_add_item.html', context={'form': form, 'title': title, 'url': url })


def admin_edit_property(request, id, **kwargs):
    if kwargs['role'] == 'admin':
        prop = Property.objects.get(pk=id)
    else:
        user_id = kwargs['user_id']
        prop = Property.objects.get(pk=id)
        if prop.user.id ==  user_id:
            pass
        else:
            return HttpResponse("Permission denied!")
        
    if request.method == "POST":
        input_form = PropertyForm(request.POST, request.FILES)
        if input_form.is_valid():
            new_name = input_form.cleaned_data['name']
            new_address = input_form.cleaned_data['address']
            new_city = City.objects.get(pk=input_form.cleaned_data['city'])
            new_price = input_form.cleaned_data['price']
            new_status = Status.objects.get(pk=input_form.cleaned_data['status'])
            new_area = input_form.cleaned_data['area']
            new_garage = input_form.cleaned_data['garage']
            new_bedroom = input_form.cleaned_data['bedroom']
            new_bathroom = input_form.cleaned_data['bathroom']
            new_category = Category.objects.get(pk=input_form.cleaned_data['category'])
            new_founded_date = input_form.cleaned_data['founded_date']
            new_avatar = input_form.cleaned_data['avatar']
            new_description = input_form.cleaned_data['description']
            new_google_map = input_form.cleaned_data['google_map']
            new_featured = input_form.cleaned_data['featured']

            prop.name = new_name
            prop.address = new_address
            prop.city = new_city
            prop.price = new_price
            prop.status = new_status
            prop.area = new_area
            prop.garage = new_garage
            prop.bedroom = new_bedroom
            prop.bathroom = new_bathroom
            prop.category =  new_category
            prop.founded_date = new_founded_date
            prop.avatar = new_avatar
            prop.description = new_description
            prop.google_map = new_google_map
            prop.featured = new_featured
            prop.save()
            return HttpResponseRedirect(reverse('admin_property'))
        else:
            title = "Edit property"
            url = "admin_edit_property"
            return render(request, 'home/admin_edit_item.html', context={'form': input_form, 'id': id, 'title': title, 'url': url})
    
    else:
        data = {
            'name': prop.name,
            'avatar': prop.avatar,
            'address': prop.address,
            'city': prop.city,
            'price': prop.price,
            'status': prop.status,
            'area': prop.area,
            'garage': prop.garage,
            'bedroom': prop.bedroom,
            'bathroom': prop.bathroom,
            'category': prop.category,
            'founded_date': prop.founded_date,
            'description': prop.description,
            'google_map': prop.google_map,
            'featured': prop.featured
        }
        form = PropertyForm(data)
        title = "Edit property"
        url = "admin_edit_property"
        return render(request, 'home/admin_edit_item.html', context={'form': form, 'id': id, 'title': title, 'url': url})



def admin_blog(request, **kwargs):
    blogs = Blog.objects.all()
    return render(request, 'home/admin_blog.html', context={'blogs': blogs})


def admin_add_blog(request, **kwargs):
    if request.method == "POST":
        input_form = BlogForm(request.POST, request.FILES)
        if input_form.is_valid():
            title = input_form.cleaned_data['title']
            user = request.user
            content = input_form.cleaned_data['content']
            avatar = input_form.cleaned_data['avatar']

            new_blog = Blog(user=user, title=title, content=content, avatar=avatar)
            new_blog.save()
            return HttpResponseRedirect(reverse('admin_blog'))
        else:
            title = "Create new blog"
            url = "admin_add_blog"
            return render(request, 'home/admin_add_item.html', context={'form': input_form, 'title': title, 'url': url})
    else:
        form = BlogForm()
        title = "Create new blog"
        url = "admin_add_blog"
        return render(request, 'home/admin_add_item.html', context={'form': form, 'title': title, 'url': url})
    

def admin_edit_blog(request, id, **kwagrs):
    blog = Blog.objects.get(pk=id)
    if request.method == "POST":
        input_form = BlogForm(request.POST, request.FILES)
        if input_form.is_valid():
            new_title = input_form.cleaned_data['title']
            new_avatar = input_form.cleaned_data['avatar']
            new_content = input_form.cleaned_data['content']
            blog.title = new_title
            blog.avatar = new_avatar
            blog.content = new_content
            blog.save()
            return HttpResponseRedirect(reverse('admin_blog'))
        else:
            title = "Edit blog"
            url = "admin_edit_blog"
            return render(request, 'home/admin_edit_item.html', context={'title': title, 'url': url, 'form': input_form, 'id': id} )

    else:
        data = {'title': blog.title, 'avatar': blog.avatar, 'content': blog.content}
        title = "Edit blog"
        url = "admin_edit_blog"
        form = BlogForm(data)
        return render(request, 'home/admin_edit_item.html', context={'title': title, 'url': url, 'form': form, 'id': id} )




def admin_delete_item(request, **kwargs):
    if request.method == "POST":
        id = request.POST['id']
        kind = request.POST['kind']
        if kind == 'property':
            try:
                item = Property.objects.get(pk=id)
                item.delete()
            except:
                return HttpResponse('object not found???')
            return HttpResponseRedirect(reverse('admin_property'))
        elif kind == 'city':
            try:
                item = City.objects.get(pk=id)
                item.delete()
            except:
                pass
            return HttpResponseRedirect(reverse('admin_city'))
        elif kind == 'category':
            try:
                item = Category.objects.get(pk=id)
                item.delete()
            except:
                pass
            return HttpResponseRedirect(reverse('admin_category'))
        elif kind == 'status':
            try:
                item = Status.objects.get(pk=id)
                item.delete()
            except:
                pass
            return HttpResponseRedirect(reverse('admin_category'))
        elif kind == 'blog':
            try:
                item = Blog.objects.get(pk=id)
                item.delete()
            except:
                pass
            return HttpResponseRedirect(reverse('admin_blog'))
        elif kind == 'review':
            try:
                item = Review.objects.get(pk=id)
                item.delete()
            except:
                pass
            return HttpResponseRedirect(reverse('admin_review'))
        elif kind == 'about':
            try:
                item = About.objects.get(pk=id)
                item.delete()
            except:
                pass
            return HttpResponseRedirect(reverse('admin_about'))

        elif kind == 'user':
            try:
                item = User.objects.get(pk=id)
                item.delete()
            except:
                pass
            return HttpResponseRedirect(reverse('admin_user'))
    else:
        return HttpResponseRedirect(reverse('admin'))
        

def admin_review(request, **kwargs):
    role = kwargs['role']
    if role == 'admin':
        reviews = Review.objects.all()
    else:
        user_id = kwargs['user_id']
        reviews = Review.objects.filter(user_id=user_id)
    return render(request, 'home/admin_review.html', context={'reviews': reviews})


def admin_add_review(request, **kwargs):
    if request.method == "POST":
        input_form = ReviewForm(request.POST)
        if input_form.is_valid():
            user = request.user
            star = input_form.cleaned_data['star']
            content = input_form.cleaned_data['content']
            career = input_form.cleaned_data['career']
            review = Review(user=user, star=star, content=content, career=career)
            review.save()
            return HttpResponseRedirect(reverse('admin_review'))
        else:
            url= "admin_add_review"
            title = "Add review"
            return render(request, 'home/admin_add_item.html', context={'form': input_form, 'url': url, 'title': title})
    else:
        form = ReviewForm()
        url= "admin_add_review"
        title = "Add review"
        return render(request, 'home/admin_add_item.html', context={'form': form, 'url': url, 'title': title})


def admin_edit_review(request, id, **kwargs):
    review = Review.objects.get(pk=id)
    if request.method == "POST":
        input_form = ReviewForm(request.POST)
        if input_form.is_valid():
            new_star = input_form.cleaned_data['star']
            new_content = input_form.cleaned_data['content']
            new_career = input_form.cleaned_data['career']
            review.star = new_star
            review.content = new_content
            review.career = new_career
            review.save()
            return HttpResponseRedirect(reverse('admin_review'))
        else:
            url= "admin_edit_review"
            title = "Edit review"
            return render(request, 'home/admin_edit_item.html', context={'form': input_form, 'url': url, 'title': title, 'id': id})
    else:
        data = {'star': review.star, 'content': review.content, 'career': review.career }
        form = ReviewForm(data)
        url= "admin_edit_review"
        title = "Edit review"
        return render(request, 'home/admin_edit_item.html', context={'form': form, 'url': url, 'title': title, 'id': id})



def admin_about(request, **kwargs):
    about = About.objects.all().order_by("-id")
    return render(request, 'home/admin_about.html', context={'about': about})


def admin_add_about(request, **kwargs):
    if request.method == "POST":
        input_form = AboutForm(request.POST, request.FILES)
        if input_form.is_valid():
            about_us = input_form.cleaned_data['about_us']
            our_quality = input_form.cleaned_data['our_quality']
            image = input_form.cleaned_data['image']
            selected_review = input_form.cleaned_data['selected_review']

            about = About(about_us=about_us, our_quality=our_quality, image=image)
            about.save()

            for i in selected_review:
                rev = about.selected_review.add(i)

            return HttpResponseRedirect(reverse('admin_about'))
        else:
            url = "admin_add_about"
            title = "Add about us"
            return render(request, 'home/admin_add_item.html', context={'form': input_form, 'url': url, 'title': title})

    else:
        form = AboutForm()
        url = "admin_add_about"
        title = "Add about us"
        return render(request, 'home/admin_add_item.html', context={'form': form, 'url': url, 'title': title})




def admin_edit_about(request, id, **kwargs):
    about = About.objects.get(pk=id)
    if request.method == "POST":
        input_form = AboutForm(request.POST, request.FILES)
        if input_form.is_valid():
            new_about_us = input_form.cleaned_data['about_us']
            new_our_quality = input_form.cleaned_data['our_quality']
            new_image = input_form.cleaned_data['image']
            new_selected_review = input_form.cleaned_data['selected_review']

            about.selected_review.clear()
            about.about_us = new_about_us
            about.our_quality = new_our_quality
            about.image = new_image
            about.save()

            for i in new_selected_review:
                about.selected_review.add(i)
            
            return HttpResponseRedirect(reverse('admin_about'))
        else:
            url = 'admin_edit_about'
            title = 'Edit about us'
            return render(request, 'home/admin_edit_item.html', context={'form': input_form, 'url': url, 'title': title, 'id': id})
    else:   
        data = {'about_us': about.about_us, 'our_quality': about.our_quality, 'image': about.image, 'selected_review': about.selected_review}
        form = AboutForm(data)
        url = 'admin_edit_about'
        title = 'Edit about us'
        return render(request, 'home/admin_edit_item.html', context={'form': form, 'url': url, 'title': title, 'id': id})





def home(request):
    cities = City.objects.all()
    featured_properties = Property.objects.filter(featured=True).order_by('-order', '-id')[:6]
    blogs = Blog.objects.all().order_by('-id')[:3]
    categories = Category.objects.all()
    return render(request, 'home/index.html', context={
        'cities': cities,
        'featured_properties': featured_properties,
        'blogs': blogs,
        'categories': categories        
    })


def property_detail(request, id):
    property_object = Property.objects.get(pk=id)
    images = PropertyImage.objects.filter(prop=id)
    related_properties = Property.objects.filter(category=property_object.category).exclude(id=property_object.id)[:4]

    return render(request, 'home/property_detail.html', context={'property': property_object, 'images': images, 'related_properties': related_properties})


def browse_result(request, result, page, search_dictionary=None):
    if request.path == '/browse/page/1/':
        return HttpResponseRedirect(reverse('browse'))
    
    if search_dictionary:
        search_text = search_dictionary['search_text']
        search_filter =  search_dictionary['search_filter']
        if search_filter == "city":
            search_cities = City.objects.filter(name__icontains=search_text).values_list('id', flat=True)
            properties =  Property.objects.filter(city_id__in=search_cities).order_by('-order', '-id')
        elif search_filter == "category":
            search_categories = Category.objects.filter(name__icontains=search_text).values_list('id', flat=True)
            properties = Property.objects.filter(category__in=search_categories).order_by('-order', '-id')
    else:
        properties = Property.objects.all().order_by('-order', '-id')

    paginator = Paginator(properties, 2)
    page_obj = paginator.get_page(page)

    page_list = []
    for i in range(1,paginator.num_pages + 1):
        page_list.append(i)

    if page == paginator.num_pages:
        next_page = 0
    else:
        next_page = page + 1
    if page == 1:
        prev_page = 0
    else:
        prev_page = page - 1
    
    if result == "ajax":
        prop_list = []
        for prop in page_obj:
            prop_list.append({"id": prop.pk, "user": prop.user.username, "name": prop.name, "address":prop.address, "area": prop.area, "bedroom": prop.bedroom, "bathroom": prop.bathroom, "founded_date": prop.founded_dateformat(), "garage": prop.garage, "absolute_url": prop.absolute_url(), 'status': prop.status.name, 'city': prop.city.name, "url": reverse("property_detail", args=[prop.pk]), "price": prop.price})
        
        data_json = {
            'page': page, 'page_list': page_list, 'next_page': next_page, 'prev_page': prev_page,
            'properties': prop_list
        }

        return JsonResponse(data_json)
        
    else:
        return render(request, 'home/browse.html', context={'properties': page_obj, 'page': page, 'page_list': page_list, 'next_page': next_page, 'prev_page': prev_page})


def browse(request, page=1, category_id=0, city_id=0, city_name="all"):
    if "page" in request.GET:
        page = int(request.GET['page'])
    else:
        page = 1

    if "text" in request.GET:
        search_text = request.GET['text']
        search_filter = request.GET['filter']
        search_dictionary = {'search_text': search_text, 'search_filter': search_filter}
        returned_result = browse_result(request=request, result="render", page=page, search_dictionary=search_dictionary)
        return returned_result
    else:
        returned_result = browse_result(request=request, result="render", page=page)
        return returned_result
    

def browse2(request, page=1, category_id=0, city_id=0, city_name="all"):
    if "page" in request.GET:
        page = int(request.GET['page'])
    else:
        page = 1

    if "text" in request.GET:
        search_text = request.GET['text']
        search_filter = request.GET['filter']
        search_dictionary = {'search_text': search_text, 'search_filter': search_filter}
        returned_result = browse_result(request=request, result="ajax", page=page, search_dictionary=search_dictionary)
        return returned_result
    else:
        returned_result = browse_result(request=request, result="ajax", page=page)
        return returned_result


def browse_city(request, city_id, page, city_name):
    properties = Property.objects.filter(city_id=city_id).order_by('-order', '-id')
    paginator = Paginator(properties, 2)
    page_obj = paginator.get_page(page)
    page_list = []
    for i in range(1,paginator.num_pages + 1):
        page_list.append(i)

    if page == paginator.num_pages:
        next_page = 0
    else:
        next_page = page + 1
    if page == 1:
        prev_page = 0
    else:
        prev_page = page - 1
    
    return render(request, 'home/browse.html', context={'properties': page_obj, 'page': page, 'page_list': page_list, 'next_page': next_page, 'prev_page': prev_page, 'filter_url': 'browse_city', 'filter_id':city_id, 'filter_name': city_name, 'filter': str("City: " + city_name) })


def browse_category(request, category_id, page, category_name):
    properties = Property.objects.filter(category_id=category_id).order_by('-order', '-id')
    paginator = Paginator(properties, 2)
    page_obj = paginator.get_page(page)

    page_list = []
    for i in range(1,paginator.num_pages + 1):
        page_list.append(i)

    if page == paginator.num_pages:
        next_page = 0
    else:
        next_page = page + 1
    if page == 1:
        prev_page = 0
    else:
        prev_page = page - 1
    
    return render(request, 'home/browse.html', context={'properties': page_obj, 'page': page, 'page_list': page_list, 'next_page': next_page, 'prev_page': prev_page, 'filter_url': 'browse_category', 'filter_id': category_id, 'filter_name': category_name, 'filter': str("Category: " + category_name)})


def browse_search(request):
    if request.method == "POST":
        filter_type = request.POST['filter']
        text = request.POST['text']
        return HttpResponseRedirect(reverse('browse_search_result', args=(filter_type, text, 1)))
    else:
        return HttpResponseRedirect(reverse('home'))


def browse_search_result(request, search, text, page):
    if search == "city":
        check = City.objects.filter(name__icontains=text).values_list('id', flat=True)
        properties = Property.objects.filter(city_id__in=check).order_by('-order', '-id')
    elif search == 'category':
        check = Category.objects.filter(name__icontains=text).values_list('id', flat=True)
        properties = Property.objects.filter(category_id__in=check).order_by('-order', '-id')

    paginator = Paginator(properties, 2)
    page_obj = paginator.get_page(page)

    page_list = []
    for i in range(1,paginator.num_pages + 1):
        page_list.append(i)

    if page == paginator.num_pages:
        next_page = 0
    else:
        next_page = page + 1
    if page == 1:
        prev_page = 0
    else:
        prev_page = page - 1
    
    return render(request, 'home/browse.html', context={'properties': page_obj, 'page': page, 'page_list': page_list, 'next_page': next_page, 'prev_page': prev_page, 'filter_url': 'browse_search_result', 'filter_id':search, 'filter_name': text, 'filter': str("Search by " + search +" " + text) })



def blog(request, page=1):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 2)
    page_obj = paginator.get_page(page)

    page_list = []
    for i in range(1,paginator.num_pages + 1):
        page_list.append(i)

    if page == paginator.num_pages:
        next_page = 0
    else:
        next_page = page + 1
    if page == 1:
        prev_page = 0
    else:
        prev_page = page - 1

    return render(request, 'home/blog.html', context={'blogs': page_obj, 'page': page, 'page_list': page_list,'next_page': next_page, 'prev_page': prev_page, })



def blog_detail(request, id):
    blog = Blog.objects.get(pk=id)
    comments = Comment.objects.filter(blog=id, parent=0).order_by('id')
    numbers = comments.count()
    for com in comments:
        com.replies = Comment.objects.filter(main=com.id).order_by("id")
        numbers += com.replies.count()

    return render(request, 'home/blog_detail.html', context={'blog': blog, 'comments': comments, "numbers": numbers})


def comment(request):
    if request.method == "POST":
        user = request.user
        content = request.POST['content']
        blog_id = request.POST['blog_id']
        parent = request.POST['parent']
        main = request.POST['main']
        blog = Blog.objects.get(pk=blog_id)

        new_comment = Comment(user=user, content=content, blog=blog, parent=parent, main=main)
        new_comment.save()

        user_id = user.id
        user_avatar = UserProfile.objects.get(user_id=user_id).absolute_url()
        user_name = user.username
        date = new_comment.dateformat()
        new_comment_id = new_comment.id
        

        return JsonResponse({
            "user_avatar": user_avatar,
            "user_name": user_name,
            "date": date,
            "new_comment_id": new_comment_id,
            "parent": parent,
            "main": main
        })



