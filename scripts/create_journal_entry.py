#!/usr/bin/env python3
"""
Script to create a journal entry from the development journal markdown file.
Run this script after setting up Django environment.

This is a utility script that was used to import the development journal
markdown file into the Django database as a journal entry.
"""

import os
import django
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'syafiqkay.settings')
django.setup()

from journals.models import Journal

def create_journal_entry():
    """Create a journal entry from the development journal markdown file."""
    
    # Read the markdown file from new location
    with open('/workspaces/syafiq-kay/journals/docs/development_journal.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get or create the GitHub Copilot user
    User = get_user_model()
    author, created = User.objects.get_or_create(
        username='github-copilot',
        defaults={
            'email': 'copilot@github.com',
            'first_name': 'GitHub',
            'last_name': 'Copilot',
            'is_staff': False,
            'is_superuser': False,
        }
    )
    
    if created:
        author.set_password('secure_password_here')  # Set a secure password
        author.save()
        print(f"Created user: {author.username}")
    
    # Create the journal entry
    journal_entry = Journal.objects.create(
        title='🥷 Building a Ninja-Themed Django Website: A Development Journey',
        summary='A comprehensive development journal documenting the creation of a Django website with ninja theming, three interconnected apps (reference management, journals, and Zettelkasten), security implementations, and bilingual support. Written from the perspective of an AI assistant.',
        content=content,
        author=author
    )
    
    print(f"Created journal entry: {journal_entry.title}")
    print(f"Entry ID: {journal_entry.id}")
    print(f"URL: /journals/journal/{journal_entry.id}/")
    
    return journal_entry

if __name__ == '__main__':
    entry = create_journal_entry()
    print("Journal entry created successfully!")
