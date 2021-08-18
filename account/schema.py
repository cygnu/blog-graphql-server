import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required

from .models import Profile, LinkInBio


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class UserProfile(DjangoObjectType):
    class Meta:
        model = Profile

class LinkInBioType(DjangoObjectType):
    class Meta:
        model = LinkInBio


class Query(graphene.ObjectType):
    viewer = graphene.Field(UserProfile)
    all_users = graphene.List(UserType)

    @login_required
    def resolve_viewer(self, info, **kwargs):
        return Profile.objects.get(user_prof=info.context.user.id)

    @login_required
    def resolve_all_users(self, info, **kwargs):
        return get_user_model().objects.all()