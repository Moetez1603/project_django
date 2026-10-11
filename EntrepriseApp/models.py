import uuid
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


matricule_fiscal_validator = RegexValidator(
    regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$',
    message='Format fiscal incorrect.',
)


def generate_user_id():
    return f'U{uuid.uuid4().hex[:7].upper()}'


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not extra_fields.get('user_id'):
            extra_fields['user_id'] = generate_user_id()
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        if not extra_fields.get('user_id'):
            extra_fields['user_id'] = generate_user_id()
        extra_fields.setdefault('role', 'admin')
        return super().create_superuser(username, email, password, **extra_fields)


class Utilisateur(AbstractUser):
    user_id = models.CharField(
        max_length=8,
        primary_key=True,
        default=generate_user_id,
        editable=False,
    )
    email = models.EmailField(unique=True, null=False, blank=False)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Admin'),
            ('chargeur', 'Chargeur'),
            ('transporteur', 'Transporteur'),
        ],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.username} ({self.role})'


class Entreprise(models.Model):
    raison_sociale = models.CharField(max_length=255, null=False, blank=False)
    matricule_fiscal = models.CharField(
        max_length=17,
        unique=True,
        validators=[matricule_fiscal_validator],
    )
    type_entreprise = models.CharField(
        max_length=100,
        choices=[
            ('chargeur', 'Chargeur'),
            ('transporteur', 'Transporteur'),
        ],
        default='chargeur',
    )

    adresse = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='entreprise',
    )

    def __str__(self):
        return self.raison_sociale
