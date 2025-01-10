from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.models import Product, Measurement, Recipe, IngredientGram, Stock, StockType, Status, Draft
from decorator import check_token
from .serializer import ProductSerializer, RecipeSerializer, IngredientGramSerializer, MeasurementSerializer, \
    IngredientSerializer, StockTypeSerializer, DraftSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = {
        'Name': 'API',
        'path': 'https://fastfoodapi2.onrender.com/api/',
        'description': 'Main API endpoint',
    }
    stock_types = [
        ('Go\'sh mahsuloti', 'Kg'),
        ('Suv', 'Liter'),
        ('Go\'sh mahsuloti', 'Gram'),
        ('Suv', 'MilliLiter'),
        ('Meva', 'Dona'),
        ('Meva', 'Kg'),
        ('Non mahsuloti', 'Dona'),
        ('Non mahsuloti', 'Cm'),
    ]
    status = [
        'Confirmed',
        'Draft',
        'Rejected',
    ]
    for stock_type_name, measurement_name in stock_types:
        stock_type, _ = StockType.objects.get_or_create(name=stock_type_name)  # Avoid duplicates
        Measurement.objects.get_or_create(name=measurement_name, type=stock_type)  # Avoid duplicates
    for statuss in status:
        Status.objects.get_or_create(name=statuss)
    return Response(routes)


@api_view(['GET'])
def GetProducts(request):
    products = Product.objects.prefetch_related('ingredients__ingredient').all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def GetProduct(request, pk):
    room = Product.objects.get(id=pk)
    serializer = ProductSerializer(room, many=False)
    return Response(serializer.data, 200)


class CustomModelViewSet(viewsets.ModelViewSet):
    def dispatch(self, request, *args, **kwargs):
        wrapped_view = check_token(super().dispatch)
        return wrapped_view(request, *args, **kwargs)


class ProductViewSet(CustomModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DraftViewSet(CustomModelViewSet):
    queryset = Draft.objects.all()
    serializer_class = DraftSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class RecipeViewSet(CustomModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def create(self, request, *args, **kwargs):
        # Handle the data from x-www-form-urlencoded
        data = request.data
        # Process or validate the data
        return super().create(request, *args, **kwargs)


class IngredientGramViewSet(viewsets.ModelViewSet):
    queryset = IngredientGram.objects.all()
    serializer_class = IngredientGramSerializer
    permission_classes = [AllowAny]


class StockTypeViewSet(CustomModelViewSet):
    queryset = StockType.objects.all()
    serializer_class = StockTypeSerializer


class IngredientViewSet(CustomModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = IngredientSerializer


class MeasurementViewSet(CustomModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
