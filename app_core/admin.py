from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile

# Inline pour afficher UserProfile directement dans l’admin User
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profil utilisateur"
    fk_name = "user"

# Nouveau UserAdmin qui inclut UserProfile
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    # pour l’affichage dans la liste des utilisateurs
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "get_role", "get_identifier")
    list_select_related = ("profile",)

    def get_role(self, instance):
        return instance.profile.role
    get_role.short_description = "Rôle"

    def get_identifier(self, instance):
        return instance.profile.user_identifier
    get_identifier.short_description = "Identifiant"

# On désenregistre le User de base et on enregistre notre version custom
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Enregistrer UserProfile séparément si tu veux le gérer directement
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user","first_name","sex","email", "user_identifier", "role", "is_verified", "city", "country")
    search_fields = ("user__username", "user_identifier", "role", "city", "country")
