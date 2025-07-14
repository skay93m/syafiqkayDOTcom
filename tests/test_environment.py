# tests/test_environment.py

# Test for Python version and virtual environment setup
import os
import sys
import pytest

def test_python_version():
    # Test that Python version meets project requirements.
    required_version = (3, 12)  # Adjust based on your pyproject.toml
    current_version = sys.version_info[:2]

    assert current_version >= required_version, (
        f"Python {'.'.join(map(str, required_version))}+ required, "
        f"but {'.'.join(map(str, current_version))} found"
    )

def test_python_executable_path():
    # Test that we're using the correct Python executable.
    
    # Should be in virtual environment
    executable = sys.executable
    
    # Check if we're in a virtual environment
    assert (
        'virtualenvs' in executable or 
        'venv' in executable or 
        os.environ.get('VIRTUAL_ENV')
    ), f"Not running in virtual environment. Using: {executable}"

# Test for Poetry virtual environment and installation
import subprocess

def test_virtual_environment():
    # Test that we're running in a Poetry virtual environment.
    # Check VIRTUAL_ENV environment variable
    virtual_env = os.environ.get('VIRTUAL_ENV')
    assert virtual_env is not None, "VIRTUAL_ENV not set"
    
    # Verify it's a Poetry environment
    assert 'poetry' in virtual_env.lower(), (
        f"Not a Poetry virtual environment: {virtual_env}"
    )

def test_poetry_installation():
    # Test that Poetry is installed and accessible.
    try:
        result = subprocess.run(
            ['poetry', '--version'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        assert 'Poetry' in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.fail("Poetry is not installed or not accessible")

def test_poetry_environment_info():
    # Test that Poetry environment information is accessible.
    try:
        result = subprocess.run(
            ['poetry', 'env', 'info'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        assert 'Python:' in result.stdout
        assert 'Path:' in result.stdout
        assert 'Valid: True' in result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Cannot get Poetry environment info")