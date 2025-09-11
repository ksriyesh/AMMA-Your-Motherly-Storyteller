# AMMA Deployment Guide

## 🚀 Deploy Frontend to GitHub Pages + Backend to Railway

### **Step 1: Deploy Backend to Railway**

1. **Go to [Railway.app](https://railway.app)** and sign in
2. **Create New Project** → **Deploy from GitHub repo**
3. **Select this repository**
4. **Configure Service:**
   - **Service Name**: `amma-backend`
   - **Dockerfile Path**: `Dockerfile.backend`
   - **Add Environment Variables**:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
5. **Deploy** and copy the generated URL (e.g., `https://amma-backend-abc123.railway.app`)

### **Step 2: Configure GitHub Pages**

1. **Go to your GitHub repository** → **Settings** → **Pages**
2. **Source**: Deploy from a branch → **GitHub Actions**
3. **Go to Settings** → **Secrets and variables** → **Actions** → **Variables**
4. **Add Repository Variables**:
   ```
   NEXT_PUBLIC_API_URL = https://your-railway-backend-url
   NEXT_PUBLIC_WS_URL = wss://your-railway-backend-url
   ```
   *(Replace with your actual Railway backend URL)*

### **Step 3: Deploy Frontend**

1. **Push to main branch** - GitHub Actions will automatically deploy
2. **Check Actions tab** to monitor deployment progress
3. **Frontend will be available at**: `https://yourusername.github.io/AMMA-Your-Motherly-Storyteller/`

### **Step 4: Test Connection**

1. **Visit your GitHub Pages URL**
2. **Open browser console** (F12)
3. **Look for**: "🌟 Connected to AMMA"
4. **Start chatting** with AMMA!

## 🔧 URLs Structure

- **Frontend**: `https://yourusername.github.io/AMMA-Your-Motherly-Storyteller/`
- **Backend**: `https://your-backend.railway.app`
- **API Docs**: `https://your-backend.railway.app/docs`
- **WebSocket**: `wss://your-backend.railway.app/ws/`

## 🐛 Troubleshooting

**If frontend can't connect to backend:**
- Check GitHub repository variables are set correctly
- Verify Railway backend is deployed and running
- Check browser console for connection errors

**If GitHub Actions fails:**
- Check the Actions tab for error details
- Ensure AMMA-UI directory structure is correct
- Verify package.json and dependencies are valid
