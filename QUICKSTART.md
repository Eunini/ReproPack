# 🚀 ReproPack - Quick Start Guide

ReproPack is a FastAPI application that packages software development environments for reproducible setups.

## 📂 Project Structure
```
repropack/
├── main.py           # FastAPI application with all endpoints
├── models.py         # Pydantic models for validation
├── utils.py          # Helper functions for package creation
├── demo.py           # Demo script showing functionality
├── test_api.py       # Comprehensive API test suite
├── packages/         # Generated packages storage
├── requirements.txt  # Python dependencies
├── start_server.bat  # Windows script to start server
└── run_tests.bat     # Windows script to run tests
```

## 🛠️ Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
**Option A: Using uvicorn directly**
```bash
uvicorn main:app --reload
```

**Option B: Using the startup script (Windows)**
```bash
start_server.bat
```

### 3. Access the API
- **Interactive Documentation**: http://localhost:8000/docs
- **API Base URL**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

## 🔧 Core Features

### ✅ Implemented Features
- ✅ **POST /create-package** - Create reproducible packages
- ✅ **GET /download-package/{package_id}** - Download packages
- ✅ **GET /list-packages** - List all packages with metadata
- ✅ **Local storage** in `/packages` directory with UUID package IDs
- ✅ **Pydantic models** for request/response validation
- ✅ **Package compression** as ZIP files
- ✅ **metadata.json** inside each package with comprehensive details
- ✅ **Dependency validation** for pip freeze style formats

### 📦 Package Contents
Each generated package includes:
- **README.md** - Comprehensive setup instructions
- **requirements.txt** - Python dependencies in pip format
- **.env.example** - Environment variables template
- **setup.sh** - Automated setup script
- **metadata.json** - Complete package metadata

## 🧪 Testing

### Run Demo
```bash
python demo.py
```

### Run API Tests
```bash
python test_api.py
```

### Using the Batch Scripts (Windows)
```bash
run_tests.bat
```

## 📋 API Usage Examples

### Create a Package
```json
POST /create-package
{
  "project_name": "Data Science Project",
  "author": "Your Name",
  "description": "ML project with common libraries",
  "dependencies": [
    {"name": "pandas", "version": "2.0.0"},
    {"name": "numpy", "version": ">=1.21.0"}
  ],
  "environment_variables": {
    "API_KEY": "your-key-here",
    "DEBUG": "false"
  },
  "setup_scripts": [
    "mkdir data models",
    "pip install --upgrade pip"
  ],
  "dataset_links": [
    "https://example.com/dataset.csv"
  ],
  "instructions": "Run setup.sh after extraction"
}
```

### List Packages
```bash
GET /list-packages
```

### Download Package
```bash
GET /download-package/{package_id}
```

## 🔍 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/create-package` | POST | Create new package |
| `/download-package/{id}` | GET | Download package |
| `/list-packages` | GET | List all packages |

## 🛡️ Validation Features

- **Dependency Format**: Validates pip freeze style (package==version, package>=version)
- **Required Fields**: project_name and author are mandatory
- **File Safety**: Sanitizes project names for safe filenames
- **Error Handling**: Comprehensive error responses with details

## 🎯 Next Steps

1. **Start the server**: `uvicorn main:app --reload`
2. **Visit documentation**: http://localhost:8000/docs
3. **Create your first package** using the interactive API docs
4. **Download and test** the generated package
5. **Integrate with your CI/CD** pipeline for automated environment packaging

## 💡 Tips

- Use the interactive API documentation at `/docs` for easy testing
- Check the `/health` endpoint to monitor API status
- Generated packages are stored in the `packages/` directory
- Each package includes complete setup instructions in README.md
- Dependency validation helps catch common format errors

---

**Ready to package your development environment? Start the server and create your first ReproPack package! 🎉**
