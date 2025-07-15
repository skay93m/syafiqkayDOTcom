# Setting Up Multiple Databases in Django

This walkthrough explains how to configure and use multiple databases in a Django project.

## Step 1: Update `settings.py`

Define multiple databases in the `DATABASES` dictionary in your `settings.py` file. Each database will have its own configuration. For example:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'secondary': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'secondary_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}
```

## Step 2: Use the `using()` Method

Specify which database to use for queries by using the `using()` method. For example:

```python
from myapp.models import MyModel

# Query from the default database
default_objects = MyModel.objects.all()

# Query from the secondary database
secondary_objects = MyModel.objects.using('secondary').all()
```

## Step 3: Migrate Databases

Run migrations for each database separately using the `--database` flag:

```bash
python manage.py migrate --database=default
python manage.py migrate --database=secondary
```

## Step 4: Configure Database Routers (Optional)

If you want Django to automatically route queries to specific databases, you can create a custom database router. For example:

```python
class MyDatabaseRouter:
    def db_for_read(self, model, **hints):
        """Point read operations to the appropriate database."""
        if model._meta.app_label == 'myapp':
            return 'secondary'
        return 'default'

    def db_for_write(self, model, **hints):
        """Point write operations to the appropriate database."""
        if model._meta.app_label == 'myapp':
            return 'secondary'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if both objects are in the same database."""
        db_set = {'default', 'secondary'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure migrations are applied to the correct database."""
        if app_label == 'myapp':
            return db == 'secondary'
        return db == 'default'
```

Add the router to your `settings.py`:

```python
DATABASE_ROUTERS = ['myproject.routers.MyDatabaseRouter']
```

## Step 5: Test Your Configuration

Ensure that your configuration works by running queries and migrations for both databases. Use the `using()` method to specify the database explicitly, and verify that the data is stored in the correct database.

---

This walkthrough provides a basic setup for using multiple databases in Django. You can customize the database router and configurations based on your project's requirements.
