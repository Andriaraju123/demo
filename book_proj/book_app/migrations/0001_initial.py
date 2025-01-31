# Generated by Django 5.0.7 on 2024-10-05 11:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Addcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Empregister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=20)),
                ('User_name', models.CharField(max_length=20)),
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('Image', models.FileField(upload_to='')),
                ('CV', models.FileField(upload_to='')),
                ('Proof', models.FileField(upload_to='')),
                ('e_licenece', models.FileField(upload_to='')),
                ('Address', models.CharField(max_length=30)),
                ('District', models.CharField(max_length=20)),
                ('State', models.CharField(max_length=20)),
                ('Password', models.CharField(max_length=20)),
                ('Phone', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.IntegerField()),
                ('place', models.CharField(max_length=50)),
                ('pin', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Registered_emp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e_name', models.CharField(max_length=20)),
                ('e_image', models.FileField(upload_to='')),
                ('e_cv', models.FileField(blank=True, null=True, upload_to='pdfs/')),
                ('e_proof', models.FileField(blank=True, null=True, upload_to='pdfs/')),
                ('E_licenece', models.FileField(blank=True, null=True, upload_to='pdfs/')),
                ('e_email', models.EmailField(max_length=200, unique=True)),
                ('e_address', models.CharField(max_length=20)),
                ('e_District', models.CharField(max_length=20)),
                ('e_State', models.CharField(max_length=20)),
                ('e_number', models.IntegerField()),
                ('e_user_name', models.CharField(max_length=20, unique=True)),
                ('e_password', models.CharField(max_length=20, unique=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateField(auto_now=True, null=True)),
                ('e_status', models.CharField(choices=[('Free', 'Free'), ('In work', 'In work'), ('Off duty', 'Off duty')], default='Free', max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Addproduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('publisher', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('image1', models.FileField(upload_to='')),
                ('image2', models.FileField(upload_to='')),
                ('language', models.CharField(max_length=50)),
                ('categry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_app.addcategory')),
            ],
        ),
        migrations.CreateModel(
            name='mycart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('total_price', models.IntegerField()),
                ('delivered', models.BooleanField(default=False)),
                ('categry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_app.addcategory')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_app.addproduct')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_app.register')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_fname', models.CharField(max_length=20)),
                ('so_email', models.EmailField(max_length=254)),
                ('so_phone', models.IntegerField()),
                ('so_address', models.TextField()),
                ('so_district', models.CharField(max_length=20)),
                ('so_pincode', models.IntegerField()),
                ('add_message', models.CharField(max_length=250)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Out For Shipping', 'Out For Shipping'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=150)),
                ('quantity', models.IntegerField()),
                ('total_price', models.FloatField()),
                ('payment_mode', models.CharField(max_length=150)),
                ('payment_id', models.CharField(max_length=150, null=True)),
                ('order_id', models.CharField(max_length=150)),
                ('tracking_no', models.CharField(max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='book_app.mycart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_app.addproduct')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_app.register')),
            ],
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=4)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_app.register')),
            ],
        ),
        migrations.CreateModel(
            name='passdelivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book_app.order')),
                ('d_emp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book_app.registered_emp')),
            ],
        ),
        migrations.CreateModel(
            name='completeddelivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deli_fname', models.CharField(max_length=20)),
                ('deli_phone', models.IntegerField()),
                ('deli_address', models.TextField()),
                ('deli_quantity', models.IntegerField()),
                ('deli_total_price', models.FloatField()),
                ('deli_payment_mode', models.CharField(max_length=150)),
                ('deli_payment_id', models.CharField(max_length=150, null=True)),
                ('deli_order_id', models.CharField(max_length=150)),
                ('deli_emp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book_app.registered_emp')),
            ],
        ),
        migrations.CreateModel(
            name='adminpassdelivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.IntegerField(unique=True)),
                ('booked_name', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('number', models.IntegerField()),
                ('district', models.CharField(max_length=200, null=True)),
                ('pin_code', models.IntegerField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('payment_mode', models.CharField(default='Razor_pay', max_length=200, null=True)),
                ('status', models.CharField(choices=[('Finished', 'Finished'), ('pending', 'pending'), ('Cancelled', 'Cancelled')], default='pending', max_length=150, null=True)),
                ('emp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book_app.registered_emp')),
            ],
        ),
        migrations.CreateModel(
            name='Sellerproduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_book_name', models.CharField(max_length=100)),
                ('s_author', models.CharField(max_length=100)),
                ('s_publisher', models.CharField(max_length=100)),
                ('s_description', models.CharField(max_length=200)),
                ('s_price', models.IntegerField()),
                ('s_image1', models.FileField(upload_to='')),
                ('s_image2', models.FileField(upload_to='')),
                ('s_image3', models.FileField(upload_to='')),
                ('s_language', models.CharField(max_length=50)),
                ('s_year', models.IntegerField()),
                ('s_page', models.IntegerField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Declined', 'Declined')], default='Pending', max_length=150)),
                ('s_categry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_app.addcategory')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book_app.register')),
            ],
        ),
        migrations.CreateModel(
            name='second_hand_books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('books', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book_app.sellerproduct')),
            ],
        ),
        migrations.CreateModel(
            name='Order_sec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_fname', models.CharField(max_length=20)),
                ('s_email', models.EmailField(max_length=254)),
                ('s_phone', models.IntegerField()),
                ('s_address', models.TextField()),
                ('s_district', models.CharField(max_length=20)),
                ('s_pincode', models.IntegerField()),
                ('s_add_message', models.CharField(max_length=250)),
                ('s_status', models.CharField(choices=[('Pending', 'Pending'), ('Out For Shipping', 'Out For Shipping'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=150)),
                ('s_quantity', models.IntegerField()),
                ('s_total_price', models.FloatField()),
                ('s_payment_mode', models.CharField(max_length=150)),
                ('s_payment_id', models.CharField(max_length=150, null=True)),
                ('s_order_id', models.CharField(max_length=150)),
                ('s_tracking_no', models.CharField(max_length=150, null=True)),
                ('s_created_at', models.DateTimeField(auto_now_add=True)),
                ('s_updated_at', models.DateTimeField(auto_now=True)),
                ('s_customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_app.register')),
                ('s_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_app.sellerproduct')),
            ],
        ),
        migrations.CreateModel(
            name='charge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.FloatField(null=True)),
                ('payment_mode', models.CharField(default='Razor_pay', max_length=200, null=True)),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book_app.register')),
                ('sec_book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book_app.sellerproduct')),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adbooks', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book_app.addproduct')),
                ('usbooks', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book_app.sellerproduct')),
            ],
        ),
        migrations.CreateModel(
            name='wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addproduct', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='book_app.addproduct')),
                ('sellerproduct', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='book_app.sellerproduct')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_app.register')),
            ],
        ),
    ]
