# Commitizen Setup

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for consistent commit messages and automated versioning.

## Quick Start

### Option 1: Using the Commit Helper Script
```bash
# Make sure you have staged changes
git add .

# Use the interactive commit helper
./scripts/commit.sh
```

### Option 2: Manual Conventional Commits
```bash
# Format: <type>(<scope>): <subject>
git commit -m "feat(auth): add user login functionality"
git commit -m "fix(database): resolve connection timeout issue"
git commit -m "docs: update API documentation"
```

### Option 3: Using Commitizen (if installed)
```bash
# Install commitizen
pip install commitizen

# Create interactive commit
cz commit

# Bump version and generate changelog
cz bump
```

## Commit Types

| Type       | Description                                    | Example                                    |
|------------|------------------------------------------------|--------------------------------------------|
| `feat`     | A new feature                                  | `feat(auth): add OAuth integration`       |
| `fix`      | A bug fix                                      | `fix(api): handle null responses`         |
| `docs`     | Documentation only changes                    | `docs: update installation guide`         |
| `style`    | Code style changes (formatting, etc.)         | `style: fix indentation in components`    |
| `refactor` | Code refactoring                              | `refactor(utils): simplify date helpers`  |
| `test`     | Adding or updating tests                       | `test(auth): add login validation tests`  |
| `chore`    | Maintenance tasks                             | `chore: update dependencies`              |
| `perf`     | Performance improvements                       | `perf(api): optimize database queries`    |
| `ci`       | CI/CD configuration changes                    | `ci: add automated testing workflow`      |
| `build`    | Build system or external dependency changes   | `build: update webpack configuration`     |
| `revert`   | Revert a previous commit                      | `revert: undo feature X implementation`   |

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Examples

**Simple commit:**
```
feat: add user authentication
```

**With scope:**
```
fix(database): resolve connection pool exhaustion
```

**With body and footer:**
```
feat(api): implement user profile endpoints

Add GET, PUT, and DELETE endpoints for user profiles.
Includes validation and error handling.

Closes #123
```

**Breaking change:**
```
feat(api)!: change user authentication method

BREAKING CHANGE: The authentication method has changed from 
JWT to OAuth 2.0. All existing JWT tokens will be invalidated.
```

## Configuration

The project is configured with:

- **pyproject.toml**: Commitizen configuration
- **.gitmessage**: Git commit template
- **.git/hooks/commit-msg**: Pre-commit hook for validation
- **scripts/commit.sh**: Interactive commit helper
- **scripts/setup-commitizen.sh**: Setup script

## Automatic Features

1. **Commit Message Validation**: The pre-commit hook validates that commits follow the conventional format
2. **Version Bumping**: Use `cz bump` to automatically increment version based on commit types
3. **Changelog Generation**: Automatically generate CHANGELOG.md from commit messages
4. **Git Templates**: Helpful commit message template when using `git commit` without `-m`

## Benefits

- ✅ Consistent commit message format
- ✅ Automated semantic versioning
- ✅ Automatic changelog generation
- ✅ Better project history tracking
- ✅ Integration with release automation tools

## Troubleshooting

If Commitizen is not working:
1. Make sure it's installed: `pip install commitizen`
2. Try the commit helper script: `./scripts/commit.sh`
3. Use manual conventional commits with the format above
4. Check the pre-commit hook is working: `git commit -m "invalid message"` should fail
