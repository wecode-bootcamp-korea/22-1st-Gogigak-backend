import os, django, csv, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gogigak.settings")
django.setup()

from users.models import *
from products.models import *
from orders.models import *
#------------------------------------------------------------------------
#users
CSV_PATH_PRODUCTS = './csvs/users_csv/users.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            email = row[0]
            password = row[1]
            name = row[2]
            phone_number = row[3]
            point = row[4]
            User.objects.create(email=email, password=password,
            name=name, phone_number=phone_number, point=point)
#----------------------------------------------------------------------
#coupons
CSV_PATH_PRODUCTS = './csvs/users_csv/coupons.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            name = row[0]
            value = row[1]
            Coupon.objects.create(name= name, value=value)
#----------------------------------------------------------------------
# addresses
CSV_PATH_PRODUCTS = './csvs/users_csv/addresses.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            user_id=row[0]
            road_address=row[1]
            zip_code=row[2]
            Address.objects.create(user_id=user_id,road_address=road_address,zip_code=zip_code)
#----------------------------------------------------
# user_coupons
CSV_PATH_PRODUCTS = './csvs/users_csv/user_coupons.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            user_id=row[0]
            coupon_id=row[1]
            UserCoupon.objects.create(user_id=user_id,coupon_id=coupon_id)
#---------------------------------------------------------------------------------
#options
CSV_PATH_PRODUCTS = './csvs/products_csv/options.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            name=row[0]
            Option.objects.create(name=name)
#------------------------------------------------------
# ## insert categories
CSV_PATH_USERS = './csvs/products_csv/categories.csv'

with open(CSV_PATH_USERS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        name = row[0]
        image = row[1]
        Category.objects.create(name=name, image=image)
#--------------------------------------------------------
# ## insert products
CSV_PATH_USERS = './csvs/products_csv/products.csv'
with open(CSV_PATH_USERS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Product.objects.create(name = row[0],category = Category.objects.get(id=row[1]),butchered_date = row[2],price = row[3],grams = row[4],is_organic = row[5],sales = row[6],reviews = row[7],
            thumbnail = row[8],stock=row[9])
#--------------------------------------------------------------------------
#order_statuses.csv
CSV_PATH_PRODUCTS = './csvs/orders_csv/order_statuses.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            status=row[0]
            OrderStatus.objects.create(status=status)
#-----------------------------------------------------------------------------
#order_item_statuses
CSV_PATH_PRODUCTS = './csvs/orders_csv/order_item_statuses.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            status=row[0]
            OrderItemStatus.objects.create(status=status)
#-----------------------------------------------------------
# orders
CSV_PATH_PRODUCTS = './csvs/orders_csv/orders.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            user_id = row[0]
            delivery_date = row[1]
            recipient = row[2]
            phone_number = row[3]
            address = row[4]
            coupon_id = row[5]
            point = row[6]
            delivery_fee = row[7]
            status_id = row[8]
            Order.objects.create(user_id=user_id, delivery_date=delivery_date, recipient=recipient, phone_number=phone_number, address=address, coupon_id=coupon_id, point=point, delivery_fee=delivery_fee, status_id=status_id)
#------------------------------------------------------------
#product_options
CSV_PATH_PRODUCTS = './csvs/products_csv/product_options.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            product_id=row[0]
            option_id=row[1]
            ProductOption.objects.create(product_id=product_id, option_id=option_id)
#------------------------------------------------------------------------
#order_items
CSV_PATH_PRODUCTS = './csvs/orders_csv/order_items.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            quantity=row[0]
            product_id=row[1]
            order_id=row[2]
            status_id=row[3]
            OrderItem.objects.create(quantity=quantity, product_id=product_id, order_id=order_id, status_id=status_id)
#------------------------------------------------------------------------------
# cart_items
CSV_PATH_PRODUCTS = './csvs/orders_csv/cart_items.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            user_id=row[0]
            quantity=row[1]
            product_options=row[2]
            CartItem.objects.create(user_id=user_id,quantity=quantity,product_options_id=product_options)
#----------------------------------------------------------
## insert images
CSV_PATH_USERS = './csvs/products_csv/images.csv'
with open(CSV_PATH_USERS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Image.objects.create(
            image_url = row[0],
            product = Product.objects.get(id=row[1]),
            sequence = row[2]
        )
#-------------------------------------------------------
#reviews
CSV_PATH_PRODUCTS = './csvs/products_csv/reviews.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            user_id=row[0]
            product_id=row[1]
            image_url=row[2]
            title=row[3]
            content=row[4]
            created_at=row[5]
            Review.objects.create(user_id=user_id,product_id=product_id,image_url=image_url,title=title,content=content,created_at=created_at)
#-----------------------------------------------------------------