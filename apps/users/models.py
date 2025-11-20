from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    ADMIN = 'ADMIN'
    TEACHER = 'TEACHER'
    STUDENT = 'STUDENT'
    PARENT = 'PARENT'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrateur'),
        (TEACHER, 'Enseignant'),
        (STUDENT, 'Élève'),
        (PARENT, 'Parent'),
    ]
    
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.get_name_display()

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    roles = models.ManyToManyField(Role, related_name='users')
    
    def __str__(self):
        return f"{self.username} ({self.get_primary_role()})"
    
    def get_primary_role(self):
        return self.roles.first().name if self.roles.exists() else None
    
    def has_role(self, role_name):
        return self.roles.filter(name=role_name).exists()
    
    class Meta:
        db_table = 'users'