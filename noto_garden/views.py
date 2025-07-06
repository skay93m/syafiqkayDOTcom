from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
import json
import html
import os
import markdown
import bleach
from django.conf import settings

from .models import Note, Tag

def garden_dashboard(request):
    """Main dashboard showing all notes"""
    notes = Note.objects.all().order_by('-updated_at')
    
    # Get filter parameters
    tag_filter = request.GET.get('tag')
    search_query = request.GET.get('search')
    
    # Apply filters
    if tag_filter:
        notes = notes.filter(tags__name=tag_filter)
    
    if search_query:
        notes = notes.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Get all tags for filtering
    tags = Tag.objects.annotate(note_count=Count('notes')).order_by('name')
    
    # Get some statistics
    total_notes = Note.objects.count()
    total_connections = sum(note.connections.count() for note in Note.objects.all())
    
    context = {
        'notes': notes,
        'tags': tags,
        'current_tag': tag_filter,
        'search_query': search_query,
        'total_notes': total_notes,
        'total_connections': total_connections,
    }
    return render(request, 'noto_garden/dashboard.html', context)

def note_detail(request, unique_id):
    """Display a single note with its connections"""
    note = get_object_or_404(Note, unique_id=unique_id)
    
    # Get connected notes and backlinks
    connected_notes = note.get_connected_notes()
    backlinks = note.get_backlinks()
    
    # Process content for display (convert [[note_id]] to links)
    processed_content = process_note_links(note.content)
    
    context = {
        'note': note,
        'connected_notes': connected_notes,
        'backlinks': backlinks,
        'processed_content': processed_content,
    }
    return render(request, 'noto_garden/note_detail.html', context)

@staff_member_required
def note_create(request):
    """Create a new note - Admin only"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag_names = request.POST.get('tags', '').split(',')
        
        if title and content:
            try:
                # Validate and sanitize input
                title, content = validate_note_input(title, content)
                
                note = Note.objects.create(
                    title=title,
                    content=content,
                    author=request.user
                )
                
                # Add tags
                for tag_name in tag_names:
                    tag_name = tag_name.strip()
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        note.tags.add(tag)
                
                # Process note links
                note.process_content_links()
                
                messages.success(request, f'Note "{note.title}" created successfully!')
                return redirect('noto_garden:note_detail', unique_id=note.unique_id)
            except ValidationError as e:
                messages.error(request, str(e))
    
    return render(request, 'noto_garden/note_form.html', {'action': 'Create'})

@staff_member_required
def note_edit(request, unique_id):
    """Edit an existing note - Admin only"""
    note = get_object_or_404(Note, unique_id=unique_id)
    
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        
        try:
            # Validate and sanitize input
            title, content = validate_note_input(title, content)
            
            note.title = title
            note.content = content
            note.save()
            
            # Update tags with validation
            note.tags.clear()
            tag_names = request.POST.get('tags', '').split(',')
            for tag_name in tag_names:
                tag_name = tag_name.strip()
                if tag_name and len(tag_name) <= 50:  # Limit tag length
                    # Validate tag name
                    if tag_name.replace('-', '').replace('_', '').isalnum():
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        note.tags.add(tag)
            
            # Update connections
            note.connections.clear()
            note.process_content_links()
            
            messages.success(request, f'Note "{note.title}" updated successfully!')
            return redirect('noto_garden:note_detail', unique_id=note.unique_id)
            
        except ValidationError as e:
            messages.error(request, str(e))
    
    # Prepare tag string for form
    tag_string = ', '.join([tag.name for tag in note.tags.all()])
    
    context = {
        'note': note,
        'tag_string': tag_string,
        'action': 'Edit'
    }
    return render(request, 'noto_garden/note_form.html', context)

def graph_view(request):
    """Graph visualization of note connections"""
    notes = Note.objects.all()
    
    # Prepare data for D3.js graph
    nodes = []
    links = []
    
    for note in notes:
        nodes.append({
            'id': note.unique_id,
            'title': note.title,
            'url': note.get_absolute_url(),
            'connections': note.connections.count(),
            'word_count': note.get_word_count(),
        })
        
        for connected_note in note.connections.all():
            links.append({
                'source': note.unique_id,
                'target': connected_note.unique_id,
            })
    
    context = {
        'graph_data': {
            'nodes': nodes,
            'links': links
        }
    }
    return render(request, 'noto_garden/graph.html', context)

def search_notes(request):
    """AJAX search for notes - CSRF protected"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '').strip()
            
            # Input validation
            if not query or len(query) < 2:
                return JsonResponse({'results': []})
            
            # Limit query length to prevent abuse
            if len(query) > 100:
                return JsonResponse({'error': 'Query too long'}, status=400)
            
            # Sanitize query input
            query = html.escape(query)
            
            if query:
                notes = Note.objects.filter(
                    Q(title__icontains=query) |
                    Q(unique_id__icontains=query)
                )[:10]  # Limit results to prevent abuse
                
                results = [
                    {
                        'id': note.unique_id,
                        'title': html.escape(note.title),  # Escape output
                        'url': note.get_absolute_url()
                    }
                    for note in notes
                ]
                
                return JsonResponse({'results': results})
        except (json.JSONDecodeError, Exception) as e:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    
    return JsonResponse({'results': []})

def process_note_links(content):
    """Convert markdown and [[note_id]] syntax to HTML - XSS safe"""
    import re
    
    # First process [[note_id]] links before markdown conversion
    def replace_note_link(match):
        note_id = match.group(1)
        # Check if it's a note ID (numeric) or a title
        if re.match(r'^\d{14,}', note_id):  # Numeric ID
            try:
                note = Note.objects.get(unique_id=note_id)
                return f'[{note.title}]({note.get_absolute_url()})'
            except Note.DoesNotExist:
                return f'**[[{note_id}]]** *(note not found)*'
        else:  # Title-based link
            try:
                note = Note.objects.filter(title__icontains=note_id).first()
                if note:
                    return f'[{note.title}]({note.get_absolute_url()})'
                else:
                    return f'**[[{note_id}]]** *(note not found)*'
            except:
                return f'**[[{note_id}]]** *(note not found)*'
    
    # Replace [[note_id]] or [[title]] with markdown links
    pattern = r'\[\[([^\]]+)\]\]'
    content_with_links = re.sub(pattern, replace_note_link, content)
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        content_with_links,
        extensions=[
            'tables',
            'fenced_code',
            'codehilite',
            'toc',
            'nl2br'
        ],
        extension_configs={
            'codehilite': {
                'css_class': 'highlight',
                'use_pygments': True
            }
        }
    )
    
    # Sanitize HTML to prevent XSS while allowing markdown elements
    allowed_tags = [
        'p', 'strong', 'em', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'blockquote', 'code', 'pre', 'a', 'table', 'thead', 'tbody', 'tr', 'td', 'th',
        'div', 'span', 'br', 'hr', 'img'
    ]
    allowed_attributes = {
        'a': ['href', 'title', 'target', 'rel', 'class'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        'table': ['class'],
        'div': ['class', 'id'],
        'span': ['class'],
        'code': ['class'],
        'pre': ['class'],
        'h1': ['id'],
        'h2': ['id'],
        'h3': ['id'],
        'h4': ['id'],
        'h5': ['id'],
        'h6': ['id']
    }
    
    clean_html = bleach.clean(
        html_content, 
        tags=allowed_tags, 
        attributes=allowed_attributes,
        strip=True
    )
    
    return mark_safe(clean_html)

def guide_view(request):
    """Display the Noto Garden guide - Path traversal safe"""
    # Use absolute path to prevent path traversal - updated to new location
    guide_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'docs', 'noto_garden_guide.md'))
    base_path = os.path.abspath(os.path.dirname(__file__))
    
    # Ensure the file is within the app directory
    if not guide_path.startswith(base_path):
        raise Http404("Guide not found")
    
    try:
        with open(guide_path, 'r', encoding='utf-8') as f:
            guide_content = f.read()
        
        # Basic content validation
        if len(guide_content) > 100000:  # 100KB limit
            raise Http404("Guide file too large")
            
    except (FileNotFoundError, IOError, OSError):
        raise Http404("Guide not found")
    
    context = {
        'guide_content': guide_content,
    }
    return render(request, 'noto_garden/guide.html', context)

# Legacy view for compatibility
def coming_soon(request):
    return redirect('noto_garden:dashboard')

def validate_note_input(title, content):
    """Validate and sanitize note input"""
    if not title or not title.strip():
        raise ValidationError("Title is required")
    
    if not content or not content.strip():
        raise ValidationError("Content is required")
    
    # Length validation
    if len(title.strip()) > 200:
        raise ValidationError("Title must be 200 characters or less")
    
    if len(content.strip()) > 50000:  # 50KB limit
        raise ValidationError("Content must be 50,000 characters or less")
    
    # Basic content validation - prevent potentially malicious patterns
    malicious_patterns = ['<script', 'javascript:', 'onload=', 'onerror=']
    content_lower = content.lower()
    title_lower = title.lower()
    
    for pattern in malicious_patterns:
        if pattern in content_lower or pattern in title_lower:
            raise ValidationError("Content contains potentially unsafe elements")
    
    return title.strip(), content.strip()
