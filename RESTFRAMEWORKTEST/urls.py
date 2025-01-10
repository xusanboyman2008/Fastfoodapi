from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tutorial.quickstart.views import UserViewSet

from api import views
from api.views import RecipeViewSet, IngredientGramViewSet, MeasurementViewSet, ProductViewSet, IngredientViewSet, \
    StockTypeViewSet, DraftViewSet

router = DefaultRouter()

# Registering routes without using the `check_token` decorator
router.register(r'products', ProductViewSet)




router.register(r'stock', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredient', IngredientGramViewSet)
router.register(r'measurements', MeasurementViewSet)
router.register(r'stockType',StockTypeViewSet)
router.register(r'draft',DraftViewSet)
urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout endpoints
    path('admin/', admin.site.urls),

    # Include API router URLs
    path('api/', include(router.urls)),

    # Include your authentication URLs
    path('auth/', include('AUTH_USER.urls')),
    path('',views.getRoutes,name='home'),
]
