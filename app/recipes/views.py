from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag, Ingredient
from recipes import serializers


class BaseRecipeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Returns only the tags that were submitted by the authenticated user"""
        return self.queryset.filter(submitted_by=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)


class TagViewSet(BaseRecipeViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
