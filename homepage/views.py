from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import Rirekisho
import markdown
import bleach
import os


def homepage(request):
<<<<<<< HEAD
    # Fetch the latest Rirekisho entry
    try:
        rirekisho = Rirekisho.objects.latest('version')
    except Rirekisho.DoesNotExist:
        rirekisho = None
    return render(request, "homepage.html", {
=======
    rirekisho = Rirekisho.objects.order_by('-id').first()  # Latest due to ordering
    return render(request, "homepage/homepage.html", {
>>>>>>> fec6094 (Refactor notoGarden app: rename to noto_garden, remove unused files, and update settings)
        "rirekisho": rirekisho,
    })


def security_assessment(request):
    """Render the security assessment markdown file."""
    file_path = os.path.join(os.path.dirname(__file__), 'docs', 'SECURITY_ASSESSMENT.md')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        content = "# Security Assessment\n\nDocument not found."
    
    # Convert markdown to HTML with security
    html_content = markdown.markdown(content, extensions=['tables', 'toc'])
    
    # Sanitize HTML to prevent XSS
    allowed_tags = [
        'p', 'strong', 'em', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'blockquote', 'code', 'pre', 'a', 'table', 'thead', 'tbody', 'tr', 'td', 'th',
        'div', 'span', 'br', 'hr'
    ]
    allowed_attributes = {
        'a': ['href', 'title', 'target', 'rel'],
        'table': ['class'],
        'div': ['class', 'id'],
        'span': ['class'],
        'code': ['class'],
        'pre': ['class']
    }
    
    clean_html = bleach.clean(html_content, tags=allowed_tags, attributes=allowed_attributes)
    
    return render(request, "homepage/security_assessment.html", {
        "content": mark_safe(clean_html),
        "title": "Security Assessment"
    })


def session_summary(request):
    """Render the session summary markdown file."""
    file_path = os.path.join(os.path.dirname(__file__), 'docs', 'SESSION_SUMMARY.md')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        content = "# Session Summary\n\nDocument not found."
    
    # Convert markdown to HTML with security
    html_content = markdown.markdown(content, extensions=['tables', 'toc'])
    
    # Sanitize HTML to prevent XSS
    allowed_tags = [
        'p', 'strong', 'em', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'blockquote', 'code', 'pre', 'a', 'table', 'thead', 'tbody', 'tr', 'td', 'th',
        'div', 'span', 'br', 'hr'
    ]
    allowed_attributes = {
        'a': ['href', 'title', 'target', 'rel'],
        'table': ['class'],
        'div': ['class', 'id'],
        'span': ['class'],
        'code': ['class'],
        'pre': ['class']
    }
    
    clean_html = bleach.clean(html_content, tags=allowed_tags, attributes=allowed_attributes)
    
    return render(request, "homepage/session_summary.html", {
        "content": mark_safe(clean_html),
        "title": "Session Summary"
    })
