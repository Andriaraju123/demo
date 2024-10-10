from django.db import models

# Create your models here.
class Register(models.Model):
    email = models.EmailField(unique=True)
    name=models.CharField(max_length=20)
    username=models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    address=models.CharField(max_length=200)
    phone=models.IntegerField()
    place=models.CharField(max_length=50)
    pin=models.IntegerField()
class Addcategory(models.Model):
    category = models.CharField(max_length=100)
class Addproduct(models.Model):
    categry = models.ForeignKey(Addcategory,on_delete=models.CASCADE)
    book_name=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    publisher=models.CharField(max_length=100)
    description=models.CharField(max_length=200)
    price=models.IntegerField()
    image1=models.FileField()
    image2=models.FileField()
    language=models.CharField(max_length=50)

class Sellerproduct(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, null=True)
    s_categry = models.ForeignKey(Addcategory, on_delete=models.CASCADE)
    s_book_name = models.CharField(max_length=100)
    s_author = models.CharField(max_length=100)
    s_publisher = models.CharField(max_length=100)
    s_description = models.CharField(max_length=200)
    s_price = models.IntegerField()
    s_image1 = models.FileField()
    s_image2 = models.FileField()
    s_image3 = models.FileField()
    s_language = models.CharField(max_length=50)
    s_year = models.IntegerField()
    s_page = models.IntegerField()
    order_status = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
    )
    status = models.CharField(max_length=150, choices=order_status, default='Pending')



class mycart(models.Model):
    categry = models.ForeignKey(Addcategory, on_delete=models.CASCADE)
    products=models.ForeignKey(Addproduct,on_delete=models.CASCADE)
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    total_price=models.IntegerField()
    delivered=models.BooleanField(default=False)

class Books(models.Model):
    adbooks = models.ForeignKey(Addproduct, on_delete=models.CASCADE, null=True)
    usbooks = models.ForeignKey(Sellerproduct, on_delete=models.CASCADE, null=True)


class wishlist(models.Model):
        user = models.ForeignKey(Register, on_delete=models.CASCADE)
        addproduct = models.ForeignKey(Addproduct, null=True, blank=True, on_delete=models.CASCADE)
        sellerproduct = models.ForeignKey(Sellerproduct, null=True, blank=True, on_delete=models.CASCADE)




# class Orderdetails(models.Model):
#     det=models.ForeignKey(Register, on_delete=models.CASCADE)
#     place=models.CharField(max_length=20)
#     pincode=models.IntegerField()

# class sellerAddproduct(models.Model):
#     s_categry = models.ForeignKey(Addcategory,on_delete=models.CASCADE)
    # s_book_name=models.CharField(max_length=100)
    # s_author=models.CharField(max_length=100)
    # s_publisher=models.CharField(max_length=100)
    # s_description=models.CharField(max_length=200)
    # s_price=models.IntegerField()
    # s_image1=models.FileField()
    # s_image2=models.FileField()
    # s_image3=models.FileField()
    # s_language=models.CharField(max_length=50)
    # s_year=models.IntegerField()
    # s_page=models.IntegerField()


class Order(models.Model):
    customer = models.ForeignKey(Register,on_delete=models.CASCADE)
    cart = models.ForeignKey(mycart, on_delete=models.CASCADE, null=True, blank=True)  # Adjust according to your requirements
    product = models.ForeignKey(Addproduct,on_delete=models.CASCADE)
    so_fname = models.CharField(max_length=20,null=False)
    so_email = models.EmailField(null=False)
    so_phone = models.IntegerField(null=False)
    so_address = models.TextField(null=False)
    so_district = models.CharField(max_length=20,null=False)
    so_pincode = models.IntegerField(null=False)
    add_message = models.CharField(max_length=250)
    order_status = (
        ('Pending','Pending'),
        ('Accepted', 'Accepted'),
        ('Out For Shipping','Out For Shipping'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
    )
    status = models.CharField(max_length=150,choices=order_status,default='Pending')
    quantity = models.IntegerField(null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=150, null=True)
    order_id = models.CharField(max_length=150, null=False)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order_sec(models.Model):
    s_customer = models.ForeignKey(Register,on_delete=models.CASCADE)
    s_product = models.ForeignKey(Sellerproduct,on_delete=models.CASCADE)
    s_fname = models.CharField(max_length=20,null=False)
    s_email = models.EmailField(null=False)
    s_phone = models.IntegerField(null=False)
    s_address = models.TextField(null=False)
    s_district = models.CharField(max_length=20,null=False)
    s_pincode = models.IntegerField(null=False)
    s_add_message = models.CharField(max_length=250)
    s_order_status = (
        ('Pending','Pending'),
        ('Out For Shipping','Out For Shipping'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
    )
    s_status = models.CharField(max_length=150,choices=s_order_status,default='Pending')
    s_quantity = models.IntegerField(null=False)
    s_total_price = models.FloatField(null=False)
    s_payment_mode = models.CharField(max_length=150, null=False)
    s_payment_id = models.CharField(max_length=150, null=True)
    s_order_id = models.CharField(max_length=150, null=False)
    s_tracking_no = models.CharField(max_length=150, null=True)
    s_created_at = models.DateTimeField(auto_now_add=True)
    s_updated_at = models.DateTimeField(auto_now=True)

class charge(models.Model):
    seller = models.ForeignKey(Register, on_delete=models.CASCADE, null=True)
    sec_book=models.ForeignKey(Sellerproduct, on_delete=models.CASCADE, null=True)
    fee = models.FloatField(null=True)
    payment_mode = models.CharField(max_length=200, default='Razor_pay', null=True)
# class orderitem(models.Model):
#     orderdet = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Addproduct, on_delete=models.CASCADE)
#     price = models.FloatField(null=False)
#     quantity = models.IntegerField(null=False)

# class Request(models.Model):
#     user = models.ForeignKey(Register, on_delete=models.CASCADE, null=True)
#     prod = models.ForeignKey(sellerAddproduct, on_delete=models.CASCADE, null=True)
#     order_status = (
#         ('Pending', 'Pending'),
#         ('Approved', 'Approved'),
#         ('Declined', 'Declined'),
#     )
#     status = models.CharField(max_length=150, choices=order_status, default='Pending')

class PasswordReset(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    #security
    token=models.CharField(max_length=4)


class second_hand_books(models.Model):
    books = models.ForeignKey(Sellerproduct, on_delete=models.CASCADE, null=True)

class Empregister(models.Model):
    Name = models.CharField(max_length=20)
    User_name = models.CharField(max_length=20)
    Email = models.EmailField(unique=True)
    Image = models.FileField()
    CV = models.FileField()
    Proof=models.FileField()
    e_licenece = models.FileField()
    Address = models.CharField(max_length=30)
    District = models.CharField(max_length=20)
    State = models.CharField(max_length=20)
    Password = models.CharField(max_length=20)
    Phone = models.IntegerField()

class Registered_emp(models.Model):
    e_name = models.CharField(max_length=20)
    e_image = models.FileField()
    e_cv = models.FileField(upload_to='pdfs/', null=True, blank=True)
    e_proof = models.FileField(upload_to='pdfs/', null=True, blank=True)
    E_licenece = models.FileField(upload_to='pdfs/', null=True, blank=True)
    e_email = models.EmailField(max_length=200,unique=True)
    e_address = models.CharField(max_length=20)
    e_District = models.CharField(max_length=20)
    e_State = models.CharField(max_length=20)
    e_number = models.IntegerField()
    e_user_name = models.CharField(max_length=20,unique=True)
    e_password = models.CharField(max_length=20, unique=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True, null=True)
    e_orderstatus = (
        ('Free', 'Free'),
        ('In work', 'In work'),
        ('Off duty', 'Off duty')

    )
    e_status = models.CharField(max_length=150, choices=e_orderstatus, default='Free', null=True)

class passdelivery(models.Model):
    d_order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    d_emp=models.ForeignKey(Registered_emp, on_delete=models.CASCADE, null=True)

class adminpassdelivery(models.Model):
    emp = models.ForeignKey(Registered_emp, on_delete=models.CASCADE, null=True)
    booking_id = models.IntegerField(unique=True)
    booked_name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    number = models.IntegerField()
    district = models.CharField(max_length=200, null=True)
    pin_code = models.IntegerField(null=True)

    price = models.IntegerField(null=True)
    payment_mode = models.CharField(max_length=200, default='Razor_pay', null=True)

    orderstatus = (

        ('Finished', 'Finished'),
        ('pending', 'pending'),
        ('Cancelled', 'Cancelled')
    )

    status = models.CharField(max_length=150, choices=orderstatus, default='pending', null=True)

class completeddelivery(models.Model):
    deli_emp=models.ForeignKey(Registered_emp, on_delete=models.CASCADE, null=True)
    deli_fname = models.CharField(max_length=20, null=False)
    deli_phone = models.IntegerField(null=False)
    deli_address = models.TextField(null=False)
    deli_quantity = models.IntegerField(null=False)
    deli_total_price = models.FloatField(null=False)
    deli_payment_mode = models.CharField(max_length=150, null=False)
    deli_payment_id = models.CharField(max_length=150, null=True)
    deli_order_id = models.CharField(max_length=150, null=False)


