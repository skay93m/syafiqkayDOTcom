#!/bin/bash

# Clean Django Project Script
# This script removes all Django-related files to provide a clean starting point

echo "🧹 Starting Django project cleanup..."

# Files and directories to KEEP
KEEP_FILES=(
    ".git"
    ".gitignore"
    "DJANGO_REBUILD_MANUAL.md"
    "MANUAL_REBUILD_WORKFLOW.md"
    "MANUAL_REBUILD_README.md"
    "GITHUB_ISSUE_TEMPLATE.md"
    "LICENSE"
    "clean_project.sh"
)

echo "📋 Files that will be preserved:"
for file in "${KEEP_FILES[@]}"; do
    if [ -e "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (not found)"
    fi
done

echo ""
echo "🗑️  Files and directories that will be removed:"

# List all items in current directory
for item in *; do
    # Check if this item should be kept
    keep_item=false
    for keep_file in "${KEEP_FILES[@]}"; do
        if [ "$item" = "$keep_file" ]; then
            keep_item=true
            break
        fi
    done
    
    # If not in keep list, mark for removal
    if [ "$keep_item" = false ]; then
        echo "  🗑️  $item"
    fi
done

echo ""
read -p "❓ Do you want to proceed with the cleanup? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 Cleaning project..."
    
    # Remove all items except those in keep list
    for item in *; do
        keep_item=false
        for keep_file in "${KEEP_FILES[@]}"; do
            if [ "$item" = "$keep_file" ]; then
                keep_item=true
                break
            fi
        done
        
        if [ "$keep_item" = false ]; then
            if [ -d "$item" ]; then
                echo "  🗂️  Removing directory: $item"
                rm -rf "$item"
            else
                echo "  📄 Removing file: $item"
                rm -f "$item"
            fi
        fi
    done
    
    # Also remove hidden files/directories (except .git and .gitignore)
    for item in .*; do
        if [ "$item" != "." ] && [ "$item" != ".." ] && [ "$item" != ".git" ] && [ "$item" != ".gitignore" ]; then
            if [ -e "$item" ]; then
                echo "  🔍 Removing hidden item: $item"
                rm -rf "$item"
            fi
        fi
    done
    
    echo ""
    echo "✅ Cleanup complete!"
    echo ""
    echo "📝 Next steps:"
    echo "1. Read DJANGO_REBUILD_MANUAL.md for complete implementation guide"
    echo "2. Follow Phase 1 in MANUAL_REBUILD_WORKFLOW.md"
    echo "3. Start with: python -m venv .venv"
    echo "4. Then: source .venv/bin/activate (on macOS/Linux)"
    echo "5. Install Django: pip install Django==5.0.14"
    echo "6. Create project: django-admin startproject syafiqkay ."
    echo ""
    echo "🥷 Happy coding!"
    
else
    echo "❌ Cleanup cancelled. No files were removed."
fi
