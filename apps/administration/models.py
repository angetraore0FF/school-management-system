from django.db import models
from apps.users.models import User
from apps.academic.models import SchoolYear

class SystemConfiguration(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.key

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Création'),
        ('UPDATE', 'Modification'),
        ('DELETE', 'Suppression'),
        ('LOGIN', 'Connexion'),
        ('LOGOUT', 'Déconnexion'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, blank=True)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.model_name}"

class AcademicSetting(models.Model):
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    setting_key = models.CharField(max_length=100)
    setting_value = models.TextField()
    
    class Meta:
        unique_together = ['school_year', 'setting_key']
    
    def __str__(self):
        return f"{self.school_year.name} - {self.setting_key}"