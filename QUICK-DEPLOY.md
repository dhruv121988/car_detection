# ⚡ Quick Deploy - Car Damage Detection

## Fastest Routes to Production

### 🐳 Docker (30 seconds)
```bash
docker-compose up -d
```
Done! → http://localhost:5000

### 🪟 Windows (1 command)
```cmd
deploy.bat
```

### 🐧 Linux/Mac (1 command)
```bash
./deploy.sh
```

### ☁️ Free Cloud (5 minutes)

**Render.com:**
1. `git init && git add . && git commit -m "Deploy"`
2. Push to GitHub
3. render.com → New Web Service → Connect repo
4. Deploy! (automatic with render.yaml)

**Railway.app:**
```bash
npm i -g @railway/cli
railway login
railway up
```

## 🔧 Manual Production

```bash
pip install -r requirements-prod.txt
gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 2
```

## ✅ Verify

```bash
curl http://localhost:5000/health
```

## 📚 Full Docs
- **Comprehensive:** DEPLOYMENT.md
- **Summary:** DEPLOYMENT-SUMMARY.md  
- **Status:** DEPLOYMENT-STATUS.txt

---
**Your app is ready!** Pick a method and deploy in minutes! 🚀
