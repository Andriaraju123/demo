from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.http import HttpResponse
from django.contrib import messages
import random
from django.core.mail import send_mail
import datetime
from django.utils.crypto import get_random_string
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType


# Create your views here.
def index(re):
    return render(re,'index.html')


def about(re):
    return render(re,'about.html')

def welcome(re):
    return render(re,'welcome.html')


def payment(re):
    return render(re,'payment.html')

def contact(re):
    return render(re,'contact.html')

def add_product(re):
    return render(re,'add_product.html')

def reg_opt(re):
    return render(re,'reg_opt.html')
def reg1(re):
    return render(re,'reg.html')

def reg(re):
    if re.method=='POST':
        a=re.POST.get('email')
        b=re.POST.get('name')
        c=re.POST.get('username')
        d=re.POST.get('passwd')
        e=re.POST.get('address')
        f=re.POST.get('phone')
        g=re.POST.get('place')
        h=re.POST.get('pin')
        try:
            existing_username=Register.objects.filter(username=c).exists()
            existing_email=Register.objects.filter(email=a).exists()
            if existing_username:
                messages.error(re,'username already exist')
            elif existing_email:
                messages.error(re,'mail id already exist')
            else:
                data=Register.objects.create(email=a,name=b,username=c,password=d,address=e,phone=f,place=g,pin=h)
                data.save()
                messages.success (re,"successfull registration")
                return redirect(login)
        except Exception:
            pass
    return redirect(reg1)

def login(re):
    if re.method=='POST':
        p=re.POST.get('username')
        q=re.POST.get('password')
        try:
            datas=Register.objects.get(username=p)
            if datas.password==q:
                re.session['user']=p
                return redirect(welcome)
            else:
                messages.error(re, 'invalid')
        except Exception:
            try:
                data = Registered_emp.objects.get(e_user_name=p)
                if (data.e_password == q):
                    re.session['empid'] = p
                    return redirect(conf_bookreq)
                else:
                    messages.error(re, 'invalid username or password')
            except:
               if p=='admin' and q=='12345':
                   re.session['ad']=p
                   return redirect(adminhome)
               else:
                   messages.error(re, 'invalid')
    return render(re,'login.html')

def userhome(re):
    return render(re,'userhome.html')



def adminhome(re):
    return render(re,'adminhome.html')







# --------------- ADD AND VIEW CATEGORIES [ADMIN] -----------------

def add_category(re):
    if 'ad' in re.session:
        if re.method=="POST":
            w = re.POST.get('cate')
            existing_catgory=Addcategory.objects.filter(category=w).exists()
            if existing_catgory:
                messages.error(re, 'category already exist')
            else:
                objs = Addcategory.objects.create(category=w)
                objs.save()
                messages.success(re, 'category added successfully')

        return render(re, 'add_category.html')
    return redirect(login)

def viewcategory(re):
    if 'ad' in re.session:
        datas= Addcategory.objects.all()
        return render(re, 'display_category.html', {'data': datas})
    return redirect(login)


def categories(re):
    if 'ad' in re.session:
        datas= Addcategory.objects.all()
        return render(re, 'categories.html', {'data': datas})
    return redirect(login)

# ----------------------------------- ADD AND VIEW BOOKS [ADMIN] --------------------------------------------


def add(re,d):
    if 'ad' in re.session:
        category=get_object_or_404(Addcategory,pk=d)
        if re.method=="POST":
            t = re.POST.get('b_name')
            u = re.POST.get('author')
            v = re.POST.get('publisher')
            w=re.POST.get('lang')
            x=re.POST.get('des')
            y=re.POST.get('price')
            z1=re.FILES.get('img1')
            z2=re.FILES.get('img2')
            objs=Addproduct.objects.create(book_name=t,author=u,publisher=v,description=x,price=y,image1=z1,image2=z2,categry=category,language=w)
            objs.save()
            messages.success(re,'added successfully')
        return render(re,'add_product.html',{'cat':category})
    return redirect(login)


def viewbook(request, d):
    if 'ad' in request.session:
        category = get_object_or_404(Addcategory, pk=d)
        products = Addproduct.objects.filter(categry=category)
        b = Sellerproduct.objects.filter(s_categry=category)
        s_products = second_hand_books.objects.filter(books__in=b)
        return render(request, 'bookslist.html', {'data': products,'s_data': s_products},)
    return redirect(login)

# ------------------------------- UPDATE AND DELETE BOOKS [ADMIN] -----------------------------------------

def update_pro(re,d):
    if 'ad' in re.session:
        data=Addproduct.objects.get(pk=d)
        return render(re,'update_book.html',{'data':data})
    return redirect(login)

def update(re,d):
    if 'ad' in re.session:
        t = re.POST.get('b_name')
        u = re.POST.get('author')
        v = re.POST.get('publisher')
        x = re.POST.get('des')
        y = re.POST.get('price')
        product = get_object_or_404(Addproduct, pk=d)
        Addproduct.objects.filter(pk=d).update(book_name=t,author=u,publisher=v,description=x,price=y)
        return redirect(viewbook, d=product.categry.pk)
    return redirect(login)

def delete_product(request, d):
    product = get_object_or_404(Addproduct, pk=d)
    product.delete()
    return redirect(viewbook, d=product.categry.pk)

# ------------------------------- VIEW USERS [ADMIN] -----------------------------------------

def userlist(re):
    if 'ad' in re.session:
        datas= Register.objects.all()
        return render(re, 'userlist.html', {'data': datas})
    return redirect(login)

# ------------------------------- VIEW ORDERS AND UPDATE STATUS [ADMIN] -----------------------------------------

def userbooking(re):
    if 'ad'in re.session:
      orders = Order.objects.all()
      orders_sec = Order_sec.objects.all()
      emp=Registered_emp.objects.filter(e_status='Free')
      emp_sel = None
      if re.method == "GET" and 'emp_ns' in re.GET:
          emp_sel = re.GET.get('emp_ns', '').strip()
      return render(re, 'user booking.html', {'orders': orders,'orders_sec':orders_sec,'emp':emp,'emp_sel': emp_sel })
    return redirect(adminhome)

def statusup(r,wal):
    if r.method == "POST":
        st = Order.objects.get(id=wal)
        st.status = r.POST.get('status')
        st.save()
    return redirect(userbooking)


# ------------------------------- VIEW BOOKS [USERS] -----------------------------------------

def viewpro(re):
    if 'user' in re.session:
        pp = Addproduct.objects.all()
        details = Register.objects.get(username=re.session['user'])
        datas2 = mycart.objects.filter(user=details)
        category = Addcategory.objects.all()
        c = datas2
        sum = []
        d = Addproduct.objects.all()
        t = 0
        sub = {}
        su = datas2
        for i in su:
            sub[i.products] = [i.quantity, i.pk, i.products.price * i.quantity]
        print(sub)
        for i in c:
            t = t + (i.products.price * i.quantity)
        for i in sub:
            sum.append(sub[i])
        print(sum)
        # return render(re, 'my_product.html', {'datas': datas2, 'total': t, 'sub': sub, 'cl': sub, 'd': d})
        return render(re,'shop.html',{'datas':datas2,'total':t,'sub':sub,'cl':sub,'d':d,'data':category})
    return redirect(login)

# ------------------------------------- CART --------------------------------------------------------------

def viewcart(re):
    if 'user' in re.session:
        pp = Addproduct.objects.all()
        details = Register.objects.get(username=re.session['user'])
        datas2 = mycart.objects.filter(user=details)
        c = datas2
        sum = []
        d = Addproduct.objects.all()
        t = 0
        sub = {}
        su = datas2
        for i in su:
            sub[i.products] = [i.quantity, i.pk, i.products.price * i.quantity]
        print(sub)
        for i in c:
            t = t + (i.products.price * i.quantity)
        for i in sub:
            sum.append(sub[i])
        print(sum)
        return render(re, 'cart.html', {'datas': datas2, 'total': t, 'sub': sub, 'cl': sub, 'd': d})
    return redirect(login)


def cart(re,d):
    if 'user' in re.session:
        a=Register.objects.get(username=re.session['user'])
        b=Addproduct.objects.get(pk=d)
        datas=mycart.objects.create(user=a,products=b,categry=b.categry,total_price=0,quantity=1)
        datas.save()
        return redirect(viewcart)
    return redirect(login)


def minuscart(d2,de):
    if 'user' in d2.session:
        c=mycart.objects.get(id=de)
        if c.quantity>1:
            c.quantity=c.quantity-1
            c.save()
        else:
            c.delete()
    return redirect(viewcart)


def pluscart(d3,de):
    if 'user' in d3.session:
        c=mycart.objects.get(id=de)
        c.quantity=c.quantity+1
        c.save()
        return redirect(viewcart)
    return redirect(viewcart)

def deletepro(re,d):
    if 'user' in re.session:
        data=mycart.objects.get(pk=d)
        data.delete()
        return redirect(viewcart)
    redirect(login)

# ------------------------------------- WISHLIST --------------------------------------------------------------
def add_to_wishlist(request, product_id):
    if 'user' in request.session:
        user = Register.objects.get(username=request.session['user'])


        product = Addproduct.objects.filter(pk=product_id).first()
        if product:

            if not wishlist.objects.filter(user=user, addproduct=product).exists():
                wishlist.objects.create(user=user, addproduct=product)
                messages.success(request, 'Added to Wishlist')
            return redirect(viewWishlist)
            messages.success(request, 'Already Exist in Wishlist')
        return redirect(viewpro)
    return redirect(login)


def add_to_wishlist_second(request, product_id):
    if 'user' in request.session:
        user = Register.objects.get(username=request.session['user'])

        products= Sellerproduct.objects.filter(pk=product_id).first()
        if products:

            if not wishlist.objects.filter(user=user, sellerproduct=products).exists():
                wishlist.objects.create(user=user, sellerproduct=products)
                messages.success(request, 'Added to Wishlist')
            return redirect(viewWishlist)
            messages.success(request, 'Already Exist in Wishlist')
        return redirect(secondhandbooks)
    return redirect(login)


def removepro(re,d):
    if 'user' in re.session:
        data=wishlist.objects.get(pk=d)
        data.delete()
        return redirect(viewWishlist)
    return redirect(login)


def viewWishlist(re):
    if 'user' in re.session:
        user = Register.objects.get(username=re.session['user'])
        datas = wishlist.objects.filter(user=user)
        return render(re,'Wishlist.html',{'datas':datas})
    return redirect(login)


# ------------------------------- VIEW AND EDIT PROFILE --------------------------------------------------------------
def prof(re):
    if 'user' in re.session:
        data=Register.objects.get(username=re.session['user'])
        return render(re,'profile.html',{'data':data})
    return redirect(login)


def profedit(re,d):
    if 'user' in re.session:
        data=Register.objects.get(pk=d)
        return render(re,'edit_profile.html',{'data':data})
    return redirect(login)

def profupdate(re,d):
    if 'user' in re.session:
        name=re.POST.get('name')
        email=re.POST.get('email')
        address=re.POST.get('address')
        phone_number=re.POST.get('phone')
        Register.objects.filter(pk=d).update(name=name,email=email,address=address,phone=phone_number)
        return redirect(prof)
    return redirect(login)


# --------------- -------------------------------PAYMENT ---------------------------------------------------------------
def singles(re, d):
    if 'user' in re.session:
        user = Register.objects.get(username=re.session['user'])
        product = Addproduct.objects.get(pk=d)
        return render(re, 'singlepay.html', {'data': user, 'pdata': product})
    return redirect(userhome)


def single_booking(request, product_id):
    if 'user' not in request.session:
        return redirect(userhome)

    product = get_object_or_404(Addproduct, pk=product_id)
    user = get_object_or_404(Register, username=request.session['user'])
    crt = mycart.objects.filter(user=user).first()


    if request.method == "POST":
        so_fname = request.POST.get('sofname', '')
        # so_lname = request.POST.get('solname', '')
        so_email = request.POST.get('semail', '')
        so_phone = int(request.POST.get('sphone', 10))
        so_address = request.POST.get('sadrs', '')
        so_district = request.POST.get('sdistrict', '')
        # so_city = request.POST.get('scity', '')
        so_pincode = int(request.POST.get('spincode', 6))
        add_message = request.POST.get('add_det', '')
        quantity = int(request.POST.get('singleqty', 1))
        total_price = float(request.POST.get('total', 0))
        paymode = request.POST.get('payment_mode', '')

        total_price=product.price

        order_id = 'ordid' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(order_id=order_id).exists():
            order_id = 'ordid' + str(random.randint(1111111, 9999999))

        tracking_no = 'book' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=tracking_no).exists():
            tracking_no = 'book' + str(random.randint(1111111, 9999999))

        single_booking = Order.objects.create(
            customer=user,
            product=product,
            cart=crt,

            so_fname=so_fname,

            so_email=so_email,
            so_phone=so_phone,
            so_address=so_address,
            so_district=so_district,

            so_pincode=so_pincode,
            add_message=add_message,
            quantity=quantity,
            status='Pending',
            payment_mode=paymode,
            payment_id=None,
            order_id=order_id,
            tracking_no=tracking_no,
            total_price=total_price,
        )
        single_booking.save()

        messages.success(request, 'Your order has been placed successfully')
        return redirect(user_orders)

    return redirect(userhome)

# razorpay

def single_razor(request, product_id):
    product = get_object_or_404(Addproduct, pk=product_id)
    user = get_object_or_404(Register, username=request.session['user'])
    crt = mycart.objects.filter(user=user).first()


    if request.method == "POST":
        print("hello")
        so_fname = request.POST.get('sofname', '')
        # so_lname = request.POST.get('solname', '')
        so_email = request.POST.get('semail', '')
        so_phone = int(request.POST.get('sphone', 10))
        so_address = request.POST.get('sadrs', '')
        so_district = request.POST.get('sdistrict', '')
        # so_city = request.POST.get('scity', '')
        so_pincode = int(request.POST.get('spincode', 6))
        add_message = request.POST.get('notes', '')
        quantity = int(request.POST.get('singleqty', 1))
        total_price = request.POST.get('total', 0)
        paymode = request.POST.get('payment_mode', '')
        print(paymode,total_price)

        order_id = 'ordid' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(order_id=order_id).exists():
            order_id = 'ordid' + str(random.randint(1111111, 9999999))

        tracking_no = 'book' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=tracking_no).exists():
            tracking_no = 'book' + str(random.randint(1111111, 9999999))

        single_booking = Order.objects.create(
            customer=user,
            product=product,
            cart=crt,
            so_fname=so_fname,

            so_email=so_email,
            so_phone=so_phone,
            so_address=so_address,
            so_district=so_district,

            so_pincode=so_pincode,
            add_message=add_message,
            quantity=quantity,
            status='Pending',
            payment_mode=paymode,
            payment_id=None,
            order_id=order_id,
            tracking_no=tracking_no,
            total_price=total_price,
        )
        single_booking.save()
        # if paymode == 'RazorPay':
        return redirect(razorpaycheck,product.price)
    #     return JsonResponse({'status': 'Your order has been placed successfully'})
    #
    # return redirect(usr_home)


def razorpaycheck(request,price):
    if 'user' in request.session:
        u = Register.objects.get(username=request.session['user'])
        s = Order.objects.filter(customer=u)
        t = price*100
        return render(request, "payment.html", {'amount': t})

    return render(request, "payment.html")

def checkout(request):
    # c = d
    mp = []
    t = 0
    if 'user' in request.session:
        user = Register.objects.get(username=request.session['user'])
        mp=mycart.objects.filter(user=user)
        c=mp
        t=0
        print (mp)
        for i in c:
            t = t + (i.products.price * i.quantity)
        return render(request, 'multiple_booking.html', {'data': user, 'pdata':mp,'t':t})
    return redirect(userhome)

def multiple_booking(request):
    if 'user' not in request.session:
        return redirect('userhome')

    user = get_object_or_404(Register, username=request.session['user'])
    crt = mycart.objects.filter(user=user)
    # crt = mycart.object.filter(usr=user).delete()
    t=0
    for i in crt:
        t = t + (i.products.price * i.quantity)
        total = t
        quty=i.quantity

    if crt.exists():
        crt_i = crt.first()
    else:
        messages.error(request, 'No cart found for the user')
        return redirect(userhome)
    if request.method == "POST":
        m_fname = request.POST.get('sofname', '')
        m_email = request.POST.get('semail', '')
        m_phone = int(request.POST.get('sphone', 10))
        m_address = request.POST.get('sadrs', '')
        m_district = request.POST.get('sdistrict', '')
        m_pincode = int(request.POST.get('spincode', 6))
        m_add_message = request.POST.get('add_det', '')
        m_quantity = int(request.POST.get('multyqty', 1))
        m_quantity =quty
        total_price = int(request.POST.get('total', 0))
        paymode = request.POST.get('payment_mode', '')
        total_price =total
        product_id =crt_i. products.pk
        product = get_object_or_404(Addproduct, id=product_id)

        order_id = 'ordid' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(order_id=order_id).exists():
            order_id = 'ordid' + str(random.randint(1111111, 9999999))

        tracking_no = 'book' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=tracking_no).exists():
            tracking_no = 'book' + str(random.randint(1111111, 9999999))

        multiple_booking =Order.objects.create(
            customer=user,
            product=product,
            cart=crt_i ,
            so_fname=m_fname,
            so_email=m_email,
            so_phone=m_phone,
            so_address=m_address,
            so_district=m_district,
            so_pincode=m_pincode,
            add_message=m_add_message,
            quantity=m_quantity,
            status='Pending',
            payment_mode=paymode,
            payment_id=None,
            order_id=order_id,
            tracking_no=tracking_no,
            total_price=total_price,
        )
        multiple_booking.save()
        mycart.objects.filter(user=user).delete()
        messages.success(request, 'Your order has been placed successfully')
        return redirect(userhome)
    return redirect(checkout)




def razorpaycheck2(request):
    if 'user' in request.session:
        u = Register.objects.get(username=request.session['user'])
        s = Order.objects.filter(customer=u)
        mp = mycart.objects.filter(user=u)
        c = mp
        t = 0
        print(mp)
        for i in c:
            t = t + (i.products.price * i.quantity)
            total=t*100
        return render(request, "payment.html", {'amount': total})

    return render(request, "payment.html")


def multiple_razor(request):
    if 'user' not in request.session:
        return redirect(userhome)

    user = get_object_or_404(Register, username=request.session['user'])
    crt = mycart.objects.filter(user=user)
    t=0
    for i in crt:
        t = t + (i.products.price * i.quantity)
        total = t
        quty = i.quantity

    if crt.exists():
        crt_i = crt.first()
    else:
        messages.error(request, 'No cart found for the user')
        return redirect(userhome)


    if request.method == "POST":
        print("hello")
        m_fname = request.POST.get('sofname', '')
        m_email = request.POST.get('semail', '')
        m_phone = int(request.POST.get('sphone', 10))
        m_address = request.POST.get('sadrs', '')
        m_district = request.POST.get('sdistrict', '')
        m_pincode = int(request.POST.get('spincode', 6))
        m_add_message = request.POST.get('notes', '')
        m_quantity = int(request.POST.get('singleqty', 1))
        m_quantity=quty
        # total_price = float(request.POST.get('total', 0))
        paymode = request.POST.get('payment_mode', '')
        # print(paymode,total_price)
        total_price =total
        product_id = crt_i.products.pk
        product = get_object_or_404(Addproduct, id=product_id)

        order_id = 'ordid' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(order_id=order_id).exists():
            order_id = 'ordid' + str(random.randint(1111111, 9999999))

        tracking_no = 'book' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=tracking_no).exists():
            tracking_no = 'book' + str(random.randint(1111111, 9999999))

        multiple_booking = Order.objects.create(
            customer=user,
            product=product,
            cart=crt_i ,
            so_fname=m_fname,
            so_email=m_email,
            so_phone=m_phone,
            so_address=m_address,
            so_district=m_district,
            so_pincode=m_pincode,
            add_message=m_add_message,
            quantity=m_quantity,
            status='Pending',
            payment_mode=paymode,
            payment_id=None,
            order_id=order_id,
            tracking_no=tracking_no,
            total_price=total_price,
        )
        # multiple_booking.save()
        # # if paymode == 'RazorPay':
        # return redirect(razorpaycheck2,product.price)

        multiple_booking.save()
        messages.success(request, 'Your order has been placed successfully')
        return redirect(razorpaycheck2)


def success(re):
    return redirect(user_orders)


# ------------------------------- VIEW ORDERS [USER] -----------------------------------------

def user_orders(re):
    if 'user' in re.session:
        user = Register.objects.get(username=re.session['user'])
        data = Order.objects.filter(customer=user)
        data_sec = Order_sec.objects.filter(s_customer=user)
        # datas=Multiple_Booking.objects.all()
        return render(re,'user_orders.html',{'order': data,'orders':data_sec})
    return redirect(userhome)

# ------------------------------- FORGET AND RESET PASSWORD -----------------------------------------
def forgot_password_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Register.objects.get(email=email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password_user)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            # return render(request, 'emailsent.html')
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password_user)

    return render(request, 'forgot_password.html')

def reset_password_user(request, token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user.Password=new_password
            password_reset.user.save()
            # password_reset.delete()
            return redirect(login)
    return render(request, 'resetpassword.html',{'token':token})

# ------------------------------------ SECOND HAND BOOKS -----------------------------------------------------

def seller_userhome(re):
    return render(re,'seller_userhome.html')

def seller_displaycategory(re):
    if 'user' in re.session:
        datas = Addcategory.objects.all()
        return render(re, 'seller_displaycategory.html', {'data': datas})
    return redirect(login)

def seller_addcategory(re):
    if 'user' in re.session:
        if re.method == "POST":
            w = re.POST.get('cate')
            objs = Addcategory.objects.create(category=w)
            objs.save()
            messages.success(re, 'category added successfully')
        return render(re, 'seller_addcategory.html')
    return redirect(login)


# ------------------------------------ ADD SECOND HAND BOOKS [USER] -----------------------------------------------------

def seller_addproduct(re,d):
    if 'user' in re.session:
        category=get_object_or_404(Addcategory,pk=d)
        return render(re,'seller_addproduct.html',{'cat':category})
    return redirect(login)


def req(re,d):
    if 'user' in re.session:
        category=get_object_or_404(Addcategory,pk=d)
        seller= Register.objects.get(username=re.session['user'])
        if re.method=="POST":
            t = re.POST.get('b_name')
            u = re.POST.get('author')
            v = re.POST.get('publisher')
            w=re.POST.get('lang')
            x=re.POST.get('des')
            y=re.POST.get('price')
            z1=re.FILES.get('img1')
            z2=re.FILES.get('img2')
            z3 = re.FILES.get('img3')
            s=re.POST.get('yob')
            r=re.POST.get('page')
            objs=Sellerproduct.objects.create(s_book_name=t,s_author=u,s_publisher=v,s_language=w,s_description=x, s_price=y,s_image1=z1,s_image2=z2,s_image3=z3,s_categry=category,s_year=s,s_page=r,user=seller)
            objs.save()
            messages.success(re,'Request sent ')
            return redirect(user_request)
        return render(re,'seller_addproduct.html',{'cat':category})
    return redirect(login)


def user_request(re):
    if 'user' in re.session:
        user = Register.objects.get(username=re.session['user'])
        data = Sellerproduct.objects.filter(user=user)
        # datas=Multiple_Booking.objects.all()
        return render(re,'my request.html',{'data': data})
    return redirect(seller_userhome)

def razorpay(request,s_price,pk):
    if 'user' in request.session:
        u = Register.objects.get(username=request.session['user'])
        s = Sellerproduct.objects.filter(user=u)
        t1 = s_price*100
        t=t1*0.1
        return render(request, "payment2.html", {'amount': t, 'pk':pk})

def success2(re,id):
    if 'user' in re.session:
        r=Register.objects.get(username=re.session['user'])
        data = Sellerproduct.objects.get(pk=id)
        p=data.s_price*0.1
        a = charge.objects.create(seller=data.user,
                                  sec_book=data,
                                  fee=p,
                                  payment_mode='Razor_pay')
        return render(re,'success2.html')




def requestlist(re):
    if 'ad' in re.session:
        data=Sellerproduct.objects.all()
        return render(re,'requestlist.html',{'data':data})
    return redirect(login)

def viewcharge(re):
    if 'ad'in re.session:
      am = charge.objects.all()
      return render(re, 'fee_paymentlist.html', {'am': am})
    return redirect(login)

def reqstatus(r,wal):
    if r.method == "POST":
        st = Sellerproduct.objects.get(id=wal)
        st.status = r.POST.get('status')
        st.save()
    return redirect(requestlist)

def req_addbook(request, d):
    s_product=Sellerproduct.objects.filter(pk=d).first()
    if not second_hand_books.objects.filter(books=s_product).exists():
        second_hand_books.objects.create(books=s_product).save()
        messages.success(request, "Book Added")

    return redirect(requestlist)



# --------------- ------------------------ VIEW SECOND HAND BOOKS [USER] ------------------------------------------------------------------

def secondhandbooks(re):
    cat = Addcategory.objects.all()
    s_books = second_hand_books.objects.all()
    return render(re, 'second-hand books.html', {'b': s_books,'data':cat})

def details(re,d):
    details = get_object_or_404(second_hand_books, pk=d)
    return render(re, 'single_product.html', {'det': details})

#--------------- ------------------------ PAYMENT SECOND HAND BOOKS [BUYER] ---------------------------------------

def singles_sec(re, d):
    if 'user' in re.session:
        user = Register.objects.get(username=re.session['user'])
        product = Sellerproduct.objects.get(pk=d)
        return render(re, 'singlepay_second.html', {'data': user, 'pdata': product})
    return redirect(userhome)

def single_booking_sec(request, product_id):
    if 'user' not in request.session:
        return redirect(userhome)

    product = get_object_or_404(Sellerproduct, pk=product_id)
    user = get_object_or_404(Register, username=request.session['user'])



    if request.method == "POST":
        so_fname = request.POST.get('sofname', '')
        so_email = request.POST.get('semail', '')
        so_phone = int(request.POST.get('sphone', 10))
        so_address = request.POST.get('sadrs', '')
        so_district = request.POST.get('sdistrict', '')
        so_pincode = int(request.POST.get('spincode', 6))
        add_message = request.POST.get('add_det', '')
        quantity = int(request.POST.get('singleqty', 1))
        total_price = request.POST.get('total', 0)
        paymode = request.POST.get('payment_mode', '')

        total_price=product.s_price

        order_id = 'ordid' + str(random.randint(1111111, 9999999))
        while Order_sec.objects.filter(s_order_id=order_id).exists():
            order_id = 'ordid' + str(random.randint(1111111, 9999999))

        tracking_no = 'book' + str(random.randint(1111111, 9999999))
        while Order_sec.objects.filter(s_tracking_no=tracking_no).exists():
            tracking_no = 'book' + str(random.randint(1111111, 9999999))

        single_booking_sec = Order_sec.objects.create(
            s_customer=user,
            s_product=product,
            s_fname=so_fname,
            s_email=so_email,
            s_phone=so_phone,
            s_address=so_address,
            s_district=so_district,
            s_pincode=so_pincode,
            s_add_message=add_message,
            s_quantity=quantity,
            s_status='Pending',
            s_payment_mode=paymode,
            s_payment_id=None,
            s_order_id=order_id,
            s_tracking_no=tracking_no,
            s_total_price=total_price,
        )
        single_booking_sec.save()

        messages.success(request, 'Your order has been placed successfully')
        return redirect(user_orders)
    return redirect(userhome)

# def single_razor_sec(request, product_id):
#     product = get_object_or_404(Sellerproduct, pk=product_id)
#     user = get_object_or_404(Register, username=request.session['user'])
#     # crt = mycart.objects.filter(user=user).first()
#
#
#     if request.method == "POST":
#         print("hello")
#         so_fname = request.POST.get('sofname', '')
#         so_email = request.POST.get('semail', '')
#         so_phone = int(request.POST.get('sphone', 10))
#         so_address = request.POST.get('sadrs', '')
#         so_district = request.POST.get('sdistrict', '')
#         so_pincode = int(request.POST.get('spincode', 6))
#         add_message = request.POST.get('add_det', '')
#         quantity = int(request.POST.get('singleqty', 1))
#         total_price = request.POST.get('total', 0)
#         paymode = request.POST.get('payment_mode', '')
#
#         order_id = 'ordid' + str(random.randint(1111111, 9999999))
#         while Order.objects.filter(order_id=order_id).exists():
#             order_id = 'ordid' + str(random.randint(1111111, 9999999))
#
#         tracking_no = 'book' + str(random.randint(1111111, 9999999))
#         while Order.objects.filter(tracking_no=tracking_no).exists():
#             tracking_no = 'book' + str(random.randint(1111111, 9999999))
#
#         single_booking_sec = Order_sec.objects.create(
#             s_customer=user,
#             s_product=product,
#             s_fname=so_fname,
#             s_email=so_email,
#             s_phone=so_phone,
#             s_address=so_address,
#             s_district=so_district,
#             s_pincode=so_pincode,
#             s_add_message=add_message,
#             s_quantity=quantity,
#             s_status='Pending',
#             s_payment_mode=paymode,
#             s_payment_id=None,
#             s_order_id=order_id,
#             s_tracking_no=tracking_no,
#             s_total_price=total_price,
#         )
#         single_booking_sec.save()
#
#         # if paymode == 'RazorPay':
#         return redirect(razorpaycheck_sec,product.price)
#     #     return JsonResponse({'status': 'Your order has been placed successfully'})
#     #
#     # return redirect(usr_home)
#
#
# def razorpaycheck_sec(request,price):
#     if 'user' in request.session:
#         u = Register.objects.get(username=request.session['user'])
#         s = Order_sec.objects.filter(customer=u)
#         t = price*100
#         return render(request, "payment.html", {'amount': t})
#
#     return render(request, "payment.html")
def single_razor_sec(request, product_id):
    product = get_object_or_404(Sellerproduct, pk=product_id)
    user = get_object_or_404(Register, username=request.session['user'])

    if request.method == "POST":
        print("hello")
        so_fname = request.POST.get('sofname', '')
        so_email = request.POST.get('semail', '')
        so_phone = int(request.POST.get('sphone', 10))
        so_address = request.POST.get('sadrs', '')
        so_district = request.POST.get('sdistrict', '')
        so_pincode = int(request.POST.get('spincode', 6))
        add_message = request.POST.get('add_det', '')
        quantity = int(request.POST.get('singleqty', 1))
        paymode = request.POST.get('payment_mode', '')

        # Handle total_price correctly
        total_price = request.POST.get('total', 0)
        try:
            total_price = float(total_price)
        except ValueError:
            total_price = 0  # Fallback to 0 if the value is invalid

        paymode = request.POST.get('payment_mode', '')

        order_id = 'ordid' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(order_id=order_id).exists():
            order_id = 'ordid' + str(random.randint(1111111, 9999999))

        tracking_no = 'book' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=tracking_no).exists():
            tracking_no = 'book' + str(random.randint(1111111, 9999999))

        single_booking_sec = Order_sec.objects.create(
            s_customer=user,
            s_product=product,
            s_fname=so_fname,
            s_email=so_email,
            s_phone=so_phone,
            s_address=so_address,
            s_district=so_district,
            s_pincode=so_pincode,
            s_add_message=add_message,
            s_quantity=quantity,
            s_status='Pending',
            s_payment_mode=paymode,
            s_payment_id=None,
            s_order_id=order_id,
            s_tracking_no=tracking_no,
            s_total_price=total_price,
        )
        single_booking_sec.save()

        return redirect(razorpaycheck_sec, product.s_price)

    return render(request, 'order_page.html')  # Return a valid response if it's a GET request


def razorpaycheck_sec(request, price):
    if 'user' in request.session:
        u = Register.objects.get(username=request.session['user'])
        t = price * 100  # Convert to smallest currency unit
        return render(request, "payment.html", {'amount': t})

    return render(request, "payment.html")

def success(re):
    return redirect(user_orders)


#--------------- ------------------------ ORDERS SECOND HAND BOOKS -------- ---------------------------------------
def orderlist_sec(re):
    if 'user' in re.session:
        a = Register.objects.get(username=re.session['user'])
        b= Sellerproduct.objects.filter(user=a)
        orders_sec = Order_sec.objects.filter(s_product__in=b)
        return render(re, 'orderlist_sec.html', {'orders_sec':orders_sec})
    return redirect(seller_userhome)

def statusup_sec(r,wal):
    if r.method == "POST":
        st = Order_sec.objects.get(id=wal)
        st.s_status = r.POST.get('status')
        st.save()
    return redirect(orderlist_sec)





# --------------- ------------------------ SEARCH -----------------------------------------------------------------------

def search(request):
    if request.method == "POST":
        ser = request.POST.get('s', '').strip()  # Get the search term and remove extra spaces

        if ser:
            # Search by book name or author in both models
            search_results = Addproduct.objects.filter(book_name__icontains=ser) | \
                             Addproduct.objects.filter(author__icontains=ser)

            search_resultss = Sellerproduct.objects.filter(s_book_name__icontains=ser) | \
                              Sellerproduct.objects.filter(s_author__icontains=ser)

            if not search_results.exists() and not search_resultss.exists():
                search_results, search_resultss = None, None

            return render(request, 'search.html', {'search': search_results, 'searchh': search_resultss})

        else:

            return render(request, 'search.html', {'search': None, 'searchh': None})


    return render(request, 'search.html')

def specific(re,d):
    if 'user' in re.session:
        category = get_object_or_404(Addcategory, pk=d)
        data = Addproduct.objects.filter(categry=category)
        s_data = Sellerproduct.objects.filter(s_categry=category)
        return render(re,'specificbook.html',{'s_data':s_data,'data':data})
    return redirect(login)



def searchlang(request):
    if 'user' in request.session:
        if request.method == "GET":  # Change to GET since the form uses the GET method
            ser = request.GET.get('lang', '').strip()  # Get the search term from GET, not POST

            if ser:
                # Search by book language in both models
                search_results = Addproduct.objects.filter(language__icontains=ser)
                search_resultss = Sellerproduct.objects.filter(s_language__icontains=ser)


                # If no results found, set to None
                if not search_results.exists() and not search_resultss.exists():
                    search_results, search_resultss = None, None

                return render(request, 'searchlanguage.html', {'search': search_results, 'searchh': search_resultss})

            else:
                # Render the search page with no results if the search term is empty
                return render(request, 'searchlanguage.html', {'search': None, 'searchh': None})

        # If it's not a GET request, just render the empty search page
        return render(request, 'searchlanguage.html')
    return redirect(login)


def employeeregister(re):
    if re.method == 'POST':
        name = re.POST.get('name')
        image = re.FILES.get('image')
        cv = re.FILES.get('cv')
        proof = re.FILES.get('proof')
        lic = re.FILES.get('lic')
        address = re.POST.get('address')
        dist = re.POST.get('place')
        state = re.POST.get('stat')
        email = re.POST.get('email')
        username = re.POST.get('username')
        phone = re.POST.get('phone')
        pw = re.POST.get('passwd')

        try:
            existing_username = Registered_emp.objects.filter(e_user_name=username).exists()
            existing_email = Registered_emp.objects.filter(e_email=email).exists()
            if existing_username:
                messages.error(re, 'Username already exist')
            elif existing_email:
                messages.error(re, 'Mail already exist')
            else:
                obj =Empregister.objects.create(Name=name, Email=email, User_name=username,Image=image,CV=cv,
                                                Proof=proof,e_licenece=lic,Address=address,District=dist,State=state,Password=pw, Phone=phone)
                obj.save()
                messages.success(re, 'Registered successfully.....')
                return redirect(index)
        except Exception:
            pass
    return render(re, 'emp_reg.html')

def Verify_workers(re):
    data=Empregister.objects.all()
    return render(re,'emp_list.html',{'da':data})

def approve_item(request, id):
    rev_item = Empregister.objects.get(pk=id)
    item = Registered_emp(e_cv=rev_item.CV,e_name=rev_item.Name,e_image=rev_item.Image,e_proof=rev_item.Proof,E_licenece=rev_item.e_licenece,e_email=rev_item.Email,e_number=rev_item.Phone,e_address=rev_item.Address,e_District=rev_item.District,e_user_name=rev_item.User_name,e_password=rev_item.Password)
    item.save()
    rev_item.delete()
    return redirect(Verify_workers)

def veri_emp_dele(request, d):
    employee = get_object_or_404(Empregister, id=d)
    employee.delete()
    return redirect(Verify_workers)

# def admin_delivery_send(re,id):
#     if 'ad' in re.session:
#         data = Order.objects.filter(pk=id)
#         delivery=data.first()
#         a = adminpassdelivery.objects.create(booked_name=delivery.so_fname,
#                                   address=delivery.so_address,
#                                   number=delivery.so_phone,
#                                   price=delivery.total_price,
#                                   payment_mode=delivery.payment_mode,
#                                   district=delivery.so_district,
#                                   pin_code=delivery.so_pincode,
#
#                                   booking_id=delivery.order_id,
#                                 )
#         a.save()
#         messages.success(re,'Notified')
#     return redirect(userbooking)

# def admin_delivery_send(re,id):
#     if 'ad' in re.session:
#         data = Order.objects.filter(pk=id)
#         delivery=data.first()
#         emp=Registered_emp.objects.get(e_user_name=re.session['empid'])
#         if not passdelivery.objects.filter(d_order=delivery).exists():
#             a = passdelivery.objects.create(d_order=delivery,d_emp=emp)
#             a.save()
#             messages.success(re,'Notified')
#         else:
#             messages.success(re, ' Already Notified')
#     return redirect(userbooking)
# def admin_delivery_send(re,id):
#     if 'ad' in re.session:
#         data = Order.objects.filter(pk=id)
#         delivery=data.first()
#         if re.method == "GET":  # Change to GET since the form uses the GET method
#             emp_sel = re.GET.get('emp_ns', '').strip()
#             emp=Registered_emp.objects.filter(e_name__in=emp_sel)
#         if not passdelivery.objects.filter(d_order=delivery).exists():
#             a = passdelivery.objects.create(d_order=delivery,d_emp=emp)
#             a.save()
#             messages.success(re,'Notified')
#         else:
#             messages.success(re, ' Already Notified')
#     return redirect(userbooking)


def admin_delivery_send(re, id):
    if 'ad' in re.session:
        data = Order.objects.filter(pk=id)
        delivery = data.first()
        if re.method == "GET":
            emp_sel = re.GET.get('emp_ns', '').strip()  # Get the selected employee's name
            emp = Registered_emp.objects.filter(e_name=emp_sel).first()  # Get the employee instance

            if emp:  # Ensure the employee exists
                if not passdelivery.objects.filter(d_order=delivery).exists():  # Check if already exists
                    a = passdelivery.objects.create(d_order=delivery, d_emp=emp)
                    messages.success(re, 'Notified')
                else:
                    messages.success(re, 'Already Notified')
            else:
                messages.error(re, 'Employee not found')
    return redirect(userbooking)


# def admin_delivery_send(re, id):
#     if 'ad' in re.session:  # Check if admin is logged in
#         try:
#             # Get the order by its primary key
#             delivery = get_object_or_404(Order, pk=id)
#
#             # Get the employee who is assigning the delivery
#             emp = Registered_emp.objects.get(e_user_name=re.session['empid'])
#
#             # Check if the delivery is already assigned
#             if not passdelivery.objects.filter(d_order=delivery).exists():
#                 # Create and save a new passdelivery record
#                 passdelivery.objects.create(d_order=delivery, d_emp=emp)
#                 messages.success(re, 'Delivery assigned successfully and notified')
#             else:
#                 messages.info(re, 'Delivery already assigned')
#         except Registered_emp.DoesNotExist:
#             # Handle case where the employee is not found
#             messages.error(re, 'Employee not found')
#     else:
#         messages.error(re, 'You are not authorized to perform this action')
#
#     return redirect(userbooking)  # Ensure 'userbooking' is correctly defined

# def admin_delivery_send(re, id, emp_id=None):  # Add optional emp_id to the parameters
#     if 'ad' in re.session:  # Ensure this is still limited to an admin
#         try:
#             # Get the order by its primary key
#             delivery = get_object_or_404(Order, pk=id)
#
#             # Fetch the employee by emp_id if provided, or assign a default employee
#             if emp_id:
#                 emp = Registered_emp.objects.get(pk=emp_id)
#             else:
#                 emp = Registered_emp.objects.first()  # Default to the first employee, modify as needed
#
#             # Check if the delivery is already assigned
#             if not passdelivery.objects.filter(d_order=delivery).exists():
#                 # Create and save a new passdelivery record
#                 passdelivery.objects.create(d_order=delivery, d_emp=emp)
#                 messages.success(re, f'Delivery assigned to {emp.e_user_name} successfully and notified')
#             else:
#                 messages.info(re, 'Delivery already assigned')
#         except Registered_emp.DoesNotExist:
#             # Handle case where the employee is not found
#             messages.error(re, 'Employee not found')
#     else:
#         messages.error(re, 'You are not authorized to perform this action')
#
#     return redirect(userbooking)






# from django.shortcuts import get_object_or_404
#
#
# def admin_delivery_send(re, id):
#     if 'ad' in re.session:
#         # Fetch order and employee
#         delivery = get_object_or_404(Order, pk=id)
#         emp = get_object_or_404(Registered_emp, e_user_name=re.session.get('empid'))
#
#         # Check if delivery assignment already exists
#         if not passdelivery.objects.filter(d_order=delivery).exists():
#             # Create and save delivery assignment
#             passdelivery.objects.create(d_order=delivery, d_emp=emp)
#             messages.success(re, 'Notified')
#         else:
#             messages.info(re, 'Already Notified')
#
#     return redirect(userbooking)  # Assuming 'userbooking' is a valid view name


#employee see the delivery
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# def conf_bookreq(request):
#     if 'empid' in request.session:
#         try:
#             emp = Registered_emp.objects.get(e_user_name=request.session['empid'])
#             data = passdelivery.objects.filter(d_emp=emp).first()  # This line can raise DoesNotExist
#             return render(request, 'view_work_employee.html', {'da': data, 's': emp})
#         except ObjectDoesNotExist:
#             # Handle the case where no passdelivery object is found
#             return render(request, 'view_work_employee.html',{'s': emp})
#     return redirect(login)


def conf_bookreq(request):
    if 'empid' in request.session:
        try:
            emp = Registered_emp.objects.get(e_user_name=request.session['empid'])
            data = passdelivery.objects.filter(d_emp=emp).first()
            if data:
                return render(request, 'view_work_employee.html', {'da': data, 's': emp})
            else:
                return render(request, 'view_work_employee.html', {'s': emp})
        except ObjectDoesNotExist:
            return render(request, 'view_work_employee.html', {'s': emp})
    return redirect(login)



# def conf_bookreq(request):
#     if 'empid' in request.session:
#         emp = Registered_emp.objects.get(e_user_name=request.session['empid'])
#         data = passdelivery.objects.get(d_emp=emp)
#         return render(request, 'view_work_employee.html', {'da': data, 's': emp})
#     return redirect(login)

# def deliverydet(request,d):
#     if 'empid' in request.session:
#         emp=Registered_emp.objects.get(e_user_name=request.session['empid'])
#         data = get_object_or_404(passdelivery, pk=d)
#         return render(request, 'deliverydet.html', {'da': data,'s':emp})
#     return redirect(login)

# def emp_status(re,d):
#     if 'empid' in re.session:
#         delivery = passdelivery.objects.filter(pk=d).first()
#         if not completeddelivery.objects.filter(deli_st=delivery).exists():
#             completeddelivery.objects.create(deli_st=delivery).save()
#             messages.success(re, "Delivery Completed")
#         return redirect(conf_bookreq)
#     return redirect(login)

def emp_status(re, d):
    if 'empid' in re.session:
        delivery = passdelivery.objects.filter(pk=d).first()

        if delivery:  # Ensure delivery exists
            if not completeddelivery.objects.filter(deli_order_id=delivery.d_order.order_id).exists():
                # Create a completed delivery
                completeddelivery.objects.create(deli_emp=delivery.d_emp,
                                                 deli_fname=delivery.d_order.so_fname,
                                                 deli_phone=delivery.d_order.so_phone,
                                                 deli_address=delivery.d_order.so_address,
                                                 deli_quantity=delivery.d_order.quantity,
                                                 deli_total_price=delivery.d_order.total_price,
                                                 deli_payment_mode=delivery.d_order.payment_mode,
                                                 deli_payment_id=delivery.d_order.payment_id,
                                                 deli_order_id=delivery.d_order.order_id).save()
                # Delete the passdelivery record after completion
                delivery.delete()
                messages.success(re, "Delivery Completed")
            else:
                messages.success(re, 'Delivery already updated')

        return redirect(conf_bookreq)
    return redirect(login)


def cur_status(re):
    if 'empid' in re.session:
        if re.method == "POST":
            st = Registered_emp.objects.get(e_user_name=re.session['empid'])
            st. e_status = re.POST.get('status')
            st.save()
        return redirect(conf_bookreq)

# def statusup2(re, booking_id):
#     if re.method == "POST":
#         st = passdelivery.objects.get(id=booking_id)
#         # od = Order.objects.get(id=booking_id)
#         st.status = re.POST.get('status')
#         st.save()
#     return redirect(conf_bookreq)
def statusup2(re, booking_id):
    if re.method == "POST":
        # Fetch the associated passdelivery object
        delivery = passdelivery.objects.get(id=booking_id)
        # Update the status of the related Order model
        order = delivery.d_order
        order.status = re.POST.get('status')
        order.save()
        messages.success(re, 'Order status updated successfully')
    return redirect(conf_bookreq)

def delivery_completed(request, d):
    if 'empid' in request.session:
        emp = Registered_emp.objects.get(e_user_name=request.session['empid'])
        # Try to find the product in Sellerproduct
        ord= passdelivery.objects.filter(pk=d).first()
        if not completeddelivery.objects.filter(delivery=emp,deli_st=ord).exists():
            completeddelivery.objects.create(delivery=emp,deli_st=ord)
            messages.success(request, 'Work completed')
            return redirect(conf_bookreq)
        else:
            messages.success(request, 'Already updated')
            return redirect(conf_bookreq)
    return redirect(login)

# def viewworks(request):
#     if 'empid' in request.session:
#         data = completeddelivery.objects.all()
#         return render(request, 'worklist.html', {'da': data})
#     return redirect(login)

def view_mydeliveries(re):
    if 'empid' in re.session:
        emp = Registered_emp.objects.get(e_user_name=re.session['empid'])
        data = completeddelivery.objects.filter(deli_emp=emp)
        return render(re,'view_mydeliveries.html',{'da': data,})
    return redirect(login)

#--------------------------LOGOUT---------------------------

def logout(re):
    if 'user' in re.session:
        re.session.flush()
    return redirect(login)

def logout_ad(re):
    if 'ad' in re.session:
        re.session.flush()
    return redirect(login)

def logout_emp(re):
    if 'empid' in re.session:
        re.session.flush()
    return redirect(login)



