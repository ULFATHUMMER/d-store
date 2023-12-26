from itertools import product

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from homeapp.models import Product, Profile, Department, Course
from .models import Cart, CartItem, ReturnedItem
from homeapp.views import logout
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

#create cart_id using session
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request):
    if request.method == 'POST':
        #get id of current user
        current_user = request.user
        print('user',current_user)
        #get profile details
        name = request.POST['name']
        dob = request.POST['dob']
        age = request.POST['age']
        gender = request.POST['gender']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']
        department_id = request.POST['department']
        department=Department.objects.get(id=department_id)
        course_id = request.POST['course']
        course=Course.objects.get(id=course_id)
        purpose = request.POST['purpose']
        print("start here")
        profile = Profile(
            name=name, dob=dob, age=age,
            user=current_user,gender=gender,
            phone=phone,mailid=email,
            address=address,department=department,
            course=course,purpose=purpose)
        print('end here')
        print("name is", profile)
        profile.save()

        #gives list of id of products
        list_of_products_id = request.POST.getlist('products')
        for x in list_of_products_id:
            if purpose == 'placeorder':
                toCart(request,x)
                logout(request)

            if purpose == 'return':
                toReturn(request,x)
                logout(request)

            else:
                None


    return redirect('homeapp:index')
    #return redirect('cartapp:cart_detail')
def toCart(request,x=None):
        # y = Product.objects.get(id=x)
        try:
            product = Product.objects.get(id=x)
            cart = Cart.objects.get(cart_id=_cart_id(request))

        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request))
        cart.save()
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            if cart_item.quantity < cart_item.product.stock:
                cart_item.quantity += 1

            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )
            cart_item.save()


def toReturn(request,x=None):
        # y = Product.objects.get(id=x)
        try:
            product = Product.objects.get(id=x)
            cart = Cart.objects.get(cart_id=_cart_id(request))

        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request))
        cart.save()
        try:
            return_item = ReturnedItem.objects.get(product=product, cart=cart)
            if return_item.quantity < return_item.product.stock:
                return_item.quantity += 1
            return_item.save()
        except ReturnedItem.DoesNotExist:
            return_item = ReturnedItem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )
            return_item.save()




# cart_details

def cart_detail(request,total=0,counter=0,cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        #puser=puser
        cart_items=CartItem.objects.filter(cart=cart,active=True)
        for item in cart_items:
            total += (item.product.price * item.quantity)
            counter += item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',dict(cart_items=cart_items,total=total,counter=counter))

#add item


def add_item(request,product_id):
    product=Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id = _cart_id(request))

    except Cart.DoesNotExist:
        cart=Cart.objects.create(
        cart_id=_cart_id(request))
    cart.save()
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity= 1,
            cart=cart
        )
        cart_item.save()
    return redirect('cartapp:add_cart')


#delete cart item
def remove_item(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cartapp:cart_detail')

def delete_item(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cartapp:cart_detail')
