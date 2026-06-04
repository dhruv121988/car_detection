# 🚀 Quick Deployment Guide

## Fastest Deployment Options

### Option 1: Automated Script (Recommended)

**Windows:**
```cmd
deploy.bat
```

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Docker (Production Ready)

```bash
# Build and run with one command
docker-compose up -d

# Access at http://localhost:5000
```

### Option 3: Manual Production Setup

```bash
# Install dependencies
pip install -r requirements-prod.txt

# Run with production server
gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 2 --timeout 120
```

## 🌐 Cloud Deployment (5 Minutes)

### Render.com (Free Tier Available)
1. Push code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New Web Service"
4. Connect repository
5. Use these settings:
   - Build: `pip install -r requirements-prod.txt`
   - Start: `gunicorn wsgi:app --bind 0.0.0.0:$PORT`

### Railway.app (Free Tier Available)
```bash
npm i -g @railway/cli
railway login
railway init
railway up
```

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

## 📝 Files Created

- `requirements-prod.txt` - Production dependencies
- `wsgi.py` - WSGI entry point
- `Procfile` - Heroku configuration
- `Dockerfile` - Docker configuration
- `docker-compose.yml` - Docker Compose setup
- `nginx.conf` - Nginx reverse proxy config
- `deploy.sh` / `deploy.bat` - Automated deployment scripts
- `DEPLOYMENT.md` - Comprehensive deployment guide
- `.env.example` - Environment variables template
- `.gitignore` - Git ignore rules

## ⚡ Quick Commands

```bash
# Local production test
gunicorn wsgi:app --bind 0.0.0.0:5000

# Docker build
docker build -t car-damage-detection .

# Docker run
docker run -p 5000:5000 car-damage-detection

# Docker Compose
docker-compose up -d

# Stop Docker
docker-compose down
```

## 🔧 Environment Setup

1. Copy `.env.example` to `.env`
2. Update `SECRET_KEY`:
   ```python
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
3. Adjust settings as needed

## 📊 Verify Deployment

```bash
# Test the API
curl http://localhost:5000

# Test upload (Linux/Mac)
curl -X POST -F "file=@test_image.jpg" http://localhost:5000/upload
```

## 🆘 Troubleshooting

**Model not found error:**
- Ensure `runs/detect/train3/weights/best.pt` exists
- Update `MODEL_PATH` in `.env` if using different location

**Port already in use:**
- Change port in command: `--bind 0.0.0.0:8000`
- Or in `.env`: `PORT=8000`

**Dependencies error:**
- Use Python 3.11: `python3.11 -m venv .venv`
- Clear cache: `pip cache purge`

## 📚 More Information

See `DEPLOYMENT.md` for comprehensive deployment instructions including:
- AWS EC2 deployment
- Google Cloud Platform
- DigitalOcean
- Security best practices
- Performance optimization
- Monitoring setup

---

**Ready to deploy? Run the deployment script or choose a cloud platform!**
