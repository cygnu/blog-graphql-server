from graphene_django.types import DjangoObjectType

from .models import (
    Tag
)

class TagType(DjangoObjectType):
    class Meta:
        model = Tag
