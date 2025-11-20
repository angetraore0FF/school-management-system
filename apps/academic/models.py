from django.db import models
from apps.users.models import User

class SchoolYear(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    capacity = models.IntegerField(default=30)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class ClassAssignment(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'roles__name': 'TEACHER'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['teacher', 'subject', 'class_obj', 'school_year']
    
    def __str__(self):
        return f"{self.teacher.username} - {self.subject.name} - {self.class_obj.name}"

class StudentEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'roles__name': 'STUDENT'})
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'class_obj', 'school_year']
    
    def __str__(self):
        return f"{self.student.username} - {self.class_obj.name}"

class Grade(models.Model):
    GRADE_TYPES = [
        ('EXAM', 'Examen'),
        ('HOMEWORK', 'Devoir'),
        ('PARTICIPATION', 'Participation'),
        ('PROJECT', 'Projet'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'roles__name': 'STUDENT'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    grade_type = models.CharField(max_length=20, choices=GRADE_TYPES)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    max_value = models.DecimalField(max_digits=5, decimal_places=2, default=20)
    comment = models.TextField(blank=True)
    date_given = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades_given')
    
    def __str__(self):
        return f"{self.student.username} - {self.value}/{self.max_value}"

class Attendance(models.Model):
    PERIOD_CHOICES = [
        ('MORNING', 'Matin'),
        ('AFTERNOON', 'Après-midi'),
        ('FULL_DAY', 'Journée complète'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'roles__name': 'STUDENT'})
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    is_present = models.BooleanField(default=True)
    reason = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances_recorded')
    
    class Meta:
        unique_together = ['student', 'class_obj', 'date', 'period']
    
    def __str__(self):
        status = "Présent" if self.is_present else "Absent"
        return f"{self.student.username} - {self.date} - {status}"