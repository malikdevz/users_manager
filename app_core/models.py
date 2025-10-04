from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    date_add=models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100)  # prénom

    #sexe---------------------
    SEX_CHOICES = [
        ("M", "M"),
        ("F", "F"),
        ("Not.Binary", "Not.Binary"),
    ]
    sex = models.CharField(max_length=50, choices=SEX_CHOICES, null=True, blank=True)
    #-------------------------------------
    date_of_birth = models.DateField(null=True, blank=True)
    #role--------
    ROLE_CHOICES = [
        ("STUDENT", "STUDENT"),
        ("TEACHER", "TEACHER"),
        ("ADMIN", "ADMIN"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")
    #--------------------------

    # identifiant utilisateur
    user_identifier = models.CharField(max_length=50, unique=True)
    #email verification (for teacher only)
    is_verified = models.BooleanField(default=False)

    # champs facultatifs
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    #controle
    is_pwd_changed=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.user_identifier}"


class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expires_at

