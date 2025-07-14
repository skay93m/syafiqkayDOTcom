# Git Flow Branching Model Guide

## Table of Contents
1. [Overview](#overview)
2. [Branch Types](#branch-types)
3. [Installation](#installation)
4. [Getting Started](#getting-started)
5. [Feature Development Workflow](#feature-development-workflow)
6. [Release Workflow](#release-workflow)
7. [Hotfix Workflow](#hotfix-workflow)
8. [Best Practices](#best-practices)
9. [Common Commands Reference](#common-commands-reference)
10. [Troubleshooting](#troubleshooting)

## Overview

Git Flow is a branching model that defines a strict branching model designed around the project release. It provides a robust framework for managing larger projects with scheduled releases.

### Key Benefits
- Clear separation of different types of work
- Parallel development of features
- Easy to maintain release versions
- Quick hotfix deployment capability
- Structured approach to code management

## Branch Types

### Main Branches (Permanent)
- **`master`** - Production-ready code, always stable
- **`develop`** - Integration branch for features, latest development changes

### Supporting Branches (Temporary)
- **`feature/*`** - New features development
- **`release/*`** - Prepare for production releases
- **`hotfix/*`** - Quick fixes for production issues

## Installation

### Install Git Flow Extension

**On Ubuntu/Debian:**
```bash
sudo apt-get install git-flow
```

**On macOS:**
```bash
brew install git-flow
```

**On Windows:**
```bash
# Using Chocolatey
choco install gitflow-avh

# Or download from: https://github.com/petervanderdoes/gitflow-avh
```

## Getting Started

### Initialize Git Flow in Your Repository

```bash
# Navigate to your repository
cd /path/to/your/repo

# Initialize git flow
git flow init

# Follow the prompts (usually accept defaults):
# - Production branch: master
# - Development branch: develop
# - Feature prefix: feature/
# - Release prefix: release/
# - Hotfix prefix: hotfix/
# - Support prefix: support/
```

### Initial Setup for Existing Repository

```bash
# If you already have master branch
git checkout master

# Create develop branch from master
git checkout -b develop
git push -u origin develop

# Initialize git flow
git flow init
```

## Feature Development Workflow

### 1. Start a New Feature

```bash
# Start a new feature branch
git flow feature start feature-name

# This creates and switches to: feature/feature-name
# Based on: develop branch
```

### 2. Work on Your Feature

```bash
# Make your changes
echo "New feature code" > new-feature.py

# Commit your changes
git add .
git commit -m "Add new feature functionality"

# Push feature branch (optional, for collaboration)
git push origin feature/feature-name
```

### 3. Finish the Feature

```bash
# Finish the feature
git flow feature finish feature-name

# This will:
# 1. Merge feature/feature-name into develop
# 2. Delete the feature branch
# 3. Switch back to develop
```

### 4. Publish/Pull Features (for team collaboration)

```bash
# Publish feature to remote repository
git flow feature publish feature-name

# Pull someone else's feature
git flow feature pull origin feature-name
```

## Release Workflow

### 1. Start a Release

```bash
# Start a new release
git flow release start 1.0.0

# This creates: release/1.0.0 from develop branch
```

### 2. Prepare the Release

```bash
# Update version numbers, documentation, etc.
echo "1.0.0" > VERSION
git add VERSION
git commit -m "Bump version to 1.0.0"

# Fix any last-minute bugs
git commit -m "Fix critical bug before release"
```

### 3. Finish the Release

```bash
# Finish the release
git flow release finish 1.0.0

# This will:
# 1. Merge release/1.0.0 into master
# 2. Tag the release on master
# 3. Merge release/1.0.0 into develop
# 4. Delete the release branch

# Push everything
git push origin master
git push origin develop
git push origin --tags
```

## Hotfix Workflow

### 1. Start a Hotfix

```bash
# Start a hotfix from master
git flow hotfix start 1.0.1

# This creates: hotfix/1.0.1 from master branch
```

### 2. Fix the Issue

```bash
# Make your critical fix
echo "Fixed critical bug" > bugfix.py
git add .
git commit -m "Fix critical security vulnerability"
```

### 3. Finish the Hotfix

```bash
# Finish the hotfix
git flow hotfix finish 1.0.1

# This will:
# 1. Merge hotfix/1.0.1 into master
# 2. Tag the hotfix on master
# 3. Merge hotfix/1.0.1 into develop
# 4. Delete the hotfix branch

# Push everything
git push origin master
git push origin develop
git push origin --tags
```

## Best Practices

### Naming Conventions

```bash
# Features - use descriptive names
git flow feature start user-authentication
git flow feature start payment-integration
git flow feature start api-optimization

# Releases - use semantic versioning
git flow release start 1.0.0
git flow release start 2.1.0
git flow release start 1.5.2

# Hotfixes - increment patch version
git flow hotfix start 1.0.1
git flow hotfix start 2.1.1
```

### Commit Message Guidelines

```bash
# Feature commits
git commit -m "feat: add user registration functionality"
git commit -m "feat: implement payment gateway integration"

# Bug fixes
git commit -m "fix: resolve login authentication issue"
git commit -m "fix: correct database connection timeout"

# Documentation
git commit -m "docs: update API documentation"
git commit -m "docs: add installation guide"

# Refactoring
git commit -m "refactor: optimize database queries"
git commit -m "refactor: restructure user service layer"
```

### Code Review Process

```bash
# For collaborative features
git flow feature publish feature-name

# Create pull request from feature branch to develop
# After review and approval:
git flow feature finish feature-name
```

### Testing Guidelines

```bash
# Before finishing features
# Run tests on feature branch
python manage.py test  # For Django projects
npm test              # For Node.js projects

# Before finishing releases
# Run full test suite
python manage.py test --verbose
```

## Common Commands Reference

### Feature Commands
```bash
git flow feature start <name>        # Start new feature
git flow feature finish <name>       # Finish feature
git flow feature publish <name>      # Publish feature to remote
git flow feature pull origin <name>  # Pull feature from remote
git flow feature list               # List all features
```

### Release Commands
```bash
git flow release start <version>     # Start new release
git flow release finish <version>    # Finish release
git flow release publish <version>   # Publish release to remote
git flow release list               # List all releases
```

### Hotfix Commands
```bash
git flow hotfix start <version>      # Start new hotfix
git flow hotfix finish <version>     # Finish hotfix
git flow hotfix publish <version>    # Publish hotfix to remote
git flow hotfix list                # List all hotfixes
```

### Utility Commands
```bash
git flow init                       # Initialize git flow
git flow version                    # Show git flow version
git flow config                     # Show current configuration
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Git Flow Not Initialized (Most Common Issue)

**Error:** `git flow feature list` fails or `git flow` commands don't work

**Solution:**
```bash
# Check if git flow is initialized
git flow version

# If not installed, install git flow first
sudo apt-get install git-flow

# Initialize git flow in your repository
git flow init

# Follow prompts and accept defaults:
# - Production branch: master (or main)
# - Development branch: develop
# - Feature prefix: feature/
# - Release prefix: release/
# - Hotfix prefix: hotfix/
```

#### 2. No Develop Branch Exists

**Error:** Git flow init fails because there's no develop branch

**Solution:**
```bash
# Create develop branch from current branch (usually master)
git checkout master
git checkout -b develop
git push -u origin develop

# Now initialize git flow
git flow init
```

#### 3. Unable to Finish Feature - Uncommitted Changes

**Error:** `git flow feature finish` fails due to uncommitted changes

**Solution:**
```bash
# Check what's uncommitted
git status

# Option 1: Commit the changes
git add .
git commit -m "Complete feature implementation"

# Option 2: Stash changes temporarily
git stash push -m "WIP: temporary stash"

# Now finish the feature
git flow feature finish feature-name

# If you stashed, apply changes back
git stash pop
```

#### 4. Unable to Finish Feature - Merge Conflicts

**Error:** Merge conflicts when finishing feature

**Solution:**
```bash
# Update your feature branch with latest develop
git checkout feature/feature-name
git fetch origin
git merge origin/develop

# Resolve conflicts manually in your editor
# Then add resolved files
git add .
git commit -m "Resolve merge conflicts with develop"

# Now finish the feature
git flow feature finish feature-name
```

#### 5. Feature Branch Not Based on Latest Develop

**Error:** Feature branch is outdated

**Solution:**
```bash
# Update develop first
git checkout develop
git pull origin develop

# Update your feature branch
git checkout feature/feature-name
git merge develop

# Or rebase for cleaner history
git rebase develop

# Resolve any conflicts and continue
git add .
git rebase --continue  # if rebasing

# Now finish the feature
git flow feature finish feature-name
```

#### 6. Remote Tracking Issues

**Error:** Feature branch has remote tracking issues

**Solution:**
```bash
# Check remote branches
git branch -r

# If feature branch exists on remote, pull it first
git checkout feature/feature-name
git pull origin feature/feature-name

# Or if you want to delete remote feature branch
git push origin --delete feature/feature-name

# Then finish locally
git flow feature finish feature-name
```

#### 7. Accidentally Deleted Feature Branch

**Solution:**
```bash
# Find the commit hash
git reflog

# Look for your feature commits and note the hash
# Recreate the branch
git checkout -b feature/feature-name <commit-hash>

# Continue working or finish the feature
git flow feature finish feature-name
```

#### 8. Need to Abort a Release

**Solution:**
```bash
# If you haven't finished the release yet
git checkout develop
git branch -D release/version-number

# If you need to undo a finished release
git checkout master
git reset --hard HEAD~1  # Remove merge commit
git tag -d version-number  # Remove tag
git push origin :refs/tags/version-number  # Remove remote tag
```

#### 9. Cannot Switch Branches - Dirty Working Directory

**Error:** Cannot checkout branch due to uncommitted changes

**Solution:**
```bash
# Option 1: Commit changes
git add .
git commit -m "WIP: work in progress"

# Option 2: Stash changes
git stash push -m "Temporary stash before branch switch"

# Option 3: Reset changes (CAUTION: loses changes)
git reset --hard HEAD

# Then proceed with git flow commands
```

#### 10. Git Flow Commands Not Found

**Error:** `bash: git-flow: command not found`

**Solution:**
```bash
# Install git flow
# On Ubuntu/Debian:
sudo apt-get update
sudo apt-get install git-flow

# On macOS:
brew install git-flow-avh

<<<<<<< HEAD
=======
# Alternative installation (if package manager fails):
curl -L -O https://raw.githubusercontent.com/petervanderdoes/gitflow-avh/develop/contrib/gitflow-installer.sh
bash gitflow-installer.sh install stable
rm gitflow-installer.sh

>>>>>>> develop
# Verify installation
git flow version

# Initialize in your repo
git flow init
```

<<<<<<< HEAD
=======
#### 11. Manual Feature Finish (Without Git Flow)

**When Git Flow is not available, you can manually finish a feature:**

```bash
# 1. Ensure all changes are committed on feature branch
git add .
git commit -m "Complete feature implementation"

# 2. Switch to develop branch and update
git checkout develop
git pull origin develop

# 3. Merge feature branch into develop
git merge feature/feature-name

# 4. Delete the feature branch
git branch -d feature/feature-name

# 5. Push updated develop branch
git push origin develop

# 6. If feature branch exists on remote, delete it
git push origin --delete feature/feature-name
```

#### 12. Environment Setup Issues

**Error:** Git Flow installation fails in containerized environments

**Solution:**
```bash
# Check if running in Docker/container
cat /proc/1/cgroup

# If in container, you may need to install build tools first
apt update && apt install -y build-essential git

# Or use manual git workflow instead of git-flow
# See "Manual Feature Finish" above
```

>>>>>>> develop
### Checking Current State

```bash
# See all branches
git branch -a

# See current git flow state
git flow feature list
git flow release list
git flow hotfix list

# Check which branch you're on
git status
```

## Integration with Your Django Project

Since you're working with a Django project, here are some additional considerations:

### Database Migrations

```bash
# In feature branches
python manage.py makemigrations
python manage.py migrate

# Before finishing release
python manage.py migrate --check
```

### Environment-Specific Settings

```bash
# Use different settings for different branches
# feature branches: settings/development.py
# release branches: settings/staging.py
# master branch: settings/production.py
```

### Testing Integration

```bash
# Run tests before finishing features
python manage.py test

# Coverage reports
coverage run --source='.' manage.py test
coverage report
```

---

## Quick Start Summary

1. **Initialize:** `git flow init`
2. **Start Feature:** `git flow feature start feature-name`
3. **Work & Commit:** Regular git commits
4. **Finish Feature:** `git flow feature finish feature-name`
5. **Start Release:** `git flow release start 1.0.0`
6. **Prepare Release:** Update versions, test
7. **Finish Release:** `git flow release finish 1.0.0`
8. **Deploy:** `git push origin master develop --tags`

Remember: Always test thoroughly before finishing releases, and use hotfixes only for critical production issues!
