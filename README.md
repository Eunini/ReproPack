# ReproPack

A FastAPI application for packaging software development environments to ensure reproducible setups across different machines and developers.

## Overview

ReproPack allows developers to package their project dependencies, environment variables, setup scripts, and dataset links into a compressed archive that other developers can use to reproduce the exact same development environment.

## Features

- **Package Creation**: Create packages with dependencies, environment variables, and setup scripts
- **Package Download**: Download packaged environments as ZIP files
- **Package Listing**: View all created packages with metadata
- **Dependency Validation**: Validates pip freeze style dependency formats
- **Metadata Storage**: Stores comprehensive metadata within each package

## Project Structure

```
repropack/
├── main.py           # FastAPI application and endpoints
├── models.py         # Pydantic models for request/response validation
├── utils.py          # Helper functions for package creation
├── packages/         # Directory storing generated packages
└── requirements.txt  # Python dependencies
```

## Installation & Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```

3. **Access the API**:
   - API Documentation: http://localhost:8000/docs
   - API Base URL: http://localhost:8000

## API Endpoints

### POST /create-package

Create a new reproducible package.

**Request Body**:
```json
{
  "project_name": "My Awesome Project",
  "author": "John Doe",
  "description": "A sample project with dependencies",
  "dependencies": [
    {
      "name": "numpy",
      "version": "1.21.0"
    },
    {
      "name": "pandas",
      "version": ">=1.3.0"
    }
  ],
  "environment_variables": {
    "API_KEY": "your-api-key-here",
    "DEBUG": "true"
  },
  "setup_scripts": [
    "mkdir data",
    "chmod +x scripts/setup.sh"
  ],
  "dataset_links": [
    "https://example.com/dataset1.csv",
    "https://example.com/dataset2.json"
  ],
  "instructions": "Make sure to set up your API key before running the application."
}
```

**Response**:
```json
{
  "package_id": "550e8400-e29b-41d4-a716-446655440000",
  "project_name": "My Awesome Project",
  "created_at": "2025-08-12T10:30:00.000Z",
  "file_path": "packages/My_Awesome_Project_550e8400-e29b-41d4-a716-446655440000.zip",
  "file_size": 2048
}
```

### GET /download-package/{package_id}

Download a package file by its ID.

**Parameters**:
- `package_id`: UUID of the package to download

**Response**: ZIP file download

### GET /list-packages

List all created packages with metadata.

**Response**:
```json
{
  "packages": [
    {
      "package_id": "550e8400-e29b-41d4-a716-446655440000",
      "project_name": "My Awesome Project",
      "author": "John Doe",
      "description": "A sample project with dependencies",
      "created_at": "2025-08-12T10:30:00.000Z",
      "dependencies_count": 2,
      "file_size": 2048,
      "file_name": "My_Awesome_Project_550e8400-e29b-41d4-a716-446655440000.zip"
    }
  ],
  "total_count": 1
}
```

## Package Contents

Each generated package contains:

- **README.md**: Comprehensive setup instructions
- **requirements.txt**: Python dependencies in pip freeze format
- **.env.example**: Environment variables template
- **setup.sh**: Automated setup script
- **metadata.json**: Package metadata and configuration

## Usage Example

1. **Create a package**:
   ```bash
   curl -X POST "http://localhost:8000/create-package" \
        -H "Content-Type: application/json" \
        -d '{
          "project_name": "Data Science Project",
          "author": "Data Scientist",
          "dependencies": [
            {"name": "pandas", "version": "1.5.0"},
            {"name": "numpy", "version": "1.21.0"}
          ],
          "environment_variables": {
            "DATA_PATH": "/path/to/data"
          }
        }'
   ```

2. **List packages**:
   ```bash
   curl -X GET "http://localhost:8000/list-packages"
   ```

3. **Download a package**:
   ```bash
   curl -X GET "http://localhost:8000/download-package/{package_id}" \
        -o package.zip
   ```

## Dependency Validation

ReproPack validates that dependencies follow pip freeze style format:
- Package names must be alphanumeric (with hyphens, underscores, dots allowed)
- Versions must include version operators (==, >=, <=, ~=, !=) or be exact versions
- Invalid formats will return a 400 error with details

## Error Handling

The API provides comprehensive error handling:
- **400 Bad Request**: Invalid input data or dependency format
- **404 Not Found**: Package not found
- **500 Internal Server Error**: Server-side errors

## Development

To extend ReproPack:

1. **Add new package formats**: Modify `utils.py` to support .tar.gz or other formats
2. **Add validation**: Extend dependency validation in `utils.py`
3. **Add metadata**: Extend the `CreatePackageRequest` model in `models.py`
4. **Add endpoints**: Add new endpoints in `main.py`

## Health Check

The API includes a health check endpoint:

```bash
curl -X GET "http://localhost:8000/health"
```

Returns application status and package count.

## License

This project is open source and available under the MIT License.
