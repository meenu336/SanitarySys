from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser  # Assuming you have a CustomUser model
# Create your views here.
from . models import Product, UserProfile


from django.contrib import messages
from django.contrib.auth import login as auth_login

def index(request):
    return render(request,'index.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')

def registration(request):
     if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']  # Make sure this matches your form field name
        role = request.POST.get('role', None)  # Make sure this matches your form field name
        #user_type = request.POST['user_type']

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'registration.html', {'error_message': 'Email address is already in use.'})
        
        #if CustomUser.objects.filter(username=username).exists():
            #return render(request, 'registration.html', {'error_message': 'username is already in use.'})

        if password != confirm_password:
            # Handle password mismatch error
            return render(request, 'registration.html', {'error_message': 'Passwords do not match'})

        # Create a new user object
        user = CustomUser.objects.create_user(username=username, email=email, password=password, role=role)
        # You may want to do additional processing here if needed
        if role:
            user.role = role
            user.save() 

        return redirect('login')  # Redirect to login page after successful registration

     return render(request,'registration.html')


def user_login(request):
    if request.method == "POST":
        # Handle the login form submission
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user1 = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            # User does not exist, handle this case (e.g., display an error message)
            
            
            messages.error(request, "User does not exist. Please register before logging in.")
            return HttpResponse("User does not exist. Please register before logging in.")

        
        user = authenticate(request, username=username, password=password)
        user1=CustomUser.objects.get(username=username)
        if user is not None:
         if user1.role == "Stockmanager":
            # The user is valid, log them in
            login(request, user)
            request.session['username'] = username
            return redirect("stocks")
         elif  user1.role == "User":
            login(request,user)
            request.session['username'] = username
            return redirect("home") 
         elif  user1.role == "Plumber":
            login(request, user)
            request.session['username'] = username
            return redirect("plumber_dashboard")  
         elif  user1.username == "admin1":
            login(request,user)
            request.session['username'] = username
            return redirect("adminn")
         elif  user1.role == "DeliveryBoy":
            login(request,user)
            request.session['username'] = username
            return redirect("delivery_dashboard")
        else:
                # Handle the case where the user is anonymous
                messages.error(request, "User does not exist. Please register before logging in.")
    else:
            # Authentication failed, show an error message
         messages.error(request, "Incorrect username or password. Please try again.")

    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response



    #         # Authentication failed, handle the error or show a message
    #         return HttpResponse("Login failed. Please check your username and password.")
    
    # # Handle the GET request (display the login form)
    # return render(request, "login.html")



@login_required(login_url='login')
def home(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'home.html', context)

def stocks(request):
    return render(request,'stocks.html')

def addproduct(request):
    return render(request,'addproduct.html')

def adminn(request):
    return render(request,'adminn.html')

def editproduct(request):
    return render(request,'editproduct.html')

def add_product(request):
    if request.method == 'POST':
        # Handle the form submission
        product_id = request.POST.get('product-id')
        product_name = request.POST.get('product-name')
        category = request.POST.get('category-name')
        subcategory = request.POST.get('subcategory-name')
        quantity = request.POST.get('quantity')
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount = request.POST.get('discount')  # Retrieve as a string
        status = request.POST.get('status')
        product_image = request.FILES.get('product-image')

        price = float(price)

        # Convert discount to a float
        discount = float(discount)

        
        

        # Calculate sale_price
        sale_price = price - (price * (discount / 100))

        # Create a new Product object and save it to the database
        product = Product(
            product_id=product_id,
            product_name=product_name,
            category=category,
            subcategory=subcategory,
            quantity=quantity,
            description=description,
            price=price,
            discount=discount,
            sale_price=sale_price,  # Assign the calculated sale price
            status=status,
            product_image=product_image
        )
        product.save()

        # Redirect to a success page or any other desired action
        return redirect('viewproduct')

    return render(request, 'addproduct.html')

def view_product(request):
    # Assuming you have a queryset of products (e.g., Product.objects.all())
    products = Product.objects.all()  # Modify this to fetch the products

    return render(request, 'viewproduct.html', {'products': products})

#def product_grid(request):
    #products = Product.objects.all()  # Fetch all products
    #return render(request, 'showers.html', {'products': products})

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse


from django.shortcuts import get_object_or_404, redirect, render
from .models import Product

def edit_product(request, product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)

        if request.method == 'POST':
            try:
                product_name = request.POST.get('product-name')
                category = request.POST.get('category-name')
                subcategory = request.POST.get('subcategory-name')
                quantity = request.POST.get('quantity')
                description = request.POST.get('description')
                price = request.POST.get('price')
                discount = request.POST.get('discount')
                status = request.POST.get('status')
                product_image = request.FILES.get('product_image')

                if product_image:
                    product.product_image = product_image

                price = float(price)
                discount = float(discount)
                sale_price = price - (price * (discount / 100))

                product.product_name = product_name
                product.category = category
                product.subcategory = subcategory
                product.quantity = quantity
                product.description = description
                product.price = price
                product.discount = discount
                product.sale_price = sale_price
                product.status = status

                product.save()

                return redirect('viewproduct')

            except Exception as e:
                print(str(e))
                return render(request, 'editproduct.html', {'product': product, 'error_message': str(e)})

        else:  # If the request method is GET, retrieve the product data and subcategories based on the selected category
            product = Product.objects.get(id=product_id)
            
            # Assuming subcategories are stored in a dictionary where keys are categories and values are subcategories
            subcategory_options = {
                'shower': ['built-in showers', 'Standalone shower'],
                'basins': ['Full Pedestal Basins', 'Semi Pedestal Basins'],
                # Add more categories and their respective subcategories as needed
            }

            # Fetch subcategory options based on the product's category
            subcategories = subcategory_options.get(product.category, [])
            selected_subcategory = product.subcategory

            context = {
                'product': product,
                'subcategory_options': subcategories,
                'selected_subcategory': selected_subcategory,
            }
            return render(request, 'editproduct.html', context)

    except Exception as e:
        print(str(e))
        return render(request, 'editproduct.html', {'product': product, 'error_message': str(e)})
  # Import your Product model here

def user_list(request):
    # Fetch users with the "Worker" role
    user = CustomUser.objects.filter(role='User')

    return render(request, 'user-list.html', {'users': user})

def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    # Delete the doctor or perform the desired action
    if request.method == 'POST':
         user.delete()
         messages.success(request, f'User {user.username} has been deleted.')
         return redirect('user-list') 
    return render(request, 'delete-user.html', {'user': user})


# your_app/views.py

def built_in_showers(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    built_in_products = Product.objects.filter(category='shower', subcategory='built-in showers')

    context = {
        'user_profile': user_profile,
        'built_in_products': built_in_products,
    }
    return render(request, 'built_in_showers.html',context)


def standalone_showers(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    standalone_products = Product.objects.filter(category='shower', subcategory='Standalone shower')

    context = {
        'user_profile': user_profile,
        'standalone_products': standalone_products,
    }
    return render(request, 'standalone_showers.html',context)

def full_pedestal_basins(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    full_pedestal_products = Product.objects.filter(category='basins', subcategory='Full Pedestal Basins')

    context = {
        'user_profile': user_profile,
        'full_pedestal_products': full_pedestal_products,
    }
    return render(request, 'full_pedestal_basins.html',context)

 # Import your UserProfile model

def semi_pedestal_basins(request):
    # Retrieve or create user profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    semi_pedestal_products = Product.objects.filter(category='basins', subcategory='Semi Pedestal Basins')

    context = {
        'user_profile': user_profile,
        'semi_pedestal_products': semi_pedestal_products,
    }

    return render(request, 'semi_pedestal_basins.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})



@login_required(login_url='login')
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Process form data manually
        user_profile.first_name = request.POST.get('first_name')
        user_profile.last_name = request.POST.get('last_name')
        user_profile.phone_number = request.POST.get('phone_number')
        user_profile.address = request.POST.get('address')
        user_profile.pincode = request.POST.get('pincode')
        user_profile.city = request.POST.get('city')
        user_profile.state = request.POST.get('state')


        # Handle image upload manually
        if 'image' in request.FILES:
            user_profile.image = request.FILES['image']

        user_profile.save()

        # Redirect to a success page or update the current page as needed
        return redirect('profile')

    return render(request, 'profile.html', {'user_profile': user_profile, 'created': created})

from .models import Product, Cart1, CartItem1
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, created = Cart1.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem1.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')

# @login_required(login_url='login')
# def remove_from_cart(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     cart = Cart1.objects.get(user=request.user)
#     try:
#         cart_item = cart.cartitem_set.get(product=product)
#         if cart_item.quantity >= 1:
#              cart_item.delete()
#     except CartItem1.DoesNotExist:
#         pass
    
#     return redirect('cart')
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = get_object_or_404(Cart1, user=request.user)
    
    try:
        cart_item = CartItem1.objects.get(cart=cart, product=product)
        if cart_item.quantity >= 1:
            cart_item.delete()
    except CartItem1.DoesNotExist:
        pass
    
    return redirect('cart')

# @login_required(login_url='login')
# def view_cart(request):
#     cart = request.user.cart
#     cart_items = CartItem1.objects.filter(cart=cart)
#     return render(request, 'cart.html', {'cart_items': cart_items})

@login_required(login_url='login')
def view_cart(request):
    try:
        # Get the user's cart using the Cart1 model associated with the user
        cart = Cart1.objects.get(user=request.user)
        cart_items = CartItem1.objects.filter(cart=cart)
        return render(request, 'cart.html', {'cart_items': cart_items})
    except Cart1.DoesNotExist:
        # Handle the case where the user doesn't have a cart yet
        # You might want to redirect to a page indicating an empty cart or create a new cart for the user
        return render(request, 'empty_cart.html')  # Replace 'empty_cart.html' with the appropriate template name


# @login_required(login_url='login')
# def increase_cart_item(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     cart = request.user.cart
#     cart_item, created = CartItem1.objects.get_or_create(cart=cart, product=product)

#     cart_item.quantity += 1
#     cart_item.save()

#     return redirect('cart')
@login_required(login_url='login')
def increase_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    
    # Ensure the user has a cart associated with them
    try:
        cart = Cart1.objects.get(user=request.user)
    except Cart1.DoesNotExist:
        cart = Cart1.objects.create(user=request.user)

    cart_item, created = CartItem1.objects.get_or_create(cart=cart, product=product)

    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')


# @login_required(login_url='login')
# def decrease_cart_item(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     cart = request.user.cart
#     cart_item = cart.cartitem_set.get(product=product)

#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     else:
#         cart_item.delete()

#     return redirect('cart')
@login_required(login_url='login')
def decrease_cart_item(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Retrieve the cart associated with the user or create a new cart if it doesn't exist
    try:
        cart = Cart1.objects.get(user=request.user)
    except Cart1.DoesNotExist:
        cart = Cart1.objects.create(user=request.user)

    # Retrieve the cart item for the specific product
    try:
        cart_item = CartItem1.objects.get(cart=cart, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem1.DoesNotExist:
        pass  # Handle the case where the cart item doesn't exist

    return redirect('cart')

@login_required(login_url='login')
def fetch_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = request.user.cart
        cart_count = CartItem1.objects.filter(cart=cart).count()
    return JsonResponse({'cart_count': cart_count})

# def get_cart_count(request):
#     if request.user.is_authenticated:
#         cart_items = CartItem1.objects.filter(cart=request.user.cart)
#         cart_count = cart_items.count()
#     else:
#         cart_count = 0
#     return cart_count

@login_required(login_url='login')
def get_cart_count(request):
    try:
        if request.user.is_authenticated:
            cart = Cart1.objects.get(user=request.user)
            cart_items = CartItem1.objects.filter(cart=cart)
            cart_count = cart_items.count()
        else:
            cart_count = 0
    except Cart1.DoesNotExist:
        cart_count = 0  # Handle the case where the user doesn't have a cart
    return cart_count



from .models import Product, CartItem1, Order, OrderItem
from django.http import JsonResponse
from django.conf import settings
import razorpay

import json
from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def create_order(request):
#     if request.method == 'POST':
#         user = request.user
#         cart = user.cart

#         cart_items = CartItem1.objects.filter(cart=cart)
#         total_amount = sum(item.product.sale_price * item.quantity for item in cart_items)

#         try:
#             order = Order.objects.create(user=user, total_amount=total_amount)
#             for cart_item in cart_items:
#                 OrderItem.objects.create(
#                     order=order,
#                     product=cart_item.product,
#                     quantity=cart_item.quantity,
#                     item_total=cart_item.product.sale_price * cart_item.quantity
#                 )

#             client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#             payment_data = {
#                 'amount': int(total_amount * 100),
#                 'currency': 'INR',
#                 'receipt': f'order_{order.id}',
#                 'payment_capture': '1'
#             }
#             orderData = client.order.create(data=payment_data)
#             order.payment_id = orderData['id']
#             order.save()

#             return JsonResponse({'order_id': orderData['id']})
        
#         except Exception as e:
#             print(str(e))
#             return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        user = request.user

        try:
            # Fetch the user's cart, assuming a Cart1 model related to the user
            cart = Cart1.objects.get(user=user)
            
            cart_items = CartItem1.objects.filter(cart=cart)
            total_amount = sum(item.product.sale_price * item.quantity for item in cart_items)

            order = Order.objects.create(user=user, total_amount=total_amount)
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    item_total=cart_item.product.sale_price * cart_item.quantity
                )

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_data = {
                'amount': int(total_amount * 100),
                'currency': 'INR',
                'receipt': f'order_{order.id}',
                'payment_capture': '1'
            }
            orderData = client.order.create(data=payment_data)
            order.payment_id = orderData['id']
            order.save()

            return JsonResponse({'order_id': orderData['id']})

        except Cart1.DoesNotExist:
            return JsonResponse({'error': 'Cart not found for this user'}, status=500)
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)
        
# def checkout(request):
#     cart_items = CartItem1.objects.filter(cart=request.user.cart)
#     total_amount = sum(item.product.price * item.quantity for item in cart_items)

#     cart_count = get_cart_count(request)
#     # email = request.user.email
#     # first_name = request.user.profile.first_name

#     context = {
#         'cart_count': cart_count,
#         'cart_items': cart_items,
#         'total_amount': total_amount,
#         # 'email':email,
#         # 'first_name': first_name
#     }
#     return render(request, 'checkout.html', context)

# @login_required(login_url='login')
# def checkout(request):
#     try:
#         # Attempt to get the user's cart using the Cart1 model associated with the user
#         cart = Cart1.objects.get(user=request.user)
#         cart_items = CartItem1.objects.filter(cart=cart)
#         total_amount = sum(item.product.sale_price * item.quantity for item in cart_items)

#         cart_count = get_cart_count(request)

#         # Fetch user profile information
#         user_profile = None
#         if request.user.is_authenticated:
#             user_profile,created = UserProfile.objects.get_or_create(user=request.user)

#         context = {
#             'cart_count': cart_count,
#             'cart_items': cart_items,
#             'total_amount': total_amount,
#              'user_profile': user_profile,
#         }
#         return render(request, 'checkout.html', context)

#     except Cart1.DoesNotExist:
#         # Handle the case where the user doesn't have a cart yet
#         # You might want to redirect to a page indicating an empty cart or create a new cart for the user
#         return render(request, 'empty_cart.html')  # Replace 'empty_cart.html' with the appropriate template name
@login_required(login_url='login')
def checkout(request):
    try:
        # Attempt to get the user's cart using the Cart1 model associated with the user
        cart = Cart1.objects.get(user=request.user)
        cart_items = CartItem1.objects.filter(cart=cart)
        
        total_quantity = sum(item.quantity for item in cart_items)  # Calculate total quantity
        total_amount = sum(item.product.sale_price * item.quantity for item in cart_items)  # Calculate total amount

        cart_count = get_cart_count(request)

        # Fetch user profile information
        user_profile = None
        if request.user.is_authenticated:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        context = {
            'cart_count': cart_count,
            'cart_items': cart_items,
            'total_amount': total_amount,
            'total_quantity': total_quantity,  # Include total_quantity in the context
            'user_profile': user_profile,
        }
        return render(request, 'checkout.html', context)

    except Cart1.DoesNotExist:
        # Handle the case where the user doesn't have a cart yet
        # You might want to redirect to a page indicating an empty cart or create a new cart for the user
        return render(request, 'empty_cart.html')  # Replace 'empty_cart.html' with the appropriate template name


# @csrf_exempt
# def handle_payment(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         razorpay_order_id = data.get('order_id')
#         payment_id = data.get('payment_id')

#         try:
#             order = Order.objects.get(payment_id=razorpay_order_id)

#             client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#             payment = client.payment.fetch(payment_id)

#             if payment['status'] == 'captured':
#                 order.payment_status = True
#                 order.save()
#                 user = request.user
#                 user.cart.cartitem_set.all().delete()
#                 return JsonResponse({'message': 'Payment successful'})
#             else:
#                 return JsonResponse({'message': 'Payment failed'})

#         except Order.DoesNotExist:
#             return JsonResponse({'message': 'Invalid Order ID'})
#         except Exception as e:

#             print(str(e))
#             return JsonResponse({'message': 'Server error, please try again later.'})
from django.contrib.auth import get_user_model
@csrf_exempt
def handle_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_order_id = data.get('order_id')
        payment_id = data.get('payment_id')

        try:
            order = Order.objects.get(payment_id=razorpay_order_id)

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment = client.payment.fetch(payment_id)

            if payment['status'] == 'captured':
                order.payment_status = True
                order.save()
                
                # Retrieve the user instance using the appropriate user model
                User = get_user_model()
                user = User.objects.get(id=order.user_id)  # Assuming user_id is related to the CustomUser model
                
                # Access the user's cart items and delete them
                if hasattr(user, 'cart') and hasattr(user.cart, 'cartitem_set'):
                    user.cart.cartitem_set.all().delete()
                
                return JsonResponse({'message': 'Payment successful'})
            else:
                return JsonResponse({'message': 'Payment failed'})

        except Order.DoesNotExist:
            return JsonResponse({'message': 'Invalid Order ID'})
        except Exception as e:
            print(str(e))
            return JsonResponse({'message': 'Server error, please try again later.'})
        
def bill_invoice(request):
    # Fetch the latest order for the logged-in user (or implement your logic)
    order = Order.objects.filter(user=request.user).latest('created_at')
    return render(request, 'billinvoice.html', {'order': order})

from django.http import JsonResponse
from .models import Product  # Import your Product model

def search_products(request):
    query = request.GET.get('query', '')  # Get the search query from the GET parameters

    if query:
        # Perform a case-insensitive search on the product names
        search_results = Product.objects.filter(product_name__icontains=query)
    else:
        search_results = []  # If no query, return an empty list

    return render(request, 'built_in_showers.html', {'search_results': search_results})

from django.shortcuts import render
from .models import Product  # Replace 'Product' with your actual model name

def search_full_pedestal_basins(request):
    query = request.GET.get('query')
    if query:
        results = Product.objects.filter(product_name__icontains=query)  # Modify this query based on your model fields
    else:
        results = Product.objects.all()  # Or handle the case when no query is provided
    
    context = {
        'search_results': results,
    }
    return render(request, 'full_pedestal_basins.html', context)

def stockmgr_registration(request):
     if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']  # Make sure this matches your form field name
        role = request.POST.get('role', None)  # Make sure this matches your form field name
        #user_type = request.POST['user_type']

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'stockmgr_registration.html', {'error_message': 'Email address is already in use.'})
        
        #if CustomUser.objects.filter(username=username).exists():
            #return render(request, 'registration.html', {'error_message': 'username is already in use.'})

        if password != confirm_password:
            # Handle password mismatch error
            return render(request, 'stockmgr_registration.html', {'error_message': 'Passwords do not match'})

        # Create a new user object
        user = CustomUser.objects.create_user(username=username, email=email, password=password, role=role)
        # You may want to do additional processing here if needed
        if role:
            user.role = role
            user.save() 

        return redirect('stockmgr_registration')  # Redirect to login page after successful registration

     return render(request,'stockmgr_registration.html')


def search_semi_pedestal_basins(request):
    query = request.GET.get('query')
    if query:
        results = Product.objects.filter(product_name__icontains=query)  # Modify this query based on your model fields
    else:
        results = Product.objects.all()  # Or handle the case when no query is provided
    
    context = {
        'search_results': results,
    }
    return render(request, 'semi_pedestal_basins.html', context)

def search_standalone_showers(request):
    query = request.GET.get('query')
    if query:
        results = Product.objects.filter(product_name__icontains=query)  # Modify this query based on your model fields
    else:
        results = Product.objects.all()  # Or handle the case when no query is provided
    
    context = {
        'search_results': results,
    }
    return render(request, 'standalone_showers.html', context)

def view_productss(request):
    # Assuming you have a queryset of products (e.g., Product.objects.all())
    products = Product.objects.all()  # Modify this to fetch the products

    return render(request, 'viewproductss.html', {'products': products})


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import JobApplication
from .models import UserProfile

@login_required
def job_application(request):

    user_profile = UserProfile.objects.get(user=request.user)
        # Check if the user has already submitted an application
    existing_application = JobApplication.objects.filter(user=request.user).exists()

    if existing_application:
        return redirect('success_page')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        full_address = request.POST.get('full_address')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_number = request.POST.get('vehicle_number')
        license = request.FILES.get('license')
        highest_education = request.POST.get('highest_education')
        languages_known = request.POST.get('languages_known')
        years_of_experience = request.POST.get('years_of_experience')
        resume = request.FILES.get('resume')

        # Save the form data to the database (you may want to add more validation)
        JobApplication.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            gender=gender,
            full_address=full_address,
            vehicle_type=vehicle_type,
            vehicle_number=vehicle_number,
            license=license,
            highest_education=highest_education,
            languages_known=languages_known,
            years_of_experience=years_of_experience,
            resume=resume
        )

        # Send email to user
        subject = 'Job Application Submitted Successfully'
        message = f'Dear {user_profile.first_name},\n\nYour job application for {job_application.job_title} has been submitted successfully.\n\nThank you for applying.'
        recipient_list = [email]
        sender_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, sender_email, recipient_list)

        # Redirect to the success page
        return redirect('success_page')

    return render(request, 'job_application.html', {'user_profile': user_profile})

def success_page(request):
    return render(request, 'success_page.html')

# def success_page(request):
#     return render(request, 'successpage.html')


# views.py
from django.shortcuts import render
from .models import JobApplication

def applicationz(request):
    # Get all job applications
    job_applications = JobApplication.objects.all()

    # Pass the job applications to the template
    return render(request, 'applicationz.html', {'job_applications': job_applications})


# from django.shortcuts import render
# from django.http import HttpResponse
# from .models import ServiceRequest


# def submit_service_request(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         address = request.POST.get('address')
#         city = request.POST.get('city')
#         district = request.POST.get('district')
#         service_required = request.POST.get('service')
#         description = request.POST.get('description')
#         select_date = request.POST.get('select_date')
        
#         # Create a new service request object and save it
#         service_request = ServiceRequest(
#             name=name,
#             email=email,
#             phone=phone,
#             address=address,
#             city=city,
#             district=district,
#             service_required=service_required,
#             description=description,
#             select_date=select_date
#         )
#         service_request.save()

# from django.shortcuts import render, redirect
# from .models import ServiceRequest

# def submit_service_request(request):
#     if request.method == 'POST':
#         # Assuming you have a CustomUser model and user information is associated with the logged-in user
#         user = request.user
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         address = request.POST.get('address')
#         city = request.POST.get('city')
#         district = request.POST.get('district')
#         service_required = request.POST.get('service')
#         description = request.POST.get('description')
#         select_date = request.POST.get('select_date')

#         # Create ServiceRequest instance with user information
#         service_request = ServiceRequest.objects.create(user=user, name=name, email=email, phone=phone, address=address, city=city, district=district, service_required=service_required, description=description, select_date=select_date)
#         # You might want to add some additional logic here, such as redirecting to a success page or displaying a message
        
        
#         # Redirect to a thank you page or display a success message
#         return HttpResponse("Service request submitted successfully!")
#     else:
#         return render(request, 'submit_service_request.html')



# from django.utils import timezone
# from .models import CustomerServiceRequest  # Updated model import
# from .models import UserProfile
# from django.shortcuts import render, HttpResponseRedirect, reverse
# from django.http import HttpResponseForbidden

# def submit_service_request(request):
#     if request.method == 'POST':
#         # Assuming you have a CustomUser model and user information is associated with the logged-in user
#         user = request.user
        
#         district = request.POST.get('district')
#         select_date = request.POST.get('select_date')
#         select_date = timezone.datetime.strptime(select_date, '%Y-%m-%d').date()
#         district_requests_count = CustomerServiceRequest.objects.filter(district=district, select_date=select_date).count()  # Updated model reference
#         if district_requests_count >= 20:
#             return HttpResponseForbidden("The maximum number of service requests from your district for this date has been reached. Please select another date.")
        
#         # Proceed with submitting the service request
#         first_name = request.POST.get('first_name')  # Updated field name
#         last_name = request.POST.get('last_name')    # Updated field name
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         address = request.POST.get('address')
#         city = request.POST.get('city')
#         pincode = request.POST.get('pincode')  # Added pincode field
#         district = request.POST.get('district')
#         service_required = request.POST.get('service_required')  # Updated field name
#         description = request.POST.get('description')
#         select_date = request.POST.get('select_date')

#         # Create CustomerServiceRequest instance with user information
#         service_request = CustomerServiceRequest.objects.create(user=user, first_name=first_name, last_name=last_name, email=email, phone=phone, address=address, city=city, pincode=pincode, district=district, service_required=service_required, description=description, select_date=select_date)  # Updated field names
        
#         # Redirect to a thank you page or display a success message
#         return HttpResponseRedirect(reverse('success_message'))
#     else:
#         # Fetch or create UserProfile object for the logged-in user
#         user_profile = UserProfile.objects.get(user=request.user)

#         service_request_id = service_request.id
#         # Pass UserProfile object to the context
#         context = {
#             'user_profile': user_profile,
#             'email': request.user.email,
#         'phone_number': user_profile.phone_number,
#         'service_request_id': service_request_id,
#         }

#         return render(request, 'submit_service_request.html', context)

from django.utils import timezone
from .models import CustomerServiceRequest  # Updated model import
from .models import UserProfile, ServiceType
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.http import HttpResponseForbidden

def submit_service_request(request):
    if request.method == 'POST':
        # Assuming you have a CustomUser model and user information is associated with the logged-in user
        user = request.user
        
        district = request.POST.get('district')
        select_date = request.POST.get('select_date')
        select_date = timezone.datetime.strptime(select_date, '%Y-%m-%d').date()
        district_requests_count = CustomerServiceRequest.objects.filter(district=district, select_date=select_date).count()  # Updated model reference
        if district_requests_count >= 20:
            return HttpResponseForbidden("The maximum number of service requests from your district for this date has been reached. Please select another date.")
        
        # Proceed with submitting the service request
        first_name = request.POST.get('first_name')  # Updated field name
        last_name = request.POST.get('last_name')    # Updated field name
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')  # Added pincode field
        district = request.POST.get('district')
        service_required = request.POST.get('service_required')  # Updated field name
        description = request.POST.get('description')
        select_date = request.POST.get('select_date')

        # Create CustomerServiceRequest instance with user information
        service_request = CustomerServiceRequest.objects.create(user=user, first_name=first_name, last_name=last_name, email=email, phone=phone, address=address, city=city, pincode=pincode, district=district, service_required=service_required, description=description, select_date=select_date)  # Updated field names
        
        # Redirect to a thank you page or display a success message
        return HttpResponseRedirect(reverse('success_message'))
    else:
        # Fetch or create UserProfile object for the logged-in user
        user_profile = UserProfile.objects.get(user=request.user)
        
        # Fetch all service types
        service_types = ServiceType.objects.all()
        # Assuming you want to retrieve the latest service request made by the user
        service_request = CustomerServiceRequest.objects.filter(user=request.user).latest('id')

        service_request_id = service_request.id
        # Pass UserProfile object and service_request to the context
        context = {
            'user_profile': user_profile,
            'email': request.user.email,
            'phone_number': user_profile.phone_number,
            'service_request_id': service_request_id,
            'service_types': service_types,
        }

        return render(request, 'submit_service_request.html', context)


def success_message(request):
    return render(request, 'successpage.html')


def plumber_reg(request):
     if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')  # Make sure this matches your form field name
        role = request.POST.get('role', None)  # Make sure this matches your form field name
        #user_type = request.POST['user_type']

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'plumber_reg.html', {'error_message': 'Email address is already in use.'})
        
        #if CustomUser.objects.filter(username=username).exists():
            #return render(request, 'registration.html', {'error_message': 'username is already in use.'})

        if password != confirm_password:
            # Handle password mismatch error
            return render(request, 'plumber_reg.html', {'error_message': 'Passwords do not match'})

        # Create a new user object
        user = CustomUser.objects.create_user(name=name, email=email, username=username, phone_number=phone_number, password=password, role=role)
        # You may want to do additional processing here if needed
        if role:
            user.role = role
            user.save() 

        return redirect('plumber_reg')  # Redirect to login page after successful registration

     return render(request,'plumber_reg.html')
    

def plumber_dashboard(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    context = {
        'user_profile': user_profile,
    }
    return render(request,'plumber_dashboard.html', context)


def deliverboy_reg(request):
     if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')  # Make sure this matches your form field name
        role = request.POST.get('role', None)  # Make sure this matches your form field name
        #user_type = request.POST['user_type']

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'deliverboy_reg.html', {'error_message': 'Email address is already in use.'})
        
        #if CustomUser.objects.filter(username=username).exists():
            #return render(request, 'registration.html', {'error_message': 'username is already in use.'})

        if password != confirm_password:
            # Handle password mismatch error
            return render(request, 'deliverboy_reg.html', {'error_message': 'Passwords do not match'})

        # Create a new user object
        user = CustomUser.objects.create_user(name=name, email=email, username=username, phone_number=phone_number, password=password, role=role)
        # You may want to do additional processing here if needed
        if role:
            user.role = role
            user.save() 

        return redirect('deliverboy_reg')  # Redirect to login page after successful registration

     return render(request,'deliverboy_reg.html')


def delivery_dashboard(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    context = {
        'user_profile': user_profile,
    }
    return render(request,'delivery_dashboard.html', context)


from django.shortcuts import render, redirect
from .models import PlumberAvailability

def add_plumber_availability(request):
    if request.method == 'POST':
        availability_date = request.POST.get('availability_date')
        city = request.POST.get('city')
        district = request.POST.get('district')
        # Assuming you have a CustomUser model and user information is associated with the logged-in user
        user = request.user
        plumber_availability = PlumberAvailability.objects.create(user=user, availability_date=availability_date, city=city, district=district)
        # You might want to add some additional logic here, such as redirecting to a success page or displaying a message
    
        return redirect('supage') # Redirect to a success page
    else:
        return render(request, 'add_plumber_availability.html')


# from django.shortcuts import render
# from .models import ServiceRequest

# def view_service_request(request):
#     if request.method == 'POST':
#         selected_city = request.POST.get('city')
        
#         # Filter service requests based on the selected city
#         service_requests = ServiceRequest.objects.filter(city=selected_city)
        
#          # Filter plumbers based on the selected city from PlumberAvailability model
#         plumbers = PlumberAvailability.objects.filter(city=selected_city)
#         # Pass the filtered service requests to the template
#         return render(request, 'service_request_details.html', {'service_requests': service_requests})
    
#     return render(request, 'submit_service_request.html')
# from django.shortcuts import render
# from django.http import HttpResponseForbidden
# from .models import ServiceRequest, PlumberAvailability

# def view_service_request(request):
#     if request.method == 'POST':
#         selected_city = request.POST.get('city')
        
#         # Filter service requests based on the selected city
#         service_requests = ServiceRequest.objects.filter(city=selected_city)
        
#         # Retrieve the logged-in user (assuming they are a plumber)
#         plumber = request.user
        
#         # Check if the logged-in plumber has availability in the selected city
#         if PlumberAvailability.objects.filter(user=plumber, city=selected_city).exists():
#             # User is authorized to view the service requests
#             return render(request, 'service_request_details.html', {'service_requests': service_requests})
#         else:
#             # User is not authorized to view the service requests
#             return HttpResponseForbidden("You are not authorized to view service requests for this city.")
    
#     return render(request, 'submit_service_request.html')


from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden  # Importing HttpResponseForbidden from django.http
from .models import CustomUser, PlumberAvailability, ServiceRequest

# Your view functions here

def view_service_request(request):
    if request.user.is_authenticated and request.user.role == 'Plumber':
        try:
            plumber_availability = PlumberAvailability.objects.get(user=request.user)
            plumber_city = plumber_availability.city
            service_requests = ServiceRequest.objects.filter(city=plumber_city)
            return render(request, 'service_request_details.html', {'service_requests': service_requests})
        except PlumberAvailability.DoesNotExist:
            return HttpResponseForbidden("Plumber's availability information not found.")
    else:
        return HttpResponseForbidden("You are not authorized to view service requests.")





from django.shortcuts import render
from .models import ServiceRequest

def service_request_details(request):
    # Retrieve all service requests
    service_requests = ServiceRequest.objects.all()
    
    # Pass the service requests to the template
    return render(request, 'service_request_details.html', {'service_requests': service_requests})


from django.shortcuts import render
from django.http import HttpResponse
from .models import Availability


def availability_form(request):
    if request.method == 'POST':
        # Handling form submission
        available_date = request.POST.get('available_date')
        cities = request.POST.get('cities')
        district = request.POST.get('district')
        user_id = request.POST.get('user_id')  # Assuming user_id is submitted via hidden input
        
        # Perform any additional processing or validation as needed
        
        # Example: Saving the data to the database (assuming you have a model named Availability)
        availability = Availability(available_date=available_date, cities=cities, district=district, user_id=user_id)
        availability.save()
        
        return HttpResponse('Availability submitted successfully!')
    else:
        # Render the form for GET requests
        return render(request, 'availability_form.html')
    
# views.py
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import CustomerServiceRequest

def confirm_request(request, request_id):
    service_request = CustomerServiceRequest.objects.get(pk=request_id)
    # Send confirmation email
    service_request.status = 'Confirmed'
    service_request.save()


    
    first_name = service_request.first_name
    last_name = service_request.last_name
    phone_number = service_request.phone

    send_mail(
        'Service Request Confirmed',
         f'Hi {first_name} {last_name},\n\nYour service request has been confirmed.\n\nThank you!',
        'annameenu00@gmail.com',  # Sender email address
        [service_request.email],  # Recipient email address
        fail_silently=False,
    )

    # Mark the service request as confirmed in the session
    # Mark the request as confirmed in the session
    confirmed_requests = request.session.get('confirmed_requests', [])
    if request_id not in confirmed_requests:
        confirmed_requests.append(request_id)
        request.session['confirmed_requests'] = confirmed_requests
        messages.success(request, f'Service request with ID {request_id} confirmed successfully.')
    else:
        messages.warning(request, f'Service request with ID {request_id} is already confirmed.')

    
    return redirect(reverse('service_request_details'))

def reject_request(request, request_id):
    service_request = CustomerServiceRequest.objects.get(pk=request_id)
    # Send rejection email
    service_request.status = 'Rejected'
    service_request.save()

    send_mail(
        'Service Request Rejected',
        'Your service request has been rejected.',
        'annameenu00@gmail.com',  # Sender email address
        [service_request.email],  # Recipient email address
        fail_silently=False,
    )
    # Additional logic (e.g., updating database, etc.)
    # Redirect back to the page where the request was made
    return redirect(reverse('service_request_details'))


def supage(request):
    return render(request, 'supage.html')




from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import ServiceRequest

def delete_request(request, request_id):
    # Retrieve the service request object from the database
    service_request = get_object_or_404(CustomerServiceRequest, pk=request_id)
    
    # Delete the service request
    service_request.delete()
    
    # Return a JSON response indicating success
    return JsonResponse({'message': 'Service request deleted successfully'}, status=200)


# from django.shortcuts import render
# from .models import CustomerServiceRequest  # Import the CustomerServiceRequest model

# def service_request_details(request):
#     # Fetch all service requests from the database
#     service_requests = CustomerServiceRequest.objects.all()

#     # Pass the service requests to the template for rendering
#     return render(request, 'service_request_details.html', {'service_requests': service_requests})

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import CustomerServiceRequest

# @login_required
# def service_request_details(request):
#     if request.method == 'POST':
#         # Handle payment button click
#         request_id = request.POST.get('request_id')
#         return redirect('enter_payment', service_request_id=request_id)

#     elif request.method == 'GET' and 'work_status' in request.GET:
#         # Handle work status update
#         request_id = request.GET.get('request_id')
#         service_request = CustomerServiceRequest.objects.get(id=request_id)
#         service_request.work_status = 'Completed'
#         service_request.save()
#         return redirect('service_request_details')  # Redirect to the same page after completion

#     # Fetch all service requests from the database
#     service_requests = CustomerServiceRequest.objects.all()

#     # Pass the service requests to the template for rendering
#     return render(request, 'service_request_details.html', {'service_requests': service_requests})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomerServiceRequest

@login_required
def service_request_details(request):
    if request.method == 'POST' and 'complete_request' in request.POST:
        # Handle completing the service request
        request_id = request.POST.get('request_id')
        service_request = CustomerServiceRequest.objects.get(id=request_id)
        service_request.work_status = 'Completed'
        service_request.save()

    # Fetch all service requests from the database
    service_requests = CustomerServiceRequest.objects.all()
    
     # Get the list of confirmed request IDs from the session
    confirmed_requests = request.session.get('confirmed_requests', [])
    # Pass the service requests to the template for rendering
    return render(request, 'service_request_details.html', {'service_requests': service_requests, 'confirmed_requests': confirmed_requests})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomerServiceRequest
from .models import UserProfile


@login_required
def service_request_history(request):
    # Retrieve service requests associated with the logged-in user
    user = request.user
    service_requests = CustomerServiceRequest.objects.filter(user=user)
    
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    # Pass the service requests to the template for rendering
    context = {
        'service_requests': service_requests,
        'user_profile': user_profile,
    }
    
    return render(request, 'service_request_history.html', context)



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment, CustomerServiceRequest

@login_required
def enter_payment(request, service_request_id):
    if request.method == 'POST':
        amount = request.POST.get('amount')  # Retrieve amount from the form data
        if amount is not None:  # Ensure amount is provided
            # Create a new Payment object
            payment = Payment.objects.create(
                amount=amount,
                service_request_id=service_request_id,
                user=request.user
            )
            # Redirect to a success page or any other appropriate page
            return redirect('payment_success')
        else:
            # Handle case where amount is not provided
            return render(request, 'enter_payment.html', {'service_request_id': service_request_id})

    else:
        # Fetch service request details
        try:
            service_request = CustomerServiceRequest.objects.get(id=service_request_id)
        except CustomerServiceRequest.DoesNotExist:
            # Handle case where service request does not exist
            return render(request, 'enter_payment.html', {'error_message': 'Service request does not exist.'})
        
        # Pass service request details to the context
        context = {
            'service_request': service_request,
            'service_request_id': service_request_id,
        }
        
        return render(request, 'enter_payment.html', context)

# @login_required
# def payment_details(request):
#     if request.method == 'POST':
#         request_id = request.POST.get('request_id')
#         service_request = CustomerServiceRequest.objects.get(id=request_id)
#         # Do something with the payment details
#         # You can pass the payment details to a template and render it here
#         return render(request, 'payment_details.html', {'service_request': service_request})


def payment_success(request):
    # Logic to render the payment success page
    return render(request, 'payment_success.html')

# views.py

# from django.shortcuts import render
# from .models import Payment

# def payment_details(request):
#     # Assuming you have a single Payment object or you want to display details of the latest payment
#     latest_payment = Payment.objects.latest('timestamp')  # Assuming 'timestamp' is the field representing when the payment was made
#     context = {
#         'latest_payment': latest_payment,
#     }
#     return render(request, 'payment_details.html', context)




# from django.shortcuts import render
# from .models import Payment

# def payment_details(request):
#     # Fetch all payment details
#     user_payments = Payment.objects.filter(user=request.user)

#     # Pass payment details to the template
#     return render(request, 'payment_details.html', {'user_payments': user_payments})



# views.py
# from django.shortcuts import render
# from .models import Payment, CustomerServiceRequest

# def payment_details(request):
#     # Fetch confirmed and completed service requests for the logged-in user
#     user_service_requests = CustomerServiceRequest.objects.filter(user=request.user, status='Confirmed', work_status='Completed')
    
#     # Fetch payment details corresponding to the confirmed and completed service requests
#     user_payments = Payment.objects.filter(service_request__in=user_service_requests)

#     # Pass payment details to the template
#     return render(request, 'payment_details.html', {'user_payments': user_payments})


from django.shortcuts import render
from .models import Payment
from .models import UserProfile

def payment_details(request, service_request_id):
    # Fetch payment details associated with the given service_request_id
    user_payments = Payment.objects.filter(service_request_id=service_request_id)
    
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    # Pass payment details to the template
    context = {
        'user_payments': user_payments,
        'user_profile': user_profile,

    }
    return render(request, 'payment_details.html', context)


from django.shortcuts import redirect, get_object_or_404
from .models import CustomerServiceRequest

def complete_service_request(request, request_id):
    if request.method == 'POST':
        service_request = get_object_or_404(CustomerServiceRequest, id=request_id)
        service_request.work_status = 'Completed'
        service_request.save()
    return redirect('service_request_details')





# from django.conf import settings

# from django.http import JsonResponse
# import razorpay

# def initiate_payment(request):
#     if request.method == 'POST':
#         amount = request.POST.get('amount')  # Get the amount from the request
#         client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

#         # Create a Razorpay order
#         payment_data = {
#             'amount': int(amount) * 100,  # Razorpay accepts amount in paisa, so convert to paise
#             'currency': 'INR',
#             'receipt': 'receipt_order_{}'.format(timezone.now().timestamp()),
#             'payment_capture': 1  # Auto capture payment
#         }
#         order = client.order.create(data=payment_data)

#         return JsonResponse(order)
#     return JsonResponse({'error': 'Invalid request'})


from django.http import JsonResponse
import razorpay
from django.conf import settings
from django.utils import timezone

def initiate_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')

        if amount is None:
            return JsonResponse({'error': 'Amount parameter is missing'})

        try:
            amount_in_paise = int(amount) * 100  # Convert amount to paise
        except ValueError:
            return JsonResponse({'error': 'Invalid amount provided'})

        if amount_in_paise < 100:
            return JsonResponse({'error': 'Minimum amount should be 1 INR'})

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        payment_data = {
            'amount': amount_in_paise,
            'currency': 'INR',
            'receipt': f'receipt_order_{timezone.now().timestamp()}',
            'payment_capture': 1
        }

        try:
            order = client.order.create(data=payment_data)
            return JsonResponse({'order_id': order['id'], 'amount': order['amount']})
        except razorpay.errors.BadRequestError as e:
            return JsonResponse({'error': str(e)})
        except Exception as e:
            return JsonResponse({'error': 'An error occurred while processing your request'})

    return JsonResponse({'error': 'Invalid request'})




# def payment_confirmation(request):
#     payment_amount = request.GET.get('amount')  # Get the payment amount from the query parameters
#     return render(request, 'payment_confirmation.html', {'payment_amount': payment_amount})

from django.shortcuts import render, get_object_or_404
from .models import CustomerServiceRequest
from django.core.mail import send_mail
from .models import UserProfile

def payment_confirmation(request):
    # Assuming you have a way to identify the logged-in user
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    logged_in_user = request.user
    
    # Fetch the latest service request made by the logged-in user
    service_request = CustomerServiceRequest.objects.filter(user=logged_in_user).latest('id')
    
    # Assuming you have the payment_amount available
    payment_amount = request.GET.get('amount', 0)  # Adjust this to fetch the payment amount correctly
    
    # Send payment successful email to the user
    subject = 'Payment Successful'
    message = f'Hi {service_request.first_name},\n\nYour payment of {payment_amount} has been successfully processed.\n\nThank you for using our service!'
    from_email = 'annameenu00@gmail.com'  # Replace with your email address
    to_email = service_request.email  # Assuming the user's email is stored in the service request object
    send_mail(subject, message, from_email, [to_email])

    # Pass the service request and payment amount to the template
    context = {
        'service_request': service_request,
        'payment_amount': payment_amount,
        'service_request_id': service_request.id, 
        'user_profile': user_profile,
    }
    
    return render(request, 'payment_confirmation.html', context)



# def view_bill(request):
#     amount = request.GET.get('amount')
#     context = {
#         'amount': amount
#     }
#     return render(request, 'view_bill.html', context)


# from django.shortcuts import render
# from .models import CustomerServiceRequest  # Import your CustomerServiceRequest model

# def view_bill(request):
#     # Fetch the payment amount from the request
#     amount = request.GET.get('amount')
    
#     # Fetch service request details (replace this query with your own)
#     customer_service_requests = CustomerServiceRequest.objects.all()  # Example query
    
#     # Pass service request details and payment amount to the template
#     context = {
#         'customer_service_requests': customer_service_requests,
#         'amount': amount
#     }
#     return render(request, 'view_bill.html', context)

# from django.shortcuts import render
# from .models import CustomerServiceRequest  # Import your CustomerServiceRequest model

# def view_bill(request):
#     # Assuming you have a way to identify the logged-in user
#     # For example, if you're using Django's authentication system
#     logged_in_user = request.user
    
#     # Fetch service request details of the logged-in user
#     customer_service_requests = CustomerServiceRequest.objects.filter(user=logged_in_user)
    
#     # Pass service request details to the template
#     context = {
#         'customer_service_requests': customer_service_requests
#     }
#     return render(request, 'view_bill.html', context)




# from django.shortcuts import render, get_object_or_404
# from .models import CustomerServiceRequest

# def view_bill(request, service_request_id):
#     # Retrieve the service request details based on the provided service_request_id
#     service_request = get_object_or_404(CustomerServiceRequest, id=service_request_id)
    
#     # Get the payment amount from the request's GET parameters
#     payment_amount = request.GET.get('amount')
    
#     # Pass the service request details and payment amount to the template for rendering
#     context = {
#         'service_request': service_request,
#         'payment_amount': payment_amount,
#     }
    
#     return render(request, 'view_bill.html', context)




from django.shortcuts import render, get_object_or_404
from .models import CustomerServiceRequest
from django.contrib.auth.decorators import login_required
from .models import CustomerServiceRequest
from .models import UserProfile  # Import your UserProfile model

def view_bill(request, service_request_id):
    # Retrieve the service request details based on the provided service_request_id
    service_request = get_object_or_404(CustomerServiceRequest, id=service_request_id)
    

    # Fetch the logged-in user's profile details
    user_profile = UserProfile.objects.get(user=request.user)
    # Get the payment amount from the request's GET parameters
    payment_amount = request.GET.get('amount')
    
    # Pass the service request details and payment amount to the template for rendering
    context = {
        'service_request': service_request,
        'payment_amount': payment_amount,
        'user_profile': user_profile,
        'payment_amount': request.GET.get('amount'),  # Retrieve payment amount from URL parameters
    }
    
    return render(request, 'view_bill.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PlumberJob

@login_required
def plumber_job_application(request):
    if request.method == 'POST':
        # Handle form submission
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        full_address = request.POST.get('full_address')
        highest_education = request.POST.get('highest_education')
        languages_known = request.POST.get('languages_known')
        years_of_experience = request.POST.get('years_of_experience')
        resume = request.FILES.get('resume')

        # Save the form data to the database (you may want to add more validation)
        PlumberJob.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            gender=gender,
            full_address=full_address,
            highest_education=highest_education,
            languages_known=languages_known,
            years_of_experience=years_of_experience,
            resume=resume
        )

        # Redirect to a success page or update the current page as needed
        return redirect('success_page')

    return render(request, 'plumber_job.html')

# views.py



from django.shortcuts import render, redirect
from .models import ServiceType

def add_service_type(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            ServiceType.objects.create(name=name)
            return redirect('submit_service_request')
    return render(request, 'add_service_type.html')

from django.shortcuts import render
from .models import ServiceType

def service_types_view(request):
    service_types = ServiceType.objects.all()
    context = {'service_types': service_types}
    return render(request, 'service_types_list.html', context)

from django.shortcuts import render
from .models import ServiceType

def service_types_list(request):
    service_types = ServiceType.objects.all()
    return render(request, 'service_types_list.html', {'service_types': service_types})


# from django.shortcuts import redirect, get_object_or_404
# from .models import ServiceType

# def update_service_type(request, pk):
#     service_type = get_object_or_404(ServiceType, pk=pk)
#     if request.method == 'POST':
#         new_name = request.POST.get('name')  # Assuming the new name is passed in the POST data
#         service_type.name = new_name
#         service_type.save()
#         return redirect('service_types_list')  # Redirect back to the service types list page
#     return redirect('service_types_list')  # If it's a GET request or any other method, simply redirect back


from django.shortcuts import render, get_object_or_404, redirect
from .models import ServiceType

def update_service_type(request, pk):
    service_type = get_object_or_404(ServiceType, pk=pk)
    
    if request.method == 'POST':
        # Update the service type name
        new_name = request.POST.get('name')
        service_type.name = new_name
        service_type.save()
        
        return redirect('service_types_list')  # Redirect to the service types list page
    
    return render(request, 'update_service_type.html', {'service_type': service_type})



def upload_image(request):
    return render(request, 'upload.html')

from django.shortcuts import render
from .models import Order
from .models import UserProfile

def available_orders(request):
    # Query the database for all orders
    all_orders = Order.objects.all()

     # Fetch or create user profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Pass orders and user profile data to the template
    context = {
        'available_orders': all_orders,
        'user_profile': user_profile,
    }


    # # Pass all_orders data to the template
    # return render(request, 'availableorders.html', {'available_orders':all_orders})
 # Render the template with context data
    return render(request, 'availableorders.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Order
import random
import logging

logger = logging.getLogger(__name__)




@login_required(login_url='login')
def delivery_update_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        delivery_status = request.POST.get('delivery_status')

        if delivery_status == 'Delivered':
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            send_mail(
                'Delivery Confirmation OTP',
                f'Your OTP for order {order.id} is: {otp}',
                settings.EMAIL_HOST_USER,
                [order.user.email],
                fail_silently=False,
            )

            # Store OTP and order ID in session for later verification
            request.session['delivery_status_otp'] = otp
            request.session['otp_order_id'] = str(order_id)

            messages.info(request, 'OTP has been sent to the customer for delivery confirmation.')
            return redirect('otp_verification', order_id=order_id)  # Redirect to OTP verification page with order_id

        else:
            order.delivery_status = delivery_status
            order.save()
            messages.success(request, 'Delivery status updated successfully.')
            return redirect('available_orders')  # Redirect to the delivery boy dashboard

    return render(request, "deliveryupdatestatus.html", {'order': order})

@login_required(login_url='login')
def otp_verification(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        submitted_otp = request.POST.get('otp')
        session_order_id = request.session.get('otp_order_id')

        if str(order_id) == session_order_id and submitted_otp == request.session.get('delivery_status_otp'):
            # OTP is correct, update the delivery status
            order.delivery_status = 'Delivered'
            order.save()

            # Clear OTP and order ID from session
            del request.session['delivery_status_otp']
            del request.session['otp_order_id']

            # Redirect to a success page or the delivery details page
            messages.success(request, 'Order marked as delivered successfully.')
            return redirect('available_orders')
        else:
            # OTP is incorrect, render the OTP verification page with error message
            messages.error(request, 'Incorrect OTP. Please try again.')
            return render(request, 'otp_verification.html', {'order': order, 'error_message': 'Incorrect OTP. Please try again.'})

    else:
        return render(request, 'otp_verification.html', {'order':order})
    

from django.http import JsonResponse

def confirm_service_request(request, request_id):
    # Here you would implement logic to confirm the request in your database
    # For demonstration purposes, let's assume it's successful
    # You can change 'Confirmed' to whatever status you want to set
    # Also, make sure to implement proper error handling and authentication checks
    try:
        service_request = CustomerServiceRequest.objects.get(id=request_id)
        service_request.status = 'Confirmed'
        service_request.save()
        return JsonResponse({'success': True})
    except CustomerServiceRequest.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Service request not found'})
