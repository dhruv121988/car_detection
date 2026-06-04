# Car Damage Detection - Deployment Guide

This guide covers multiple deployment options for the Car Damage Detection application.

## 📋 Prerequisites

- Python 3.11
- Trained YOLO model at `runs/detect/train3/weights/best.pt`
- Git (for most deployment methods)

## 🚀 Deployment Options

### 1. Local Production Server (Recommended for Testing)

Using Gunicorn as a production WSGI server:

```bash
# Install production dependencies
pip install -r requirements-prod.txt

# Run with Gunicorn
gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 2 --timeout 120
```

Access at: `http://localhost:5000`

### 2. Docker Deployment 🐳

**Build and run with Docker:**

```bash
# Build the Docker image
docker build -t car-damage-detection .

# Run the container
docker run -p 5000:5000 -v $(pwd)/static/uploads:/app/static/uploads -v $(pwd)/static/results:/app/static/results car-damage-detection
```

**Or use Docker Compose:**

```bash
docker-compose up -d
```

Access at: `http://localhost:5000`

### 3. Heroku Deployment ☁️

```bash
# Install Heroku CLI first
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name

# Add Python buildpack
heroku buildpacks:set heroku/python

# Set environment variables
heroku config:set FLASK_ENV=production

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Scale the app
heroku ps:scale web=1
```

**Important:** Update `requirements-prod.txt` if needed and ensure your model file is included in the Git repo (or use cloud storage).

### 4. Render Deployment 🎨

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: car-damage-detection
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements-prod.txt`
   - **Start Command**: `gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
5. Click "Create Web Service"

Or use the `render.yaml` file for automatic deployment.

### 5. Google Cloud Platform (App Engine) 🌐

```bash
# Install Google Cloud SDK
# Initialize gcloud
gcloud init

# Deploy to App Engine
gcloud app deploy app.yaml
```

### 6. AWS EC2 Deployment 🖥️

**Step 1: Launch EC2 Instance**
- Choose Ubuntu 22.04 LTS
- Instance type: t3.medium or larger (for ML inference)
- Configure security group to allow HTTP (80) and HTTPS (443)

**Step 2: Connect and Setup**

```bash
# SSH into your instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.11 python3-pip nginx -y

# Clone your repository
git clone your-repo-url
cd car-damage-detection

# Install Python packages
pip install -r requirements-prod.txt

# Setup Nginx (edit nginx.conf with your paths)
sudo cp nginx.conf /etc/nginx/sites-available/car-damage
sudo ln -s /etc/nginx/sites-available/car-damage /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Run with systemd (create service file)
sudo nano /etc/systemd/system/car-damage.service
```

**systemd service file:**

```ini
[Unit]
Description=Car Damage Detection App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/car-damage-detection
Environment="PATH=/home/ubuntu/.local/bin"
ExecStart=/home/ubuntu/.local/bin/gunicorn wsgi:app --bind 127.0.0.1:5000 --workers 2 --timeout 120

[Install]
WantedBy=multi-user.target
```

**Start the service:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable car-damage
sudo systemctl start car-damage
```

### 7. DigitalOcean App Platform 🌊

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Connect your GitHub repository
4. Configure:
   - **Type**: Web Service
   - **Run Command**: `gunicorn wsgi:app --bind 0.0.0.0:8080 --workers 2 --timeout 120`
   - **HTTP Port**: 8080
5. Add environment variables if needed
6. Deploy

### 8. Railway Deployment 🚂

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

## ⚙️ Environment Variables

Create a `.env` file based on `.env.example`:

```env
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=static/uploads
RESULT_FOLDER=static/results
MODEL_PATH=runs/detect/train3/weights/best.pt
```

## 🔒 Security Considerations

1. **Change Secret Key**: Generate a strong secret key
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

2. **HTTPS**: Always use HTTPS in production
   - Use Let's Encrypt for free SSL certificates
   - Configure your hosting platform's SSL

3. **File Upload Security**: Already implemented
   - File size limits (16MB)
   - File type validation
   - Unique filenames using UUID

4. **Rate Limiting**: Consider adding Flask-Limiter
   ```bash
   pip install Flask-Limiter
   ```

5. **Environment Variables**: Never commit `.env` file

## 📊 Performance Optimization

1. **Workers**: Adjust Gunicorn workers based on CPU cores
   ```
   workers = (2 × CPU_cores) + 1
   ```

2. **Caching**: Consider adding Redis for caching results

3. **CDN**: Use a CDN for static files in production

4. **Model Optimization**: 
   - Use quantized models for faster inference
   - Consider GPU instances for heavy load

## 🧪 Testing Production Setup

```bash
# Test with curl
curl -X POST -F "file=@test_image.jpg" http://your-domain.com/upload

# Load testing with Apache Bench
ab -n 100 -c 10 http://your-domain.com/
```

## 📱 Monitoring

Consider adding monitoring services:
- **Sentry** for error tracking
- **New Relic** for performance monitoring
- **Datadog** for infrastructure monitoring

## 🆘 Troubleshooting

### Issue: Model not loading
- Ensure model file exists at specified path
- Check file permissions
- Verify ultralytics version compatibility

### Issue: Out of memory
- Reduce number of workers
- Use a larger instance/server
- Implement request queuing

### Issue: Slow inference
- Enable GPU if available
- Use model quantization
- Implement caching for repeated images

## 📞 Support

For issues or questions:
- Check application logs: `journalctl -u car-damage -f` (Linux)
- Review server logs based on your hosting platform
- Verify all dependencies are installed correctly

## 🎯 Quick Start Checklist

- [ ] Choose deployment platform
- [ ] Prepare `.env` file with production settings
- [ ] Ensure model file is accessible
- [ ] Install production dependencies
- [ ] Configure security (HTTPS, secret keys)
- [ ] Set up monitoring
- [ ] Test deployment
- [ ] Configure domain (if applicable)
- [ ] Set up backups

---

**Need help?** Refer to your hosting platform's documentation for specific configuration details.
