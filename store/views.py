from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile, Order, Customer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
 


@login_required
def my_orders(request):
    profile = Profile.objects.get(user=request.user)
    customer = Customer.objects.get(profile=profile)
    orders = Order.objects.filter(customer=customer).order_by('-date')
    return render(request, 'my_orders.html', {'orders': orders})

def search(request):
    #Determine if they filled out the search form
    if request.method == 'POST':
        searched = request.POST['searched']
        #Query the database for products that match the search term
        searched = Product.objects.filter(Q(name__contains=searched) | Q(description__contains=searched) | Q(category__name__contains=searched))
        #Test for null
        if not searched:
            messages.success(request, ('No products found.'))
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched}) 
    else:
        return render(request, 'search.html', {}) 

def update_info(request):
    if request.user.is_authenticated:
        #Get the current user
        curerent_user = Profile.objects.get(user__id=request.user.id)
        #Get the current shipping Info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        #Get original user form
        form = UserInfoForm(request.POST or None, instance=curerent_user)
        shipping_form =ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            #Save original form
            form.save()
            #Save shipping form
            shipping_form.save()
            messages.success(request, 'Your information has been updated.')
            return redirect('home')
        return render(request, 'update_info.html', {'form':form, 'shipping_form':shipping_form})
    else:
        messages.success(request, ('You must be logged in to view this page.'))
        return redirect('login')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            #Is the form valid?
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been updated.')
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})  
    else:
        messages.success(request, 'You must have be logged in to view that page.')
        return redirect('home')
def update_user(request):
    if request.user.is_authenticated:
        curerent_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=curerent_user)

        if user_form.is_valid():
            user_form.save()

            login(request, curerent_user)
            messages.success(request, 'Your profile has been updated.')
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.success(request, ('You must be logged in to view this page.'))
        return redirect('login')

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories':categories})

def category(request,foo):
    # Replace Hyphens with Spaces
    foo = foo.replace('-', ' ')
    #Grab the category from the url
    try:
        #Look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category': category})
    except:
        messages.success(request, ('That category doesn\'t exist.'))
        return redirect('home')

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            #Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            #Get their saved cart from database 
            save_cart = current_user.old_cart
            #Convert database string to python dictionary
            if save_cart:
                #Convert to dictionary using JSON
                converted_cart = json.loads(save_cart)
                #Add the loaded cart dictionary to our sessions
                #Get the cart
                cart = Cart(request)
                #Loop through the cart and add items from the database
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)


            messages.success(request, ('You have successfully logged in.'))
            return redirect('home')
        else:
            messages.success(request, ('There was an error logging in. Please try again later.'))
            return redirect('login') 
    else:

        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Username Created - Please fill out your profile information.")
            return redirect('update_info')
        else:
            # Loop through form errors and display them as messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})

    
