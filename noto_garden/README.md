# 🌸 Noto Garden App

A sophisticated Zettelkasten-style note-taking system with bi-directional linking, graph visualization, and advanced knowledge management features.

## Purpose

Noto Garden (ノートの庭) is a digital zen garden for thoughts and ideas, implementing the Zettelkasten methodology for knowledge management. It provides a sacred space for nurturing seeds of creativity and wisdom with admin-controlled access.

## Features

### 🌱 Core Functionality
- **Zettelkasten Method**: Atomic notes with unique identifiers
- **Bi-directional Linking**: Wiki-style connections between notes
- **Graph Visualization**: Interactive network of connected thoughts
- **Tag Management**: Flexible categorization with colored tags
- **Search System**: Full-text search across all notes
- **Admin Control**: Restricted note creation and editing

### 🎨 Design Elements
- **Purple Gradient Theme**: Zen-inspired color scheme
- **Japanese Aesthetics**: Traditional garden metaphors
- **Responsive Design**: Mobile-optimized interface
- **Graph Visualization**: D3.js-powered network diagrams

## Models

### Note
- **Purpose**: Core note storage with unique identification
- **Fields**:
  - `unique_id`: Auto-generated 8-character ID (CharField)
  - `title`: Note title (CharField, max_length=200)
  - `content`: Full note content (TextField)
  - `tags`: ManyToMany relationship to Tag model
  - `connections`: ManyToMany self-relationship
  - `created_at`: Auto timestamp
  - `updated_at`: Auto-updating timestamp

### Methods
- `get_word_count()`: Returns word count of content
- `get_connected_notes()`: Returns connected notes
- `save()`: Auto-generates unique_id if not provided
- `__str__()`: Returns title for admin display

### Tag
- **Purpose**: Categorization and organization
- **Fields**:
  - `name`: Tag name (CharField, max_length=50)
  - `color`: Hex color code (CharField)
  - `description`: Optional description (TextField)
  - `created_at`: Auto timestamp

### Methods
- `note_count()`: Returns number of notes with this tag
- `__str__()`: Returns tag name

## Views

### Dashboard View
- **URL**: `/noto-garden/`
- **Template**: `noto_garden/dashboard.html`
- **Features**: 
  - Statistics display (notes, connections, tags)
  - Search and tag filtering
  - Note table with horizontal layout
  - Access level indicators
  - Admin-only creation buttons

### Note Detail View
- **URL**: `/noto-garden/note/<str:unique_id>/`
- **Template**: `noto_garden/note_detail.html`
- **Features**:
  - Full note content display
  - Tag badges with colors
  - Connection list with links
  - Admin-only edit controls
  - Breadcrumb navigation

### Note Form Views
- **Create**: `/noto-garden/note/create/`
- **Edit**: `/noto-garden/note/<str:unique_id>/edit/`
- **Template**: `noto_garden/note_form.html`
- **Access**: Admin users only (`@staff_member_required`)

### Graph View
- **URL**: `/noto-garden/graph/`
- **Template**: `noto_garden/graph.html`
- **Features**:
  - Interactive D3.js visualization
  - Node and edge relationships
  - Zoom and pan capabilities
  - Reset view functionality

### Guide View
- **URL**: `/noto-garden/guide/`
- **Template**: `noto_garden/guide.html`
- **Features**:
  - Comprehensive user documentation
  - Markdown-rendered guide
  - Navigation integration

## Templates

### Template Structure
```
templates/noto_garden/
├── dashboard.html        # Main garden overview
├── note_detail.html      # Individual note view
├── note_form.html        # Create/edit note form
├── graph.html           # Interactive graph view
├── guide.html           # User guide documentation
└── coming_soon.html     # Placeholder template
```

### Key Features
- **Access Control**: Visual indicators for user permissions
- **Responsive Design**: Mobile-optimized layouts
- **Japanese Theming**: Zen garden metaphors throughout
- **Interactive Elements**: Hover effects and transitions

## Admin Interface

### Note Admin
- **List Display**: Unique ID, title, tag count, connections, word count
- **Search Fields**: Title, content, unique_id
- **List Filter**: Tags, creation date, word count ranges
- **Ordering**: By creation date (newest first)
- **Fieldsets**: Organized form with tag and connection management

### Tag Admin
- **List Display**: Name, color, note count, creation date
- **Search Fields**: Name, description
- **Color Picker**: Visual color selection
- **Bulk Actions**: Mass tag operations

## URLs

```python
from django.urls import path
from . import views

app_name = 'noto_garden'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('note/<str:unique_id>/', views.note_detail, name='note_detail'),
    path('note/create/', views.note_create, name='note_create'),
    path('note/<str:unique_id>/edit/', views.note_edit, name='note_edit'),
    path('graph/', views.graph, name='graph'),
    path('guide/', views.guide, name='guide'),
]
```

## Graph Visualization

### D3.js Implementation
- **Force-directed Layout**: Natural node positioning
- **Interactive Nodes**: Clickable note connections
- **Zoom and Pan**: Full navigation control
- **Legend**: Color-coded node types
- **Responsive**: Adapts to container size

### Graph Data Structure
```json
{
  "nodes": [
    {"id": "ABC12345", "title": "Note Title", "group": 1}
  ],
  "links": [
    {"source": "ABC12345", "target": "DEF67890"}
  ]
}
```

## Security Measures

### Access Control
- **Admin Only**: Note creation and editing restricted
- **Staff Required**: `@staff_member_required` decorator
- **Visual Indicators**: Clear permission display
- **Graceful Degradation**: Read-only for non-admin users

### Content Security
- **Input Validation**: Form data sanitization
- **CSRF Protection**: All forms protected
- **XSS Prevention**: Content escaping
- **Path Traversal**: Unique ID validation

## Search and Filtering

### Search Features
- **Full-text Search**: Title and content search
- **Tag Filtering**: Individual tag selection
- **Combined Search**: Multiple criteria support
- **Real-time Results**: Instant filtering

### Filter Interface
- **Responsive Form**: Mobile-friendly layout
- **Clear Options**: Easy filter reset
- **URL Parameters**: Bookmarkable states
- **Visual Feedback**: Active filter display

## Performance Optimizations

- **Lazy Loading**: Deferred content loading
- **Database Indexing**: Search optimization
- **Caching**: Frequent queries cached
- **Graph Optimization**: Efficient D3.js rendering
- **Pagination**: Large dataset handling

## Development Notes

### Unique ID Generation
- **Format**: 8-character alphanumeric
- **Collision Handling**: Automatic regeneration
- **URL Safe**: No special characters
- **Human Readable**: Distinguishable characters

### Connection Management
- **Bi-directional**: Automatic reverse connections
- **Self-referential**: ManyToMany to self
- **Cascade Handling**: Proper deletion management
- **Validation**: Prevents self-connections

## API Endpoints

### AJAX Search
- **URL**: `/noto-garden/search/`
- **Method**: GET
- **Parameters**: `q` (query), `tag` (filter)
- **Response**: JSON note list

### Graph Data
- **URL**: `/noto-garden/graph-data/`
- **Method**: GET
- **Response**: JSON graph structure
- **Caching**: Optimized for performance

## Future Enhancements

- **Export Options**: Markdown, PDF formats
- **Import Tools**: Bulk note creation
- **Version Control**: Note history tracking
- **Collaboration**: Multi-user editing
- **Mobile App**: Native iOS/Android clients
- **AI Integration**: Automatic connections and suggestions
