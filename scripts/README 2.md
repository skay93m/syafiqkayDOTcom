# Scripts Directory

This directory contains utility scripts for the Django website project.

## Files

### `create_journal_entry.py`
A one-time utility script that was used to import the development journal markdown file (`/static/development_journal.md`) into the Django database as a journal entry.

**Purpose**: Creates a journal entry with the GitHub Copilot user as the author, containing the development journey documentation.

**Usage**: 
```bash
cd /workspaces/syafiq-kay
python scripts/create_journal_entry.py
```

**Note**: This script was already executed during the initial setup and is kept here for reference and documentation purposes.

## Adding New Scripts

When adding new utility scripts:
1. Place them in this directory
2. Add proper documentation headers
3. Update this README with a description
4. Make sure to set proper Django environment if needed
