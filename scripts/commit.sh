#!/bin/bash

# Conventional Commit Helper Script

echo "🚀 Conventional Commit Helper"
echo "=============================="

# Function to show commit types
show_types() {
    echo "Available commit types:"
    echo "  feat     - A new feature"
    echo "  fix      - A bug fix"  
    echo "  docs     - Documentation changes"
    echo "  style    - Code style changes (formatting, etc.)"
    echo "  refactor - Code refactoring"
    echo "  test     - Adding or updating tests"
    echo "  chore    - Maintenance tasks"
    echo "  perf     - Performance improvements"
    echo "  ci       - CI/CD changes"
    echo "  build    - Build system changes"
    echo "  revert   - Revert previous commit"
}

# Check if there are staged changes
if ! git diff --cached --quiet; then
    echo "📝 You have staged changes ready to commit."
else
    echo "❌ No staged changes found. Please stage your changes first with 'git add'."
    exit 1
fi

echo ""
show_types
echo ""

# Get commit type
read -p "Enter commit type: " type

# Validate type
valid_types="feat fix docs style refactor test chore perf ci build revert"
if [[ ! " $valid_types " =~ " $type " ]]; then
    echo "❌ Invalid commit type. Please use one of: $valid_types"
    exit 1
fi

# Get optional scope
read -p "Enter scope (optional, press enter to skip): " scope

# Get subject
read -p "Enter commit subject (brief description): " subject

# Validate subject
if [ -z "$subject" ]; then
    echo "❌ Subject is required"
    exit 1
fi

# Build commit message
if [ -z "$scope" ]; then
    commit_msg="$type: $subject"
else
    commit_msg="$type($scope): $subject"
fi

# Get optional body
echo ""
read -p "Enter detailed description (optional, press enter to skip): " body

# Get optional footer
read -p "Enter footer (breaking changes, closes issues, etc. - optional): " footer

# Build full commit message
full_msg="$commit_msg"
if [ ! -z "$body" ]; then
    full_msg="$full_msg

$body"
fi

if [ ! -z "$footer" ]; then
    full_msg="$full_msg

$footer"
fi

echo ""
echo "📋 Commit message preview:"
echo "=========================="
echo "$full_msg"
echo "=========================="
echo ""

read -p "Proceed with this commit? (y/N): " confirm
if [[ $confirm =~ ^[Yy]$ ]]; then
    git commit -m "$full_msg"
    echo "✅ Commit created successfully!"
else
    echo "❌ Commit cancelled."
fi
