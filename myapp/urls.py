
from django.urls import path
from.import views
from django.contrib.auth import views as auth_views

from .views import add_to_cart, remove_from_cart,view_cart,increase_cart_item,decrease_cart_item,fetch_cart_count,create_order,handle_payment,checkout,bill_invoice,job_application,success_page,applicationz,submit_service_request,add_plumber_availability,availability_form,delete_request,service_request_history,enter_payment,payment_details,initiate_payment,view_bill,plumber_job_application,add_service_type,service_types_view,upload_image,confirm_service_request

urlpatterns = [
   path('',views.index,name="index"),
   path('registration/',views.registration,name="registration"),
   path('stockmgr_registration/',views.stockmgr_registration,name="stockmgr_registration"),
   path('login/',views.user_login,name="login"),
   path('home/',views.home,name="home"),
   path('logout/', views.logout_view, name='logout'),
   path('stocks/',views.stocks,name='stocks'),
   path('addproduct/',views.add_product,name='addproduct'),
   path('adminn/',views.adminn,name='adminn'),
   path('viewproduct/',views.view_product,name="viewproduct"),
   path('viewproductss/',views.view_productss,name="viewproductss"),
   #path('showers/',views.product_grid,name="showers"),
   path('editproduct/', views.edit_product, name='editproduct'),
   path('user-list/',views.user_list,name='user-list'),
   path('delete-user/<int:user_id>/', views.delete_user, name='delete-user'),
   path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
   path('profile/',views.profile,name='profile'),
   path('search/', views.search_products, name='search_products'),
   path('search_full_pedestal_basins/', views.search_full_pedestal_basins, name='search_full_pedestal_basins'),


   

   path('product/<int:product_id>/', views.product_detail, name='product_detail'),


   path('shower/built-in/', views.built_in_showers, name='built_in_showers'),
    path('shower/standalone/', views.standalone_showers, name='standalone_showers'),
    path('basins/full-pedestal/', views.full_pedestal_basins, name='full_pedestal_basins'),
    path('basins/semi-pedestal/', views.semi_pedestal_basins, name='semi_pedestal_basins'),

   path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove-from-cart'),
    path('cart/', view_cart, name='cart'),
    path('increase-cart-item/<int:product_id>/', increase_cart_item, name='increase-cart-item'),
    path('decrease-cart-item/<int:product_id>/', decrease_cart_item, name='decrease-cart-item'),
    path('fetch-cart-count/', fetch_cart_count, name='fetch-cart-count'),
    path('create-order/', create_order, name='create-order'),
    path('handle-payment/', handle_payment, name='handle-payment'),
    path('checkout/', checkout, name='checkout'),
    path('billinvoice/', bill_invoice, name='bill_invoice'),

    path('apply/', job_application, name='apply'),
    path('success/', views.success_page, name='success_page'),
    path('applicationz/', applicationz, name='applicationz'),
    path('submit_service_request/', submit_service_request, name='submit_service_request'),
    path('plumber_reg/',views.plumber_reg,name="plumber_reg"),
    path('plumber_dashboard/',views.plumber_dashboard,name='plumber_dashboard'),
    path('deliverboy_reg/',views.deliverboy_reg,name="deliverboy_reg"),
    path('delivery_dashboard/',views.delivery_dashboard,name='delivery_dashboard'),
    path('add_plumber_availability/', add_plumber_availability, name='add_plumber_availability'),
    path('success_message/', views.success_message, name='success_message'),
    path('delete-request/<int:request_id>/', delete_request, name='delete_request'),
    
    

     path('submit_service_request/', views.view_service_request, name='view_service_request'),
     path('view_service_request/', views.view_service_request, name='view_service_request'),
     path('service_request_details/', views.service_request_details, name='service_request_details'),
     path('view_service_request/', views.submit_service_request, name='view_service_request'),
     path('supage/', views.supage, name='supage'),
    path('confirm-request/<int:request_id>/', views.confirm_request, name='confirm_request'),
    path('reject-request/<int:request_id>/', views.reject_request, name='reject_request'),
    # Add other URL patterns as needed
    path('availability/form/', availability_form, name='availability_form'),


    path('service-request-history/', service_request_history, name='service_request_history'),
    path('submit-service-request/', submit_service_request, name='submit_service_request'),
    path('enter-payment/<int:service_request_id>/', views.enter_payment, name='enter_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
     path('payment-details/', payment_details, name='payment_details'),
     path('payment-details/<int:service_request_id>/', views.payment_details, name='payment_details'),

    path('complete_service_request/<int:request_id>/', views.complete_service_request, name='complete_service_request'),
     path('payment-details/<int:service_request_id>/', payment_details, name='payment_details'),

    
     path('initiate_payment/', initiate_payment, name='initiate_payment'),

    #  path('payment-successful/', views.payment_successful, name='payment_successful'),
    #  path('view-bill/<int:amount_paid>/', view_bill, name='view_bill'),
    
     path('payment_confirmation/', views.payment_confirmation, name='payment_confirmation'),
        # path('view_bill/', views.view_bill, name='view_bill'),
        path('view-bill/<int:service_request_id>/', view_bill, name='view_bill'),

        path('plumber_job/', plumber_job_application, name='plumber_job_application'),
        
     path('add_service_type/', add_service_type, name='add_service_type'),
     path('service-types/', service_types_view, name='service_types'),
     path('service-types/', views.service_types_list, name='service_types_list'),
     path('service-types/', views.service_types_view, name='service_types_list'),
    path('service-types/<int:pk>/update/', views.update_service_type, name='update_service_type'),

    path('upload/', upload_image, name='upload_image'),
    path('availableorders/', views.available_orders, name='available_orders'),
    path('deliveryupdatestatus/<int:order_id>/', views.delivery_update_status, name='delivery_update_status'),
    path('otp-verification/<int:order_id>/', views.otp_verification, name='otp_verification'),
     path('confirm-service-request/<int:request_id>/', confirm_service_request, name='confirm_service_request'),

    path('accounts/login/',views.user_login,name="login"),

    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset_done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
  
]