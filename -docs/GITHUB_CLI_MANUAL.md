# GitHub CLI (gh) Manual

## Table of Contents
1. [Installation](#installation)
2. [Authentication](#authentication)
3. [Configuration](#configuration)
4. [Repository Management](#repository-management)
5. [Issue Management](#issue-management)
6. [Pull Request Management](#pull-request-management)
7. [Release Management](#release-management)
8. [GitHub Actions](#github-actions)
9. [Gist Management](#gist-management)
10. [Codespaces](#codespaces)
11. [Organization Management](#organization-management)
12. [Advanced Features](#advanced-features)
13. [Troubleshooting](#troubleshooting)
14. [Tips and Best Practices](#tips-and-best-practices)

---

## Installation

### macOS
```bash
# Using Homebrew
brew install gh

# Using MacPorts
sudo port install gh

# Using Conda
conda install gh --channel conda-forge
```

### Linux
```bash
# Debian/Ubuntu
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# CentOS/RHEL/Fedora
sudo dnf install gh

# Arch Linux
sudo pacman -S github-cli
```

### Windows
```powershell
# Using Chocolatey
choco install gh

# Using Scoop
scoop install gh

# Using Winget
winget install --id GitHub.cli
```

### Verify Installation
```bash
gh --version
```

---

## Authentication

### Initial Authentication
```bash
# Interactive authentication (recommended)
gh auth login

# Token authentication
gh auth login --with-token < token.txt

# SSH authentication
gh auth login --git-protocol ssh
```

### Managing Authentication
```bash
# Check authentication status
gh auth status

# Refresh authentication
gh auth refresh

# Logout
gh auth logout

# Switch between accounts
gh auth switch

# List authenticated accounts
gh auth status --show-token
```

### SSH Key Management
```bash
# List SSH keys
gh ssh-key list

# Add SSH key
gh ssh-key add ~/.ssh/id_rsa.pub --title "My Key"

# Delete SSH key
gh ssh-key delete <key-id>
```

---

## Configuration

### Global Configuration
```bash
# Set default editor
gh config set editor "code --wait"

# Set default protocol
gh config set git_protocol ssh

# Set default browser
gh config set browser firefox

# View all configuration
gh config list

# Get specific config value
gh config get editor

# Reset configuration
gh config set --reset editor
```

### Repository-specific Configuration
```bash
# Set default repository
gh repo set-default owner/repo

# View current default repository
gh repo view
```

---

## Repository Management

### Creating Repositories
```bash
# Create repository (interactive)
gh repo create

# Create public repository
gh repo create my-repo --public

# Create private repository
gh repo create my-repo --private

# Create repository with description
gh repo create my-repo --description "My awesome project"

# Create repository from template
gh repo create my-repo --template owner/template-repo

# Create repository and clone
gh repo create my-repo --clone

# Create repository with specific gitignore
gh repo create my-repo --gitignore Node

# Create repository with license
gh repo create my-repo --license MIT
```

### Repository Operations
```bash
# Clone repository
gh repo clone owner/repo

# Clone to specific directory
gh repo clone owner/repo ~/projects/repo

# Fork repository
gh repo fork owner/repo

# Fork and clone
gh repo fork owner/repo --clone

# View repository
gh repo view owner/repo

# View repository in browser
gh repo view owner/repo --web

# Archive repository
gh repo archive owner/repo

# Delete repository (be careful!)
gh repo delete owner/repo --confirm

# Rename repository
gh repo edit owner/repo --name new-name

# Change repository description
gh repo edit owner/repo --description "New description"

# Change repository visibility
gh repo edit owner/repo --visibility private
```

### Repository Information
```bash
# List your repositories
gh repo list

# List organization repositories
gh repo list myorg

# List repositories with filters
gh repo list --public
gh repo list --private
gh repo list --source
gh repo list --fork
gh repo list --archived

# Search repositories
gh search repos "machine learning" --language python

# Get repository statistics
gh repo view owner/repo --json stargazerCount,forkCount,openIssues
```

---

## Issue Management

### Creating Issues
```bash
# Create issue (interactive)
gh issue create

# Create issue with title and body
gh issue create --title "Bug report" --body "Description of the bug"

# Create issue from template
gh issue create --template bug_report.md

# Create issue with labels
gh issue create --title "Feature request" --label enhancement,feature

# Create issue with assignees
gh issue create --title "Bug fix" --assignee username

# Create issue with milestone
gh issue create --title "Release bug" --milestone "v1.0"

# Create issue from file
gh issue create --title "Bug report" --body-file issue-body.md
```

### Managing Issues
```bash
# List issues
gh issue list

# List issues with filters
gh issue list --state open
gh issue list --state closed
gh issue list --assignee username
gh issue list --author username
gh issue list --label bug
gh issue list --milestone "v1.0"

# View issue details
gh issue view 123

# View issue in browser
gh issue view 123 --web

# Edit issue
gh issue edit 123 --title "New title"
gh issue edit 123 --body "New description"
gh issue edit 123 --add-label bug
gh issue edit 123 --remove-label enhancement
gh issue edit 123 --add-assignee username
gh issue edit 123 --remove-assignee username

# Close issue
gh issue close 123

# Close issue with comment
gh issue close 123 --comment "Fixed in PR #456"

# Reopen issue
gh issue reopen 123

# Pin issue
gh issue pin 123

# Unpin issue
gh issue unpin 123

# Transfer issue
gh issue transfer 123 owner/other-repo

# Delete issue
gh issue delete 123 --confirm
```

### Issue Comments
```bash
# Add comment to issue
gh issue comment 123 --body "This is a comment"

# Edit comment
gh issue comment 123 --edit

# Delete comment
gh issue comment 123 --delete
```

---

## Pull Request Management

### Creating Pull Requests
```bash
# Create pull request (interactive)
gh pr create

# Create pull request with title and body
gh pr create --title "Add new feature" --body "Description of changes"

# Create draft pull request
gh pr create --draft

# Create pull request with reviewers
gh pr create --reviewer username1,username2

# Create pull request with assignees
gh pr create --assignee username

# Create pull request with labels
gh pr create --label enhancement,feature

# Create pull request to specific branch
gh pr create --base main --head feature-branch

# Create pull request from template
gh pr create --template pull_request_template.md

# Create pull request and auto-merge
gh pr create --title "Hotfix" --body "Critical fix" && gh pr merge --auto --squash
```

### Managing Pull Requests
```bash
# List pull requests
gh pr list

# List pull requests with filters
gh pr list --state open
gh pr list --state closed
gh pr list --state merged
gh pr list --author username
gh pr list --assignee username
gh pr list --label bug
gh pr list --base main
gh pr list --head feature-branch

# View pull request details
gh pr view 123

# View pull request in browser
gh pr view 123 --web

# View pull request diff
gh pr diff 123

# Checkout pull request
gh pr checkout 123

# Edit pull request
gh pr edit 123 --title "New title"
gh pr edit 123 --body "New description"
gh pr edit 123 --add-reviewer username
gh pr edit 123 --remove-reviewer username
gh pr edit 123 --add-assignee username
gh pr edit 123 --add-label enhancement

# Convert to draft
gh pr ready 123 --undo

# Mark as ready for review
gh pr ready 123
```

### Pull Request Reviews
```bash
# Request review
gh pr review 123 --request-changes --body "Please fix these issues"
gh pr review 123 --approve --body "Looks good!"
gh pr review 123 --comment --body "Some suggestions"

# Review pull request interactively
gh pr review 123

# View pull request reviews
gh pr view 123 --json reviews
```

### Merging Pull Requests
```bash
# Merge pull request (create merge commit)
gh pr merge 123

# Merge with squash
gh pr merge 123 --squash

# Merge with rebase
gh pr merge 123 --rebase

# Auto-merge when checks pass
gh pr merge 123 --auto --squash

# Merge with custom commit message
gh pr merge 123 --squash --subject "Custom commit message"

# Delete branch after merge
gh pr merge 123 --delete-branch
```

### Pull Request Status
```bash
# Check pull request status
gh pr status

# Check specific pull request checks
gh pr checks 123

# View pull request comments
gh pr view 123 --comments

# Close pull request
gh pr close 123

# Reopen pull request
gh pr reopen 123
```

---

## Release Management

### Creating Releases
```bash
# Create release (interactive)
gh release create

# Create release with tag
gh release create v1.0.0

# Create release with title and notes
gh release create v1.0.0 --title "Release v1.0.0" --notes "Release notes"

# Create release from notes file
gh release create v1.0.0 --notes-file CHANGELOG.md

# Create prerelease
gh release create v1.0.0-beta --prerelease

# Create draft release
gh release create v1.0.0 --draft

# Auto-generate release notes
gh release create v1.0.0 --generate-notes

# Upload assets during creation
gh release create v1.0.0 --title "Release v1.0.0" app.zip README.md
```

### Managing Releases
```bash
# List releases
gh release list

# View release details
gh release view v1.0.0

# View latest release
gh release view --tag latest

# Edit release
gh release edit v1.0.0 --title "New title"
gh release edit v1.0.0 --notes "Updated notes"

# Upload assets to existing release
gh release upload v1.0.0 app.zip

# Download release assets
gh release download v1.0.0

# Download specific asset
gh release download v1.0.0 --pattern "*.zip"

# Delete release
gh release delete v1.0.0 --yes

# Delete release but keep tag
gh release delete v1.0.0 --cleanup-tag=false
```

---

## GitHub Actions

### Workflow Management
```bash
# List workflows
gh workflow list

# View workflow details
gh workflow view workflow.yml

# Run workflow
gh workflow run workflow.yml

# Run workflow with inputs
gh workflow run workflow.yml --field environment=production

# Enable workflow
gh workflow enable workflow.yml

# Disable workflow
gh workflow disable workflow.yml
```

### Workflow Runs
```bash
# List workflow runs
gh run list

# List runs for specific workflow
gh run list --workflow=workflow.yml

# View run details
gh run view 123456

# View run logs
gh run view 123456 --log

# Download run artifacts
gh run download 123456

# Rerun failed jobs
gh run rerun 123456 --failed

# Rerun all jobs
gh run rerun 123456

# Cancel run
gh run cancel 123456

# Delete run
gh run delete 123456

# Watch run in real-time
gh run watch 123456
```

### Secrets Management
```bash
# List repository secrets
gh secret list

# Set repository secret
gh secret set SECRET_NAME --body "secret-value"

# Set secret from file
gh secret set SECRET_NAME < secret.txt

# Delete secret
gh secret delete SECRET_NAME

# List organization secrets
gh secret list --org myorg

# Set organization secret
gh secret set SECRET_NAME --org myorg --body "secret-value"
```

### Variables Management
```bash
# List variables
gh variable list

# Set variable
gh variable set VAR_NAME --body "value"

# Delete variable
gh variable delete VAR_NAME

# List organization variables
gh variable list --org myorg
```

---

## Gist Management

### Creating Gists
```bash
# Create gist from file
gh gist create file.txt

# Create gist with description
gh gist create file.txt --desc "My awesome script"

# Create public gist
gh gist create file.txt --public

# Create gist from multiple files
gh gist create file1.txt file2.py

# Create gist from stdin
echo "Hello World" | gh gist create --filename hello.txt
```

### Managing Gists
```bash
# List your gists
gh gist list

# View gist
gh gist view gist-id

# Edit gist
gh gist edit gist-id

# Clone gist
gh gist clone gist-id

# Download gist
gh gist view gist-id --raw > file.txt

# Delete gist
gh gist delete gist-id
```

---

## Codespaces

### Managing Codespaces
```bash
# List codespaces
gh codespace list

# Create codespace
gh codespace create

# Create codespace for specific repository
gh codespace create --repo owner/repo

# Create codespace with specific machine type
gh codespace create --machine basicLinux32gb

# Connect to codespace
gh codespace ssh

# Connect to specific codespace
gh codespace ssh --name codespace-name

# View codespace logs
gh codespace logs

# Stop codespace
gh codespace stop

# Delete codespace
gh codespace delete

# Port forward from codespace
gh codespace ports forward 3000:3000

# List codespace ports
gh codespace ports
```

---

## Organization Management

### Organization Information
```bash
# List organization members
gh api orgs/myorg/members

# List organization repositories
gh repo list myorg

# View organization profile
gh org view myorg
```

### Team Management
```bash
# List teams
gh api orgs/myorg/teams

# Create team
gh api orgs/myorg/teams --method POST --field name="dev-team" --field privacy="closed"

# Add member to team
gh api orgs/myorg/teams/dev-team/memberships/username --method PUT --field role="member"
```

---

## Advanced Features

### Using GitHub API
```bash
# Make API requests
gh api repos/owner/repo

# POST request with data
gh api repos/owner/repo/issues --method POST --field title="New issue"

# Use pagination
gh api repos/owner/repo/issues --paginate

# Format output with jq
gh api repos/owner/repo --jq '.stargazers_count'
```

### Aliases
```bash
# Create alias
gh alias set prs 'pr list --state=open --author=@me'

# List aliases
gh alias list

# Delete alias
gh alias delete prs

# Useful aliases
gh alias set co 'pr checkout'
gh alias set pv 'pr view'
gh alias set bugs 'issue list --label=bug'
gh alias set features 'issue list --label=enhancement'
```

### Extensions
```bash
# List available extensions
gh extension list

# Install extension
gh extension install owner/gh-extension

# Upgrade extensions
gh extension upgrade --all

# Remove extension
gh extension remove gh-extension

# Popular extensions
gh extension install github/gh-copilot
gh extension install dlvhdr/gh-dash
gh extension install vilmibm/gh-screensaver
```

### Formatting Output
```bash
# JSON output
gh repo view --json name,description,stargazerCount

# Template output
gh issue list --template '{{range .}}{{.number}}: {{.title}}{{"\n"}}{{end}}'

# CSV output (with jq)
gh repo list --json name,stargazerCount | jq -r '.[] | [.name, .stargazerCount] | @csv'
```

---

## Troubleshooting

### Common Issues and Solutions

#### Authentication Issues
```bash
# Problem: "gh: command not found"
# Solution: Reinstall gh CLI
brew reinstall gh

# Problem: Authentication expired
# Solution: Re-authenticate
gh auth refresh

# Problem: Permission denied
# Solution: Check scopes and re-authenticate
gh auth status
gh auth refresh --scopes repo,read:org
```

#### Repository Issues
```bash
# Problem: "No default repository"
# Solution: Set default repository
gh repo set-default owner/repo

# Problem: "Repository not found"
# Solution: Check repository name and permissions
gh repo view owner/repo

# Problem: Cannot clone private repository
# Solution: Check authentication and permissions
gh auth status
gh repo clone owner/private-repo
```

#### Network Issues
```bash
# Problem: Slow API responses
# Solution: Check GitHub status and network
curl -I https://api.github.com

# Problem: API rate limiting
# Solution: Wait or use authenticated requests
gh api rate_limit

# Problem: Corporate firewall blocking
# Solution: Configure proxy
export HTTPS_PROXY=http://proxy.company.com:8080
gh auth login
```

#### Pull Request Issues
```bash
# Problem: Cannot create PR from forked repository
# Solution: Ensure you're in the forked repository
cd /path/to/forked/repo
gh pr create

# Problem: PR merge conflicts
# Solution: Resolve conflicts and update
git pull origin main
git push origin feature-branch
```

### Debugging Commands
```bash
# Enable debug logging
GH_DEBUG=api gh repo view owner/repo

# Verbose output
gh repo list --debug

# Check configuration
gh config list

# Test authentication
gh auth status --show-token
```

### Getting Help
```bash
# General help
gh help

# Command-specific help
gh pr create --help
gh issue list --help

# Manual pages
man gh
man gh-pr
man gh-issue

# Online documentation
gh repo view cli/cli --web
```

---

## Tips and Best Practices

### Productivity Tips
```bash
# Use shell completion
gh completion -s zsh > /usr/local/share/zsh/site-functions/_gh

# Create useful aliases
gh alias set co 'pr checkout'
gh alias set prs 'pr list --author=@me'
gh alias set issues 'issue list --assignee=@me'

# Use templates for consistent formatting
gh pr create --template .github/pull_request_template.md

# Batch operations
gh issue list --json number | jq '.[].number' | xargs -I {} gh issue close {}
```

### Security Best Practices
```bash
# Use minimal scopes
gh auth refresh --scopes repo

# Regularly rotate tokens
gh auth refresh

# Use SSH for Git operations
gh config set git_protocol ssh

# Review active tokens
gh auth status --show-token
```

### Workflow Integration
```bash
# Git hooks integration
echo 'gh pr create --fill' > .git/hooks/post-commit
chmod +x .git/hooks/post-commit

# CI/CD integration
gh workflow run deploy.yml --field environment=production

# Issue linking in commits
git commit -m "Fix login bug (fixes #123)"
```

### Advanced Automation
```bash
# Auto-merge dependabot PRs
gh pr list --author dependabot[bot] --json number | \
  jq '.[].number' | \
  xargs -I {} gh pr merge {} --auto --squash

# Bulk issue labeling
gh issue list --state open --json number | \
  jq '.[].number' | \
  xargs -I {} gh issue edit {} --add-label needs-triage

# Weekly status report
gh pr list --state merged --base main --limit 20 --json title,mergedAt | \
  jq '.[] | select(.mergedAt | fromdateiso8601 > (now - 604800))'
```

### Performance Optimization
```bash
# Use pagination for large datasets
gh api repos/owner/repo/issues --paginate

# Filter results at API level
gh issue list --state closed --limit 10

# Use specific fields in JSON queries
gh repo list --json name,stargazerCount,updatedAt

# Cache frequently used data
gh repo list --json name > ~/.gh-repos-cache.json
```

---

## Conclusion

This manual covers the essential and advanced features of GitHub CLI. For the most up-to-date information, always refer to:
- `gh help` for built-in documentation
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitHub CLI Repository](https://github.com/cli/cli)

Remember to keep your GitHub CLI updated for the latest features and security improvements:
```bash
gh extension upgrade --all
brew upgrade gh  # on macOS with Homebrew
```

Happy coding with GitHub CLI! 🚀
