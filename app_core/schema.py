import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import PermissionDenied
from .models import UserProfile
from .queries import Query as uQuery
from .mutations import Mutation as uMutation

# ====== QUERIES ======
class Query(uQuery,graphene.ObjectType):
    pass

# ====== MUTATIONS ======
class Mutation(uMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
