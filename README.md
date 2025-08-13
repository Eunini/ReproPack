# ReproPack

Full‑stack (FastAPI + Next.js) tool for packaging software development environments so any teammate can reproduce an identical setup quickly.

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
ReproPack/
├── main.py                  # FastAPI application
├── models.py                # Pydantic models
├── utils.py                 # Packaging helpers
├── packages/                # Generated ZIP artifacts
├── test_api.py              # Stand‑alone demo/integration script (optional)
├── tests/                   # Pytest suite (unit / fast integration)
│   └── test_app.py
├── requirements.txt         # Backend deps (FastAPI, httpx, etc.)
├── start_server.bat         # Windows helper to run backend
├── run_tests.bat            # Windows helper to run legacy demo tests
└── frontend/                # Next.js 15 + Tailwind CSS 4 UI
  ├── src/app/             # App router pages
  ├── src/components/      # UI components
  ├── src/hooks/           # Custom hooks (scroll animations, etc.)
  └── tailwind.config.ts   # Tailwind v4 config
```

## Quick Start (Backend + Frontend)

### 1. Python backend
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Visit http://localhost:8000/docs

### 2. Frontend (Next.js)
```powershell
cd frontend
npm install
npm run dev
```
Visit http://localhost:3000

The frontend expects the API at http://localhost:8000 (adjust via environment variable if deploying separately).

## Backend Only (Alternate Minimal Setup)
```powershell
pip install -r requirements.txt
uvicorn main:app --reload
```
Docs: http://localhost:8000/docs

## API Endpoints (Backend)

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

## Usage Example (cURL)

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

## Testing

We provide two styles:

| Type | Command | Notes |
|------|---------|-------|
| Unit / fast API tests | `pytest -q` | Uses `tests/` with FastAPI TestClient (no external server needed). |
| Optional full download cycle | `set RUN_INTEGRATION=1` then `pytest -q` | Runs marked `@pytest.mark.integration` test in `test_api.py`. |
| Legacy demo script | `python test_api.py` | Requires the server running at localhost:8000. |

PowerShell examples:
```powershell
.venv\Scripts\activate
pytest -q              # fast suite
$env:RUN_INTEGRATION=1
pytest -q              # include integration download test
```

## Development

To extend ReproPack:

1. **Add new package formats**: Modify `utils.py` to support .tar.gz or other formats
2. **Add validation**: Extend dependency validation in `utils.py`
3. **Add metadata**: Extend the `CreatePackageRequest` model in `models.py`
4. **Add endpoints**: Add new endpoints in `main.py`

## Frontend Styling Notes

The UI uses Tailwind CSS v4 (`@import "tailwindcss";`) plus custom CSS variables for theme colors and scroll-triggered animations (IntersectionObserver). Gradient text utilities and animated sections appear as you scroll.

## Health Check

The API includes a health check endpoint:

```bash
curl -X GET "http://localhost:8000/health"
```

Returns application status and package count.

## Deployment Overview

Recommended split deployment:

| Layer | Option | Notes |
|-------|--------|-------|
| Backend | Railway / Render / Fly.io | Simple container or `uvicorn` deploy, mount persistent storage for `packages/`. |
| Frontend | Vercel | Build Next.js; set `NEXT_PUBLIC_API_BASE` to backend URL. |
| Alt (all-in-one) | Docker Compose on VPS | Reverse proxy (Nginx) + separate services. |

Environment variables (suggested for production):
| Name | Purpose |
|------|---------|
| REPROPACK_PACKAGES_DIR | Override `packages` directory path (default: packages). |
| REPROPACK_CORS_ORIGINS | Comma list of allowed origins or * for all. |
| NEXT_PUBLIC_API_BASE | Frontend API base URL. |

### Basic Dockerfile Sketch (not yet added)
```Dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Add a separate Dockerfile in `frontend/` for the Next.js build if containerizing both.

### Deploying Backend to Railway (Step-by-Step)

1. Create (or sign in to) a Railway account: https://railway.app
2. New Project → Deploy from GitHub (or Upload repo). Ensure this repository is pushed to GitHub.
3. Select the repository containing `main.py` and `Procfile`.
4. Railway will auto-detect Python because of `requirements.txt`.
5. Verify the build & start command:
  - Railway will use `pip install -r requirements.txt` then start via the `Procfile` line: `web: uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}`.
6. Set Environment Variables in the service Settings:
  - `REPROPACK_CORS_ORIGINS` = `https://your-frontend-domain.vercel.app`
  - (Optional) `REPROPACK_PACKAGES_DIR` = `/data/packages` (create a volume below)
7. (Optional persistence) Add a Volume:
  - In Railway service → Storage → Add Volume
  - Mount path: `/data`
  - Then set `REPROPACK_PACKAGES_DIR=/data/packages`
8. Deploy: The first deploy starts automatically. Watch logs; you should see Uvicorn listening on the assigned `$PORT`.
9. Copy the public domain from the Railway service (e.g. `https://repropack-production.up.railway.app`).
10. Frontend: In Vercel, set `NEXT_PUBLIC_API_BASE` (or `NEXT_PUBLIC_API_URL` if you retain that name) to the Railway URL (no trailing slash).
11. Redeploy frontend so it picks up the new API base.

Health check URL to test after deploy:
```
curl -s https://<your-railway-domain>/health | jq
```

If you get CORS errors in the browser, confirm `REPROPACK_CORS_ORIGINS` includes your exact Vercel domain (https scheme, no trailing slash). For local testing, you can temporarily set it to `*`.

#### Common Railway Troubleshooting
| Symptom | Cause | Fix |
|--------|-------|-----|
| 404 at root | Wrong service path or deploy failing | Check logs for import errors. |
| 500 on create-package | Missing write perms to dir | Ensure `REPROPACK_PACKAGES_DIR` exists and is writable (volume mounted). |
| CORS blocked | Origin not allowed | Update `REPROPACK_CORS_ORIGINS`. |
| Packages lost after redeploy | Using ephemeral filesystem | Add persistent volume and point `REPROPACK_PACKAGES_DIR` to it. |

#### Minimal Environment Variable Matrix
| Scenario | REPROPACK_CORS_ORIGINS | REPROPACK_PACKAGES_DIR |
|----------|------------------------|------------------------|
| Local dev only | * | packages |
| Prod w/ volume | https://your-frontend.vercel.app | /data/packages |
| Staging | https://staging-frontend.vercel.app | /data/packages |

## Roadmap Ideas
- Optional S3/Blob storage backend for packages
- Auth & API keys
- Package signatures / integrity verification
- GitHub Actions CI (pytest + build)

## License

MIT
