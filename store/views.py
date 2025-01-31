from django.shortcuts import render,redirect
from .models import Product,Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm ,UpdateUserForm ,UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

# Create your views here.

def search(request):
	# Determine if they filled out the form
	if request.method == "POST":
		searched = request.POST['searched']
		# Query The Products DB Model
		searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
		# Test for null
		if not searched:
			messages.success(request, "That Product Does Not Exist...Please try Again.")
			return render(request, "search.html", {})
		else:
			return render(request, "search.html", {'searched':searched})
	else:
		return render(request, "search.html", {})	



def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		

        if form.is_valid() or shipping_form.is_valid():
                form.save()
                shipping_form.save()
                messages.success(request,  "Your Info Has Been Updated !!")
                return redirect('home')
        return render(request, "update_info.html", {'form': form, 'shipping_form': shipping_form })
    else:
        messages.error(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')



def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')




def category(request, foo):
	# Replace Hyphens with Spaces
	foo = foo.replace('-', ' ')
	# Grab the category from the url
	try:
		# Look Up The Category
		category = Category.objects.get(name=foo)
		products = Product.objects.filter(category=category)
		return render(request, 'category.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("That Category Doesn't Exist..."))
		return redirect('home')



def product(request,pk):
	product = Product.objects.get(id=pk)
	return render(request, 'product.html', {'product':product})


def home(request):
    products =Product.objects.order_by('?')[:8]
    return render(request, 'home.html', {'products':products})


def about(request):
    return render(request, 'about.html',{})



def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Do some shopping cart stuff
            try:
                current_user = Profile.objects.get(user=user)
                saved_cart = current_user.old_cart  # Assuming 'old_cart' is a JSON string
            except Profile.DoesNotExist:
                messages.error(request, "Profile not found for this user.")
                return redirect('login')

            if saved_cart:  # If a saved cart exists
                try:
                    # Convert JSON string to Python dictionary
                    converted_cart = json.loads(saved_cart)

                    # Add items from the saved cart to the current session cart
                    cart = Cart(request)
                    for key, value in converted_cart.items():
                        cart.db_add(product=key, quantity=value)

                    messages.success(request, "Your cart has been restored.")
                except json.JSONDecodeError:
                    messages.error(request, "Error decoding the saved cart. Please try again.")

            messages.success(request, "You have been logged in!")
            return redirect('home')  # Adjust to the correct redirect view for your app
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')

    else:
        return render(request, 'login.html')



def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out ... bye bye !"))
    return redirect('home')


def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, (" Account Created - Welcome <3 ..."))
			return redirect('home')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})


