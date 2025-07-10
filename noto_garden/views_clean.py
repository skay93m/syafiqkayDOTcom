from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib import messages
from .models import Note, Tag
import json


def garden_dashboard(request):
    """Main dashboard for Noto Garden"""
    notes = Note.objects.all().order_by('-updated_at')[:10]
    total_notes = Note.objects.count()
    
    context = {
        'notes': notes,
        'total_notes': total_notes,
    }
    return render(request, 'noto_garden/dashboard.html', context)


def guide_view(request):
    """Guide for using the Zettelkasten system"""
    return render(request, 'noto_garden/guide.html')


def note_detail(request, unique_id):
    """Display a specific note"""
    note = get_object_or_404(Note, unique_id=unique_id)
    connected_notes = note.get_connected_notes()
    backlinks = note.get_backlinks()
    
    context = {
        'note': note,
        'connected_notes': connected_notes,
        'backlinks': backlinks,
    }
    return render(request, 'noto_garden/note_detail.html', context)


@login_required
def note_create(request):
    """Create a new note"""
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        tag_names = request.POST.get('tags', '')
        
        if title and content:
            note = Note.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            
            # Process tags
            if tag_names:
                tag_list = [tag.strip() for tag in tag_names.split(',')]
                for tag_name in tag_list:
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        note.tags.add(tag)
            
            # Process content links
            note.process_content_links()
            
            messages.success(request, f'Note "{note.title}" created successfully!')
            return redirect('noto_garden:note_detail', unique_id=note.unique_id)
        else:
            messages.error(request, 'Title and content are required.')
    
    context = {
        'all_tags': Tag.objects.all().order_by('name'),
    }
    return render(request, 'noto_garden/note_form.html', context)


@login_required
def note_edit(request, unique_id):
    """Edit an existing note"""
    note = get_object_or_404(Note, unique_id=unique_id)
    
    if request.method == 'POST':
        note.title = request.POST.get('title', note.title)
        note.content = request.POST.get('content', note.content)
        tag_names = request.POST.get('tags', '')
        
        note.save()
        
        # Update tags
        note.tags.clear()
        if tag_names:
            tag_list = [tag.strip() for tag in tag_names.split(',')]
            for tag_name in tag_list:
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    note.tags.add(tag)
        
        # Process content links
        note.connections.clear()
        note.process_content_links()
        
        messages.success(request, f'Note "{note.title}" updated successfully!')
        return redirect('noto_garden:note_detail', unique_id=note.unique_id)
    
    context = {
        'note': note,
        'all_tags': Tag.objects.all().order_by('name'),
        'note_tags': ', '.join([tag.name for tag in note.tags.all()]),
    }
    return render(request, 'noto_garden/note_form.html', context)


def graph_view(request):
    """Graph visualization of note connections"""
    notes = Note.objects.all()
    
    # Prepare data for D3.js visualization
    nodes = []
    links = []
    
    for note in notes:
        nodes.append({
            'id': note.unique_id,
            'title': note.title,
            'url': f'/noto_garden/note/{note.unique_id}/',
        })
        
        for connected_note in note.connections.all():
            links.append({
                'source': note.unique_id,
                'target': connected_note.unique_id,
            })
    
    graph_data = {
        'nodes': nodes,
        'links': links,
    }
    
    context = {
        'graph_data': json.dumps(graph_data),
    }
    return render(request, 'noto_garden/graph.html', context)


def search_notes(request):
    """Search notes by title, content, or tags"""
    query = request.GET.get('q', '')
    notes = []
    
    if query:
        notes = Note.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-updated_at')
    
    context = {
        'notes': notes,
        'query': query,
    }
    
    if request.headers.get('Content-Type') == 'application/json':
        results = []
        for note in notes:
            results.append({
                'id': note.unique_id,
                'title': note.title,
                'url': f'/noto_garden/note/{note.unique_id}/',
            })
        return JsonResponse({'results': results})
    
    return render(request, 'noto_garden/search.html', context)


def coming_soon(request):
    """Coming soon placeholder"""
    return render(request, 'noto_garden/coming_soon.html')
