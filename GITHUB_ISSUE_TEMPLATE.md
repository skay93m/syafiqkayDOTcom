# Manual Django Application Rebuild Project

## Objective
Rebuild the entire Django application manually from scratch to gain deep understanding of every component and take full ownership of the codebase.

## Background
The application was initially built with AI assistance, which resulted in a working system but limited personal understanding of the implementation details. This project aims to rebuild everything manually while using the existing implementation as reference.

## Scope
Complete reconstruction of all Django apps and functionality:

### Apps to Rebuild
- [ ] **Homepage App** - Personal statement, visitor tracking, statistics
- [ ] **Journals App** - Blog-like entries with tags, search, and filtering
- [ ] **Noto Garden App** - Note-taking system with linking and graph visualization
- [ ] **Reference App** - Reference management system
- [ ] **Experiments App** - Experiment tracking and documentation

### Core Features to Implement
- [ ] Database models with proper relationships
- [ ] Views with filtering, search, and CRUD operations
- [ ] Template inheritance and responsive design
- [ ] Admin interface customization
- [ ] Visitor tracking and analytics
- [ ] Bilingual support (English/Japanese)
- [ ] Static file management
- [ ] URL routing and namespacing

## Implementation Plan
Following the structured workflow in `MANUAL_REBUILD_WORKFLOW.md` over approximately 22 days:

### Phase 1 (Days 1-2): Project Foundation
- Environment setup and basic Django configuration

### Phase 2 (Days 3-4): Core Apps Structure  
- Homepage app with models and basic templates

### Phase 3 (Days 5-7): Journals App
- Complete journal system with filtering and search

### Phase 4 (Days 8-10): Note Garden App
- Note-taking system with graph visualization

### Phase 5 (Days 11-12): Reference App
- Reference management system

### Phase 6 (Days 13-14): Experiments App
- Experiment tracking framework

### Phase 7 (Days 15-17): Advanced Features
- Template inheritance, styling, visitor tracking

### Phase 8 (Days 18-20): Integration and Testing
- URL integration, data relationships, admin setup

### Phase 9 (Days 21-22): Production Readiness
- Security, settings, final testing

## Success Criteria
- [ ] Fully functional Django application built entirely by hand
- [ ] Deep understanding of every component and its purpose
- [ ] Ability to explain and modify any part of the system
- [ ] Confidence in Django development patterns
- [ ] Clean, well-documented codebase

## Branch Strategy
- **Reference**: `main` - Contains working implementation for reference
- **Backup**: `ai-assisted-backup` - Backup of AI-assisted work  
- **Development**: `manual-rebuild` - Manual implementation branch

## Resources
- Django Documentation
- Existing implementation in `main` branch for reference
- `MANUAL_REBUILD_WORKFLOW.md` for detailed daily planning

## Learning Objectives
- Master Django models, views, templates, and admin
- Understand database relationships and migrations
- Learn proper Django project structure and best practices
- Gain confidence in full-stack Django development
- Build problem-solving skills through hands-on implementation

## Timeline
Estimated 22 days with 2-4 hours daily commitment

## Notes
This is a learning-focused project prioritizing understanding over speed. The goal is not to recreate exactly the same implementation, but to understand the functionality and build it independently.
