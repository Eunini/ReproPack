"""
Simple demo script for ReproPack API
"""

import json
import uuid
from datetime import datetime
from models import CreatePackageRequest, DependencyModel
from utils import create_package_archive

def demo_package_creation():
    """Create a demo package without API calls"""
    print("ReproPack Demo - Creating a sample package")
    print("=" * 50)
    
    # Create sample request data
    sample_dependencies = [
        DependencyModel(name="numpy", version="1.21.0"),
        DependencyModel(name="pandas", version=">=1.3.0"),
        DependencyModel(name="scikit-learn", version="1.0.2"),
        DependencyModel(name="matplotlib", version=">=3.5.0")
    ]
    
    sample_request = CreatePackageRequest(
        project_name="Data Science Starter Kit",
        author="ReproPack Demo",
        description="A complete data science environment with essential libraries for machine learning and data analysis",
        dependencies=sample_dependencies,
        environment_variables={
            "DATA_PATH": "/data",
            "MODEL_PATH": "/models", 
            "API_KEY": "your-api-key-here",
            "DEBUG": "false"
        },
        setup_scripts=[
            "mkdir -p data models notebooks",
            "pip install --upgrade pip",
            "jupyter notebook --generate-config",
            "echo 'Environment setup complete!'"
        ],
        dataset_links=[
            "https://archive.ics.uci.edu/ml/datasets/iris",
            "https://www.kaggle.com/datasets/titanic"
        ],
        instructions="After running setup.sh, start Jupyter with 'jupyter notebook' and begin your data science project!"
    )
    
    # Generate package
    package_id = str(uuid.uuid4())
    packages_dir = "packages"
    
    try:
        package_path, file_size = create_package_archive(sample_request, package_id, packages_dir)
        
        print(f"✅ Package created successfully!")
        print(f"📋 Package ID: {package_id}")
        print(f"📝 Project Name: {sample_request.project_name}")
        print(f"👤 Author: {sample_request.author}")
        print(f"📊 Dependencies: {len(sample_request.dependencies)} packages")
        print(f"🔧 Environment Variables: {len(sample_request.environment_variables)} variables")
        print(f"📜 Setup Scripts: {len(sample_request.setup_scripts)} scripts")
        print(f"🔗 Dataset Links: {len(sample_request.dataset_links)} links")
        print(f"📄 Package File: {package_path}")
        print(f"📊 File Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
        print(f"\n📦 Package Contents:")
        print("   - README.md (setup instructions)")
        print("   - requirements.txt (Python dependencies)")
        print("   - .env.example (environment variables template)")
        print("   - setup.sh (automated setup script)")
        print("   - metadata.json (package metadata)")
        
        return package_id
        
    except Exception as e:
        print(f"❌ Error creating package: {e}")
        return None

def demo_dependency_validation():
    """Demonstrate dependency validation"""
    print(f"\n🔍 Dependency Validation Demo")
    print("-" * 30)
    
    from utils import validate_pip_dependencies
    
    # Valid dependencies
    valid_deps = [
        DependencyModel(name="numpy", version="1.21.0"),
        DependencyModel(name="pandas", version=">=1.3.0"),
        DependencyModel(name="scikit-learn", version="==1.0.2")
    ]
    
    # Invalid dependencies
    invalid_deps = [
        DependencyModel(name="", version="1.0.0"),  # Empty name
        DependencyModel(name="valid-package", version=""),  # Empty version
    ]
    
    print("✅ Valid dependencies:")
    for dep in valid_deps:
        print(f"   - {dep.to_pip_format()}")
    
    valid_errors = validate_pip_dependencies(valid_deps)
    print(f"   Validation errors: {len(valid_errors)}")
    
    print(f"\n❌ Invalid dependencies:")
    for dep in invalid_deps:
        print(f"   - {dep.name or '[empty]'} {dep.version or '[empty]'}")
    
    invalid_errors = validate_pip_dependencies(invalid_deps)
    print(f"   Validation errors: {len(invalid_errors)}")
    for error in invalid_errors:
        print(f"     • {error}")

if __name__ == "__main__":
    # Run the demo
    package_id = demo_package_creation()
    demo_dependency_validation()
    
    print(f"\n💡 Next Steps:")
    print("1. Start the API server: uvicorn main:app --reload")
    print("2. Visit http://localhost:8000/docs for interactive API documentation")
    print("3. Use the API endpoints to create, list, and download packages")
    print("4. Run test_api.py for comprehensive API testing")
    
    if package_id:
        print(f"\n🎉 Demo package created with ID: {package_id[:8]}...")
        print("   Check the packages/ directory for the generated ZIP file!")
