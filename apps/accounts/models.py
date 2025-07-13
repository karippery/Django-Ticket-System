from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('agent', 'Agent'),
        ('user', 'User'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        app_label = 'accounts'

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_agent(self):
        return self.role == 'agent'

    @property
    def is_user(self):
        return self.role == 'user'
