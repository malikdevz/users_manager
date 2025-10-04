import graphene
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .models import *
from .types import *
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

# ====== QUERIES ======
class Query(graphene.ObjectType):
    account = graphene.Field(UserProfileDeep)
    all_accounts = graphene.List(UserProfileType)
    account_by_identifiant = graphene.Field(UserProfileType, user_identifiant=graphene.String(required=True))

    @login_required
    def resolve_account(root, info):
        user = info.context.user
        if not UserProfile.objects.filter(user=user).exists():
            raise GraphQLError("INVALID_USER_IDENTIFIANT")
        return UserProfile.objects.get(user=user)

    @login_required
    def resolve_all_accounts(root, info):
        user = info.context.user
        return UserProfile.objects.filter(user__is_superuser=False)

    @login_required
    def resolve_account_by_identifiant(root, info, user_identifiant):
        user = info.context.user
        if not UserProfile.objects.filter(user_identifier=user_identifiant).exists():
            raise GraphQLError("ACCOUNT_DOESNT_EXIST")

        return UserProfile.objects.get(user_identifier=user_identifiant)