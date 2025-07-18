#!/bin/bash
# ====================================================
# 🧪 Task Manager Test Runner — run_tests.sh
# Clean, reset, test, and report using pytest (SQLite only)
# ====================================================

# 📘 Usage:
#   chmod +x run_tests.sh         # Make script executable
#   ./run_tests.sh                # Full test run
#   ./run_tests.sh -k 'task'      # Run tests matching "task"
#   ./run_tests.sh --maxfail=1    # Stop after 1 failure
#   ./run_tests.sh --help         # Show usage summary

# ✅ Help text
if [[ "$1" == "--help" ]]; then
  echo "Usage: ./run_tests.sh [pytest options]"
  echo ""
  echo "Runs all tests with clean environment and stores output in .tests_output/"
  echo ""
  echo "Examples:"
  echo "  ./run_tests.sh                   # Full test run"
  echo "  ./run_tests.sh -k 'task'        # Run tests with 'task' in name"
  echo "  ./run_tests.sh --maxfail=1      # Stop after one failure"
  echo ""
  exit 0
fi
# 🧹 Ensure script is run from project root
if [[ ! -f manage.py ]]; then
  echo "Error: This script must be run from the project root directory."
  exit 1
fi

# 🐍 Ensure Python environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
  echo "Error: Please activate your Python virtual environment before running this script."
  echo "Example: source venv/bin/activate"
  exit 1
fi

# 📦 Ensure pytest and coverage are installed
if ! command -v pytest &> /dev/null; then
  echo "Error: pytest is not installed."
  exit 1
fi
if ! command -v coverage &> /dev/null; then
  echo "Error: coverage is not installed."
  exit 1
fi

# 🧼 Step 1: Prepare fresh output folder
echo "🔄 Cleaning .tests_output/..."
rm -rf .tests_output
mkdir -p .tests_output/.cache

# 🧼 Step 2: Remove SQLite test database (if exists)
echo "🗑️  Resetting SQLite database..."
rm -f db.sqlite3

# 📂 Step 3: Set coverage file path
export COVERAGE_FILE=.tests_output/.coverage

# 🧪 Step 4: Run tests with clean output formatting
echo "🚀 Running tests..."
pytest \
  --cache-dir=.tests_output/.cache \
  --tb=short \
  --disable-warnings \
  --strict-markers \
  --maxfail=3 \
  --cov=taskmanager \
  --cov-report=term-missing \
  --html=.tests_output/report.html \
  --junitxml=.tests_output/results.xml \
  "$@"

# ✅ Final summary
echo ""
echo "📦 Output saved to: .tests_output/"
echo "  - coverage:        .coverage"
echo "  - pytest cache:    .cache/"
echo "  - html report:     report.html"
echo "  - junit report:    results.xml"

