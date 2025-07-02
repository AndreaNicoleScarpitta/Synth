# Deployment Guide - Synthetic Ascension EHR Platform

This guide covers deploying the Synthetic Ascension EHR Platform outside of Replit to various hosting platforms and local environments.

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
  - [Docker Deployment](#docker-deployment)
  - [Cloud Platforms](#cloud-platforms)
  - [Traditional VPS](#traditional-vps)
- [Database Setup](#database-setup)
- [Environment Variables](#environment-variables)
- [Monitoring & Maintenance](#monitoring--maintenance)
- [Troubleshooting](#troubleshooting)

## Architecture Overview

The platform consists of:
- **React Frontend** (Port 5000) - TypeScript + Tailwind CSS
- **Enhanced Backend V3** (Port 8004) - FastAPI with 50+ AI agents (Primary)
- **Legacy Backend** (Port 8003) - FastAPI with 18+ agents (Fallback)
- **API Documentation** (Port 8001) - Swagger/OpenAPI docs
- **PostgreSQL Database** - Patient data and job tracking

## Prerequisites

### System Requirements
- **CPU:** 2+ cores (4+ recommended for production)
- **RAM:** 4GB minimum (8GB+ recommended)
- **Storage:** 10GB minimum (SSD recommended)
- **OS:** Linux (Ubuntu 20.04+), macOS, or Windows with WSL2

### Software Dependencies
- **Node.js:** v18+ (v20 recommended)
- **Python:** 3.11+
- **PostgreSQL:** 14+
- **Git:** Latest version
- **npm/yarn:** Latest version

## Environment Setup

### 1. Clone Repository
```bash
git clone <your-repository-url>
cd synthetic-ascension-ehr-platform
```

### 2. Install Dependencies

#### Frontend Dependencies
```bash
npm install
```

#### Backend Dependencies
```bash
# Using pip (recommended for external deployment)
pip install -r dependencies.txt

# Or using the Replit-specific file (if available)
pip install -r requirements.txt

# Or using pipenv
pipenv install

# Or using poetry
poetry install
```

### 3. Database Setup
```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE synthetic_ascension;
CREATE USER sa_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE synthetic_ascension TO sa_user;
\q
```

## Local Development

### Quick Start
```bash
# 1. Set environment variables
export DATABASE_URL="postgresql://sa_user:your_secure_password@localhost/synthetic_ascension"
export NODE_ENV="development"

# 2. Start frontend (Terminal 1)
npm run dev

# 3. Start Enhanced Backend V3 (Terminal 2)
python integrated_server_v3_enhanced.py

# 4. Start Legacy Backend (Terminal 3)
python integrated_server_v2.py

# 5. Start API Documentation (Terminal 4)
python api/swagger_docs.py
```

### Development Scripts
```bash
# Frontend development server
npm run dev

# Frontend build
npm run build

# Frontend preview (production build)
npm run preview

# Run frontend tests
npm run test

# Run backend tests
python -m pytest tests/backend/ -v

# Type checking
npm run type-check

# Linting
npm run lint
```

## Production Deployment

### Docker Deployment

#### 1. Create Dockerfile
```dockerfile
# Frontend Dockerfile
FROM node:20-alpine as frontend-build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=frontend-build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### 2. Create docker-compose.yml
```yaml
version: '3.8'

services:
  frontend:
    build: .
    ports:
      - "80:80"
    depends_on:
      - backend-v3
      - database
    environment:
      - VITE_API_BASE_URL=http://backend-v3:8004

  backend-v3:
    build: ./backend
    ports:
      - "8004:8004"
    depends_on:
      - database
    environment:
      - DATABASE_URL=postgresql://sa_user:${DB_PASSWORD}@database:5432/synthetic_ascension
      - PORT=8004
    volumes:
      - ./logs:/app/logs

  backend-legacy:
    build: ./backend
    command: python integrated_server_v2.py
    ports:
      - "8003:8003"
    depends_on:
      - database
    environment:
      - DATABASE_URL=postgresql://sa_user:${DB_PASSWORD}@database:5432/synthetic_ascension
      - PORT=8003

  api-docs:
    build: ./backend
    command: python api/swagger_docs.py
    ports:
      - "8001:8001"
    depends_on:
      - backend-v3

  database:
    image: postgres:16
    environment:
      - POSTGRES_DB=synthetic_ascension
      - POSTGRES_USER=sa_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

#### 3. Deploy with Docker
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Scale backend services
docker-compose up -d --scale backend-v3=3

# Stop services
docker-compose down
```

### Cloud Platforms

#### Vercel (Frontend Only)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# Environment variables in Vercel dashboard:
# VITE_API_BASE_URL=https://your-backend-domain.com
```

#### Railway
```yaml
# railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python app.py"
healthcheckPath = "/"
healthcheckTimeout = 100
restartPolicyType = "ON_FAILURE"

[[services]]
name = "frontend"
source = "."
```

#### DigitalOcean App Platform
```yaml
# .do/app.yaml
name: synthetic-ascension
services:
- name: frontend
  source_dir: /
  github:
    repo: your-username/synthetic-ascension
    branch: main
  build_command: npm run build
  run_command: npx serve -s dist -l 8080
  environment_slug: node-js
  instance_count: 1
  instance_size_slug: basic-xxs
  
- name: backend-v3
  source_dir: /
  github:
    repo: your-username/synthetic-ascension
    branch: main
  build_command: pip install -r requirements.txt
  run_command: python integrated_server_v3_enhanced.py
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xs

databases:
- name: synthetic-ascension-db
  engine: PG
  num_nodes: 1
  size: db-s-dev-database
```

#### AWS (EC2 + RDS)
```bash
# 1. Launch EC2 instance (Ubuntu 22.04)
# 2. Install dependencies
sudo apt update
sudo apt install -y nodejs npm python3 python3-pip nginx

# 3. Clone and setup application
git clone <your-repo>
cd synthetic-ascension-ehr-platform
npm install
pip3 install -r requirements.txt

# 4. Build frontend
npm run build

# 5. Configure Nginx
sudo nano /etc/nginx/sites-available/synthetic-ascension

# 6. Create systemd services
sudo nano /etc/systemd/system/sa-backend-v3.service
sudo nano /etc/systemd/system/sa-frontend.service

# 7. Enable and start services
sudo systemctl enable sa-backend-v3
sudo systemctl start sa-backend-v3
```

#### Google Cloud Platform (Cloud Run)
```yaml
# cloudbuild.yaml
steps:
# Build frontend
- name: 'node:20'
  entrypoint: 'npm'
  args: ['install']
- name: 'node:20'
  entrypoint: 'npm'
  args: ['run', 'build']

# Build backend container
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', 'gcr.io/$PROJECT_ID/sa-backend:$COMMIT_SHA', '.']
- name: 'gcr.io/cloud-builders/docker'
  args: ['push', 'gcr.io/$PROJECT_ID/sa-backend:$COMMIT_SHA']

# Deploy to Cloud Run
- name: 'gcr.io/cloud-builders/gcloud'
  args: ['run', 'deploy', 'sa-backend', '--image', 'gcr.io/$PROJECT_ID/sa-backend:$COMMIT_SHA', '--platform', 'managed', '--region', 'us-central1']
```

### Traditional VPS

#### Nginx Configuration
```nginx
# /etc/nginx/sites-available/synthetic-ascension
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/synthetic-ascension/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API V3
    location /api/v3/ {
        proxy_pass http://127.0.0.1:8004;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Legacy Backend API
    location /api/v2/ {
        proxy_pass http://127.0.0.1:8003;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # API Documentation
    location /docs {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Systemd Service Files
```ini
# /etc/systemd/system/sa-backend-v3.service
[Unit]
Description=Synthetic Ascension Enhanced Backend V3
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/synthetic-ascension
Environment=DATABASE_URL=postgresql://sa_user:password@localhost/synthetic_ascension
ExecStart=/usr/bin/python3 integrated_server_v3_enhanced.py
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Process Manager (PM2)
```bash
# Install PM2
npm install -g pm2

# Create ecosystem file
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [
    {
      name: 'sa-backend-v3',
      script: 'integrated_server_v3_enhanced.py',
      interpreter: 'python3',
      instances: 2,
      exec_mode: 'cluster',
      env: {
        PORT: 8004,
        DATABASE_URL: 'postgresql://sa_user:password@localhost/synthetic_ascension'
      }
    },
    {
      name: 'sa-backend-legacy',
      script: 'integrated_server_v2.py',
      interpreter: 'python3',
      instances: 1,
      env: {
        PORT: 8003,
        DATABASE_URL: 'postgresql://sa_user:password@localhost/synthetic_ascension'
      }
    }
  ]
};
EOF

# Start applications
pm2 start ecosystem.config.js
pm2 startup
pm2 save
```

## Database Setup

### PostgreSQL Configuration
```sql
-- Create database and user
CREATE DATABASE synthetic_ascension;
CREATE USER sa_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE synthetic_ascension TO sa_user;

-- Enable required extensions
\c synthetic_ascension;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
```

### Database Migrations
```bash
# Run initial migrations
python -c "
from integrated_server_v3_enhanced import enhanced_job_manager
enhanced_job_manager.init_db()
print('Database initialized successfully')
"
```

### Backup and Restore
```bash
# Backup
pg_dump -U sa_user -h localhost synthetic_ascension > backup.sql

# Restore
psql -U sa_user -h localhost synthetic_ascension < backup.sql
```

## Environment Variables

### Required Variables
```bash
# Database
DATABASE_URL="postgresql://username:password@host:port/database"

# Application
NODE_ENV="production"
PORT="5000"

# API URLs
VITE_API_BASE_URL="https://your-domain.com"

# Security (generate secure values)
JWT_SECRET="your-jwt-secret-key"
ENCRYPTION_KEY="your-encryption-key"

# Optional: External Services
OPENAI_API_KEY="your-openai-key"
ANTHROPIC_API_KEY="your-anthropic-key"
```

### Environment Files
```bash
# .env.production
DATABASE_URL=postgresql://sa_user:secure_password@localhost/synthetic_ascension
NODE_ENV=production
VITE_API_BASE_URL=https://api.your-domain.com
JWT_SECRET=your-super-secure-jwt-secret
ENCRYPTION_KEY=your-encryption-key-32-chars

# .env.development
DATABASE_URL=postgresql://sa_user:dev_password@localhost/synthetic_ascension_dev
NODE_ENV=development
VITE_API_BASE_URL=http://localhost:8004
```

## Monitoring & Maintenance

### Health Checks
```bash
# Frontend health check
curl http://localhost:5000/

# Backend V3 health check
curl http://localhost:8004/

# Database health check
curl http://localhost:8004/api/ux/system/health
```

### Logging
```bash
# Application logs
tail -f /var/log/synthetic-ascension/app.log

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# System logs
journalctl -u sa-backend-v3 -f
```

### Performance Monitoring
```bash
# Install monitoring tools
npm install -g clinic
pip install psutil

# Monitor backend performance
clinic doctor -- python integrated_server_v3_enhanced.py

# Database monitoring
SELECT * FROM pg_stat_activity WHERE datname = 'synthetic_ascension';
```

### Automated Backups
```bash
# Create backup script
cat > backup.sh << EOF
#!/bin/bash
DATE=\$(date +%Y%m%d_%H%M%S)
pg_dump -U sa_user synthetic_ascension > /backups/sa_backup_\$DATE.sql
find /backups -name "sa_backup_*.sql" -mtime +7 -delete
EOF

# Add to crontab (daily at 2 AM)
echo "0 2 * * * /path/to/backup.sh" | crontab -
```

## Troubleshooting

### Common Issues

#### Frontend Build Fails
```bash
# Clear cache and rebuild
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### Backend Won't Start
```bash
# Check Python dependencies
pip check

# Verify database connection
python -c "
import psycopg2
conn = psycopg2.connect('postgresql://sa_user:password@localhost/synthetic_ascension')
print('Database connection successful')
"
```

#### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -U sa_user -h localhost -d synthetic_ascension -c "SELECT 1;"

# Check logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

#### Port Conflicts
```bash
# Check what's using ports
sudo netstat -tulpn | grep :5000
sudo netstat -tulpn | grep :8004

# Kill processes if needed
sudo kill $(sudo lsof -t -i:5000)
```

### Performance Issues

#### High Memory Usage
```bash
# Monitor processes
htop
ps aux | grep python

# Optimize Python backend
export PYTHONOPTIMIZE=1
ulimit -v 2097152  # Limit virtual memory to 2GB
```

#### Slow Database Queries
```sql
-- Enable query logging
ALTER SYSTEM SET log_statement = 'all';
SELECT pg_reload_conf();

-- Analyze slow queries
SELECT query, mean_time, calls
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

### SSL/HTTPS Setup

#### Let's Encrypt with Certbot
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

#### Nginx SSL Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # ... rest of configuration
}
```

## Security Considerations

### Firewall Setup
```bash
# Ubuntu UFW
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw --force enable
```

### Database Security
```sql
-- Create read-only user for monitoring
CREATE USER sa_readonly WITH PASSWORD 'readonly_password';
GRANT CONNECT ON DATABASE synthetic_ascension TO sa_readonly;
GRANT USAGE ON SCHEMA public TO sa_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO sa_readonly;
```

### Application Security
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Set secure file permissions
chmod 600 .env.production
chown www-data:www-data /var/www/synthetic-ascension -R
```

---

## Support

For additional support with deployment:
1. Check the main README.md for project-specific details
2. Review the logs using the monitoring commands above
3. Ensure all environment variables are properly set
4. Verify database connectivity and migrations

This deployment guide provides multiple options to suit different infrastructure needs and technical requirements.