# ClassDojo Parent Portal

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

- **Backend**: Django 5.x
- **Database**: MySQL 8.0+ (SQLite for development)
- **Python**: 3.9+
- **Frontend**: Django Templates with Bootstrap 5
- **CSS Framework**: Bootstrap 5 + Custom CSS

## 📋 Prerequisites

Before setting up the project, make sure you have:

- **macOS**: macOS 10.15+ (for Homebrew compatibility)
- **Python**: 3.9 or higher
- **MySQL**: 8.0+ (for production) or SQLite (for development)
- **Git**: Version control
- **Homebrew**: Package manager for macOS

## 🍺 Initial Setup for macOS (Homebrew Installation)

### Step 1: Install Homebrew

If you don't have Homebrew installed:

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Follow the instructions to add Homebrew to your PATH
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

# Verify installation
brew --version
```

### Step 2: Install System Dependencies

```bash
# Install Python (if not already installed)
brew install python

# Install MySQL
brew install mysql

# Install pkg-config (required for mysqlclient)
brew install pkg-config

# Install Git (if not already installed)
brew install git

# Start MySQL service
brew services start mysql

# Secure MySQL installation (recommended)
mysql_secure_installation
```

### Step 3: Verify Installations

```bash
# Check Python version (should be 3.9+)
python3 --version

# Check MySQL
mysql --version

# Check Git
git --version

# Check pkg-config
pkg-config --version
```

## 🏗️ Development Environment Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/ClassDojo-Parent-Portal.git
cd ClassDojo-Parent-Portal
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (you should see (venv) in your prompt)
which python
```

### Step 3: Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install django>=5.0 mysqlclient python-dotenv

# If mysqlclient fails, you can use PyMySQL as alternative:
# pip install django>=5.0 PyMySQL python-dotenv
```

**Create requirements.txt for future use:**
```bash
# Generate requirements file
pip freeze > requirements.txt
```

### Step 4: Database Configuration

#### Option A: SQLite (Recommended for Development)

SQLite is already configured by default. No additional setup needed.

#### Option B: MySQL (For Production/Advanced Development)

1. **Create Database**:
   ```bash
   # Connect to MySQL
   mysql -u root -p
   
   # Create database
   CREATE DATABASE classdojo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   
   # Create user (optional but recommended)
   CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'your_secure_password';
   GRANT ALL PRIVILEGES ON classdojo_db.* TO 'django_user'@'localhost';
   FLUSH PRIVILEGES;
   
   EXIT;
   ```

2. **Test Database Connection**:
   ```bash
   # Test connection
   mysql -u django_user -p classdojo_db
   ```

### Step 5: Environment Configuration

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env
```

Add the following content to `.env`:

```bash
# Database Configuration
MYSQL_USER=django_user
MYSQL_PASSWORD=your_secure_password
MYSQL_DATABASE=classdojo_db
MYSQL_HOST=localhost
MYSQL_PORT=3306

# Django Configuration
DEBUG=True
SECRET_KEY=django-insecure-8k2m9n#x7v$q@w3e4r5t6y7u8i9o0p-a1s2d3f4g5h6j7k8l9

# Email Configuration (Optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Time Zone
TIME_ZONE=Asia/Colombo
```

**⚠️ Security Note**: Never commit `.env` to version control:
```bash
echo ".env" >> .gitignore
```

## 🏗️ Django Project Setup

### Step 1: Create Django Project Structure

```bash
# Create Django project
django-admin startproject classdojo_project .

# Create core app
python manage.py startapp core

# Create necessary directories
mkdir -p templates/core templates/registration static/css static/js media
```

### Step 2: Configure Django Settings

Update `classdojo_project/settings.py` to include:

- Environment variables loading
- Database configuration
- Static files configuration
- Template settings
- Installed apps (add 'core')

### Step 3: Create Database Tables

```bash
# Check project configuration
python manage.py check

# Create migration files
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

### Step 4: Create Superuser

```bash
# Create admin user
python manage.py createsuperuser

# Follow prompts to enter:
# - Username
# - Email
# - Password
```

### Step 5: Collect Static Files

```bash
# Collect static files
python manage.py collectstatic
```

## 🏃‍♂️ Running the Development Server

```bash
# Ensure virtual environment is activated
source venv/bin/activate

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
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── core/                     # Main application
│   ├── migrations/          # Database migrations
│   ├── __init__.py
│   ├── admin.py            # Django admin configuration
│   ├── apps.py
│   ├── models.py           # Database models
│   ├── urls.py            # App URL routing
│   └── views.py           # View functions
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── core/            # Core app templates
│   └── registration/    # Authentication templates
├── static/               # Static files
│   ├── css/             # Stylesheets
│   └── js/              # JavaScript files
├── media/               # User uploaded files
├── venv/                # Virtual environment
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore file
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🗃️ Database Models

The system includes the following main models:

- **User**: Extended Django user with custom fields
- **Role, UserRole**: Role-based access control
- **Class, Student**: Academic structure
- **ParentStudentRelationship**: Parent-child relationships
- **Post, Message**: Communication features
- **Attendance, LearningActivity**: Tracking features
- **AuditLog**: Activity monitoring

## 🔧 Available Management Commands

```bash
# Database operations
python manage.py makemigrations            # Create new migrations
python manage.py migrate                   # Apply migrations
python manage.py showmigrations           # Show migration status
python manage.py dbshell                  # Access database shell

# User management
python manage.py createsuperuser          # Create admin user
python manage.py changepassword username  # Change user password

# Development utilities
python manage.py runserver                # Start development server
python manage.py shell                   # Interactive Python shell
python manage.py check                   # Check for issues
python manage.py collectstatic           # Collect static files

# Data operations
python manage.py inspectdb               # Generate models from existing DB
python manage.py loaddata fixture.json  # Load data from fixture
python manage.py dumpdata core > data.json # Export data
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test core

# Run with verbose output
python manage.py test --verbosity=2
```

## 🚀 Production Deployment

### Environment Variables for Production

```bash
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
MYSQL_USER=production_user
MYSQL_PASSWORD=secure_production_password
MYSQL_DATABASE=production_db
MYSQL_HOST=your_db_host
MYSQL_PORT=3306
```

### Basic Production Setup

```bash
# Install production dependencies
pip install gunicorn whitenoise

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

# Run with Gunicorn
gunicorn classdojo_project.wsgi:application --bind 0.0.0.0:8000
```

## 🐛 Troubleshooting

### Common macOS Issues

1. **Homebrew Issues**:
   ```bash
   # Fix Homebrew permissions
   sudo chown -R $(whoami) /opt/homebrew/*
   
   # Update Homebrew
   brew update && brew upgrade
   ```

2. **MySQL Connection Issues**:
   ```bash
   # Restart MySQL service
   brew services restart mysql
   
   # Check MySQL status
   brew services list | grep mysql
   
   # Test database connection
   python manage.py dbshell
   ```

3. **Virtual Environment Issues**:
   ```bash
   # Deactivate and recreate virtual environment
   deactivate
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **mysqlclient Installation Issues**:
   ```bash
   # Install required system dependencies
   brew install mysql pkg-config
   
   # Set environment variables
   export PKG_CONFIG_PATH="$(brew --prefix)/lib/pkgconfig"
   
   # Alternative: Use PyMySQL
   pip uninstall mysqlclient
   pip install PyMySQL
   ```

5. **Permission Errors**:
   ```bash
   # Fix manage.py permissions
   chmod +x manage.py
   
   # Fix directory permissions
   chmod -R 755 static/ media/ templates/
   ```

### Development Tips

- Always activate virtual environment before working: `source venv/bin/activate`
- Check Django version compatibility: `python -m django --version`
- Use Django debug toolbar for development: `pip install django-debug-toolbar`
- Monitor database with: `python manage.py dbshell`

## 🔒 Security Considerations

- **Environment Variables**: Never commit `.env` to Git
- **Secret Key**: Generate unique keys for each environment
- **Database**: Use strong passwords and limit privileges
- **Dependencies**: Keep packages updated with `pip list --outdated`
- **HTTPS**: Always use HTTPS in production
