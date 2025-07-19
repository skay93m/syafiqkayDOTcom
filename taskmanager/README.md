# Task Manager Readme

Task Manager is a web app that is based upon the Agile methodology. There are three main objects: Task, Sprint, and Epic.

**Task**: Represents a work item that needs to be completed within a sprint.

Task has the following attributes:

- `title`: The title of the task.
- `description`: A detailed description of the task.
- `status`: The current status of the task (e.g., UNASSIGNED, IN_PROGRESS, DONE, ARCHIVED).
- `due_date` : The date by which the task should be completed.
- `created_at`: The date and time when the task was created.
- `updated_at`: The date and time when the task was last updated.
- `creator`: The user who created the task.
- `owner`: The user who is currently assigned to the task.
- `sprint`: The sprint to which the task belongs.
- `epic`: The epic to which the task belongs.

**Sprint**: Represents a time-boxed period during which a specific set of tasks is completed.

Sprint has the following attributes:

- `name`: The title of the sprint.
- `decscription`: A detailed description of the sprint.
- `start_date`: The date when the sprint starts.
- `end_date`: The date when the sprint ends.
- `created_at`: The date and time when the sprint was created.
- `updated_at`: The date and time when the sprint was last updated.
- `creator`: The user who created the sprint.
- `tasks`: A list of tasks associated with the sprint.

**Epic**: Represents a large body of work that can be broken down into smaller tasks or user stories. It has attributes like title, description, and a list of associated tasks.

Epic has the following attributes:

- `name`: The title of the epic.
- `description`: A detailed description of the epic.
- `created_at`: The date and time when the epic was created.
- `updated_at`: The date and time when the epic was last updated.
- `creator`: The user who created the epic.
- `tasks`: A list of tasks associated with the epic.

## Task Manager Directory Structure

- docs: Contains documentation files for the project.
- migrations: Contains database migration files.
- services: Contains service layer logic for various functionalities.
- static: Contains static files like CSS, JavaScript, and images.
- templates: Holds HTML templates for rendering views.
- `admin.py`: Contains admin configurations for the Django admin interface.
- `apps.py`: Contains the application configuration for the Django app.
- `models.py`: Contains the data models for the application.
- `tests.py`: Contains the main test cases for the application.
- `urls.py`: Contains URL routing configurations for the application.
- `views.py`: Contains the view logic for handling requests and rendering responses.

## Test Driven Development Approach

### Milestones

1. **Unit Tests**: Write tests for individual components (models, views, services).

    - urls
        - 'TestTaskManagerEndpoints'

    - models
        - 'TestTaskModel'
            - [ ] can create a task
            - [ ] can update a task
            - [ ] can delete a task
            - [ ] can retrieve a task
            - [ ] can list tasks
        - 'TestSprintModel'
            - [ ] can create a sprint
            - [ ] can update a sprint
            - [ ] can delete a sprint
            - [ ] can retrieve a sprint
            - [ ] can list sprints
        - 'TestEpicModel'
            - [ ] can create an epic
            - [ ] can update an epic
            - [ ] can delete an epic
            - [ ] can retrieve an epic
            - [ ] can list epics
    
    - views
        - 'TestTaskView'
        - 'TestSprintView'
        - 'TestEpicView'
    
    - services
        - 'TestTaskService'
        - 'TestSprintService'
        - 'TestEpicService'

2. **Integration Tests**: Test how components work together (e.g., views with models).

    - 'TestTaskManagerIntegration'

3. **Functional Tests**: End-to-end tests that simulate user interactions with the application.

    - 'TestTaskManagerFunctional'
