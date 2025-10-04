import graphene
import graphql_jwt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import PermissionDenied
from .models import*
from .types import*
from .tools import*
from graphql_jwt.decorators import login_required
from graphql import GraphQLError

# ====== MUTATIONS ======

#CREATE -------------------------------------------------
class CreateUser(graphene.Mutation):
    account = graphene.Field(UserProfileDeep)

    class Arguments:
        #mandatory
        first_name = graphene.String(required=True)
        sex=graphene.String(required=True)
        date_of_birth=graphene.Date(required=True)
        password = graphene.String(required=True)
        role = graphene.String(required=True)

        #facultative
        email = graphene.String()
        city = graphene.String()
        country = graphene.String()
        phone=graphene.String()
        

    def mutate(self, info, first_name,sex,date_of_birth, password,role,email=None, city=None,country=None,phone=None):
        user_identifiant=generate_identifiant()
        #checking data
        data={
            "user_identifier":user_identifiant,
            "first_name":clean_and_capitalize(first_name),
            "sex":check_sex(sex),
            "date_of_birth":has_required_age(date_of_birth),
            "password":is_strong_password(password),
            "role":check_role(role),
            "email":is_valid_email(email) if email else None,
            "city":city if city else None,
            "country":country if country else None,
            "phone":is_phone_number_valid(phone) if phone else None

        }
        if data['role']=="TEACHER":
            if not email:
                raise GraphQLError("EMAIL_REQUIRED:A valid email adress are required for teacher account")
            if not phone:
                raise GraphQLError("PHONE_REQUIRED:A valid phone number are required for teacher account")
            if not city:
                raise GraphQLError("CITY_REQUIRED:A city of residence are required for teacher account")
            if not country:
                raise GraphQLError("COUNTRY_REQUIRED:A country of residence are required for teacher account")
        if email and UserProfile.objects.filter(email=email).exists():
            raise GraphQLError("EMAIL_ALREAD_TEKEN") 

        #create Django User instance(for login)
        user = User.objects.create(
            username=data['user_identifier'],
            email=data['email'] if data['email'] else "",
            password=make_password(data.pop('password'))
        )
        data['user']=user

        user_account=UserProfile.objects.create(**data)
        return CreateUser(account=user_account)
#-------------------------------------------------------------------------------

#UPDATE ACCOUNT-----------------------------------------------------------------
class UpdateUserProfile(graphene.Mutation):
    account = graphene.Field(UserProfileDeep)

    class Arguments:
        first_name=graphene.String()
        sex=graphene.String()
        date_of_birth=graphene.Date()
        city = graphene.String()
        country = graphene.String()
        email=graphene.String()
        phone=graphene.String()

    @login_required
    def mutate(self, info,first_name=None, sex=None, date_of_birth=None, email=None,phone=None, city=None, country=None):
        user=info.context.user
        if not UserProfile.objects.filter(user=user).exists():
            raise GraphQLError("USER_ACCOUNT_NOT_EXIST")
        u_account=UserProfile.objects.get(user=user)

        if email and is_valid_email(email):
            if u_account.email != email:
                u_account.email=email
                u_account.is_verified=False
                user.email=email
                user.save()

        if first_name and clean_and_capitalize(first_name):
            if u_account.first_name != first_name:
                u_account.first_name=first_name

        if sex and check_sex(sex):
            if u_account.sex != sex:
                u_account.sex=sex

        if date_of_birth and has_required_age(date_of_birth):
            if u_account.date_of_birth != date_of_birth:
                u_account.date_of_birth=date_of_birth

        if phone and is_phone_number_valid(phone):
            if u_account.phone != phone:
                u_account.phone=phone

        if city and u_account.city != city:
                u_account.city=city
        if country and u_account.country != country:
                u_account.country=country
        u_account.save()
        return UpdateUserProfile(account=u_account)
#-----------------------------------------------------------------------------------

#VERIFY ACCOUNT--------------------------------------------------------------------
class VerifyAccount(graphene.Mutation):
    is_verified=graphene.Boolean()
    

    class Arguments:
        code_verif=graphene.String(required=True)

    @login_required
    def mutate(root, info, code_verif):
        user=info.context.user
        try:
            vc = VerificationCode.objects.filter(user=user, code=code_verif).latest('created_at')
        except VerificationCode.DoesNotExist:
            raise GraphQLError("CODE_INVALID")
        if not vc.is_valid():
            raise GraphQLError("CODE_EXPIRED")

        account=user.profile
        account.is_verified=True
        account.save()
        vc.delete()
        return VerifyAccount(is_verified=True)

#REQUEST CODE-----------------------------------------------------------------------
class RequestCode(graphene.Mutation):
    is_code_sent=graphene.Boolean()
    

    class Arguments:
        email_title=graphene.String(required=True)

    @login_required
    def mutate(root, info, email_title):
        user=info.context.user
        send_verification_code(user, title=email_title)
        return RequestCode(is_code_sent=True)

#DELETE ACCOUNT--------------------------------------------
class DeleteAccount(graphene.Mutation):
    is_deleted = graphene.Boolean()

    class Arguments:
        user_password=graphene.String(required=True)

    @login_required
    def mutate(self, info, user_password):
        user = info.context.user
        if not check_password(user_password, user.password):
            raise GraphQLError("WRONG_PASSWORD")
        try:
            user.delete()#this will also delete user profile
            return DeleteAccount(is_deleted=True)
        except:
            raise GraphQLError("DELETE_ACCOUNT_ERROR")

class AdminDeleteAccount(graphene.Mutation):
    is_deleted = graphene.Boolean()

    class Arguments:
        acc_identifiant=graphene.String(required=True)
        admin_password=graphene.String(required=True)

    @login_required
    def mutate(self, info, acc_identifiant):
        user = info.context.user
        if not check_password(admin_password, user.password):
            raise GraphQLError("WRONG_PASSWORD")
        if not user.is_superuser:
            raise GraphQLError("OPERATION_DENIED")

        if not UserProfile.objects.filter(user_identifier=acc_identifiant).exists():
            raise GraphQLError("ACCOUNT_DOESNT_EXIST")
        UserProfile.objects.get(user_identifier=acc_identifiant).user.delete()
        return AdminDeleteAccount(is_deleted=True)

class DeleteStudentAccount():#teacher can delete they student account

    class Arguments:
        pass

#-------------------------------------------------------------------------------------

        


#MOT DE PASSE--------------------------------------------------------------
class ChangePassword(graphene.Mutation):
    is_pwd_changed = graphene.Boolean()

    class Arguments:
        old_password = graphene.String(required=True)
        new_password = graphene.String(required=True)

    @login_required
    def mutate(self, info, old_password, new_password):
        user = info.context.user
        profile = user.profile
        if not check_password(old_password, user.password):
            raise GraphQLError("WRONG_CURRENT_PASSWORD")

        user.password = make_password(new_password)
        user.save()
        return ChangePassword(is_pwd_changed=True)
#----------------------------------------------------------------------------------


class ResetPassword(graphene.Mutation):
    is_pwd_reset = graphene.Boolean()

    class Arguments:
        username = graphene.String(required=True)
        code = graphene.String(required=True)
        new_password = graphene.String(required=True)

    def mutate(self, info, username, code, new_password):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise GraphQLError("USERNAME_DOESNT_EXIST")

        try:
            vc = VerificationCode.objects.filter(user=user, code=code).latest('created_at')
        except VerificationCode.DoesNotExist:
            raise GraphQLError("CODE_INVALID")
        if not vc.is_valid():
            raise GraphQLError("CODE_EXPIRED")
        user.password = make_password(is_strong_password(new_password))
        user.save()
        vc.delete()
        return ResetPassword(is_pwd_reset=True)

# ====== MUTATION ROOT ======
class Mutation(graphene.ObjectType):
    create_account = CreateUser.Field()
    update_account = UpdateUserProfile.Field()
    delete_account = DeleteAccount.Field()
    admin_delete_account=AdminDeleteAccount.Field()
    change_password = ChangePassword.Field()
    request_code=RequestCode.Field()
    verify_account=VerifyAccount.Field()
    reset_password = ResetPassword.Field()

    #Token manager------------------------
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    #-----------------------------