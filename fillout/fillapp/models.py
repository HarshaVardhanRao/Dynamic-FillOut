from django.contrib.auth.models import AbstractUser
from django.db import models

# 1. Extend Default CustomUser (optional, or use settings.AUTH_USER_MODEL directly)
class CustomUser(AbstractUser):
    pass  # Add custom fields later if needed


# 2. CustomUser Profile (holds reusable details)
class UserProfile(models.Model):
    CustomUser = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    dob = models.DateField(null=True, blank=True)
    # Add more reusable fields as needed

    def __str__(self):
        return self.CustomUser.username


# 3. UserGroup Model
class UserGroup(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField('CustomUser', related_name='custom_groups')


    def __str__(self):
        return self.name


# 4. Form
class Form(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    assigned_group = models.ForeignKey(UserGroup, on_delete=models.SET_NULL, null=True, blank=True)
    open_to_all = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# 5. Form Fields (dynamic questions)
class FormField(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='fields')
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=50, choices=[
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('choice', 'Choice'),
    ])
    required = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.form.title} - {self.label}"


# 6. Form Assignment (track who filled it)
class FormAssignment(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    filled = models.BooleanField(default=False)
    filled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('form', 'assigned_to')


# 7. Form Response
class FormResponse(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    CustomUser = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)


# 8. Field Response
class FieldResponse(models.Model):
    response = models.ForeignKey(FormResponse, on_delete=models.CASCADE, related_name='answers')
    field = models.ForeignKey(FormField, on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return f"{self.field.label}: {self.answer}"
