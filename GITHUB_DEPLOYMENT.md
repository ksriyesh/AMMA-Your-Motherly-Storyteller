# 🐙 GitHub Deployment Guide for AMMA

## 🚀 Deployment Options

### **Option 1: GitHub Pages + External Backend (Recommended)**

#### **Frontend on GitHub Pages (Free)**
1. **Enable GitHub Pages in your repository:**
   - Go to Settings → Pages
   - Source: GitHub Actions
   - The workflow will automatically deploy your frontend

2. **Deploy Backend Separately:**
   - **Railway**: Connect GitHub repo, auto-deploy backend
   - **Render**: Connect GitHub repo, auto-deploy backend  
   - **Vercel**: Deploy backend as serverless functions

#### **Setup Steps:**

```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy AMMA to GitHub"
git push origin main

# 2. Configure repository secrets
# Go to Settings → Secrets and variables → Actions
# Add: BACKEND_URL (your backend deployment URL)

# 3. Enable GitHub Pages
# Settings → Pages → Source: GitHub Actions
```

### **Option 2: GitHub Codespaces (Development)**

#### **One-Click Development Environment:**

1. Click "Code" → "Codespaces" → "Create codespace"
2. Wait for automatic setup (uses `.devcontainer/devcontainer.json`)
3. Environment will have Python 3.11, Node.js 18, and all dependencies installed

### **Option 3: GitHub Actions CI/CD**

#### **Automated Testing & Deployment:**

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: python install.py
      - name: Run tests
        run: pytest tests/
```

## 🌐 Live Demo URLs

After deployment, your AMMA will be available at:

- **Frontend**: `https://yourusername.github.io/repository-name/`
- **Backend**: `https://your-backend-service.railway.app/` (or similar)

## 💰 Cost Breakdown

### **Free Tier (Perfect for Personal Use):**
- **GitHub Pages**: Free (public repos)
- **GitHub Actions**: 2,000 minutes/month free
- **Railway/Render**: Free tier with limitations
- **Total**: $0/month

### **Paid Tier (Production Ready):**
- **GitHub Pro**: $4/month (private repos)
- **Railway Pro**: $5/month (better performance)
- **Custom Domain**: $10-15/year
- **Total**: ~$10/month

## 🔧 Configuration

### **Environment Variables:**
```bash
# Add to GitHub Secrets
OPENAI_API_KEY=your_openai_api_key
BACKEND_URL=https://your-backend.railway.app
```

### **Custom Domain Setup:**
1. Add `CNAME` file to `AMMA-UI/public/`:
   ```
   yourdomain.com
   ```
2. Configure DNS records with your domain provider
3. Enable HTTPS in GitHub Pages settings

## 🚀 Quick Deploy Commands

```bash
# Deploy everything to GitHub
git add .
git commit -m "🚀 Deploy AMMA"
git push origin main

# Check deployment status
gh workflow list
gh workflow view "Deploy Frontend to GitHub Pages"
```

## 📊 Monitoring & Analytics

### **GitHub Insights:**
- Traffic analytics in repository Insights tab
- Actions usage in Settings → Billing

### **Add Analytics to Frontend:**
```javascript
// Add to AMMA-UI/app/layout.tsx
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

## 🔒 Security Best Practices

1. **Never commit API keys** - use GitHub Secrets
2. **Enable Dependabot** for security updates
3. **Use branch protection** rules for main branch
4. **Enable 2FA** on GitHub account

## 🛠️ Troubleshooting

### **Common Issues:**

**Build fails:**
```bash
# Check GitHub Actions logs
gh run list
gh run view [run-id]
```

**Frontend not loading:**
- Check if `output: 'export'` is in `next.config.mjs`
- Verify GitHub Pages is enabled
- Check custom domain configuration

**Backend connection issues:**
- Verify `BACKEND_URL` in GitHub Secrets
- Check CORS settings in FastAPI backend
- Ensure WebSocket connections work with your backend host

## 🎯 Recommended Setup

### **For Personal Projects:**
1. Frontend: GitHub Pages
2. Backend: Railway (free tier)
3. Domain: GitHub's `.github.io` subdomain

### **For Production:**
1. Frontend: GitHub Pages with custom domain
2. Backend: Railway Pro or Render
3. Monitoring: GitHub Insights + backend logs
4. CI/CD: GitHub Actions for automated deployments

---

**🌙 Your AMMA bedtime story agent will be live and accessible to the world!** ✨
