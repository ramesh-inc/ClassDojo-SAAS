# ClassDojo system 

A comprehensive Django-based management system for preschools, featuring user management, class enrollment, attendance tracking, messaging, and learning progress monitoring.

## 🚀 Features

- **User Management**: Teachers, Parents, Admins with role-based access
- **Class Management**: Class creation, student enrollment, teacher assignments
- **Attendance Tracking**: Daily attendance with check-in/check-out times
- **Learning Progress**: Activity tracking and student progress records
- **Messaging System**: Secure communication between parents and teachers
- **News Feed**: Announcements, posts with attachments and engagement
- **Audit System**: Complete activity logging and download tracking

## 🛠️ Tech Stack

- **Backend**: Django 4.x
- **Database**: MySQL 8.0+ (SQLite for development)
- **Python**: 3.9+
- **Frontend**: Django Templates (extendable to React/Vue)

## 📋 Prerequisites

Before setting up the project, make sure you have:

- Python 3.9 or higher
- MySQL 8.0+ (for production) or SQLite (for development)
- Git
- pip (Python package manager)

## 🏗️ Development Environment Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/ClassDojo-Parent-Portal.git
cd ClassDojo-Parent-Portal
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

**If `requirements.txt` doesn't exist, install manually:**
```bash
pip install django>=4.2
pip install mysqlclient  # For MySQL support
# or
pip install PyMySQL     # Alternative MySQL driver
```

### Step 4: Database Configuration

#### Option A: SQLite (Recommended for Development)

SQLite is already configured by default. No additional setup needed.

#### Option B: MySQL (For Production/Advanced Development)

1. **Install MySQL** (if not already installed):
   ```bash
   # macOS (using Homebrew)
   brew install mysql
   brew services start mysql
   
   # Ubuntu/Debian
   sudo apt-get install mysql-server
   sudo systemctl start mysql
   
   # Windows
   # Download from https://dev.mysql.com/downloads/mysql/
   ```

2. **Create Database**:
   ```bash
   # Connect to MySQL
   mysql -u root -p
   
   # Create database
   CREATE DATABASE classdojo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   
   # Create user (optional)
   CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON classdojo_db.* TO 'django_user'@'localhost';
   FLUSH PRIVILEGES;
   
   EXIT;
   ```

3. **Update Database Settings**:
   
   Edit `classdojo_project/settings.py`:
   ```python
   # For MySQL
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'classdojo_db',
           'USER': 'django_user',  # or 'root'
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
           'OPTIONS': {
               'charset': 'utf8mb4',
               'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
           },
       }
   }
   ```

### Step 5: Environment Variables (Optional)

Create a `.env` file in the project root:

```bash
# .env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=classdojo_db
DB_USER=django_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

Update `settings.py` to use environment variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'your-fallback-secret-key')
```

## 🗄️ Database Setup and Migrations

### Step 1: Verify Project Configuration

```bash
# Check if Django can connect to database
python manage.py check

# Expected output: System check identified no issues (0 silenced).
```

### Step 2: Run Migrations

```bash
# Create migration files (if not already created)
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

### Step 3: Create Superuser

```bash
# Create admin user
python manage.py createsuperuser

# Follow prompts to enter:
# - Username
# - Email
# - Password
```

### Step 4: Load Sample Data (Optional)

```bash
# If you have fixtures/sample data
python manage.py loaddata sample_data.json

# Or create learning activities (already included in migrations)
# This is automatically done during migration 0010_populate_learning_activities
```

## 🏃‍♂️ Running the Development Server

```bash
# Start the development server
python manage.py runserver

# Server will start at http://127.0.0.1:8000/
# Admin panel available at http://127.0.0.1:8000/admin/
```

## 📂 Project Structure

```
ClassDojo-Parent-Portal/
├── classdojo_project/          # Main project settings
│   ├── __init__.py
│   ├── settings.py            # Django settings
│   ├── urls.py               # Main URL routing
│   └── wsgi.py              # WSGI application
├── core/                     # Main application
│   ├── migrations/          # Database migrations
│   ├── __init__.py
│   ├── admin.py            # Django admin configuration
│   ├── apps.py
│   ├── models.py           # Database models
│   ├── urls.py            # App URL routing
│   └── views.py           # View functions
├── static/                 # Static files (CSS, JS, images)
├── templates/             # HTML templates
├── media/                # User uploaded files
├── venv/                 # Virtual environment
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🗃️ Database Models

The system includes the following main models:

- **User**: Extended Django user with custom fields
- **Teacher, Parent, Admin**: Role-specific profiles
- **Class, Student**: Academic structure
- **Enrollment, Assignment**: Relationship management
- **Post, Message**: Communication features
- **Attendance, LearningActivity**: Tracking features
- **AuditLog**: Activity monitoring

## 🔧 Available Management Commands

```bash
# Database operations
python manage.py makemigrations            # Create new migrations
python manage.py migrate                   # Apply migrations
python manage.py showmigrations           # Show migration status
python manage.py sqlmigrate core 0001     # Show SQL for migration

# User management
python manage.py createsuperuser          # Create admin user
python manage.py changepassword username  # Change user password

# Development utilities
python manage.py runserver                # Start development server
python manage.py shell                   # Interactive Python shell
python manage.py check                   # Check for issues
python manage.py collectstatic           # Collect static files

# Data operations
python manage.py loaddata fixture.json   # Load data from fixture
python manage.py dumpdata core > data.json # Export data
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test core

# Run with coverage (if installed)
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Production Deployment

### Environment Variables for Production

```bash
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=production_db
DB_USER=production_user
DB_PASSWORD=secure_password
DB_HOST=db_server_host
DB_PORT=3306
```

### Basic Production Setup

```bash
# Install production dependencies
pip install gunicorn whitenoise

# Collect static files
python manage.py collectstatic --noinput

# Run with Gunicorn
gunicorn classdojo_project.wsgi:application --bind 0.0.0.0:8000
```

## 🔒 Security Considerations

- **Environment Variables**: Never commit sensitive data to Git
- **Secret Key**: Use a strong, unique secret key for production
- **Database**: Use strong passwords and limit user privileges
- **HTTPS**: Always use HTTPS in production
- **Static Files**: Use a CDN or proper static file serving

## 🐛 Troubleshooting

### Common Issues

1. **Migration Errors**:
   ```bash
   # Reset migrations (development only)
   rm core/migrations/0*.py
   python manage.py makemigrations core
   python manage.py migrate
   ```

2. **Database Connection Issues**:
   ```bash
   # Test database connection
   python manage.py dbshell
   
   # Check database settings
   python manage.py check --database default
   ```

3. **Static Files Not Loading**:
   ```bash
   # Collect static files
   python manage.py collectstatic
   
   # Check STATIC_URL and STATIC_ROOT in settings
   ```

4. **Permission Errors**:
   ```bash
   # Check file permissions
   chmod +x manage.py
   
   # Virtual environment activation issues
   source venv/bin/activate  # Ensure this works
   ```

### Getting Help

- Check Django documentation: https://docs.djangoproject.com/
- Project issues: Create an issue in the GitHub repository
- Django community: https://forum.djangoproject.com/

## 🤝 Contributing

1. Fork the repository (optional)
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
