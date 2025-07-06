# 🏠 Homepage App

The main homepage application that serves as the entry point to the digital ninja portfolio.

## Purpose

The homepage app provides the primary interface for visitors, featuring a beautiful zen-inspired design with personal branding and navigation to other sections of the site.

## Features

### 🌸 Main Components
- **Banner Section**: Japanese welcome message with ASCII art
- **Zen Landscape**: Inspirational image with ninja philosophy
- **Personal Statement**: Dynamic content from Rirekisho model
- **LinkedIn Integration**: Professional networking section
- **Static Pages**: Security assessment and session summary

### 🎨 Design Elements
- **Pink Sakura Theme**: Unified gradient backgrounds
- **Japanese Typography**: Authentic font stacks
- **Responsive Layout**: A4-width container for optimal reading
- **Ninja Aesthetics**: Martial arts philosophy integration

## Models

### Rirekisho
- **Purpose**: Stores personal statement and resume information
- **Fields**: 
  - `personal_statement`: Text field for main content
  - `created_at`: Timestamp
  - `updated_at`: Auto-updating timestamp

### WorkExperience
- **Purpose**: Professional experience entries
- **Fields**:
  - `company`: Company name
  - `position`: Job title
  - `start_date`: Employment start
  - `end_date`: Employment end (optional)
  - `description`: Role description
  - `created_at`: Timestamp

## Views

### Homepage View
- **URL**: `/`
- **Template**: `homepage/homepage.html`
- **Context**: Latest Rirekisho entry
- **Features**: Zen landscape, personal statement, LinkedIn section

### Security Assessment View
- **URL**: `/security-assessment/`
- **Template**: `homepage/security_assessment.html`
- **Purpose**: Display security analysis and measures

### Session Summary View
- **URL**: `/session-summary/`
- **Template**: `homepage/session_summary.html`
- **Purpose**: Development session documentation

## Templates

### Base Structure
```
templates/homepage/
├── homepage.html          # Main homepage template
├── security_assessment.html  # Security documentation
└── session_summary.html      # Session summary
```

### Key Template Features
- **Zen Landscape Section**: Inspirational image with caption
- **Responsive Design**: Mobile-first approach
- **Bilingual Content**: English and Japanese text
- **Ninja Theming**: Consistent aesthetic throughout

## Static Assets

### CSS
- Integrated with main `custom-2025-07-03.css`
- Zen landscape specific styling
- Pink sakura gradient backgrounds
- Japanese font specifications

### Images
- Zen landscape from Unsplash
- Proper attribution and responsive sizing
- Hover effects and transitions

## Admin Integration

### Rirekisho Admin
- **Editable Fields**: Personal statement, timestamps
- **Display**: List view with creation dates
- **Search**: Full-text search capabilities

### WorkExperience Admin
- **Inline Editing**: Manage experiences efficiently
- **Filtering**: By company, date range
- **Ordering**: Chronological display

## URLs

```python
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('security-assessment/', views.security_assessment, name='security_assessment'),
    path('session-summary/', views.session_summary, name='session_summary'),
]
```

## Security Considerations

- **Input Validation**: All form inputs sanitized
- **CSRF Protection**: Enabled on all forms
- **XSS Prevention**: Content properly escaped
- **Access Control**: Admin-only editing for sensitive content

## Development Notes

- **Responsive Design**: Tested on mobile, tablet, desktop
- **Performance**: Optimized images and minimal JS
- **SEO**: Proper meta tags and semantic HTML
- **Accessibility**: ARIA labels and keyboard navigation

## Future Enhancements

- **Multi-language Support**: Dynamic language switching
- **Portfolio Gallery**: Image showcase section
- **Contact Form**: Direct messaging capability
- **Analytics**: Visitor tracking and insights
