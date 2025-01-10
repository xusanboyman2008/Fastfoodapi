from rest_framework import serializers

from .models import Measurement, Stock, IngredientGram, Recipe, Product, StockType, Draft


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
        fields = ['id', 'name', 'created', 'updated', 'deleted']


class MeasurementSerializer(serializers.ModelSerializer):
    # measurement_unit = StockTypeSerializer()
    types = serializers.PrimaryKeyRelatedField(queryset=StockType.objects.all(), source='type',
                                               write_only=True)
    type = StockTypeSerializer(read_only=True)

    class Meta:
        model = Measurement
        fields = ['id', 'name', 'type', 'types', 'created', 'updated', 'deleted']


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.CharField(source="measurement_unit.name", read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'name', 'real_price', 'selling_price', 'measurement_unit', 'size', 'amount', 'expired_at']


class IngredientGramSerializer(serializers.ModelSerializer):
    ingredient_details = IngredientSerializer(source="ingredient", read_only=True)

    class Meta:
        model = IngredientGram
        fields = ['id', 'amount', 'ingredient_details']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientGramSerializer(source="ingredient", many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'changes', 'changed_price', 'ingredients']


class DraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ['id', 'name', 'real_price', 'selling_price', 'measurement_unit', 'amount', 'expired_at',
                  'status', 'user']
        read_only_fields = ['user']  # Make 'user' read-only so it's auto-assigned

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Assign the authenticated user to the 'user' field (optional)
        validated_data['user'] = self.context['request'].user
        return super().update(instance, validated_data)


class ProductSerializer(serializers.ModelSerializer):
    recipe_details = RecipeSerializer(source="recipe", read_only=True)
    selling_price = serializers.FloatField(write_only=True)
    cost = serializers.FloatField(read_only=True, source="selling_price")

    class Meta:
        model = Product
        fields = ['id', 'name', 'selling_price', 'cost', 'real_price', 'recipe', 'recipe_details', 'created', 'updated',
                  'deleted']
