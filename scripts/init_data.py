import os
import django
import sys

# Ajouter le chemin du projet au Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User, Role
from apps.academic.models import SchoolYear, Subject, Class

def init_roles():
    roles = [
        ('ADMIN', 'Administrateur du système'),
        ('TEACHER', 'Enseignant'),
        ('STUDENT', 'Élève'),
        ('PARENT', 'Parent'),
    ]
    
    for role_name, description in roles:
        Role.objects.get_or_create(
            name=role_name,
            defaults={'description': description}
        )
    print("✅ Rôles initialisés")

def init_admin_user():
    admin_role = Role.objects.get(name='ADMIN')
    
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@school.com',
            password='admin123',
            first_name='Admin',
            last_name='System'
        )
        admin_user.roles.add(admin_role)
        print("✅ Utilisateur admin créé")
    else:
        print("⚠️  Utilisateur admin existe déjà")

def init_sample_data():
    # Année scolaire
    current_year, created = SchoolYear.objects.get_or_create(
        name='2024-2025',
        defaults={
            'start_date': '2024-09-01',
            'end_date': '2025-06-30',
            'is_active': True
        }
    )
    
    # Matières
    subjects = [
        ('MATH', 'Mathématiques'),
        ('FRENCH', 'Français'),
        ('ENGLISH', 'Anglais'),
        ('HISTORY', 'Histoire'),
        ('SCIENCE', 'Sciences'),
    ]
    
    for code, name in subjects:
        Subject.objects.get_or_create(
            code=code,
            defaults={'name': name}
        )
    
    # Classes
    classes_data = [
        ('Terminale S1', 'TS1'),
        ('Terminale S2', 'TS2'),
        ('Première S1', '1S1'),
        ('Seconde G1', '2G1'),
    ]
    
    for name, code in classes_data:
        Class.objects.get_or_create(
            name=name,
            code=code,
            defaults={
                'capacity': 35,
                'school_year': current_year
            }
        )
    
    print("✅ Données d'exemple créées")

if __name__ == '__main__':
    print("🎯 Début de l'initialisation des données...")
    init_roles()
    init_admin_user()
    init_sample_data()
    print("🎉 Initialisation terminée avec succès!")