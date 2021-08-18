import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from blog.scalar import Uuid

from graphene_django.filter import DjangoFilterConnectionField
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

    post = graphene.Field(
        PostNode,
        id=Uuid(),
        author_username=graphene.String(),
        tags_name=graphene.List(graphene.String),
        category_name=graphene.String(),
    )
    all_posts = DjangoFilterConnectionField(PostNode)

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

    @login_required
    def resolve_post(self, info, id, author__username, tags__name, category__name):
        return Post.objects.filter(
            pk=id,
            author_username=author__username,
            tags_name=tags__name,
            category_name=category__name,
        ).first()

    @login_required
    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.all()


class AddTagInput(graphene.InputObjectType):
    name = graphene.String(required=True)

class AddTagMutation(graphene.Mutation):
    tag = graphene.Field(TagType)

    class Arguments:
        input = AddTagInput(required=True)

    @login_required
    def mutate(self, info, **kwargs):
        tag = Tag.objects.create(**kwargs)
        return AddTagMutation(tag=tag)


class RemoveTagInput(graphene.InputObjectType):
    id = Uuid(required=True)

class RemoveTagMutation(graphene.Mutation):
    tag = graphene.Field(TagType)

    class Arguments:
        input = RemoveTagInput(required=True)

    @login_required
    def mutate(self, info, **kwargs):
        tag = Tag.objects.get(**kwargs)
        tag.delete()
        return RemoveTagMutation(tag=None)


class Mutation(graphene.ObjectType):
    add_tag = AddTagMutation.Field()
    remove_tag = RemoveTagMutation.Field()