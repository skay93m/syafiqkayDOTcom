# Poetry and Commitizen Setup Guide

This document explains how to fix common Poetry activation issues and set up Commitizen for conventional commits.

## Table of Contents
1. [Poetry Issues and Solutions](#poetry-issues-and-solutions)
2. [Commitizen Setup](#commitizen-setup)
3. [Troubleshooting](#troubleshooting)
4. [Alternative Solutions](#alternative-solutions)

---

## Poetry Issues and Solutions

### Problem: Poetry Cannot Be Activated

**Common Error Messages:**
```bash
Poetry was unable to find a compatible version
The currently activated Python version X.X.X is not supported by the project (>=Y.Y)
poetry shell command is not available (Poetry 2.x)
```

### Root Causes and Solutions

#### 1. Python Version Mismatch

**Problem:** Project requires Python 3.13 but system has Python 3.12

**Solution:** Update `pyproject.toml` to use available Python version

```toml
# Before (causing issues)
requires-python = ">=3.13"

# After (fixed)
requires-python = ">=3.12"
```

**Steps:**
```bash
# Check available Python versions
python3 --version
ls /usr/bin/python*

# Edit pyproject.toml to match available version
# Then regenerate lock file
poetry lock
poetry install
```

#### 2. Outdated Lock File

**Problem:** `poetry.lock` is out of sync with `pyproject.toml`

**Error Message:** 
```
pyproject.toml changed significantly since poetry.lock was last generated
```

**Solution:**
```bash
# Regenerate lock file
poetry lock

# Then install dependencies
poetry install
```

#### 3. Poetry 2.x Shell Command Changes

**Problem:** `poetry shell` command not available in Poetry 2.x

**Error Message:**
```
the shell command is not installed by default
```

**Solutions:**

**Option A: Use new activation method**
```bash
# Get activation command
poetry env activate

# Run the returned command
source /path/to/venv/bin/activate
```

**Option B: Use poetry run for commands**
```bash
poetry run python script.py
poetry run django-admin runserver
```

**Option C: Install shell plugin**
```bash
poetry self add poetry-plugin-shell
poetry shell
```

### Complete Poetry Fix Workflow

```bash
# 1. Check current Python version
python3 --version

# 2. Update pyproject.toml if needed
# Edit requires-python to match available version

# 3. Regenerate lock file
poetry lock

# 4. Install dependencies
poetry install

# 5. Verify environment
poetry env info

# 6. Test activation
poetry env activate
# or
poetry run python --version
```

---

## Commitizen Setup

### Problem: Setting Up Conventional Commits

Commitizen helps enforce conventional commit format for better version management and changelog generation.

### Step-by-Step Setup

#### 1. Add Commitizen to Dependencies

**Option A: Via Poetry (preferred)**
```bash
poetry add --group dev commitizen
```

**Option B: Manual pyproject.toml edit**
```toml
[tool.poetry.group.dev.dependencies]
pytest = "^8.4.1"
commitizen = "^3.14.1"
```

Then run:
```bash
poetry lock
poetry install
```

**Option C: Global installation**
```bash
pip install commitizen
```

#### 2. Configure Commitizen

Add to `pyproject.toml`:
```toml
[tool.commitizen]
name = "cz_conventional_commits"
tag_format = "$version"
version_scheme = "pep440"
version_provider = "pep621"
update_changelog_on_bump = true
major_version_zero = true
```

#### 3. Create Git Commit Template

Create `.gitmessage`:
```
# <type>(<scope>): <subject>
#
# <body>
#
# <footer>

# Types:
# feat:     A new feature
# fix:      A bug fix
# docs:     Documentation only changes
# style:    Changes that do not affect the meaning of the code
# refactor: A code change that neither fixes a bug nor adds a feature
# perf:     A code change that improves performance
# test:     Adding missing tests or correcting existing tests
# chore:    Changes to build process or auxiliary tools
# ci:       Changes to CI configuration files and scripts
# build:    Changes that affect the build system or external dependencies
# revert:   Reverts a previous commit

# Scope (optional): auth, database, ui, api, etc.
# Subject: Brief description (50 chars max, no period)
# Body: Detailed explanation (optional, 72 chars per line)
# Footer: Breaking changes, closes issues (optional)
```

Configure git to use it:
```bash
git config commit.template .gitmessage
```

#### 4. Create Pre-commit Hook

Create `.git/hooks/commit-msg`:
```bash
#!/bin/sh
# Pre-commit hook to validate conventional commit messages

commit_regex='^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(\(.+\))?\!?:\s.{1,50}'

commit_message=$(cat "$1")

if echo "$commit_message" | grep -qE "$commit_regex"; then
    echo "✓ Commit message follows conventional commit format"
    exit 0
else
    echo "✗ Invalid commit message format"
    echo "Please use: <type>(<scope>): <subject>"
    echo "Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert"
    exit 1
fi
```

Make it executable:
```bash
chmod +x .git/hooks/commit-msg
```

#### 5. Create Interactive Commit Helper

Create `scripts/commit.sh`:
```bash
#!/bin/bash

echo "🚀 Conventional Commit Helper"

# Check for staged changes
if ! git diff --cached --quiet; then
    echo "📝 You have staged changes ready to commit."
else
    echo "❌ No staged changes found. Please stage your changes first."
    exit 1
fi

# Interactive prompts for commit details
read -p "Enter commit type (feat/fix/docs/etc): " type
read -p "Enter scope (optional): " scope
read -p "Enter commit subject: " subject

# Build commit message
if [ -z "$scope" ]; then
    commit_msg="$type: $subject"
else
    commit_msg="$type($scope): $subject"
fi

# Show preview and confirm
echo "📋 Commit message: $commit_msg"
read -p "Proceed? (y/N): " confirm

if [[ $confirm =~ ^[Yy]$ ]]; then
    git commit -m "$commit_msg"
    echo "✅ Commit created!"
else
    echo "❌ Commit cancelled."
fi
```

Make it executable:
```bash
chmod +x scripts/commit.sh
```

### Usage Examples

**Using the helper script:**
```bash
git add .
./scripts/commit.sh
```

**Manual conventional commits:**
```bash
git commit -m "feat(auth): add user login functionality"
git commit -m "fix(api): resolve timeout issue"
git commit -m "docs: update installation guide"
git commit -m "chore: update dependencies"
```

**Using Commitizen directly:**
```bash
cz commit  # Interactive commit creation
cz bump    # Version bump and changelog
```

---

## Troubleshooting

### Poetry Issues

**Issue: "No module named 'poetry'"**
```bash
# Reinstall poetry
curl -sSL https://install.python-poetry.org | python3 -
```

**Issue: "Virtual environment not found"**
```bash
# Recreate environment
poetry env remove python
poetry install
```

**Issue: "Permission denied"**
```bash
# Fix permissions
sudo chown -R $USER:$USER ~/.cache/pypoetry
```

### Commitizen Issues

**Issue: "Command 'cz' not found"**
```bash
# Install globally
pip install commitizen

# Or use with poetry
poetry run cz --help
```

**Issue: "Pre-commit hook not working"**
```bash
# Make sure hook is executable
chmod +x .git/hooks/commit-msg

# Test hook
echo "invalid message" | .git/hooks/commit-msg
```

**Issue: "Configuration not found"**
```bash
# Check pyproject.toml has [tool.commitizen] section
# Or create .cz.toml file
```

---

## Alternative Solutions

### Without Poetry (using pip + venv)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install from requirements.txt
pip install -r requirements.txt

# Or install packages directly
pip install django requests psycopg
```

### Without Commitizen (manual conventional commits)

```bash
# Use git aliases for common commit types
git config alias.feat '!f() { git commit -m "feat: $1"; }; f'
git config alias.fix '!f() { git commit -m "fix: $1"; }; f'
git config alias.docs '!f() { git commit -m "docs: $1"; }; f'

# Usage
git feat "add user authentication"
git fix "resolve API timeout"
```

### Git Flow Alternative (manual branching)

```bash
# Instead of git flow feature start
git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# Instead of git flow feature finish
git checkout develop
git merge feature/my-feature
git branch -d feature/my-feature
git push origin develop
```

---

## Summary Checklist

### Poetry Setup ✅
- [ ] Check Python version compatibility
- [ ] Update `requires-python` in pyproject.toml if needed
- [ ] Run `poetry lock` to regenerate lock file
- [ ] Run `poetry install` to install dependencies
- [ ] Verify with `poetry env info`
- [ ] Use `poetry run` or `poetry env activate` for activation

### Commitizen Setup ✅
- [ ] Add commitizen to dev dependencies
- [ ] Configure in pyproject.toml
- [ ] Create .gitmessage template
- [ ] Set up pre-commit hook
- [ ] Create helper scripts
- [ ] Test with sample commit

### Verification ✅
- [ ] Poetry environment activates properly
- [ ] Dependencies install without errors
- [ ] Commit hook validates messages
- [ ] Helper script works interactively
- [ ] Documentation is clear and complete

This guide should help you replicate the setup in any future project or troubleshoot similar issues.
