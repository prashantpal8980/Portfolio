from django.contrib import admin
from .models import ContactMessage, Certification, Project


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuer', 'issue_date', 'level', 'is_highlighted', 'display_order')
    list_filter = ('level', 'is_highlighted', 'issuer')
    search_fields = ('title', 'issuer', 'credential_id', 'description')
    list_editable = ('is_highlighted', 'display_order')
    ordering = ('display_order', '-issue_date')
    readonly_fields = ('created_at',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'category', 'is_highlighted', 'display_order', 'date_label')
    list_filter = ('section', 'category', 'is_highlighted')
    search_fields = ('title', 'description', 'tags')
    list_editable = ('is_highlighted', 'display_order')
    ordering = ('display_order', 'section')
    readonly_fields = ('created_at',)
