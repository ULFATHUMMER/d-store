from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import format_html
from . models import Category, Product,Profile,Department,Course

# Create your views here.
 ##view for index
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')

def home(request):
    return render(request,'home.html')

def profiless(request,user):
    print("user in profile",user)
    if request.method == "POST":
        print("PSOT WORKED")
        name = request.POST['name']
        user = request.POST['user']
        puser = User.objects.get(id=user)
        dob = request.POST['dob']
        age = request.POST['age']
        gender = request.POST['gender']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']
        department = request.POST['department']
        purpose = request.POST['purpose']
        print("start here")
        profile = Profile(
            name=name,dob=dob, age=age,
            user=puser,
            gender=gender, phone=phone,
            mailid=email, address=address,
            department=department, purpose=purpose)
        print('end here')
        print("name is", profile)
        profile.save()
        print("SAVED USER PRFILE")
        return redirect('homeapp:allProdCat', user)
    else:
        print("Request.method ", request.method)
        return render(request, 'profile.html', {"user": user})


##view for auth
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username is taken")
                return redirect('register')

            else:
                user = User.objects.create_user(username=username, password=password)
                user.save();
                print("registered user is",user)
                return redirect('homeapp:login')
        else:
            messages.info(request, "password do not match")
            return redirect('register')

        return redirect('/')
    return render(request, "register.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            user_obj=User.objects.get(username=username)
            return render(request, 'home.html')
            #return redirect('homeapp:home',user_obj.id)
        else:
            messages.info(request, "Invalid credentials")
            return redirect('login')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return  redirect('homeapp:index')

###view for shoping
def load_courses(request):
    department_id = request.GET.get('department')
    print("department id",department_id)
    courses = Course.objects.filter(department_id=department_id).order_by('name')
    return render(request, 'courses.html', {'courses': courses})
def shope(request):
    products_list = Product.objects.all().filter(available=True)
    departments = Department.objects.all()
    return render(request,'shope.html',{"products":products_list,"departments":departments})


def allProdCat1(request,c_slug=None):
    #user=User.objects.filter(id=user)
    c_page = None
    products_list=None
    if c_slug!=None:
        c_page = get_object_or_404(Category,slug=c_slug)
        products_list=Product.objects.all().filter(category=c_page,available=True)
    else:
        products_list=Product.objects.all().filter(available=True)
    paginator = Paginator(products_list,12)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page=1
    try:
        products = paginator.page(page)
    except (EmptyPage,InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request,'shope.html',{"category":c_page,"products":products})

    #return render(request,'shope.html',{"category":c_page,"products":products,'user':user.first().id})

def proDetails(request,c_slug,p_slug):
    try:
        product=Product.objects.get(category__slug=c_slug,slug=p_slug)
    except Exception as e:
        raise e
    return render(request,'product.html',{"product":product})

def paymsg(request):
    print("im here")
    text1="your order is confirmed"
    text2="Back to home"
    messages.info(request, format_html("{} <a href='/index'>{}</a>",text1 , text2))
    return  redirect('cartapp:cart_detail')