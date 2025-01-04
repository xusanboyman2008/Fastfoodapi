from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Product, Measurement, Recipe, IngredientGram, Stock, StockType
from decorator import check_token
from .serializer import ProductSerializer, RecipeSerializer, IngredientGramSerializer, MeasurementSerializer, \
    IngredientSerializer, StockTypeSerializer


@api_view(['GET'])
def getRoutes(request):
    routes =  {
            'Name': 'API',
            'path': 'http://127.0.0.1:8000/api/',
            'description': 'Main API endpoint',
        }
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
        # Apply the check_token decorator to every method call
        wrapped_view = check_token(super().dispatch)
        return wrapped_view(request, *args, **kwargs)
class ProductViewSet(CustomModelViewSet):
    queryset = Product.objects.prefetch_related('recipe__ingredient').all()
    serializer_class = ProductSerializer

class RecipeViewSet(CustomModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class IngredientGramViewSet(CustomModelViewSet):
    queryset = IngredientGram.objects.all()
    serializer_class = IngredientGramSerializer

class StockTypeViewSet(CustomModelViewSet):
    queryset = StockType.objects.all()
    serializer_class = StockTypeSerializer

class IngredientViewSet(CustomModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = IngredientSerializer

class MeasurementViewSet(CustomModelViewSet):
        queryset = Measurement.objects.all()
        serializer_class = MeasurementSerializer
