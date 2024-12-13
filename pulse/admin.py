from django.contrib import admin
from .models import ContactMessage
from .models import CustomUser, Ticket, Response

# Register your models here.

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)
    
@admin.register(Ticket)
class Ticket(admin.ModelAdmin):
    list_display = ('id', 'customer', 'subject', 'status', 'created_at', 'assigned_staff', 'resolved_by')
    list_filter = ('status',)
    search_fields = ('customer__username', 'subject', 'description', 'issue')
    ordering = ('-created_at',)
    
admin.site.register(CustomUser)

admin.site.register(Response)
