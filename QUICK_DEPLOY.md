# Quick Deployment Guide

Fast deployment instructions for common scenarios.

## Local Development (5 minutes)

```bash
# 1. Prerequisites
# - Node.js 18+, Python 3.11+, PostgreSQL 14+

# 2. Clone and setup
git clone <your-repo>
cd synthetic-ascension-ehr-platform
npm install
pip install -r dependencies.txt

# 3. Database setup
createdb synthetic_ascension
export DATABASE_URL="postgresql://localhost/synthetic_ascension"

# 4. Start services (4 terminals)
npm run dev                                  # Frontend (Port 5000)
python integrated_server_v3_enhanced.py     # Backend V3 (Port 8004)
python integrated_server_v2.py             # Legacy Backend (Port 8003)
python api/swagger_docs.py                 # API Docs (Port 8001)

# 5. Open http://localhost:5000
```

## Docker (10 minutes)

```bash
# 1. Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://sa_user:password@database:5432/synthetic_ascension
DB_PASSWORD=your_secure_password
VITE_API_BASE_URL=http://localhost:8004
EOF

# 2. Create docker-compose.yml (see DEPLOYMENT.md)

# 3. Deploy
docker-compose up -d

# 4. Check health
curl http://localhost/
curl http://localhost:8004/
```

## Vercel + Railway (15 minutes)

### Frontend (Vercel)
```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy frontend
vercel --prod

# 3. Set environment variables in Vercel dashboard:
# VITE_API_BASE_URL=https://your-backend.railway.app
```

### Backend (Railway)
```bash
# 1. Create railway.toml
cat > railway.toml << EOF
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python app.py"
EOF

# 2. Deploy to Railway
# - Connect GitHub repo
# - Deploy from main branch
# - Add PostgreSQL service
# - Set DATABASE_URL environment variable
```

## DigitalOcean App Platform (20 minutes)

```bash
# 1. Create .do/app.yaml (see DEPLOYMENT.md)
# 2. Connect GitHub repo in DO dashboard
# 3. Deploy with one click
# 4. Add managed PostgreSQL database
```

## Traditional VPS (30 minutes)

```bash
# 1. Ubuntu 22.04 server setup
sudo apt update
sudo apt install -y nodejs npm python3 python3-pip postgresql nginx

# 2. Application setup
git clone <your-repo>
cd synthetic-ascension-ehr-platform
npm install && npm run build
pip3 install -r requirements.txt

# 3. Database setup
sudo -u postgres createdb synthetic_ascension
export DATABASE_URL="postgresql://localhost/synthetic_ascension"

# 4. Configure Nginx (see DEPLOYMENT.md for full config)
sudo nano /etc/nginx/sites-available/synthetic-ascension
sudo ln -s /etc/nginx/sites-available/synthetic-ascension /etc/nginx/sites-enabled/
sudo systemctl reload nginx

# 5. Start services with PM2
npm install -g pm2
pm2 start ecosystem.config.js
pm2 startup && pm2 save
```

## Environment Variables

```bash
# Required for all deployments
DATABASE_URL=postgresql://user:pass@host:port/db
NODE_ENV=production
VITE_API_BASE_URL=https://your-backend-domain.com

# Optional
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
JWT_SECRET=your-secret
```

## Health Check URLs

After deployment, verify these endpoints:
- Frontend: `https://your-domain.com/`
- Backend V3: `https://your-domain.com/api/v3/`
- API Docs: `https://your-domain.com/docs`
- Health: `https://your-domain.com/api/ux/system/health`

## Common Issues

### Build Failures
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Database Connection
```bash
# Test connection
python -c "import psycopg2; psycopg2.connect('$DATABASE_URL'); print('OK')"
```

### Port Conflicts
```bash
# Check what's using ports
sudo netstat -tulpn | grep :5000
sudo lsof -i :5000
```

For detailed configuration and advanced options, see [DEPLOYMENT.md](./DEPLOYMENT.md).