from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    pincode = models.CharField(max_length=6)

    payment_mode = models.CharField(max_length=20)
    payment_status = models.CharField(max_length=20)

    payment_id = models.CharField(max_length=200, blank=True, null=True)

    total_amount = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name



class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()

    price = models.IntegerField()

    def __str__(self):
        return self.product.name