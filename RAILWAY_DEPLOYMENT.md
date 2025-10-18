# 🚂 Railway Deployment Guide

This guide will help you deploy the Medical Document Parser API to Railway.

## 📋 Prerequisites

1. A [Railway.app](https://railway.app/) account (free tier available)
2. Your GitHub repository connected to Railway
3. OpenAI API key

## 🚀 Deployment Steps

### Step 1: Create a New Project on Railway

1. Go to [Railway.app](https://railway.app/) and sign in
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository: `Rovlad/meddoc_parse`
5. Railway will automatically detect it's a Python project

### Step 2: Configure Environment Variables

Railway needs your OpenAI API key to work. Set it up:

1. In your Railway project dashboard, click on your service
2. Go to the **"Variables"** tab
3. Add the following environment variable:
   - **Variable name**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key (starts with `sk-...`)

**Optional environment variables** (Railway will use defaults if not set):
- `OPENAI_MODEL`: `gpt-4o` (default)
- `MAX_IMAGE_SIZE`: `10485760` (10MB, default)
- `MAX_IMAGE_DIMENSION`: `2048` (default)
- `LOG_LEVEL`: `INFO` (default)

### Step 3: Deploy

1. Railway will automatically deploy after you connect your repo
2. Wait for the build to complete (usually 2-3 minutes)
3. Once deployed, Railway will provide you with a public URL like:
   - `https://your-project.up.railway.app`

### Step 4: Test Your Deployment

1. Open your Railway URL in a browser:
   ```
   https://your-project.up.railway.app
   ```

2. You should see a welcome message with links to:
   - API Documentation: `https://your-project.up.railway.app/docs`
   - Test Interface: `https://your-project.up.railway.app/test`

3. Test the API by uploading a medical document at:
   ```
   https://your-project.up.railway.app/test
   ```

## 📁 Required Files (Already Included)

Your project already has all necessary files for Railway deployment:

✅ **Procfile** - Tells Railway how to start your app
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

✅ **requirements.txt** - Lists all Python dependencies

✅ **runtime.txt** - Specifies Python version (3.13.3)

✅ **.gitignore** - Ensures `.env` is not committed

## 🔧 Railway Configuration

Railway automatically handles:
- Installing dependencies from `requirements.txt`
- Setting the correct Python version from `runtime.txt`
- Running the command from `Procfile`
- Assigning a `PORT` environment variable
- Providing a public HTTPS URL

## 💰 Pricing

Railway offers:
- **Free Trial**: $5 in credits to start
- **Hobby Plan**: $5/month for personal projects
- **Pro Plan**: $20/month for production apps

Your API should run comfortably on the Hobby plan for moderate usage.

## 🐛 Troubleshooting

### Build Fails

1. Check the build logs in Railway dashboard
2. Make sure all files are committed to GitHub:
   ```bash
   git status
   git add .
   git commit -m "Add deployment files"
   git push
   ```

### App Crashes on Startup

1. Check the deployment logs in Railway
2. Verify that `OPENAI_API_KEY` is set correctly in environment variables
3. Make sure the key is valid (test it locally first)

### API Returns Errors

1. Check the application logs in Railway dashboard
2. Verify your OpenAI API key has credits
3. Test locally first to isolate the issue:
   ```bash
   ./run.sh
   ```

### File Upload Issues

If image uploads fail:
1. Check that `MAX_IMAGE_SIZE` is set appropriately
2. Railway has a 100MB request limit (your default is 10MB, which is fine)
3. Make sure images are in supported formats: JPEG, PNG, GIF, BMP, TIFF

## 🔄 Continuous Deployment

Railway automatically redeploys when you push to your main branch:

```bash
git add .
git commit -m "Your update message"
git push origin master
```

Railway will detect the push and redeploy automatically.

## 🌐 Custom Domain (Optional)

To use your own domain:

1. Go to your service in Railway
2. Click on **"Settings"**
3. Scroll to **"Domains"**
4. Click **"Add Domain"**
5. Follow the DNS configuration instructions

## 📊 Monitoring

Railway provides:
- **Metrics**: CPU, Memory, Network usage
- **Logs**: Real-time application logs
- **Deployments**: History of all deployments

Access these from your project dashboard.

## 🔒 Security Notes

1. **Never commit `.env` file** - It's already in `.gitignore` ✅
2. **Use Railway's environment variables** for sensitive data
3. **Rotate your OpenAI API key** if it's ever exposed
4. **Set usage limits** in your OpenAI dashboard

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

---

## Quick Start Summary

```bash
# 1. Commit all changes
git add .
git commit -m "Prepare for Railway deployment"
git push origin master

# 2. Go to Railway.app
# 3. New Project → Deploy from GitHub
# 4. Select your repo
# 5. Add OPENAI_API_KEY in Variables tab
# 6. Wait for deployment
# 7. Visit your-project.up.railway.app/test
```

That's it! Your Medical Document Parser API is now live! 🎉

