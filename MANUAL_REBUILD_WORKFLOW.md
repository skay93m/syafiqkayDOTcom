# Manual Rebuild Workflow

## Overview
This document outlines a structured approach to manually rebuild the Django application functionality by analyzing the existing implementation and writing everything from scratch. This approach will help you understand every component deeply and take full ownership of the codebase.

## Branch Strategy
- **Reference Branch**: `main` - Contains the fully working merged implementation
- **Development Branch**: `manual-rebuild` - Where you'll implement everything manually
- **Backup Branch**: `ai-assisted-backup` - Clean backup of the AI-assisted work

## Phase 1: Project Foundation (Days 1-2)

### 1.1 Environment Setup
- [ ] Create and activate virtual environment
- [ ] Install Django and basic dependencies
- [ ] Create basic Django project structure
- [ ] Set up basic settings.py configuration
- [ ] Create basic URL routing

### 1.2 Database Configuration
- [ ] Analyze current database schema from `main` branch
- [ ] Set up SQLite database configuration
- [ ] Create initial superuser
- [ ] Verify basic admin access

**Reference Files to Study:**
- `syafiqkay/settings.py`
- `manage.py`
- `syafiqkay/urls.py`

## Phase 2: Core Apps Structure (Days 3-4)

### 2.1 Homepage App
- [ ] Create homepage app
- [ ] Analyze existing models in `homepage/models.py`
- [ ] Implement Rirekisho model manually
- [ ] Implement VisitorTracking model manually
- [ ] Implement VisitorSession model manually
- [ ] Create and run migrations
- [ ] Set up basic admin registration

### 2.2 Basic Views and Templates
- [ ] Create base templates structure
- [ ] Implement homepage view
- [ ] Create basic homepage template
- [ ] Test basic functionality

**Reference Files to Study:**
- `homepage/models.py`
- `homepage/views.py`
- `homepage/admin.py`
- `templates/base/`
- `templates/homepage/`

## Phase 3: Journals App (Days 5-7)

### 3.1 Journal Models
- [ ] Create journals app
- [ ] Analyze Journal model structure
- [ ] Implement Journal model with all fields
- [ ] Add tags functionality
- [ ] Add author relationships
- [ ] Create migrations

### 3.2 Journal Views and Templates
- [ ] Implement dashboard view with filtering
- [ ] Implement journal detail view
- [ ] Create journal templates
- [ ] Add search functionality
- [ ] Add tag filtering
- [ ] Add author filtering

### 3.3 Journal Admin
- [ ] Set up admin interface
- [ ] Add custom admin actions
- [ ] Test CRUD operations

**Reference Files to Study:**
- `journals/models.py`
- `journals/views.py`
- `journals/urls.py`
- `journals/admin.py`
- `templates/journals/`

## Phase 4: Note Garden App (Days 8-10)

### 4.1 Note Models
- [ ] Create noto_garden app
- [ ] Implement Note model
- [ ] Add relationships and tags
- [ ] Create migrations

### 4.2 Note Features
- [ ] Implement note creation
- [ ] Implement note editing
- [ ] Implement note linking
- [ ] Add search functionality
- [ ] Create note graph visualization

### 4.3 Note Templates
- [ ] Create dashboard template
- [ ] Create note detail template
- [ ] Create note form template
- [ ] Create graph visualization template

**Reference Files to Study:**
- `noto_garden/models.py`
- `noto_garden/views.py`
- `noto_garden/urls.py`
- `templates/noto_garden/`

## Phase 5: Reference App (Days 11-12)

### 5.1 Reference System
- [ ] Create reference app
- [ ] Implement Reference model
- [ ] Add categorization system
- [ ] Create migrations

### 5.2 Reference Management
- [ ] Implement CRUD operations
- [ ] Add search and filtering
- [ ] Create templates

**Reference Files to Study:**
- `reference/models.py`
- `reference/views.py`
- `templates/reference/`

## Phase 6: Experiments App (Days 13-14)

### 6.1 Experiments Framework
- [ ] Create experiments app
- [ ] Implement Experiment model
- [ ] Add experiment tracking
- [ ] Create migrations

### 6.2 Experiment Features
- [ ] Implement experiment dashboard
- [ ] Add experiment detail views
- [ ] Create experiment templates

**Reference Files to Study:**
- `experiments/models.py`
- `experiments/views.py`
- `templates/experiments/`

## Phase 7: Advanced Features (Days 15-17)

### 7.1 Visitor Tracking
- [ ] Implement visitor session tracking
- [ ] Add statistics collection
- [ ] Create visitor analytics

### 7.2 Template Inheritance
- [ ] Create comprehensive base templates
- [ ] Implement consistent styling
- [ ] Add navigation components
- [ ] Add footer components

### 7.3 Static Files and Styling
- [ ] Set up static files handling
- [ ] Implement CSS styling
- [ ] Add responsive design
- [ ] Add Japanese/English bilingual support

**Reference Files to Study:**
- `templates/base/`
- `templates/components/`
- `static/css/`

## Phase 8: Integration and Testing (Days 18-20)

### 8.1 URL Integration
- [ ] Connect all app URLs
- [ ] Test navigation between apps
- [ ] Verify all links work

### 8.2 Data Integration
- [ ] Test relationships between models
- [ ] Verify data consistency
- [ ] Test search across apps

### 8.3 Admin Integration
- [ ] Set up comprehensive admin
- [ ] Test all admin functionality
- [ ] Add admin customizations

## Phase 9: Production Readiness (Days 21-22)

### 9.1 Security and Settings
- [ ] Review security settings
- [ ] Set up environment variables
- [ ] Configure production settings

### 9.2 Database Migrations
- [ ] Verify all migrations work
- [ ] Test migration rollbacks
- [ ] Document migration dependencies

### 9.3 Final Testing
- [ ] Test all functionality end-to-end
- [ ] Verify responsive design
- [ ] Test error handling

## Daily Learning Process

### Morning Routine (30 minutes)
1. Review the reference implementation for the day's target feature
2. Document what you understand about the functionality
3. Plan your implementation approach

### Implementation Time (2-4 hours)
1. Write code without copying - understand and implement
2. Test each small piece as you build
3. Document any challenges or learnings

### Evening Review (30 minutes)
1. Compare your implementation with the reference
2. Note differences and improvements
3. Plan the next day's work

## Key Learning Objectives

### Technical Skills
- [ ] Deep understanding of Django models and relationships
- [ ] Mastery of Django views and URL routing
- [ ] Template inheritance and Django template language
- [ ] Database migrations and schema design
- [ ] Admin interface customization

### Architecture Understanding
- [ ] App separation and responsibility
- [ ] Model relationships and data flow
- [ ] Template organization and reuse
- [ ] Static file management
- [ ] URL namespace organization

### Best Practices
- [ ] Code organization and structure
- [ ] Error handling and validation
- [ ] Security considerations
- [ ] Performance optimization
- [ ] Documentation and commenting

## Reference Commands

### Development Commands
```bash
# Start development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Check for issues
python manage.py check
```

### Git Commands
```bash
# Switch to reference branch
git checkout main

# Switch back to development
git checkout manual-rebuild

# Compare implementations
git diff main manual-rebuild -- filename

# View file from reference branch
git show main:path/to/file
```

## Success Criteria

By the end of this workflow, you should have:
1. A fully functional Django application built entirely by hand
2. Deep understanding of every component and its purpose
3. Ability to explain and modify any part of the system
4. Confidence in Django development patterns
5. A codebase that you fully own and understand

## Notes and Learnings
Use this space to document key insights and challenges as you progress:

- [ ] Day 1: 
- [ ] Day 2: 
- [ ] Day 3: 
- [ ] Day 4: 
- [ ] Day 5: 

---

Remember: The goal is not to recreate exactly the same implementation, but to understand the functionality and build it in your own way. Feel free to improve upon the original design!
