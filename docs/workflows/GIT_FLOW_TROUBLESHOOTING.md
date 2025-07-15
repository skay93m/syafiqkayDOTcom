# Git-Flow Troubleshooting Guide

This document provides solutions for common git-flow issues encountered during setup and usage.

## Table of Contents

- [Python Syntax Error](#python-syntax-error)
- [Common Git-Flow Issues](#common-git-flow-issues)
- [Prevention Tips](#prevention-tips)
- [Additional Resources](#additional-resources)

## Python Syntax Error

### Problem Description

When running `git flow init` or any git-flow command, you encounter the following error:

```bash
$ git flow init
  File "/home/codespace/.python/current/bin/git-flow", line 58
    except (GitflowError, GitCommandError), e:
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: multiple exception types must be parenthesized
```

### Root Cause

This error occurs when a Python-based git-flow package is installed via pip that uses outdated Python 2 syntax. The syntax `except (GitflowError, GitCommandError), e:` is valid in Python 2 but incompatible with Python 3.x, where it should be `except (GitflowError, GitCommandError) as e:`.

### Solution Steps

#### Step 1: Identify the Conflicting Package

Check which git-flow is being used:

```bash
which git-flow
```

If it returns a path like `/home/codespace/.python/current/bin/git-flow`, you have the Python package installed.

#### Step 2: Remove the Python Package

Uninstall the conflicting Python git-flow package:

```bash
pip uninstall gitflow -y
```

#### Step 3: Verify System Git-Flow

Check that the system git-flow is now being used:

```bash
which git-flow
```

This should now return `/usr/local/bin/git-flow` or `/usr/bin/git-flow`.

Verify it works:

```bash
git flow version
```

#### Step 4: Handle Uncommitted Changes

If you get an error about uncommitted changes:

```bash
Fatal: Index contains uncommited changes. Aborting.
```

Check your git status and commit any pending changes:

```bash
git status
git add .
git commit -m "fix: commit pending changes before git-flow init"
```

#### Step 5: Initialize Git-Flow

Use the default initialization to avoid interactive prompts:

```bash
git flow init -d
```

#### Step 6: Test the Setup

Test git-flow with a feature branch:

```bash
# Start a test feature
git flow feature start test-feature

# Finish the test feature
git flow feature finish test-feature
```

### Expected Output

After successful initialization, you should see:

```bash
Using default branch names.

Which branch should be used for bringing forth production releases?
   - develop
Branch name for production releases: [master] 

Which branch should be used for integration of the "next release"?
   - develop
Branch name for "next release" development: [develop] 

How to name your supporting branch prefixes?
Feature branches? [feature/] 
Bugfix branches? [bugfix/] 
Release branches? [release/] 
Hotfix branches? [hotfix/] 
Support branches? [support/] 
Version tag prefix? [] 
Hooks and filters directory? [/path/to/your/project/.git/hooks]
```

## Common Git-Flow Issues

### Issue: Permission Denied Error

**Problem:**
```bash
E: Could not open lock file /var/lib/dpkg/lock-frontend - open (13: Permission denied)
```

**Solution:**
Use `sudo` when installing system packages:
```bash
sudo apt-get install git-flow
```

### Issue: Branches Have Diverged

**Problem:**
```bash
Branches 'develop' and 'origin/develop' have diverged.
And local branch 'develop' is ahead of 'origin/develop'.
```

**Solution:**
This is a warning, not an error. Push your changes when ready:
```bash
git push origin develop
```

### Issue: Conventional Commit Format Required

**Problem:**
```bash
✗ Invalid commit message format
Please use conventional commit format:
  <type>(<scope>): <subject>
```

**Solution:**
Use proper conventional commit format:
```bash
git commit -m "fix: correct file naming and update requirements.txt"
```

Valid types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`, `revert`

### Issue: Missing Branch Name

**Problem:**
```bash
Fatal: Missing branch name
```

**Solution:**
Use the `-d` flag for default settings or provide branch names manually:
```bash
git flow init -d
```

## Prevention Tips

### 1. Avoid Python Git-Flow Package

Always use the system git-flow package instead of Python alternatives:

```bash
# Install system git-flow
sudo apt-get install git-flow

# Avoid installing Python git-flow
# pip install gitflow  # DON'T DO THIS
```

### 2. Check Installation Before Use

Before using git-flow, verify the correct installation:

```bash
which git-flow
git flow version
```

### 3. Keep Environment Clean

Regularly check for conflicting packages:

```bash
pip list | grep -i git
```

### 4. Use Virtual Environments Carefully

Be aware that Python packages in virtual environments can override system tools. Consider using:

```bash
# Check PATH order
echo $PATH

# Use absolute path if needed
/usr/local/bin/git-flow version
```

## Additional Resources

### Git-Flow Commands Reference

- `git flow feature start <name>` - Start a new feature branch
- `git flow feature finish <name>` - Finish a feature branch
- `git flow release start <version>` - Start a release branch
- `git flow release finish <version>` - Finish a release branch
- `git flow hotfix start <version>` - Start a hotfix branch
- `git flow hotfix finish <version>` - Finish a hotfix branch

### Branch Structure

After initialization, git-flow uses this branch structure:

- **master/main**: Production-ready code
- **develop**: Integration branch for features
- **feature/***: New features in development
- **release/***: Preparing releases
- **hotfix/***: Emergency fixes for production

### Configuration Files

Git-flow configuration is stored in `.git/config`:

```ini
[gitflow "branch"]
    master = master
    develop = develop
[gitflow "prefix"]
    feature = feature/
    bugfix = bugfix/
    release = release/
    hotfix = hotfix/
    support = support/
```

## Troubleshooting Checklist

When encountering git-flow issues:

- [ ] Check which git-flow is being used (`which git-flow`)
- [ ] Verify git-flow version (`git flow version`)
- [ ] Check for Python git-flow packages (`pip list | grep git`)
- [ ] Ensure clean working directory (`git status`)
- [ ] Use proper commit message format
- [ ] Try with default settings (`git flow init -d`)
- [ ] Check PATH for conflicts (`echo $PATH`)

---

**Last Updated:** July 14, 2025  
**Author:** Documentation Team  
**Related:** [GIT_FLOW_GUIDE.md](./GIT_FLOW_GUIDE.md), [STYLE_GUIDE.md](./STYLE_GUIDE.md)
