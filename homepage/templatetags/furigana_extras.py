import re
import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='furigana')
def furigana(value):
    """Convert text with furigana notation to HTML ruby tags."""
    if not value:
        return value
    
    # Pattern to match kanji (reading) format
    pattern = r'(\S+)\s*\(([ひらがなカタカナ\u3040-\u309F\u30A0-\u30FF]+)\s*-?\s*([ひらがなカタカナ\u3040-\u309F\u30A0-\u30FF]*)\)'
    
    def replace_furigana(match):
        kanji = match.group(1)
        reading = match.group(2)
        alt_reading = match.group(3) if match.group(3) else reading
        
        # Use the primary reading
        return f'<ruby>{kanji}<rt>{reading}</rt></ruby>'
    
    # Replace all occurrences
    result = re.sub(pattern, replace_furigana, value)
    
    return mark_safe(result)

@register.filter(name='simple_furigana')
def simple_furigana(value):
    """Convert simple kanji(reading) format to HTML ruby tags."""
    if not value:
        return value
    
    # Pattern for simple kanji(reading) format
    pattern = r'([一-龯]+)\s*\(([ひらがなカタカナ\u3040-\u309F\u30A0-\u30FF]+)\)'
    
    def replace_simple(match):
        kanji = match.group(1)
        reading = match.group(2)
        return f'<ruby>{kanji}<rt>{reading}</rt></ruby>'
    
    result = re.sub(pattern, replace_simple, value)
    return mark_safe(result)

@register.filter(name='markdown')
def markdown_filter(value):
    """Convert markdown text to HTML."""
    if not value:
        return value
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        value,
        extensions=['extra', 'codehilite'],
        extension_configs={
            'codehilite': {
                'css_class': 'highlight',
                'use_pygments': False,
            }
        }
    )
    
    return mark_safe(html_content)
