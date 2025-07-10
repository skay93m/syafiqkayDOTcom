from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils import timezone
from django.conf import settings
from .models import Rirekisho, VisitorTracking, VisitorSession
import markdown
import bleach
import os


def homepage(request):
    """Homepage view with latest Rirekisho and visitor tracking"""
    # Track visitor
    track_visitor(request)
    
    # Get latest Rirekisho
    latest_rirekisho = Rirekisho.objects.first()
    
    context = {
        'latest_rirekisho': latest_rirekisho,
    }
    return render(request, 'homepage/homepage.html', context)


def track_visitor(request):
    """Track unique visitors daily"""
    # Get or create visitor session
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    # Get visitor IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    
    # Get today's date
    today = timezone.now().date()
    
    # Check if this session was already tracked today
    visitor_session, created = VisitorSession.objects.get_or_create(
        session_key=session_key,
        date=today,
        defaults={'ip_address': ip_address}
    )
    
    if created:
        # Increment daily visitor count
        tracking, tracking_created = VisitorTracking.objects.get_or_create(
            date=today,
            defaults={'daily_visitors': 1}
        )
        if not tracking_created:
            tracking.daily_visitors += 1
            tracking.save()


@staff_member_required
def security_assessment(request):
    """Security assessment view for staff"""
    return render(request, 'homepage/security_assessment.html')


@staff_member_required 
def session_summary(request):
    """Session summary view for staff"""
    return render(request, 'homepage/session_summary.html')
