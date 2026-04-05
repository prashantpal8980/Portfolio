from django.urls import path
from . import views

urlpatterns = [
    # ── Public ─────────────────────────────────────────────────────
    path('', views.portfolio, name='portfolio'),
    path('projects/', views.projects, name='projects'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('certifications/', views.certifications, name='certifications'),

    # ── Messages admin ──────────────────────────────────────────────
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/view/<int:pk>/', views.view_message, name='view_message'),
    path('dashboard/edit/<int:pk>/', views.edit_message, name='edit_message'),
    path('dashboard/delete/<int:pk>/', views.delete_message, name='delete_message'),

    # ── Certifications admin ────────────────────────────────────────
    path('dashboard/certs/', views.cert_dashboard, name='cert_dashboard'),
    path('dashboard/certs/add/', views.cert_add, name='cert_add'),
    path('dashboard/certs/edit/<int:pk>/', views.cert_edit, name='cert_edit'),
    path('dashboard/certs/delete/<int:pk>/', views.cert_delete, name='cert_delete'),
    path('dashboard/certs/highlight/<int:pk>/', views.cert_toggle_highlight, name='cert_toggle_highlight'),

    # ── Projects admin ──────────────────────────────────────────────
    path('dashboard/projects/', views.project_dashboard, name='project_dashboard'),
    path('dashboard/projects/add/', views.project_add, name='project_add'),
    path('dashboard/projects/edit/<int:pk>/', views.project_edit, name='project_edit'),
    path('dashboard/projects/delete/<int:pk>/', views.project_delete, name='project_delete'),
    path('dashboard/projects/highlight/<int:pk>/', views.project_toggle_highlight, name='project_toggle_highlight'),
]
