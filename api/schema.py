import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from blog.scalar import Uuid

from graphql_jwt.decorators import login_required

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


class Query(graphene.ObjectType):
    tag = graphene.Field(
        TagType,
        id=Uuid(),
        name=graphene.String(),
    )
    all_tags = graphene.List(TagType)

    category = graphene.Field(
        CategoryType,
        id=Uuid(),
        name=graphene.String(),
    )
    all_categories = graphene.List(CategoryType)

    @login_required
    def resolve_tag(self, info, id, name):
        return Tag.objects.filter(pk=id, name=name).first()

    @login_required
    def resolve_all_tags(self, info, **kwargs):
        return Tag.objects.all()

    @login_required
    def resolve_category(self, info, id, name):
        return Category.objects.filter(pk=id, name=name).first()

    @login_required
    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()