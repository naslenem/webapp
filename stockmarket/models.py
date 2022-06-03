from django.db import models
from django.contrib.auth.models import Permission, User
from django.urls import reverse
# Create your models here.


class Stock(models.Model):
    symbol = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    countrycode = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    point_q = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    day_lowest = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    day_highest = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    p_e = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    market_cap = models.CharField(max_length=100, default="0")
    public_float = models.CharField(max_length=100, default="0")
    eps = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    dividend = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def get_absolute_url(self):
        return reverse('stockmarket:detail', kwargs={'album_id': self.pk})

    def __str__(self):
        return self.name


class Associate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=10000)

    def __str__(self):
        return str(self.user) + "'s account"


class StocksOwned(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    numberofstocks = models.IntegerField()
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=10000)
    transactiontype = models.CharField(max_length=4)
    date = models.DateField()
