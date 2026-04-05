from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} — {self.subject or 'No Subject'} ({self.submitted_at:%Y-%m-%d %H:%M})"


class Certification(models.Model):
    LEVEL_CHOICES = [
        ('expert',       'Expert / Top Tier'),
        ('professional', 'Professional'),
        ('associate',    'Associate'),
        ('beginner',     'Beginner / Foundation'),
    ]

    title           = models.CharField(max_length=200)
    badge_label     = models.CharField(max_length=60, blank=True)
    issuer          = models.CharField(max_length=200)
    issue_date      = models.DateField()
    credential_id   = models.CharField(max_length=200, blank=True)
    credential_url  = models.URLField(blank=True)
    description     = models.TextField(blank=True)
    certificate_image = models.ImageField(upload_to='certificates/', blank=True, null=True)
    level           = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='professional')
    is_highlighted  = models.BooleanField(default=False)
    display_order   = models.PositiveIntegerField(default=0)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-issue_date', '-created_at']
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'

    def __str__(self):
        return f"{self.title} — {self.issuer} ({self.issue_date:%b %Y})"


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('dev',      'Full-Stack Development'),
        ('security', 'Cybersecurity'),
        ('ml',       'ML / Research'),
        ('research', 'Research'),
        ('other',    'Other'),
    ]
    SECTION_CHOICES = [
        ('featured',  'Featured Work'),
        ('security',  'Cybersecurity Projects'),
    ]

    # ── Content ──────────────────────────────────────────────────
    title         = models.CharField(max_length=200)
    subtitle      = models.CharField(max_length=200, blank=True,
                                     help_text="Second line of title, e.g. 'Secure Photo Journal'")
    category      = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='dev')
    section       = models.CharField(max_length=20, choices=SECTION_CHOICES, default='featured',
                                     help_text="Which section on the Projects page this appears in")
    description   = models.TextField()
    icon_emoji    = models.CharField(max_length=10, blank=True, default='🚀',
                                     help_text="Emoji shown on small cards, e.g. 🛡️")

    # ── Stats (optional — 2 key metrics) ─────────────────────────
    stat1_value = models.CharField(max_length=30, blank=True, help_text="e.g. '100%'")
    stat1_label = models.CharField(max_length=60, blank=True, help_text="e.g. 'XSS / SQLi blocked'")
    stat2_value = models.CharField(max_length=30, blank=True, help_text="e.g. '30%'")
    stat2_label = models.CharField(max_length=60, blank=True, help_text="e.g. 'Faster request handling'")

    # ── Tags (comma-separated) ────────────────────────────────────
    tags          = models.CharField(max_length=500, blank=True,
                                     help_text="Comma-separated tags, e.g. 'Python, Django, Nginx'")

    # ── Links ─────────────────────────────────────────────────────
    live_url      = models.URLField(blank=True, help_text="Live / demo link")
    source_url    = models.URLField(blank=True, help_text="GitHub / source link")

    # ── Image ─────────────────────────────────────────────────────
    image         = models.ImageField(upload_to='projects/', blank=True, null=True)
    image_alt     = models.CharField(max_length=200, blank=True)
    # For featured cards: image left (False) or right (True)
    image_right   = models.BooleanField(default=False,
                                        help_text="Featured card: put image on the right side")

    # ── Display ───────────────────────────────────────────────────
    CARD_STYLE_CHOICES = [
        ('long',  'Long Card — full layout with image panel'),
        ('short', 'Short Card — compact, no image panel'),
    ]
    card_style     = models.CharField(max_length=10, choices=CARD_STYLE_CHOICES, default='long',
                                      help_text="How this project appears on the public Projects page")
    is_highlighted = models.BooleanField(default=False,
                                         help_text="Show highlight glow / pin at top of its section")
    display_order  = models.PositiveIntegerField(default=0,
                                                  help_text="Lower = shown first (0 = top)")
    date_label     = models.CharField(max_length=30, blank=True,
                                      help_text="Date shown on card, e.g. 'Mar 2026'")
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'section', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return f"{self.title} [{self.get_section_display()}]"

    def tags_list(self):
        """Return tags as a Python list."""
        return [t.strip() for t in self.tags.split(',') if t.strip()]
