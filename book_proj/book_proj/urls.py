"""
URL configuration for book_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from book_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('index',views.index),
    path('about',views.about),
    path('contact',views.contact),

# --------------- LOGIN AND REGISTER -----------------

    path('reg_opt',views.reg_opt),
    path('login',views.login),
    path('reg',views.reg),
    path('reg1',views.reg1),



# --------------- USER SIDE -----------------
    path('welcome',views.welcome),

# --------------- FORGOT PASSWORD -----------------

    path('forgot', views.forgot_password_user, name="forgot"),
    path('reset/<token>', views.reset_password_user, name='reset_password'),


# --------------- EDIT PROFILE -----------------

    path('profile',views.prof),
    path('edit_profile/<int:d>',views.profedit),
    path('profupdate/<int:d>',views.profupdate),


# --------------- USER AS SELLER -----------------
    path('seller_userhome',views.seller_userhome),

    path('seller_displaycategory',views.seller_displaycategory),
    path('seller_addcategory', views.seller_addcategory),

    path('seller_addproduct/<int:d>',views.seller_addproduct),

    path('user_request',views.user_request),
    path('req/<int:d>',views.req),

    path('orderlist_sec',views.orderlist_sec),

    path('razorpay/<int:s_price>/<int:pk>/',views.razorpay,name='razorpay'),
    path('success2/<int:id>', views.success2,name='success2'),



# --------------- USER AS BUYER -----------------
    path('userhome',views.userhome),

# --------------- VIEW BOOKS -----------------

    path('shop',views.viewpro),
    path('secondhandbooks',views.secondhandbooks),
    # path('single_product',views.single_product),
    path('details/<int:d>/',views.details),

# --------------- SEARCH -----------------

    path('spec/<int:d>', views.specific),
    path('search', views.search),
    path('searchlang', views.searchlang),

# ---------------  CART -----------------

    path('cart/<int:d>', views.cart),
    path('mycart', views.viewcart),

    path('minuscart/<int:de>', views.minuscart),
    path('pluscart/<int:de>', views.pluscart),

    path('delete_cart/<int:d>', views.deletepro),

# --------------- WISHLIST -----------------

    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('add_to_wishlist_second/<int:product_id>/', views.add_to_wishlist_second, name='add_to_wishlist_second'),
    path('Wishlist/', views.viewWishlist),
    path('remove_wl/<int:d>', views.removepro),

# --------------- PAYMENT -----------------
# --------------- SINGLE BOOKING -----------------

    path('singles/<int:d>/', views.singles, name='single'),
    path('single_booking/<int:product_id>', views.single_booking, name='single_booking'),
    path('single_razor/<int:product_id>', views.single_razor, name='single_razor'),
    path('razor_pay/<int:price>', views.razorpaycheck),


    path('singles_sec/<int:d>/', views.singles_sec, name='singles_sec'),
    path('single_booking_sec/<int:product_id>', views.single_booking_sec, name='single_booking_sec'),

    path('single_razor_sec/<int:product_id>', views.single_razor_sec, name='single_razor_sec'),
    path('razor_pay_sec/<int:price>', views.razorpaycheck_sec),

# --------------- MULTIPLE BOOKING -----------------

    path('checkout', views.checkout, name='checkout'),
    path('multiple_booking', views.multiple_booking, name='multiple_booking'),
    path('multiple_razor', views.multiple_razor, name='multiple_razor'),
    path('razor_pay2', views.razorpaycheck2),
    # path('multiple_checkout/<int:d>',views.multiple_checkout),

    path('payment',views.payment),
    path('success', views.success, name='success'),


# --------------- VIEW ORDER -----------------
    path('user_orders', views.user_orders),




    # path('myrequest',views.myrequest),

    path('reqstatus/<wal>', views.reqstatus, name="reqstatus"),
    # path('delete_request/<int:d>/', views.delete_request, name='delete_request')
    path('req_addbook/<int:d>', views.req_addbook),

# --------------- ADMIN SIDE -----------------
    path('adminhome',views.adminhome),

# --------------- ADD AND VIEW CATEGORIES [ADMIN] -----------------
    path('add_category',views.add_category),
    path('display_category',views.viewcategory),
    path('categories',views.categories),

    path('add_product',views.add_product),
    path('bookslist/<int:d>/', views.viewbook),  # Named URL for viewing books





    # path('add_product',views.add_product),
    # path('bookslist/<int:d>/',views.viewbook),

# --------------- UPDATE PRODUCT DETAILS -----------------
    path('update_pro/<int:d>/', views.update_pro),
    path('update/<int:d>', views.update),


    path('delete_product/<int:d>/', views.delete_product, name='delete_product'),
    # path('update/<int:pk>/', views.update_product, name='update_product'),

    path('userlist',views.userlist),
    path('booking', views.userbooking),
    path('requestlist', views.requestlist),
    path('viewcharge', views.viewcharge),

    # path('orders',views.orders),
    # path('mycart',views.checkout),
    path('add_product/<int:d>',views.add),
    path('add_product',views.add_product),

    path('statusup/<wal>', views.statusup, name="statusup"),

    path('statusup_sec/<wal>', views.statusup_sec, name="statusup_sec"),



# --------------- EMPLOYEE -----------------
# --------------- LOGIN AND REGISTER [EMP] -----------------

    path('emp_reg',views.employeeregister),
    path('employeeregister',views.employeeregister),
    path('employeehome',views.conf_bookreq),
    path('emplist',views.Verify_workers),
    path('emp_status/<int:d>', views.emp_status),
    path('approve_item/<int:id>', views.approve_item),
    path('veri_emp_dele/<int:d>', views.veri_emp_dele),
    path('admin_delivery_send/<int:id>', views.admin_delivery_send),
    path('statusup2/<int:booking_id>',views.statusup2, name='statusup2'),
    path('delivery_completed/<int:d>', views.delivery_completed),
    # path('viewworks', views.viewworks),
    path('view_mydeliveries', views.view_mydeliveries),
    path('cur_status', views.cur_status),


#--------------------------LOGOUT---------------------------

    path('logout', views.logout),
    path('logout_ad', views.logout_ad),
    path('logout_emp', views.logout_emp),

    # path('del/<int:d>',views.delete),



    # path('Wishlist',views.viewWishlist),




]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
