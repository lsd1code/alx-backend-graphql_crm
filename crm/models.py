from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f'{self.name} - {self.email}'


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    stock = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'{self.name} - {self.price}'


class Order(models.Model):
    customer_id = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, related_name='orders',
    )
    product_ids = models.ManyToManyField(
        Product
    )
    order_date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.id} - {self.order_date}'  # type:ignore
