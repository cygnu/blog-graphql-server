from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

from .models import Profile


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class UserProfile(DjangoObjectType):
    class Meta:
        model = Profile