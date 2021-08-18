import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

from .models import (
    Tag, Category, Post
)

class TagType(DjangoObjectType):
    class Meta:
        model = Tag

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        filter_fields = {
            'title': ['icontains'],
            'author': ['exact'],
            'content': ['icontains'],
            'tags': ['exact'],
            'tags__name': ['exact'],
            'category': ['exact'],
            'category__name': ['icontains'],
        }
        interfaces = (relay.Node,)