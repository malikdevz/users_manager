from graphql import GraphQLError
from django.contrib.auth.models import User
from datetime import date
import random
import re
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
import random, string
from datetime import timedelta
from django.utils import timezone
from .models import VerificationCode
from django.core.mail import send_mail
from django.conf import settings


#une fonction utilitaire pour envoyer le mail--------------------------------------------------------------
def send_verification_code(user, title="ICARTABLE!"):
    # Générer un code à 6 chiffres
    code = ''.join(random.choices(string.digits, k=6))
    expires_at = timezone.now() + timedelta(minutes=10)  # expire après 10 min

    VerificationCode.objects.create(user=user, code=code, expires_at=expires_at)

    send_mail(title,f"Hello {user.profile.first_name}, votre code de confirmation est: {code}. valable pour 10 minutes",settings.EMAIL_HOST_USER,[user.email],fail_silently=False)

def generate_identifiant():
	idx=1
	u_gen_id=""
	while len(u_gen_id) < 1 or User.objects.filter(username=u_gen_id).exists():
		idx=idx+1
		u_gen_id=f"U{random.randint(1000,9999)+idx}"
	return u_gen_id
	

def check_sex(sex):
	if sex not in ['M','F','Not.Binary']:
		raise GraphQLError("INVALID_SEX:Must be one of these, M, F, Not.Binary")
	return sex


def has_required_age(birth_date, required_age=10):
    """
    Vérifie si l'utilisateur a au moins l'âge requis.
    
    :param birth_date: datetime.date — date de naissance
    :param required_age: int — âge minimum requis
    :return: bool
    """
    today = date.today()
    age = today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )
    if age >= required_age:
    	return birth_date
    else:
    	raise GraphQLError("AGE_INVALID:Must have atleast 10 years")


def is_strong_password(password):
    """
    Vérifie si un mot de passe est fort :
    - au moins 6 caractères
    - contient des lettres majuscules et minuscules
    - contient des chiffres
    - contient au moins un caractère spécial
    """
    if len(password) < 6:
        raise GraphQLError("PASSWORD_TO_SHORT:Must have atleast 6 characteres")
    
    has_upper = re.search(r'[A-Z]', password)
    has_lower = re.search(r'[a-z]', password)
    has_digit = re.search(r'\d', password)
    has_special =re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=/\\\[\]~`]', password)

    if not all([has_upper, has_lower, has_digit, has_special]):
    	raise GraphQLError("PASSWORD_INVALID:Must merge upper, lower, digit and special chart")

    return password

def check_role(role):
	if role not in ['STUDENT','TEACHER','ADMIN']:
		raise GraphQLError("INVALID_ROLE:Must be one of these, STUDENT, TEACHER, ADMIN")
	return role

def is_valid_email(email):
    """
    Vérifie si l'adresse e-mail est valide.
    Retourne True si valide, False sinon.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email) is not None:
    	raise GraphQLError("EMAIL_INVALID:Must provide valid email for verification")

    return email


def is_phone_number_valid(numero):
    """
    Vérifie si un numéro de téléphone est valide selon le format international.
    Utilise la librairie 'phonenumbers'.
    Exemple de format accepté : +243970000000
    """
    try:
        parsed = phonenumbers.parse(numero, None)  # None = détecte l'indicatif auto
        if phonenumbers.is_valid_number(parsed):
        	return numero
        else:
        	raise GraphQLError("PHONE_INVALID:Must provide valid phone number")
    except NumberParseException:
        raise GraphQLError("PHONE_INVALID:Must provide valid phone number")


def clean_and_capitalize(first_name):
    """
    Vérifie que le mot ne contient pas de chiffres ni de caractères spéciaux.
    Si c'est correct, renvoie le mot avec la première lettre en majuscule.
    Sinon, renvoie None.
    """
    if re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ]+$', first_name):  # accepte lettres et accents
        return first_name.capitalize()
    raise GraphQLError("FIRST_NAME_INVALID:Must contain only letters")

