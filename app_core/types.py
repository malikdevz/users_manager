import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import UserProfile

# ====== TYPES ======
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id","username")

class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = ("date_add","first_name","sex","date_of_birth","role","city","country")

class UserProfileDeep(DjangoObjectType):
     class Meta:
        model=UserProfile
        fields="__all__"