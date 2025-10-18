from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'System Admin'),
        ('driver', 'Bus Driver'),
        ('parent', 'Parent'),
        ('school_staff', 'School Staff'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='parent')
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"