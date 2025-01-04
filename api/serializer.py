from django.utils.safestring import mark_safe
from rest_framework import serializers

# from rest_framework.exceptions import AuthenticationFailed
from .models import Measurement, Stock, IngredientGram, Recipe, Product, StockType


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         try:
#             data = super().validate(attrs)
#         except AuthenticationFailed:
#             raise AuthenticationFailed({
#                 "ok": False,
#                 "error_code": "INVALID_CREDENTIALS",
#                 "message": "The provided credentials are incorrect or the account is inactive."
#             })
#         user = self.user
#         data['username'] = getattr(self.user, 'username', None)
#         data['role'] = user.groups.first().name if user.groups.exists() else None
#         data['permissions'] = list(user.get_all_permissions())
#         data['superuser_status'] = user.is_superuser
#         return data


class StockTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockType
        fields = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.CharField(read_only=True)
    types = serializers.PrimaryKeyRelatedField(
        queryset=StockType.objects.all(),
        source='type',  # Assuming 'measurement_unit' is the field name in your model
        write_only=True
    )
    type = StockTypeSerializer(read_only=True)  # Use StockTypeSerializer here

    class Meta:
        model = Measurement
        fields = ['id', 'name', 'type', 'types', 'measurement_unit', 'created', 'updated', 'deleted']


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = MeasurementSerializer(read_only=True, help_text='Yangi mahsulot nomini kiriting',
                                             allow_null=False)

    measurements = serializers.PrimaryKeyRelatedField(
        allow_null=False,
        queryset=Measurement.objects.all(),
        source='measurement_unit',
        write_only=True,
        help_text=('Measurement ni qo`shish uchun <a href="/api/measurements/" target="_self">StockType</a>')
    )

    class Meta:
        model = Stock
        fields = ['id', 'name', 'real_price', 'selling_price', 'measurement_unit', 'measurements', 'created', 'updated',
                  'deleted']

    def update(self, instance, validated_data):
        # Store the old price values and measurement unit
        old_real_price = instance.real_price
        old_selling_price = instance.selling_price
        old_name = instance.name
        old_measurement_unit_id = instance.measurement_unit.id

        # Perform the default update
        instance = super().update(instance, validated_data)

        # If the name or measurement unit id has changed, sync prices
        if old_name != instance.name or old_measurement_unit_id != instance.measurement_unit.id:
            self.sync_prices(instance)

        return instance

    def sync_prices(self, instance):
        # Find all products with the same name and measurement unit id
        matching_products = Product.objects.filter(
            name=instance.name,
            measurement_unit=instance.measurement_unit
        )

        # Update their prices to match the current instance's prices
        for product in matching_products:
            if product != instance:  # Avoid updating the current instance again
                product.real_price = instance.real_price
                product.selling_price = instance.selling_price
                product.save()

        # Update prices for all related stocks as well
        matching_stocks = Stock.objects.filter(
            name=instance.name,
            measurement_unit=instance.measurement_unit
        )

        for stock in matching_stocks:
            if stock != instance:  # Avoid updating the current instance again
                stock.real_price = instance.real_price
                stock.selling_price = instance.selling_price
                stock.save()


class IngredientGramSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)  # Include ingredient details
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=Stock.objects.all(),
        source='ingredient',
        write_only=True,
        help_text=mark_safe(
            'Kerak bo`lgan ritsept uchun qancha mahsulot ketishi yoziladi (Missol uchun: Dona: Sosiska -> 1 yani bir dona Sosiska kerak). '
            'Mahsulot qo\'shish uchun <a href="/api/stock/" target="_self">Stock</a>.'
        )
    )

    # measurement_id = serializers.PrimaryKeyRelatedField(queryset=Measurement.objects.all(),write_only=True,source='measurement_unit',)

    class Meta:
        model = IngredientGram
        fields = ['id', 'ingredient_id', 'amount', 'ingredient', 'created', 'updated', 'deleted']


class RecipeSerializer(serializers.ModelSerializer):
    ingredient = IngredientGramSerializer(many=True, read_only=True)  # Expand ingredient details
    ingredients = serializers.PrimaryKeyRelatedField(
        queryset=IngredientGram.objects.all(),
        source='ingredient',
        many=True,
        write_only=True,
        help_text="Ingridentini 2 va undan ortiqini tanlash uchun \"ctrl\" ni bosib turib tanlan."
                  "Yangi Ingredient yaratish uchun <a href='/api/ingredient-grams/' target='_self'>Ingredient</a> "
    )

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'ingredient', 'ingredients', 'created', 'updated', 'deleted']


class ProductSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(many=True, read_only=True)
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        source='recipe',
        write_only=True,
        help_text='Recipe ID ni <a href="/api/recipes/" target="_self">Recipe</a> bo‘limidan tuzing va bu yerda mahsulotingizni yarating',
    )
    real_cost = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'selling_price', 'recipe', 'recipe_id', 'real_cost', 'created', 'updated', 'deleted',
                  'real_price']
