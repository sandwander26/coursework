from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models

class FlowerList(models.Model):
    CATEGORY_CHOICES = (
        ('bouquet', 'Букет'),
        ('gift', 'Подарок'),
        ('set', 'Набор'),
    )
    def __str__(self) -> str:
        return f"{self.name}, ID = {self.id!r}"

    image = models.ImageField(null=True, blank=True, upload_to='flowers/')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    archived = models.BooleanField(default=False)
    number_of_uses = models.SmallIntegerField(default=0)

class Cart(models.Model):
    def __str__(self) -> str:
        return f"ID = {self.id!r}, автор = {self.user}"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(FlowerList, related_name="products")

class Order(models.Model):
    def __str__(self) -> str:
        return f"ID = {self.id!r}, автор = {self.user}"

    delivery_adress = models.TextField(null=True, blank=True)
    phone = models.BigIntegerField(null=True, blank=True, default=0)
    promocode = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(FlowerList, related_name="order_products")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    final_sum = models.SmallIntegerField(null=True, blank=True)
    # cart = models.OneToOneField(Cart, related_name="flowers", on_delete=models.CASCADE)

class Promocode(models.Model):
    def __str__(self) -> str:
        return f"Text = {self.text!r}, процент скидки = {self.count!r}"

    text = models.TextField(null=False, blank=False, max_length=10)
    count = models.SmallIntegerField(null=False, blank=False, validators=[MaxValueValidator(100)])