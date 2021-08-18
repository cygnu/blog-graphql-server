from graphene_django.types import DjangoObjectType

from .models import (
    Tag, Category
)

class TagType(DjangoObjectType):
    class Meta:
        model = Tag

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category