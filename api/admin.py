from django.contrib import admin

from AUTH_USER.models import User
from api.models import Recipe, Stock, Product, Measurement, IngredientGram, StockType

# Register your models here.
admin.site.register(User)
admin.site.register(Recipe)
admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(StockType)
admin.site.register(Measurement)
admin.site.register(IngredientGram)