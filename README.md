# 🎓 Système de Gestion Scolaire (SMS)

Un système de gestion scolaire moderne développé avec Django REST Framework et React.

## 🚀 Fonctionnalités

### Rôles et Permissions
- 👨‍💼 **Administrateur** : Gestion complète du système
- 👨‍🏫 **Enseignant** : Gestion des notes et absences
- 👨‍🎓 **Élève** : Consultation des notes (à venir)
- 👨‍👩‍👧 **Parent** : Suivi des enfants (à venir)

### Modules Principaux
- ✅ Authentification JWT sécurisée
- ✅ Gestion des utilisateurs et rôles
- ✅ Gestion académique (classes, matières, notes)
- ✅ Gestion des absences
- ✅ API RESTful complète
- ✅ Architecture modulaire et extensible

## 🛠️ Stack Technique

### Backend
- **Framework** : Django 4.2 & Django REST Framework
- **Base de données** : PostgreSQL / SQLite3 (développement)
- **Authentification** : JWT (JSON Web Tokens)
- **Architecture** : API RESTful

### Frontend (À venir)
- **Framework** : React
- **State Management** : Redux Toolkit
- **UI Library** : Material-UI ou Ant Design

## 📦 Installation

### Prérequis
- Python 3.8+
- PostgreSQL (recommandé) ou SQLite3
- Node.js (pour le frontend, à venir)

### Backend

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/school-management-system.git
cd school-management-system

python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser
python manage.py runserver

Fork le projet

Créer une branche feature (git checkout -b feature/AmazingFeature)

Commit les changements (git commit -m 'Add AmazingFeature')

Push vers la branche (git push origin feature/AmazingFeature)

Ouvrir une Pull Request
