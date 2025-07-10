# Experiments Admin Interface Guide

## Overview
The experiments app now has a comprehensive admin interface that allows you to manage experiments and their associated resources through Django's admin panel.

## Features

### Experiment Management
- **List View**: See all experiments with status badges, publication status, and resource counts
- **Detailed Views**: Full experiment details organized in collapsible fieldsets
- **Status Badges**: Color-coded status indicators (Conceptualizing, Designing, Testing, Analyzing, Completed, Abandoned)
- **Search**: Search through titles, descriptions, hypotheses, methodologies, and tags
- **Filters**: Filter by status, publication status, and creation/update dates
- **Bulk Actions**: Mark multiple experiments as published/unpublished or change status
- **Bilingual Interface**: Templates display both English and Japanese text with ruby annotations

### Resource Management
- **Inline Editing**: Add/edit resources directly from the experiment edit page
- **Separate Admin**: Dedicated admin interface for managing resources independently
- **Quick Links**: Easy navigation between experiments and their resources

### Admin Interface Enhancements
- **Frontend Links**: Direct links to view published experiments on the frontend
- **Resource Counters**: See how many resources are associated with each experiment
- **Auto-generated Slugs**: Slugs are automatically generated from titles
- **Organized Fields**: Fields are grouped logically with collapsible sections

## How to Use

### Accessing the Admin
1. Start the Django development server: `python manage.py runserver`
2. Navigate to `http://localhost:8000/admin/`
3. Log in with your superuser credentials
4. Look for the "Experiments" section

### Creating a New Experiment
1. Click "Add" next to "Experiments"
2. Fill in the basic information (title, description, tags)
3. Add experiment details (hypothesis, methodology)
4. Set the status and publication status
5. Add resources using the inline forms at the bottom
6. Save the experiment

### Managing Experiments
- **Search**: Use the search bar to find experiments by title, description, or tags
- **Filter**: Use the right sidebar to filter by status, publication status, or dates
- **Bulk Actions**: Select multiple experiments and use the action dropdown to:
  - Mark as published/unpublished
  - Change status to completed/testing
- **View on Site**: Click the 👁️ View link to see published experiments on the frontend

### Working with Resources
- **From Experiment Page**: Add resources directly while editing an experiment
- **From Resources Admin**: Manage all resources independently under "Experiment resources"
- **Quick Navigation**: Click resource counts to see all resources for an experiment

## Sample Data
Run the following command to create sample experiments for testing:
```bash
python manage.py create_sample_experiments --count 6
```

**Note:** New experiments are created as published by default. If you need to create unpublished experiments, you can change their status through the admin interface.

## Publishing Experiments
- Only published experiments appear on the public dashboard
- Use the admin interface to toggle publication status
- You can bulk publish experiments using the admin actions

## Admin Customizations
The admin interface includes:
- Custom site header: "Syafiq Kay Admin 🌸"
- Color-coded status badges
- Clickable links to resources and frontend views
- Organized fieldsets for better UX
- Helpful tooltips and descriptions

## Status Workflow
The typical experiment workflow:
1. **Conceptualizing** → Initial idea phase
2. **Designing** → Planning the experiment
3. **Testing** → Running the experiment
4. **Analyzing** → Processing results
5. **Completed** → Finished with conclusions
6. **Abandoned** → Discontinued experiment

## Tips
- Use tags for better organization and searching
- Keep hypothesis and methodology clear and detailed
- Update status as experiments progress
- Only publish experiments when they're ready for public viewing
- Use resources to link to relevant documentation, datasets, or tools
