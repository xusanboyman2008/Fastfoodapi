from django.db import models

from AUTH_USER.models import User


class StockType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Measurement(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # Changed TextField to CharField for max_length
    type = models.ForeignKey(
        StockType,
        on_delete=models.CASCADE,
        null=True,
        related_name="measurements"  # Unique related_name
    )
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {self.type}"


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(
        StockType,
        on_delete=models.CASCADE,
        null=True,
        related_name="stocks"  # Unique related_name
    )
    name = models.CharField(max_length=100)
    real_price = models.FloatField(null=True)
    selling_price = models.FloatField(null=True)
    amount = models.FloatField(null=True)
    size = models.FloatField(null=True, blank=True)
    measurement_unit = models.ForeignKey(
        Measurement,
        on_delete=models.CASCADE,
        null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {self.type}"



class IngredientGram(models.Model):
    id = models.AutoField(primary_key=True)
    ingredient = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount = models.FloatField(null=True,blank=True)
    # measure_unit = models.ForeignKey(Measurement, on_delete=models.CASCADE,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.ingredient.name} {self.amount}"


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100,null=True)
    changes = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)
    ingredient = models.ManyToManyField(IngredientGram)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ManyToManyField(Recipe)
    name = models.CharField(max_length=100, null=False)
    real_price = models.FloatField(null=False)
    selling_price = models.FloatField(null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
    

class SellProduct(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    changes = models.TextField(null=True,blank=True)
    price = models.FloatField(null=False)
    updated_price = models.FloatField(null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name

