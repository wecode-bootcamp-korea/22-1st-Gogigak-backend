from django.db import models

class Category(models.Model):
    name  = models.CharField(max_length=30) 
    image = models.CharField(max_length=2000)
    
    class Meta:
        db_table = 'categories'

class Product(models.Model):
    name           = models.CharField(max_length=30) 
    category       = models.ForeignKey(Category, on_delete=models.CASCADE)
    butchered_date = models.DateField()
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    grams          = models.DecimalField(max_digits=10, decimal_places=2)
    is_organic     = models.BooleanField(default=False)
    sales          = models.IntegerField()   
    reviews        = models.IntegerField()
    thumbnail      = models.CharField(max_length=2000)
    options        = models.ManyToManyField('Option', through='ProductOption')

    class Meta:
        db_table = 'products'

class Option(models.Model):
    name = models.CharField(max_length=2000)

    class Meta:
        db_table = 'options'

class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option  = models.ForeignKey(Option, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'products_options'


class Image(models.Model):
    product        = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url      = models.CharField(max_length=2000)
    sequence       = models.IntegerField()

    class Meta:
        db_table = 'images'

class Review(models.Model):
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url  = models.CharField(max_length=2000, null=True)
    title      = models.CharField(max_length=100)
    content    = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'