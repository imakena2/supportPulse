from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm,TicketForm,TicketResponseForm,CustomerRegistrationForm,Ticket
from .models import ContactMessage
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
import requests
from decouple import config
from django.conf import settings
from datetime import datetime
import base64


# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def features(request):
    return render(request, 'features.html')

def services(request):
    return render(request, 'services.html')

def pricing(request):
    return render(request, 'pricing.html')

def monitoring(request):
    return render(request, 'monitoring.html')

def details(request):
    return render(request, 'details.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data to the ContactMessage model
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
            )
            return JsonResponse({"success": "Your message has been sent. Thank you!"})
        else:
            return JsonResponse({"error": "Please correct the errors in the form."}, status=400)
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})




@login_required

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            # Save the ticket data
            ticket = form.save(commit=False)
            ticket.customer = request.user
            ticket.save()

            # Show a success message
            messages.success(request, "Your ticket has been submitted successfully! Thank you for your patience as we work to resolve your issue.")

            # Redirect to the same page to clear the form
            return redirect('create_ticket')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = TicketForm()

    return render(request, 'create_tickets.html', {'form': form})

# amendments
def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save(commit=False)
            user.role = 'customer'  # Assign the 'customer' role
            user.set_password(form.cleaned_data['password'])  # Set the password
            user.save()

            # Automatically log the user in after registration
            login(request, user)

            # Show a success message
            messages.success(request, "You have successfully registered! Please log in.")

            # Redirect to login page
            return redirect('login')  # Redirect to the login page

    else:
        form = CustomerRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def staff_dashboard(request):
    if request.user.role != 'staff':
        return redirect('login')  # Restrict access to staff only
    tickets = Ticket.objects.all()
    return render(request, 'staff_dashboard.html', {'tickets': tickets})

@login_required
def respond_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Ensure only staff members can access this page
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to respond to tickets.")
        return redirect('staff_dashboard')

    if request.method == 'POST':
        form = TicketResponseForm(request.POST)
        if form.is_valid():
            # Save the response
            ticket.response = form.cleaned_data['response']
            ticket.status = 'resolved'  
            ticket.resolved_by = request.user  
            ticket.save()

            messages.success(request, "Ticket has been resolved successfully!")
            return redirect('staff_dashboard')  
    else:
        form = TicketResponseForm()

    return render(request, 'respond_ticket.html', {'form': form, 'ticket': ticket})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect based on user role
            if user.role == 'customer':
                return redirect('create_ticket')  
            elif user.role == 'staff':
                return redirect('staff_dashboard')  
            else:
                return redirect('index') 
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


