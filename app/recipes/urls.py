from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipes import views

"""Create DefaultRouter for the TagViewSet and route all requests to recipe API to that router"""
router = DefaultRouter() # includes standard routes for CRUD operations
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
app_name = 'recipes'

urlpatterns = [
    path('', include(router.urls)) # route all requests against recipes API to DefaultRouter
]
