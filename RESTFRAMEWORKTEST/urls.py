from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views
from api.views import RecipeViewSet, IngredientGramViewSet, MeasurementViewSet, ProductViewSet, IngredientViewSet, StockTypeViewSet

router = DefaultRouter()

# Registering routes without using the `check_token` decorator
router.register(r'products', ProductViewSet)




router.register(r'stock', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredient-grams', IngredientGramViewSet)
router.register(r'measurements', MeasurementViewSet)
router.register(r'stockType',StockTypeViewSet)

urlpatterns = [
    # Admin URL doesn't require token checking by this decorator
    path('admin/', admin.site.urls),

    # Include API router URLs
    path('api/', include(router.urls)),

    # Include your authentication URLs
    path('auth/', include('AUTH_USER.urls')),
    path('',views.getRoutes,name='home'),
]
