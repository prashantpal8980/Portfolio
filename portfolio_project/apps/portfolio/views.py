from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import ContactMessage, Certification, Project


# ── Public Views ─────────────────────────────────────────────────────────────

def portfolio(request):
    image = "/static/images/test.jpg"

    # Top 3 certifications for homepage preview
    featured_certs = Certification.objects.order_by('display_order', '-issue_date')[:3]

    # Top 3 projects: highlighted ones first, then by display_order
    featured_projects = Project.objects.order_by(
        '-is_highlighted', 'display_order', '-created_at'
    )[:3]

    return render(request, 'portfolio.html', {
        "image": image,
        "featured_certs": featured_certs,
        "featured_projects": featured_projects,
    })


def projects(request):
    all_projects = Project.objects.all().order_by('display_order', '-created_at')
    return render(request, 'projects.html', {'projects': all_projects})


def about(request):
    return render(request, 'about.html')


def contact(request):
    success = False
    error   = None
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
            success = True
        else:
            error = "Please fill in all required fields (Name, Email, Message)."
    return render(request, 'contact.html', {'success': success, 'error': error})


def certifications(request):
    cutoff = timezone.now().date() - timedelta(days=180)
    certs  = Certification.objects.all().order_by('display_order', '-issue_date')
    return render(request, 'certifications.html', {'certs': certs, 'recent_cutoff': cutoff})


# ── Admin / Messages Dashboard ────────────────────────────────────────────────

@login_required
def dashboard(request):
    messages      = ContactMessage.objects.all().order_by('-submitted_at')
    alert_success = request.session.pop('alert_success', None)
    return render(request, 'dashboard.html', {'messages': messages, 'alert_success': alert_success})


@login_required
def view_message(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    return render(request, 'view_message.html', {'message': message})


@login_required
def edit_message(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        msg_txt = request.POST.get('message', '').strip()
        if name and email and msg_txt:
            message.name = name; message.email = email
            message.subject = subject; message.message = msg_txt
            message.save()
            request.session['alert_success'] = f"Message from '{name}' updated."
            return redirect('dashboard')
    return render(request, 'edit_message.html', {'message': message})


@login_required
def delete_message(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        name = message.name; message.delete()
        request.session['alert_success'] = f"Message from '{name}' deleted."
    return redirect('dashboard')


# ── Admin / Certifications ────────────────────────────────────────────────────

@login_required
def cert_dashboard(request):
    certs         = Certification.objects.all().order_by('display_order', '-issue_date')
    alert_success = request.session.pop('cert_alert', None)
    return render(request, 'cert_dashboard.html', {'certs': certs, 'alert_success': alert_success})


@login_required
def cert_add(request):
    if request.method == 'POST':
        try:
            cert = Certification(
                title          = request.POST.get('title', '').strip(),
                badge_label    = request.POST.get('badge_label', '').strip(),
                issuer         = request.POST.get('issuer', '').strip(),
                issue_date     = request.POST.get('issue_date'),
                credential_id  = request.POST.get('credential_id', '').strip(),
                credential_url = request.POST.get('credential_url', '').strip(),
                description    = request.POST.get('description', '').strip(),
                level          = request.POST.get('level', 'professional'),
                is_highlighted = 'is_highlighted' in request.POST,
                display_order  = int(request.POST.get('display_order', 0) or 0),
            )
            if 'certificate_image' in request.FILES:
                cert.certificate_image = request.FILES['certificate_image']
            cert.save()
            request.session['cert_alert'] = f"'{cert.title}' added."
            return redirect('cert_dashboard')
        except Exception as e:
            return render(request, 'cert_form.html', {'mode': 'add', 'error': str(e), 'levels': Certification.LEVEL_CHOICES})
    return render(request, 'cert_form.html', {'mode': 'add', 'levels': Certification.LEVEL_CHOICES})


@login_required
def cert_edit(request, pk):
    cert = get_object_or_404(Certification, pk=pk)
    if request.method == 'POST':
        try:
            cert.title = request.POST.get('title', '').strip()
            cert.badge_label = request.POST.get('badge_label', '').strip()
            cert.issuer = request.POST.get('issuer', '').strip()
            cert.issue_date = request.POST.get('issue_date')
            cert.credential_id = request.POST.get('credential_id', '').strip()
            cert.credential_url = request.POST.get('credential_url', '').strip()
            cert.description = request.POST.get('description', '').strip()
            cert.level = request.POST.get('level', 'professional')
            cert.is_highlighted = 'is_highlighted' in request.POST
            cert.display_order = int(request.POST.get('display_order', 0) or 0)
            if 'certificate_image' in request.FILES:
                cert.certificate_image = request.FILES['certificate_image']
            elif request.POST.get('clear_image'):
                cert.certificate_image = None
            cert.save()
            request.session['cert_alert'] = f"'{cert.title}' updated."
            return redirect('cert_dashboard')
        except Exception as e:
            return render(request, 'cert_form.html', {'mode': 'edit', 'cert': cert, 'error': str(e), 'levels': Certification.LEVEL_CHOICES})
    return render(request, 'cert_form.html', {'mode': 'edit', 'cert': cert, 'levels': Certification.LEVEL_CHOICES})


@login_required
def cert_delete(request, pk):
    cert = get_object_or_404(Certification, pk=pk)
    if request.method == 'POST':
        title = cert.title; cert.delete()
        request.session['cert_alert'] = f"'{title}' deleted."
    return redirect('cert_dashboard')


@login_required
def cert_toggle_highlight(request, pk):
    cert = get_object_or_404(Certification, pk=pk)
    cert.is_highlighted = not cert.is_highlighted
    cert.save()
    status = "highlighted" if cert.is_highlighted else "un-highlighted"
    request.session['cert_alert'] = f"'{cert.title}' {status}."
    return redirect('cert_dashboard')


# ── Admin / Projects ──────────────────────────────────────────────────────────

@login_required
def project_dashboard(request):
    all_projects  = Project.objects.all().order_by('display_order', 'section', '-created_at')
    alert_success = request.session.pop('project_alert', None)
    return render(request, 'project_dashboard.html', {
        'projects': all_projects,
        'alert_success': alert_success,
    })


@login_required
def project_add(request):
    if request.method == 'POST':
        try:
            proj = Project(
                title         = request.POST.get('title', '').strip(),
                subtitle      = request.POST.get('subtitle', '').strip(),
                category      = request.POST.get('category', 'dev'),
                section       = request.POST.get('section', 'featured'),
                description   = request.POST.get('description', '').strip(),
                icon_emoji    = request.POST.get('icon_emoji', '🚀').strip() or '🚀',
                stat1_value   = request.POST.get('stat1_value', '').strip(),
                stat1_label   = request.POST.get('stat1_label', '').strip(),
                stat2_value   = request.POST.get('stat2_value', '').strip(),
                stat2_label   = request.POST.get('stat2_label', '').strip(),
                tags          = request.POST.get('tags', '').strip(),
                live_url      = request.POST.get('live_url', '').strip(),
                source_url    = request.POST.get('source_url', '').strip(),
                image_alt     = request.POST.get('image_alt', '').strip(),
                image_right   = 'image_right' in request.POST,
                card_style    = request.POST.get('card_style', 'long'),
                is_highlighted= 'is_highlighted' in request.POST,
                display_order = int(request.POST.get('display_order', 0) or 0),
                date_label    = request.POST.get('date_label', '').strip(),
            )
            if 'image' in request.FILES:
                proj.image = request.FILES['image']
            proj.save()
            request.session['project_alert'] = f"'{proj.title}' added."
            return redirect('project_dashboard')
        except Exception as e:
            return render(request, 'project_form.html', {
                'mode': 'add', 'error': str(e),
                'categories': Project.CATEGORY_CHOICES,
                'sections': Project.SECTION_CHOICES,
                'card_styles': Project.CARD_STYLE_CHOICES,
            })
    return render(request, 'project_form.html', {
        'mode': 'add',
        'categories': Project.CATEGORY_CHOICES,
        'sections': Project.SECTION_CHOICES,
        'card_styles': Project.CARD_STYLE_CHOICES,
    })


@login_required
def project_edit(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        try:
            proj.title         = request.POST.get('title', '').strip()
            proj.subtitle      = request.POST.get('subtitle', '').strip()
            proj.category      = request.POST.get('category', 'dev')
            proj.section       = request.POST.get('section', 'featured')
            proj.description   = request.POST.get('description', '').strip()
            proj.icon_emoji    = request.POST.get('icon_emoji', '🚀').strip() or '🚀'
            proj.stat1_value   = request.POST.get('stat1_value', '').strip()
            proj.stat1_label   = request.POST.get('stat1_label', '').strip()
            proj.stat2_value   = request.POST.get('stat2_value', '').strip()
            proj.stat2_label   = request.POST.get('stat2_label', '').strip()
            proj.tags          = request.POST.get('tags', '').strip()
            proj.live_url      = request.POST.get('live_url', '').strip()
            proj.source_url    = request.POST.get('source_url', '').strip()
            proj.image_alt     = request.POST.get('image_alt', '').strip()
            proj.image_right   = 'image_right' in request.POST
            proj.card_style    = request.POST.get('card_style', 'long')
            proj.is_highlighted= 'is_highlighted' in request.POST
            proj.display_order = int(request.POST.get('display_order', 0) or 0)
            proj.date_label    = request.POST.get('date_label', '').strip()
            if 'image' in request.FILES:
                proj.image = request.FILES['image']
            elif request.POST.get('clear_image'):
                proj.image = None
            proj.save()
            request.session['project_alert'] = f"'{proj.title}' updated."
            return redirect('project_dashboard')
        except Exception as e:
            return render(request, 'project_form.html', {
                'mode': 'edit', 'proj': proj, 'error': str(e),
                'categories': Project.CATEGORY_CHOICES,
                'sections': Project.SECTION_CHOICES,
                'card_styles': Project.CARD_STYLE_CHOICES,
            })
    return render(request, 'project_form.html', {
        'mode': 'edit', 'proj': proj,
        'categories': Project.CATEGORY_CHOICES,
        'sections': Project.SECTION_CHOICES,
        'card_styles': Project.CARD_STYLE_CHOICES,
    })


@login_required
def project_delete(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        title = proj.title; proj.delete()
        request.session['project_alert'] = f"'{title}' deleted."
    return redirect('project_dashboard')


@login_required
def project_toggle_highlight(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    proj.is_highlighted = not proj.is_highlighted
    proj.save()
    status = "highlighted" if proj.is_highlighted else "un-highlighted"
    request.session['project_alert'] = f"'{proj.title}' {status}."
    return redirect('project_dashboard')
