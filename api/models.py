from django.db import models
from django.utils import timezone

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

class Status(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)
    def __str__(self):
        return self.name

class Draft(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    real_price = models.FloatField(null=True, blank=True)
    selling_price = models.FloatField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    measurement_unit = models.ForeignKey(
        Measurement,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)
    expired_at = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)

    def expired(self):
        if self.expired_at:
            return timezone.now() > self.expired_at
        else:
            return True

    def __str__(self):
        return self.name


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    real_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    amount = models.FloatField(null=True, blank=False)
    size = models.FloatField(null=True, blank=True)
    measurement_unit = models.ForeignKey(
        Measurement,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    expired_at = models.DateField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)

    def is_expired(self):
        return self.expired_at < timezone.now().date()

    def __str__(self):
        return f"{self.name}: {self.measurement_unit.type.name}"

    class Meta:
        ordering = ['-expired_at']


class IngredientGram(models.Model):
    id = models.AutoField(primary_key=True)
    ingredient = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE, null=False, blank=False, related_name="ingredient"
    )
    amount = models.FloatField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ingredient.name} {self.amount}"


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    ingredient = models.ManyToManyField(
        IngredientGram,
        related_name="recipes",
        blank=False,
    )
    name = models.TextField(max_length=100, null=False, blank=False)
    changes = models.TextField(null=True, blank=True)

    # Always define the field as a FloatField, don't make it conditional.
    changed_price = models.FloatField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    real_price = models.FloatField(null=True, blank=True)
    selling_price = models.FloatField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)

    def calculate_real_price(self):
        total_price = 0
        # Loop through ingredients in the recipe associated with this product
        for ingredient_gram in self.recipe.ingredient.all():
            # Get the price of the ingredient from the Stock model
            stock = ingredient_gram.ingredient
            # Calculate the price based on amount and stock price
            ingredient_price = stock.real_price * ingredient_gram.amount
            total_price += ingredient_price
        return total_price

    def save(self, *args, **kwargs):
        # Automatically calculate the real price before saving
        self.real_price = self.calculate_real_price()
        # Set selling_price if not provided (Optional: Add custom logic here)
        if self.selling_price is None:
            self.selling_price = self.real_price * 1.2  # Example: 20% markup for selling price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


class SellProduct(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(null=False, blank=False)
    changes = models.TextField(null=True, blank=True)
    price = models.FloatField(null=False)
    updated_price = models.FloatField(null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name
