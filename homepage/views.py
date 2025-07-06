from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.db.models import Sum, Count
from .models import Rirekisho, VisitorTracking, VisitorSession
from journals.models import Journal
from noto_garden.models import Note
from reference.models import Reference
import markdown
import bleach
import os
import re
from collections import Counter


def get_client_ip(request):
    """Get the client's IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def track_visitor(request):
    """Track visitor session and daily statistics."""
    if not request.session.session_key:
        request.session.create()
    
    session_key = request.session.session_key
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    today = timezone.now().date()
    
    # Check if this session already visited today
    visitor_session, created = VisitorSession.objects.get_or_create(
        session_key=session_key,
        date=today,
        defaults={
            'ip_address': ip_address,
            'user_agent': user_agent,
        }
    )
    
    # Update daily visitor count if this is a new session for today
    if created:
        visitor_tracking, _ = VisitorTracking.objects.get_or_create(
            date=today,
            defaults={'daily_visitors': 0}
        )
        visitor_tracking.daily_visitors += 1
        visitor_tracking.save()


def generate_tag_cloud():
    """Generate tag cloud data from Noto Garden notes."""
    from noto_garden.models import Tag
    from django.db.models import Count
    
    # Get tags with their usage count
    tags_with_count = Tag.objects.annotate(
        note_count=Count('notes')
    ).filter(note_count__gt=0).order_by('-note_count')
    
    if not tags_with_count:
        return []
    
    # Get top 15 most used tags
    top_tags = list(tags_with_count[:15])
    
    if not top_tags:
        return []
    
    # Calculate relative sizes and opacity
    max_count = top_tags[0].note_count if top_tags else 0
    min_count = top_tags[-1].note_count if len(top_tags) > 1 else max_count
    
    tag_cloud = []
    for tag in top_tags:
        count = tag.note_count
        
        # Calculate relative size (1.0 to 1.4)
        if max_count == min_count:
            size = 1.2
        else:
            size = 1.0 + (count - min_count) / (max_count - min_count) * 0.4
        
        # Calculate opacity (0.6 to 1.0)
        if max_count == min_count:
            opacity = 1.0
        else:
            opacity = 0.6 + (count - min_count) / (max_count - min_count) * 0.4
        
        tag_cloud.append({
            'name': tag.name,
            'count': count,
            'size': round(size, 1),
            'opacity': round(opacity, 1),
            'color': tag.color if hasattr(tag, 'color') else '#FFB6C1'
        })
    
    # Shuffle for visual variety
    import random
    random.shuffle(tag_cloud)
    
    return tag_cloud


def homepage(request):
<<<<<<< HEAD
<<<<<<< HEAD
    # Fetch the latest Rirekisho entry
    try:
        rirekisho = Rirekisho.objects.latest('version')
    except Rirekisho.DoesNotExist:
        rirekisho = None
    return render(request, "homepage.html", {
=======
=======
    # Track visitor
    track_visitor(request)
    
>>>>>>> bb55f45 (feat: Populate Noto Garden with Zettelkasten notes and visualization commands)
    rirekisho = Rirekisho.objects.order_by('-id').first()  # Latest due to ordering
    
    # Get statistics
    today = timezone.now().date()
    today_visitors = VisitorTracking.objects.filter(date=today).first()
    daily_visitors = today_visitors.daily_visitors if today_visitors else 0
    
    # Total visitors (sum of all daily visitors)
    total_visitors = VisitorTracking.objects.aggregate(
        total=Sum('daily_visitors')
    )['total'] or 0
    
    # Content statistics
    journal_count = Journal.objects.count()
    note_count = Note.objects.count()
    reference_count = Reference.objects.count()
    total_posts = journal_count + note_count + reference_count
    
    # Recent activity (last 7 days)
    week_ago = today - timezone.timedelta(days=7)
    weekly_visitors = VisitorTracking.objects.filter(
        date__gte=week_ago
    ).aggregate(total=Sum('daily_visitors'))['total'] or 0
    
    # Generate tag cloud
    tag_cloud = generate_tag_cloud()
    
    statistics = {
        'daily_visitors': daily_visitors,
        'total_visitors': total_visitors,
        'weekly_visitors': weekly_visitors,
        'journal_count': journal_count,
        'note_count': note_count,
        'reference_count': reference_count,
        'total_posts': total_posts,
        'today_date': today,
        'tag_cloud': tag_cloud,
    }
    
    return render(request, "homepage/homepage.html", {
>>>>>>> fec6094 (Refactor notoGarden app: rename to noto_garden, remove unused files, and update settings)
        "rirekisho": rirekisho,
        "statistics": statistics,
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
