import datetime
from django.db import models
from mahsulotlar.models import Product


class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=30)

    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        else:
            return False

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def register(self):
        self.save()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Orders(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=40, default='', blank=True)
    phone_number = models.CharField(max_length=15, default='', blank=True)
    date = models.DateTimeField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Orders.objects.filter(customer=customer_id).order_by('-date')

    def get_order(self):
        self.save()

    def __str__(self):
        return f'{self.customer} {self.id}'
