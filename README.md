# Pithak Chhorn Portfolio - Backend API

A FastAPI-based backend for the Pithak Chhorn portfolio website. This backend provides authentication, blog posts management, and certificate handling with file upload capabilities.

## Features

- ✅ JWT Authentication for admin access
- ✅ Blog Posts CRUD operations (public read, admin write)
- ✅ Certificates management with image upload (full CRUD)
- ✅ File storage and static file serving
- ✅ CORS enabled for React frontend
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Auto-generated API documentation (Swagger UI & ReDoc)

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Validation**: Pydantic
- **File Upload**: Multipart form data
- **Password Hashing**: SHA256 (with bcrypt fallback)

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   ├── deps.py              # Dependencies (get_db, current_user)
│   ├── routers/             # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   ├── posts.py         # Blog posts routes
│   │   └── certificates.py  # Certificates routes (full CRUD)
│   └── uploads/             # Uploaded files storage
│       ├── posts/           # Post images
│       └── certificates/    # Certificate images
├── requirements.txt         # Python dependencies
├── portfolio.db            # SQLite database (auto-created)
└── README.md              # This file
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login with username/password, returns JWT token

### Posts (Blog)
- `GET /api/posts` - Get all posts (public)
- `GET /api/posts/{id}` - Get single post (public)
- `POST /api/posts` - Create new post (admin only)
- `PUT /api/posts/{id}` - Update post (admin only)
- `DELETE /api/posts/{id}` - Delete post (admin only)

### Certificates (Full CRUD)
- `GET /api/certificates` - Get all certificates (public)
- `GET /api/certificates/{id}` - Get single certificate (public)
- `POST /api/certificates` - Upload new certificate with image (admin only)
- `PUT /api/certificates/{id}` - Update certificate (with image) (admin only)
- `PATCH /api/certificates/{id}` - Partial update certificate (admin only)
- `DELETE /api/certificates/{id}` - Delete certificate (admin only)

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Clone and Setup
```bash
# Navigate to project directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run the Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at: `http://localhost:8000`

### Step 3: Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Default Admin Credentials
- **Username**: `admin`
- **Password**: `admin123`

**⚠️ Important**: Change the default password immediately after first login in production!

## Complete API Testing Guide

### 1. Get JWT Token (Login)
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123&grant_type=password"
```

### 2. Posts Management

#### Create Post (with optional image)
```bash
# Without image
curl -X POST "http://localhost:8000/api/posts" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is my first blog post...",
    "tags": "webdev,fastapi",
    "category": "Tutorial"
  }'

# With image upload
curl -X POST "http://localhost:8000/api/posts" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "title=Post with Image" \
  -F "content=Content with image" \
  -F "tags=image,upload" \
  -F "category=Demo" \
  -F "image=@/path/to/image.jpg"
```

#### Get All Posts (Public)
```bash
curl -X GET "http://localhost:8000/api/posts"

# With pagination
curl -X GET "http://localhost:8000/api/posts?skip=0&limit=10"

# Filter by category
curl -X GET "http://localhost:8000/api/posts?category=Tutorial"
```

#### Get Single Post
```bash
curl -X GET "http://localhost:8000/api/posts/1"
```

#### Update Post
```bash
# Partial update
curl -X PUT "http://localhost:8000/api/posts/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'

# Full update
curl -X PUT "http://localhost:8000/api/posts/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete Update",
    "content": "Updated content...",
    "tags": "updated,fastapi",
    "category": "Updated"
  }'
```

#### Delete Post
```bash
curl -X DELETE "http://localhost:8000/api/posts/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 3. Certificates Management (Full CRUD)

#### Create Certificate (with image)
```bash
curl -X POST "http://localhost:8000/api/certificates" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "title=Full Stack Developer Certificate" \
  -F "issuer=Coursera" \
  -F "date=January 2024" \
  -F "image=@/path/to/certificate.jpg"
```

#### Get All Certificates
```bash
curl -X GET "http://localhost:8000/api/certificates"

# With pagination
curl -X GET "http://localhost:8000/api/certificates?skip=0&limit=10"
```

#### Get Single Certificate
```bash
curl -X GET "http://localhost:8000/api/certificates/1"
```

#### Update Certificate
```bash
# Update without changing image
curl -X PUT "http://localhost:8000/api/certificates/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "title=Updated Certificate Title" \
  -F "issuer=Updated Issuer" \
  -F "date=February 2024"

# Update with new image
curl -X PUT "http://localhost:8000/api/certificates/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "title=Updated Title" \
  -F "issuer=Updated Issuer" \
  -F "date=2024-02-01" \
  -F "image=@/path/to/new/image.jpg"
```

#### Partial Update Certificate (JSON only)
```bash
curl -X PATCH "http://localhost:8000/api/certificates/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Only Update Title"}'
```

#### Delete Certificate
```bash
curl -X DELETE "http://localhost:8000/api/certificates/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 4. Health Check
```bash
curl -X GET "http://localhost:8000/api/health"
```

## File Upload Details

### Supported File Types
- Images: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- Documents: `.pdf`

### Storage Locations
- Post images: `backend/app/uploads/posts/`
- Certificate images: `backend/app/uploads/certificates/`

### Access Uploaded Files
Uploaded files are served statically at:
- `http://localhost:8000/static/posts/filename.jpg`
- `http://localhost:8000/static/certificates/filename.pdf`

### File Naming Strategy
Files are automatically renamed with unique names to prevent conflicts:
- Format: `{random_hex}_{title_slug}{extension}`
- Example: `a1b2c3d4_full_stack_certificate.jpg`

## Database Schema

### Users Table
- `id` (Integer, Primary Key)
- `username` (String, Unique)
- `hashed_password` (String)
- `is_active` (Boolean)
- `created_at` (DateTime)

### Posts Table
- `id` (Integer, Primary Key)
- `title` (String)
- `content` (Text)
- `tags` (String, comma-separated)
- `category` (String)
- `image_url` (String, nullable)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Certificates Table
- `id` (Integer, Primary Key)
- `title` (String)
- `issuer` (String)
- `date` (String)
- `image_url` (String)
- `created_at` (DateTime)

## Authentication Flow

1. **Login**: POST `/api/auth/login` with username/password
2. **Get Token**: Receive JWT token in response
3. **Use Token**: Include in Authorization header: `Bearer {token}`
4. **Access Protected Routes**: Token validates admin privileges

## PowerShell Testing Script

Create `test_api.ps1`:
```powershell
Write-Host "=== Testing Portfolio API ===" -ForegroundColor Cyan

# Login
$response = curl -s -X POST "http://localhost:8000/api/auth/login" -d "username=admin&password=admin123"
$token = ($response | ConvertFrom-Json).access_token
Write-Host "Token: $($token.Substring(0,20))..." -ForegroundColor Green

# Create post
curl -X POST "http://localhost:8000/api/posts" `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d '{"title":"Test Post","content":"Content","tags":"test","category":"Test"}'

# Get posts
curl -X GET "http://localhost:8000/api/posts"

# Create certificate (with test file)
"Test certificate" | Out-File test_cert.txt
curl -X POST "http://localhost:8000/api/certificates" `
  -H "Authorization: Bearer $token" `
  -F "title=Test Cert" -F "issuer=Test" -F "date=2024" -F "image=@test_cert.txt"

# Get certificates
curl -X GET "http://localhost:8000/api/certificates"
```

## Environment Configuration

Create `.env` file for production:
```env
SECRET_KEY=your-secure-random-secret-key-here
DATABASE_URL=sqlite:///./portfolio.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
UPLOAD_MAX_SIZE=10485760  # 10MB
```

## Production Deployment

### 1. Security Hardening
```python
# Update auth.py for production
import os
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
```

### 2. Database Migration (for production)
```python
# Consider using Alembic for migrations
# pip install alembic
# alembic init migrations
```

### 3. File Storage Optimization
- Use cloud storage (AWS S3, Cloudinary) for production
- Implement CDN for static files
- Add file compression
- Set up backup strategy

### 4. Monitoring & Logging
- Add structured logging
- Implement error tracking (Sentry)
- Set up health checks
- Monitor API performance

## Common Operations

### Reset Everything
```bash
# Delete database and uploaded files
rm portfolio.db
rm -rf app/uploads/*

# Restart server
uvicorn app.main:app --reload
```

### Backup Database
```bash
# Copy SQLite database
cp portfolio.db portfolio_backup_$(date +%Y%m%d).db
```

### Export Data
```bash
# Export posts to JSON
sqlite3 portfolio.db -json "SELECT * FROM posts;" > posts_export.json
```

## Troubleshooting Guide

### Error: "401 Unauthorized"
```bash
# Check if token is valid
curl -X POST "http://localhost:8000/api/auth/login" -d "username=admin&password=admin123"

# Verify token format in headers
# Should be: Authorization: Bearer eyJhbGciOiJ...
```

### Error: "422 Validation Error"
- Check required fields are provided
- Verify data types match schema
- Ensure file extensions are supported

### Error: "500 Internal Server Error"
```bash
# Check server logs
# Verify upload directories exist
# Check file permissions
```

### Database Issues
```bash
# Reset database
rm portfolio.db
uvicorn app.main:app --reload

# Check database schema
sqlite3 portfolio.db ".schema"
```

## Frontend Integration Examples

### React with Fetch API
```javascript
// Configuration
const API_BASE = 'http://localhost:8000/api';
let authToken = null;

// Login function
const login = async (username, password) => {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);
  formData.append('grant_type', 'password');
  
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData
  });
  
  const data = await response.json();
  authToken = data.access_token;
  return data;
};

// Get all posts
const getPosts = async () => {
  const response = await fetch(`${API_BASE}/posts`);
  return await response.json();
};

// Create post
const createPost = async (postData) => {
  const response = await fetch(`${API_BASE}/posts`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${authToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(postData)
  });
  return await response.json();
};

// Upload certificate
const uploadCertificate = async (formData) => {
  const response = await fetch(`${API_BASE}/certificates`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${authToken}`
    },
    body: formData
  });
  return await response.json();
};
```

## API Response Examples

### Successful Login
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Post Response
```json
{
  "id": 1,
  "title": "My First Post",
  "content": "Post content...",
  "tags": "webdev,fastapi",
  "category": "Tutorial",
  "image_url": "/static/posts/image.jpg",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Certificate Response
```json
{
  "id": 1,
  "title": "Full Stack Certificate",
  "issuer": "Coursera",
  "date": "January 2024",
  "image_url": "/static/certificates/a1b2c3d4_cert.jpg",
  "created_at": "2024-01-15T10:30:00Z"
}
```

## Performance Tips

1. **Database Indexing**: Add indexes for frequently queried fields
2. **Pagination**: Always use skip/limit for list endpoints
3. **File Optimization**: Compress images before upload
4. **Caching**: Implement Redis for frequent queries
5. **Connection Pooling**: Configure SQLAlchemy connection pool

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Submit pull request with description

## License

This project is created for portfolio purposes. Feel free to use and modify as needed.

## Support

For issues or questions:
1. Check the troubleshooting guide
2. Review API documentation at `/docs`
3. Test with curl commands provided

---

**Backend API Ready for Production!** 🚀

*Last Updated: January 2024*# Portfolio_learn_2025-backend_v2
