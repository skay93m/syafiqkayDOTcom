#!/bin/bash
# scripts/tdd_workflow.sh
# Test-Driven Development workflow script
# Usage: ./scripts/tdd_workflow.sh [test_file] [test_function]

set -e

echo "🧪 TDD Workflow Script"
echo "====================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    printf "${1}${2}${NC}\n"
}

# Function to run tests
run_tests() {
    local test_path="$1"
    local verbose="$2"
    
    if [ -n "$test_path" ]; then
        print_color $YELLOW "Running specific test: $test_path"
        if [ "$verbose" = "true" ]; then
            poetry run pytest "$test_path" -v --tb=short
        else
            poetry run pytest "$test_path" -v --tb=short --quiet
        fi
    else
        print_color $YELLOW "Running all tests"
        poetry run pytest -v --tb=short
    fi
}

# Function to run tests with coverage
run_tests_with_coverage() {
    local test_path="$1"
    
    print_color $YELLOW "Running tests with coverage"
    if [ -n "$test_path" ]; then
        poetry run pytest "$test_path" --cov=. --cov-report=term-missing --cov-report=html
    else
        poetry run pytest --cov=. --cov-report=term-missing --cov-report=html
    fi
}

# Function to demonstrate TDD cycle
tdd_demo() {
    print_color $GREEN "TDD Cycle Demonstration"
    print_color $GREEN "======================"
    
    print_color $RED "1. RED Phase - Write a failing test"
    print_color $YELLOW "   Write your test first, before implementing the feature"
    print_color $YELLOW "   The test should fail because the feature doesn't exist yet"
    
    print_color $GREEN "2. GREEN Phase - Make the test pass"
    print_color $YELLOW "   Write the minimum code needed to make the test pass"
    print_color $YELLOW "   Don't worry about perfect code, just make it work"
    
    print_color $GREEN "3. REFACTOR Phase - Improve the code"
    print_color $YELLOW "   Clean up the code while keeping tests passing"
    print_color $YELLOW "   Improve structure, performance, readability"
    
    print_color $GREEN "4. REPEAT - Continue the cycle"
    print_color $YELLOW "   Add more tests for edge cases and new features"
}

# Function to check test status
check_test_status() {
    local test_path="$1"
    
    if poetry run pytest "$test_path" --quiet; then
        print_color $GREEN "✓ Tests are passing"
        return 0
    else
        print_color $RED "✗ Tests are failing"
        return 1
    fi
}

# Function to run specific test categories
run_test_category() {
    local category="$1"
    
    case "$category" in
        "unit")
            print_color $YELLOW "Running unit tests"
            poetry run pytest -m unit -v
            ;;
        "integration")
            print_color $YELLOW "Running integration tests"
            poetry run pytest -m integration -v
            ;;
        "models")
            print_color $YELLOW "Running model tests"
            poetry run pytest -k "model" -v
            ;;
        "views")
            print_color $YELLOW "Running view tests"
            poetry run pytest -k "view" -v
            ;;
        "forms")
            print_color $YELLOW "Running form tests"
            poetry run pytest -k "form" -v
            ;;
        *)
            print_color $RED "Unknown test category: $category"
            print_color $YELLOW "Available categories: unit, integration, models, views, forms"
            exit 1
            ;;
    esac
}

# Main script logic
case "$1" in
    "demo")
        tdd_demo
        ;;
    "run")
        run_tests "$2" "true"
        ;;
    "coverage")
        run_tests_with_coverage "$2"
        ;;
    "status")
        check_test_status "$2"
        ;;
    "category")
        run_test_category "$2"
        ;;
    "watch")
        print_color $YELLOW "Watching for file changes and running tests..."
        # Note: This would need additional setup for file watching
        # For now, just run tests once
        run_tests "$2" "true"
        ;;
    *)
        print_color $GREEN "TDD Workflow Usage:"
        print_color $YELLOW "  ./scripts/tdd_workflow.sh demo                    - Show TDD explanation"
        print_color $YELLOW "  ./scripts/tdd_workflow.sh run [test_path]         - Run tests"
        print_color $YELLOW "  ./scripts/tdd_workflow.sh coverage [test_path]    - Run tests with coverage"
        print_color $YELLOW "  ./scripts/tdd_workflow.sh status [test_path]      - Check test status"
        print_color $YELLOW "  ./scripts/tdd_workflow.sh category [category]     - Run specific test category"
        print_color $YELLOW "  ./scripts/tdd_workflow.sh watch [test_path]       - Watch and run tests"
        print_color $YELLOW ""
        print_color $GREEN "Examples:"
        print_color $YELLOW "  ./scripts/tdd_workflow.sh run homepage/tests.py"
        print_color $YELLOW "  ./scripts/tdd_workflow.sh coverage taskmanager/tests.py"
        print_color $YELLOW "  ./scripts/tdd_workflow.sh category models"
        ;;
esac
