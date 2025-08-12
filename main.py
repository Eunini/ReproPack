from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from datetime import datetime
from typing import List

from models import (
    CreatePackageRequest, 
    PackageResponse, 
    PackageListResponse, 
    PackageMetadata
)
from utils import (
    generate_package_id,
    create_package_archive,
    get_package_metadata_from_file,
    validate_pip_dependencies
)

# Initialize FastAPI app
app = FastAPI(
    title="ReproPack",
    description="Package software development environments for reproducible setups",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
PACKAGES_DIR = "packages"
os.makedirs(PACKAGES_DIR, exist_ok=True)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to ReproPack API",
        "description": "Package software development environments for reproducible setups",
        "version": "1.0.0",
        "endpoints": {
            "create_package": "POST /create-package",
            "download_package": "GET /download-package/{package_id}",
            "list_packages": "GET /list-packages"
        }
    }


@app.post("/create-package", response_model=PackageResponse)
async def create_package(request: CreatePackageRequest):
    """
    Create a new package with project dependencies, environment variables, 
    setup scripts, and optional dataset links.
    """
    try:
        # Validate dependencies format
        if request.dependencies:
            validation_errors = validate_pip_dependencies(request.dependencies)
            if validation_errors:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid dependency format: {'; '.join(validation_errors)}"
                )
        
        # Generate unique package ID
        package_id = generate_package_id()
        
        # Create package archive
        package_path, file_size = create_package_archive(request, package_id, PACKAGES_DIR)
        
        # Return response
        return PackageResponse(
            package_id=package_id,
            project_name=request.project_name,
            created_at=datetime.now(),
            file_path=package_path,
            file_size=file_size
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create package: {str(e)}")


@app.get("/download-package/{package_id}")
async def download_package(package_id: str):
    """
    Download a package file by package ID.
    """
    try:
        # Find package file by ID
        package_files = [f for f in os.listdir(PACKAGES_DIR) if package_id in f and f.endswith('.zip')]
        
        if not package_files:
            raise HTTPException(status_code=404, detail="Package not found")
        
        package_filename = package_files[0]
        package_path = os.path.join(PACKAGES_DIR, package_filename)
        
        if not os.path.exists(package_path):
            raise HTTPException(status_code=404, detail="Package file not found")
        
        return FileResponse(
            path=package_path,
            filename=package_filename,
            media_type='application/zip'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download package: {str(e)}")


@app.get("/list-packages", response_model=PackageListResponse)
async def list_packages():
    """
    List all created packages with metadata.
    """
    try:
        packages = []
        
        # Scan packages directory
        for filename in os.listdir(PACKAGES_DIR):
            if filename.endswith('.zip'):
                package_path = os.path.join(PACKAGES_DIR, filename)
                
                # Get file stats
                file_stats = os.stat(package_path)
                file_size = file_stats.st_size
                created_at = datetime.fromtimestamp(file_stats.st_ctime)
                
                # Try to get metadata from the package
                metadata = get_package_metadata_from_file(package_path)
                
                if metadata:
                    package_metadata = PackageMetadata(
                        package_id=metadata["package_id"],
                        project_name=metadata["project_name"],
                        author=metadata["author"],
                        description=metadata.get("description"),
                        created_at=datetime.fromisoformat(metadata["created_at"]),
                        dependencies_count=len(metadata.get("dependencies", [])),
                        file_size=file_size,
                        file_name=filename
                    )
                else:
                    # Fallback metadata extraction from filename
                    package_id = filename.replace('.zip', '').split('_')[-1]
                    project_name = filename.replace('.zip', '').replace(f'_{package_id}', '')
                    
                    package_metadata = PackageMetadata(
                        package_id=package_id,
                        project_name=project_name,
                        author="Unknown",
                        description="No metadata available",
                        created_at=created_at,
                        dependencies_count=0,
                        file_size=file_size,
                        file_name=filename
                    )
                
                packages.append(package_metadata)
        
        # Sort by creation date (newest first)
        packages.sort(key=lambda x: x.created_at, reverse=True)
        
        return PackageListResponse(
            packages=packages,
            total_count=len(packages)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list packages: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "packages_directory": PACKAGES_DIR,
        "packages_count": len([f for f in os.listdir(PACKAGES_DIR) if f.endswith('.zip')])
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
