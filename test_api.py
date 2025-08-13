"""
Test script for ReproPack API

This script demonstrates how to use the ReproPack API endpoints.
Run this after starting the FastAPI server with: uvicorn main:app --reload
"""

import requests
import json
import time
import os
from pathlib import Path
import pytest

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"Health check passed: {data['status']}")
            print(f"Packages count: {data['packages_count']}")
        else:
            print(f"Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Cannot connect to API. Make sure the server is running.")
        return False
    return True

def test_create_package():
    """Test creating a new package"""
    print("\nTesting package creation...")
    
    package_data = {
        "project_name": "Data Science Starter Kit",
        "author": "ReproPack Tester",
        "description": "A complete data science environment with common libraries",
        "dependencies": [
            {"name": "pandas", "version": "2.0.0"},
            {"name": "numpy", "version": "1.24.0"},
            {"name": "scikit-learn", "version": ">=1.3.0"},
            {"name": "matplotlib", "version": "3.7.0"},
            {"name": "jupyter", "version": ">=1.0.0"}
        ],
        "environment_variables": {
            "DATA_PATH": "/data",
            "MODEL_PATH": "/models",
            "DEBUG": "false",
            "API_KEY": "your-api-key-here"
        },
        "setup_scripts": [
            "mkdir -p data models notebooks",
            "pip install --upgrade pip",
            "jupyter notebook --generate-config"
        ],
        "dataset_links": [
            "https://archive.ics.uci.edu/ml/datasets/iris",
            "https://www.kaggle.com/datasets/holtskinner/ecommerce-data"
        ],
        "instructions": "After setup, run 'jupyter notebook' to start the development environment. Make sure to configure your API key in the .env file."
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/create-package",
            json=package_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f" Package created successfully!")
            print(f" Package ID: {data['package_id']}")
            print(f" Project Name: {data['project_name']}")
            print(f" File Size: {data['file_size']} bytes")
            return data['package_id']
        else:
            print(f" Package creation failed: {response.status_code}")
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f" Error creating package: {e}")
        return None

def test_list_packages():
    """Test listing all packages"""
    print("\nTesting package listing...")
    
    try:
        response = requests.get(f"{BASE_URL}/list-packages")
        
        if response.status_code == 200:
            data = response.json()
            print(f" Found {data['total_count']} packages:")
            
            for package in data['packages']:
                print(f"   {package['project_name']}")
                print(f"     ID: {package['package_id']}")
                print(f"     Author: {package['author']}")
                print(f"     Dependencies: {package['dependencies_count']}")
                print(f"     Size: {package['file_size']} bytes")
                print(f"     Created: {package['created_at']}")
                print()
        else:
            print(f" Package listing failed: {response.status_code}")
    except Exception as e:
        print(f"Error listing packages: {e}")

@pytest.mark.integration
def test_download_package():
    """Full cycle: create then download a package (requires running server)"""
    if not os.getenv("RUN_INTEGRATION"):
        pytest.skip("Set RUN_INTEGRATION=1 to run integration download test")

    # First create a package to ensure we have an ID
    package_data = {
        "project_name": "DownloadTestPkg",
        "author": "ReproPack Tester",
        "description": "Temp package for download test",
        "dependencies": [],
        "environment_variables": {},
        "setup_scripts": [],
        "dataset_links": [],
        "instructions": "None"
    }
    create_resp = requests.post(f"{BASE_URL}/create-package", json=package_data)
    assert create_resp.status_code == 200, f"Failed to create package: {create_resp.text}"
    pkg_id = create_resp.json()["package_id"]

    print(f"\n⬇ Testing package download for ID: {pkg_id}")
    resp = requests.get(f"{BASE_URL}/download-package/{pkg_id}")
    assert resp.status_code == 200, f"Download failed: {resp.status_code} {resp.text}"
    filename = f"test_download_{pkg_id[:8]}.zip"
    with open(filename, 'wb') as f:
        f.write(resp.content)
    try:
        file_size = len(resp.content)
        assert file_size > 0
    finally:
        Path(filename).unlink(missing_ok=True)

def test_invalid_package():
    """Test creating a package with invalid data"""
    print("\n Testing invalid package creation...")
    
    invalid_data = {
        "project_name": "Invalid Package",
        "author": "Tester",
        "dependencies": [
            {"name": "", "version": "1.0.0"},  # Invalid: empty name
            {"name": "valid-package", "version": ""},  # Invalid: empty version
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/create-package",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            print(" Invalid package correctly rejected")
            print(f"Error message: {response.json().get('detail', 'No details')}")
        else:
            print(f"Expected 400 error, got: {response.status_code}")
    except Exception as e:
        print(f"Error testing invalid package: {e}")

def main():
    """Run all tests"""
    print(" Starting ReproPack API Tests")
    print("=" * 50)
    
    # Test health check first
    if not test_health_check():
        print("Cannot proceed with tests - API is not available")
        return
    
    # Test package creation
    package_id = test_create_package()
    
    # Wait a moment for package to be fully created
    time.sleep(1)
    
    # Test package listing
    test_list_packages()
    
    # Test package download
    test_download_package(package_id)
    
    # Test invalid package creation
    test_invalid_package()
    
    print("\n✨ All tests completed!")
    print("\n💡 Tips:")
    print("- Visit http://localhost:8000/docs for interactive API documentation")
    print("- Check the 'packages/' directory for generated package files")
    print("- Use the /health endpoint to monitor API status")

if __name__ == "__main__":
    main()
