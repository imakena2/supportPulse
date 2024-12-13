from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('features/', views.features, name='features'),
    path('services/', views.services, name='services'),
    path('pricing/', views.pricing, name='pricing'),
    path('contact/', views.contact, name='contact'),
    path('details/', views.details, name='details'),
    path('monitoring/', views.monitoring, name='monitoring'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),  
    path('register/', views.register_customer, name='register_customer'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('respond-ticket/<int:ticket_id>/', views.respond_ticket, name='respond_ticket'),

    # Login/logout
    path('accounts/login/', views.custom_login, name='login'),  
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

]
