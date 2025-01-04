from django.db import models



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
    name = models.TextField(max_length=100)
    type = models.ForeignKey(StockType, on_delete=models.CASCADE,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {self.type}"



class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(StockType, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    real_price = models.FloatField(null=True)
    selling_price = models.FloatField(null=True)
    amount = models.FloatField(null=True)
    size = models.FloatField(null=True, blank=True)
    measurement_unit = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)

    def update_related_real_price(self):
        """
        Update the real_price for all products with the same name and measurement unit,
        excluding the current product.
        """
        related_stocks = Stock.objects.filter(
            name=self.name,
            measurement_unit=self.measurement_unit
        ).exclude(id=self.id)  # Exclude the current stock instance to avoid updating itself.

        for stock in related_stocks:
            related_products = Product.objects.filter(
                recipe__ingredient__ingredient=stock
            )
            for product in related_products:
                product.real_price = self.real_price  # Update real_price of the product
                product.save()

    def update_related_selling_price(self):
        """
        Update the selling_price for all products with the same name and measurement unit,
        excluding the current product.
        """
        related_stocks = Stock.objects.filter(
            name=self.name,
            measurement_unit=self.measurement_unit
        ).exclude(id=self.id)  # Exclude the current stock instance to avoid updating itself.

        for stock in related_stocks:
            related_products = Product.objects.filter(
                recipe__ingredient__ingredient=stock
            )
            for product in related_products:
                product.selling_price = self.selling_price  # Update selling_price of the product
                product.save()


class IngredientGram(models.Model):
    id = models.AutoField(primary_key=True)
    ingredient = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount = models.FloatField()
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
    if changes:
        change_price = models.FloatField(null=True)
    else:
        change_price = models.FloatField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)
    ingredient = models.ManyToManyField(IngredientGram)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    real_price = models.FloatField(null=False)
    selling_price = models.FloatField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)
    recipe = models.ManyToManyField(Recipe)

    def __str__(self):
        return self.name