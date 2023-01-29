from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)

class Transaction(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    notes = models.TextField(blank=True)
    is_income = models.BooleanField(default=False)
    reciept = models.ImageField(upload_to='', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
