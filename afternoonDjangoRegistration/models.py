from django.db import models


class Product(models.Model):
    prod_name = models.CharField(max_length=30,
                                 blank=False, null=False)
    prod_price = models.CharField(max_length=30,
                                  blank=False, null=False)
    prod_quantity = models.CharField(max_length=30,
                                     blank=False, null=False)


def __str__(self):
    return self.prod_name


class Supplier(models.Model):
    sup_name = models.CharField(max_length=30,
                                blank=False, null=False)
    sup_email = models.EmailField(max_length=30,
                                  blank=False, null=False)
    sup_phone = models.CharField(max_length=30,
                                 blank=False, null=False)
    sup_product = models.CharField(max_length=30,
                                   blank=False, null=False)


def __str__(self):
    return self.sup_name
