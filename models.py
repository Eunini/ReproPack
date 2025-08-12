from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class DependencyModel(BaseModel):
    """Model for project dependencies following pip freeze style"""
    name: str = Field(..., description="Package name")
    version: str = Field(..., description="Package version (e.g., '1.0.0', '>=1.0.0')")
    
    def to_pip_format(self) -> str:
        """Convert to pip freeze format"""
        return f"{self.name}=={self.version}" if "==" not in self.version else f"{self.name}{self.version}"


class CreatePackageRequest(BaseModel):
    """Request model for creating a new package"""
    project_name: str = Field(..., description="Name of the project")
    author: str = Field(..., description="Author of the project")
    description: Optional[str] = Field(None, description="Project description")
    dependencies: List[DependencyModel] = Field(default_factory=list, description="Project dependencies")
    environment_variables: Dict[str, str] = Field(default_factory=dict, description="Required environment variables")
    setup_scripts: List[str] = Field(default_factory=list, description="Setup scripts to run")
    dataset_links: List[str] = Field(default_factory=list, description="Optional dataset download links")
    instructions: Optional[str] = Field(None, description="Additional setup instructions")


class PackageResponse(BaseModel):
    """Response model for package creation"""
    package_id: str = Field(..., description="Unique package identifier")
    project_name: str = Field(..., description="Name of the project")
    created_at: datetime = Field(..., description="Package creation timestamp")
    file_path: str = Field(..., description="Path to the package file")
    file_size: int = Field(..., description="Size of the package file in bytes")


class PackageMetadata(BaseModel):
    """Model for package metadata"""
    package_id: str = Field(..., description="Unique package identifier")
    project_name: str = Field(..., description="Name of the project")
    author: str = Field(..., description="Author of the project")
    description: Optional[str] = Field(None, description="Project description")
    created_at: datetime = Field(..., description="Package creation timestamp")
    dependencies_count: int = Field(..., description="Number of dependencies")
    file_size: int = Field(..., description="Size of the package file in bytes")
    file_name: str = Field(..., description="Name of the package file")


class PackageListResponse(BaseModel):
    """Response model for listing packages"""
    packages: List[PackageMetadata] = Field(..., description="List of package metadata")
    total_count: int = Field(..., description="Total number of packages")
