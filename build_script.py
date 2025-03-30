#!/usr/bin/env python3
"""
FlatForge Build Script

This script handles the build process for FlatForge, including:
- Cleaning build artifacts
- Running tests
- Building the package
- Publishing to PyPI

Usage:
    python build.py [clean|test|build|publish|all]
"""

import os
import sys
import shutil
import subprocess
import re
import time
from datetime import datetime

# Configuration
PACKAGE_NAME = "flatforge"
VERSION_FILE = "flatforge/__init__.py"
TEST_DIR = "tests"
BUILD_DIR = "dist"
DOCS_DIR = "docs"


def get_version():
    """Get the current version from the version file."""
    with open(VERSION_FILE, "r") as f:
        content = f.read()
    version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string in {}".format(VERSION_FILE))


def clean():
    """Clean build artifacts."""
    print("Cleaning build artifacts...")
    dirs_to_clean = [
        BUILD_DIR,
        "build",
        "{}.egg-info".format(PACKAGE_NAME),
        "__pycache__",
        ".pytest_cache",
    ]
    
    for dir_to_clean in dirs_to_clean:
        if os.path.exists(dir_to_clean):
            print(f"Removing {dir_to_clean}")
            try:
                shutil.rmtree(dir_to_clean)
            except PermissionError:
                print(f"Permission error when removing {dir_to_clean}")
                print("Trying alternative method...")
                try:
                    # Try to rename the folder first, which often helps with permission issues
                    temp_name = f"{dir_to_clean}_old_{int(time.time())}"
                    os.rename(dir_to_clean, temp_name)
                    shutil.rmtree(temp_name, ignore_errors=True)
                    print(f"Successfully removed {dir_to_clean} using alternative method")
                except Exception as e:
                    print(f"Warning: Could not remove {dir_to_clean}: {e}")
                    print(f"You may need to manually delete {dir_to_clean} before building")
            except Exception as e:
                print(f"Warning: Could not remove {dir_to_clean}: {e}")
    
    # Clean __pycache__ directories recursively
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                pycache_path = os.path.join(root, dir_name)
                print(f"Removing {pycache_path}")
                try:
                    shutil.rmtree(pycache_path)
                except Exception as e:
                    print(f"Warning: Could not remove {pycache_path}: {e}")
    
    # Clean .pyc files
    for root, dirs, files in os.walk("."):
        for file_name in files:
            if file_name.endswith(".pyc"):
                pyc_path = os.path.join(root, file_name)
                print(f"Removing {pyc_path}")
                try:
                    os.remove(pyc_path)
                except Exception as e:
                    print(f"Warning: Could not remove {pyc_path}: {e}")
    
    print("Cleaning complete.")


def run_tests():
    """Run the test suite."""
    print("Running tests...")
    result = subprocess.run(["pytest", TEST_DIR, "-v"])
    if result.returncode != 0:
        print("Tests failed.")
        sys.exit(1)
    print("All tests passed.")


def build():
    """Build the package."""
    print("Building package...")
    version = get_version()
    print(f"Building version: {version}")
    
    # Ensure build tools are installed
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "build", "twine"])
    
    # Build the package
    result = subprocess.run([sys.executable, "-m", "build", "."])
    if result.returncode != 0:
        print("Build failed.")
        sys.exit(1)
    
    print(f"Build complete. Package version: {version}")
    
    # Verify the build
    if os.path.exists(BUILD_DIR):
        wheel_file = None
        for file in os.listdir(BUILD_DIR):
            if file.endswith(".whl") and version in file:
                wheel_file = os.path.join(BUILD_DIR, file)
                break
        
        if wheel_file:
            print(f"Built wheel file: {wheel_file}")
        else:
            print("Warning: Could not find the built wheel file.")
    else:
        print(f"Warning: Build directory {BUILD_DIR} not found. Build may have failed.")


def check_version_tag():
    """Check if the current version has a git tag."""
    version = get_version()
    result = subprocess.run(
        ["git", "tag", "-l", f"v{version}"], 
        capture_output=True, 
        text=True
    )
    
    if f"v{version}" in result.stdout:
        print(f"Version {version} already has a git tag.")
        return True
    
    print(f"Version {version} does not have a git tag yet.")
    return False


def create_version_tag():
    """Create a git tag for the current version."""
    version = get_version()
    print(f"Creating git tag for version {version}...")
    
    # Add a tag for the version
    tag_message = f"Release version {version} - {datetime.now().strftime('%Y-%m-%d')}"
    result = subprocess.run(
        ["git", "tag", "-a", f"v{version}", "-m", tag_message]
    )
    
    if result.returncode != 0:
        print("Failed to create git tag.")
        return False
    
    # Push the tag
    result = subprocess.run(["git", "push", "origin", f"v{version}"])
    if result.returncode != 0:
        print("Failed to push git tag.")
        return False
    
    print(f"Git tag v{version} created and pushed successfully.")
    return True


def publish():
    """Publish the package to PyPI."""
    print("Publishing to PyPI...")
    version = get_version()
    
    # Check if this version is already on PyPI
    try:
        import requests
        response = requests.get(f"https://pypi.org/pypi/{PACKAGE_NAME}/json")
        if response.status_code == 200:
            pypi_version = response.json()["info"]["version"]
            if pypi_version == version:
                print(f"Version {version} is already published on PyPI.")
                proceed = input("Do you want to proceed anyway? (y/n): ")
                if proceed.lower() != "y":
                    print("Publishing aborted.")
                    return
    except Exception as e:
        print(f"Could not check PyPI version: {e}")
        proceed = input("Do you want to proceed with publishing? (y/n): ")
        if proceed.lower() != "y":
            print("Publishing aborted.")
            return
    
    # Check for version tag
    if not check_version_tag():
        create_tag = input("No git tag found for this version. Create one? (y/n): ")
        if create_tag.lower() == "y":
            if not create_version_tag():
                proceed = input("Failed to create git tag. Proceed with publishing anyway? (y/n): ")
                if proceed.lower() != "y":
                    print("Publishing aborted.")
                    return
    
    # Upload to PyPI
    result = subprocess.run(
        [sys.executable, "-m", "twine", "upload", f"{BUILD_DIR}/*"]
    )
    
    if result.returncode != 0:
        print("Publishing failed.")
        sys.exit(1)
    
    print(f"Package {PACKAGE_NAME} version {version} published successfully to PyPI.")


def all_steps():
    """Run all build steps."""
    clean()
    run_tests()
    build()
    
    publish_prompt = input("Do you want to publish to PyPI? (y/n): ")
    if publish_prompt.lower() == "y":
        publish()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify a command: clean, test, build, publish, or all")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "clean":
        clean()
    elif command == "test":
        run_tests()
    elif command == "build":
        build()
    elif command == "publish":
        if not os.path.exists(BUILD_DIR):
            print("Build directory not found. Run 'build' first.")
            sys.exit(1)
        publish()
    elif command == "all":
        all_steps()
    else:
        print("Unknown command. Use: clean, test, build, publish, or all")
        sys.exit(1) 