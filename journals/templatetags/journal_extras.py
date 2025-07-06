from django import template
from django.utils.safestring import mark_safe
import markdown
import bleach
import re

register = template.Library()

@register.filter
def markdown_safe(value):
    """
    Convert markdown to HTML with XSS protection.
    Allows safe HTML tags while preventing malicious content.
    """
    if not value:
        return ''
    
    # Convert markdown to HTML
    html = markdown.markdown(value, extensions=[
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        'markdown.extensions.toc',
        'markdown.extensions.codehilite',
        'markdown.extensions.nl2br',
    ])
    
    # Allow safe HTML tags
    allowed_tags = [
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'p', 'br', 'strong', 'em', 'u', 'i', 'b',
        'ul', 'ol', 'li', 'dl', 'dt', 'dd',
        'blockquote', 'code', 'pre',
        'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'a', 'img', 'div', 'span',
        'hr', 'sub', 'sup',
    ]
    
    allowed_attributes = {
        'a': ['href', 'title', 'target', 'rel'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        'div': ['class', 'id'],
        'span': ['class', 'id'],
        'code': ['class'],
        'pre': ['class'],
        'table': ['class'],
        'th': ['class'],
        'td': ['class'],
        'h1': ['id'],
        'h2': ['id'],
        'h3': ['id'],
        'h4': ['id'],
        'h5': ['id'],
        'h6': ['id'],
    }
    
    # Clean HTML with bleach
    clean_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True
    )
    
    return mark_safe(clean_html)

@register.filter
def truncate_words_safe(value, num_words):
    """
    Truncate text to specified number of words, HTML-safe.
    """
    if not value:
        return ''
    
    # Strip HTML tags for truncation
    text = bleach.clean(value, tags=[], strip=True)
    words = text.split()
    
    if len(words) <= num_words:
        return value
    
    truncated = ' '.join(words[:num_words])
    return f"{truncated}..."

@register.filter
def add_emoji_class(value):
    """
    Add CSS class to emoji characters for better styling.
    """
    if not value:
        return ''
    
    # Simple emoji pattern (basic Unicode emoji ranges)
    emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+'
    
    def replace_emoji(match):
        emoji = match.group()
        return f'<span class="emoji">{emoji}</span>'
    
    result = re.sub(emoji_pattern, replace_emoji, value)
    return mark_safe(result)
