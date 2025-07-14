# Scripts

Utility scripts for the Django manual rebuild project.

## Files

- **[clean_project.sh](clean_project.sh)** - Interactive script to clean up existing Django code and start fresh

## Usage

### Cleanup Script
```bash
# Make executable (if needed)
chmod +x scripts/clean_project.sh

# Run the cleanup script
./scripts/clean_project.sh
```

The cleanup script will:
- Show you what will be removed
- Ask for confirmation before each step
- Preserve documentation and essential files
- Create a fresh requirements.txt for new start
