from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission

# Custom User model with roles
class CustomUser(AbstractUser):
    ROLES = (
        ('customer', 'Customer'),
        ('staff', 'Staff'),
    )
    role = models.CharField(max_length=10, choices=ROLES)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Unique related_name
        blank=True
    )

# Ticket Model
class Ticket(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_tickets'
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    issue = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('resolved', 'Resolved')],  # Renamed completed to resolved
        default='pending'
    )
    assigned_staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_tickets'
    )
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_tickets'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Ticket ID {self.id} - {self.subject} ({self.status})"

# Response Model
class Response(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='responses')
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'staff'}
    )
    response_text = models.TextField()
    responded_at = models.DateTimeField(auto_now_add=True)
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
