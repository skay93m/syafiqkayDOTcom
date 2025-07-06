# 📚 Reference App

A comprehensive reference management system for academic and professional resources with category-based organization and search functionality.

## Purpose

The reference app provides a structured way to organize, categorize, and access academic papers, articles, books, and other professional resources. It features a ninja-themed interface with pink sakura styling.

## Features

### 🗂️ Core Functionality
- **Category Management**: Organize references by topic/field
- **Search System**: Full-text search across titles and summaries
- **External Links**: Direct access to online resources
- **Horizontal Layout**: Card-based display for easy scanning
- **Tag System**: Flexible categorization with badges

### 🎨 Design Elements
- **Pink Sakura Theme**: Consistent with site aesthetic
- **Horizontal Cards**: Improved readability and space usage
- **Category Badges**: Visual organization with color coding
- **Responsive Design**: Mobile-friendly layout

## Models

### Reference
- **Purpose**: Core reference storage
- **Fields**:
  - `title`: Reference title (CharField, max_length=200)
  - `author`: Author name (CharField, max_length=100)
  - `summary`: Brief description (TextField)
  - `url`: External link (URLField, optional)
  - `category`: Comma-separated categories (CharField)
  - `created_at`: Auto timestamp
  - `updated_at`: Auto-updating timestamp

### Methods
- `get_categories()`: Returns list of categories from comma-separated string
- `__str__()`: Returns title for admin display

## Views

### Dashboard View
- **URL**: `/reference/`
- **Template**: `reference/dashboard.html`
- **Features**: 
  - Category filtering
  - Search functionality
  - Horizontal card layout
  - Responsive design

### Reference Detail View
- **URL**: `/reference/reference/<int:pk>/`
- **Template**: `reference/reference_detail.html`
- **Features**:
  - Full reference display
  - External link access
  - Category badges
  - Navigation breadcrumbs

## Templates

### Template Structure
```
templates/reference/
├── dashboard.html        # Main reference library
└── reference_detail.html # Individual reference view
```

### Key Features
- **Purpose Description**: Bilingual ninja-themed introduction
- **Horizontal Cards**: Left content, right metadata
- **Category Filtering**: Button-based navigation
- **Search Integration**: Real-time filtering
- **Responsive Layout**: Mobile-optimized design

## Admin Interface

### Reference Admin
- **List Display**: Title, author, categories, creation date
- **Search Fields**: Title, author, summary
- **List Filter**: Categories, creation date
- **Ordering**: By creation date (newest first)
- **Fieldsets**: Organized form layout

### Features
- **Bulk Actions**: Mass category assignment
- **Inline Editing**: Quick modifications
- **Rich Text**: Summary field with formatting
- **Validation**: URL and category validation

## URLs

```python
from django.urls import path
from . import views

app_name = 'reference'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('reference/<int:pk>/', views.reference_detail, name='reference_detail'),
]
```

## Styling

### CSS Classes
- `.reference-card-horizontal`: Horizontal card layout
- `.reference-list`: Container for references
- `.purpose-description`: Ninja-themed intro section
- `.category-badges`: Pink sakura category tags

### Color Scheme
- **Primary**: Pink sakura (#FADADD)
- **Secondary**: Light pink (#FFB6C1)
- **Accent**: Dark sakura (#C2185B)
- **Background**: Cloud white (#FAFAFA)

## Search Functionality

### Search Features
- **Title Search**: Full-text search in titles
- **Author Search**: Author name matching
- **Summary Search**: Content-based filtering
- **Category Filter**: Dropdown selection
- **Combined Search**: Multiple criteria support

### Implementation
- **Django Q Objects**: Complex query construction
- **Case-insensitive**: User-friendly search
- **Partial Matching**: Substring search support
- **Real-time**: Instant results display

## Security Measures

- **Input Validation**: Form data sanitization
- **CSRF Protection**: All forms protected
- **XSS Prevention**: Content escaping
- **URL Validation**: External link verification
- **Access Control**: Public read, admin write

## Performance Optimizations

- **Pagination**: Large dataset handling
- **Database Indexing**: Search optimization
- **Caching**: Frequent queries cached
- **Image Optimization**: Responsive images
- **Lazy Loading**: Improved page speed

## API Endpoints

### Planned Features
- **REST API**: JSON reference access
- **Export Options**: BibTeX, CSV formats
- **Import Tools**: Bulk reference upload
- **Tagging System**: Advanced categorization

## Development Notes

- **Model Design**: Flexible category system
- **Template Inheritance**: DRY principle
- **Form Validation**: Client and server-side
- **Error Handling**: Graceful failure modes
- **Testing**: Unit and integration tests

## Future Enhancements

- **Citation Generator**: Academic format support
- **PDF Storage**: Local file management
- **Note Taking**: Reference annotations
- **Sharing**: Public reference lists
- **Integration**: Connect with journals app
