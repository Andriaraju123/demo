from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Register)
admin.site.register(Addproduct)
admin.site.register(Addcategory)
# admin.site.register(Orderdetails)
admin.site.register(Order)
admin.site.register(Order_sec)
# admin.site.register(orderitem)
admin.site.register(PasswordReset)
admin.site.register(mycart)
admin.site.register(wishlist)
admin.site.register(Sellerproduct)
admin.site.register(charge)
admin.site.register(second_hand_books)
admin.site.register(Books)

admin.site.register(Empregister)
admin.site.register(Registered_emp)
admin.site.register(passdelivery)
admin.site.register(completeddelivery)

