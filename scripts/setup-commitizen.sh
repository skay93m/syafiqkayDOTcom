#!/bin/bash

echo "Setting up Commitizen for conventional commits..."

# Install commitizen globally if not already installed
if ! command -v cz &> /dev/null; then
    echo "Installing Commitizen..."
    pip install commitizen
fi

# Check if .cz.toml exists, if not create it
if [ ! -f .cz.toml ]; then
    echo "Creating .cz.toml configuration file..."
    cat > .cz.toml << EOF
[tool.commitizen]
name = "cz_conventional_commits"
tag_format = "\$version"
version_scheme = "pep440"
version_provider = "pep621"
update_changelog_on_bump = true
major_version_zero = true
EOF
fi

echo "Commitizen setup complete!"
echo ""
echo "Usage:"
echo "  cz commit        - Create a conventional commit interactively"
echo "  cz bump          - Bump version and create changelog"
echo "  cz changelog     - Generate changelog"
echo ""
echo "Conventional commit format:"
echo "  <type>(<scope>): <subject>"
echo ""
echo "Types: feat, fix, docs, style, refactor, test, chore"
echo "Example: feat(auth): add user login functionality"
