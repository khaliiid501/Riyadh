# Deployment Guide for Vercel

This guide will help you deploy the Riyadh Real Estate AI Frontend to Vercel.

## Prerequisites

- A Vercel account (sign up at https://vercel.com)
- The frontend code pushed to a GitHub repository
- Your backend API URL ready

## Option 1: Deploy via Vercel Dashboard (Recommended)

### Step 1: Import Your Repository

1. Go to https://vercel.com/new
2. Click "Add New Project"
3. Import your GitHub repository
4. Select the repository containing your frontend code

### Step 2: Configure Project

Vercel will automatically detect that this is a Next.js project. You may need to configure:

- **Framework Preset**: Next.js (auto-detected)
- **Root Directory**: `frontend` (if deploying from a monorepo)
- **Build Command**: `npm run build` (default)
- **Output Directory**: `.next` (default)
- **Install Command**: `npm install` (default)

### Step 3: Set Environment Variables

Before deploying, add your environment variables:

1. In the project configuration, scroll to "Environment Variables"
2. Add the following variable:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your production API URL (e.g., `https://api.yourdomain.com/api`)
3. Select which environments to apply it to:
   - ✅ Production
   - ✅ Preview (optional)
   - ✅ Development (optional)

### Step 4: Deploy

1. Click "Deploy"
2. Wait for the deployment to complete (usually 1-2 minutes)
3. Your site will be live at `https://your-project-name.vercel.app`

## Option 2: Deploy via Vercel CLI

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

Follow the prompts to authenticate.

### Step 3: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 4: Deploy to Preview

```bash
vercel
```

This will:
- Create a new project (if first time)
- Deploy to a preview URL
- Prompt you to link to an existing project or create a new one

### Step 5: Set Environment Variables

```bash
vercel env add NEXT_PUBLIC_API_URL
```

When prompted:
- Enter your production API URL
- Select which environments to apply it to (Production, Preview, Development)

### Step 6: Deploy to Production

```bash
vercel --prod
```

Your app will be deployed to production.

## Post-Deployment Configuration

### Custom Domain (Optional)

1. Go to your project in Vercel Dashboard
2. Navigate to Settings → Domains
3. Add your custom domain
4. Follow the DNS configuration instructions

### Environment Variables Management

To update environment variables after deployment:

**Via Dashboard:**
1. Go to Project Settings → Environment Variables
2. Edit or add variables
3. Redeploy for changes to take effect

**Via CLI:**
```bash
vercel env add NEXT_PUBLIC_API_URL production
vercel env ls
```

### Automatic Deployments

Once connected to GitHub:
- Every push to your main branch triggers a production deployment
- Every push to other branches creates a preview deployment
- Pull requests get unique preview URLs

## Verifying Your Deployment

1. Visit your deployed URL
2. Check that the API Base URL displays correctly on the homepage
3. Open browser console to check for any errors
4. Test API calls (if your backend is deployed)

## Troubleshooting

### Build Failures

- Check the build logs in Vercel Dashboard
- Ensure all dependencies are in `package.json`
- Verify TypeScript types are correct

### Environment Variables Not Working

- Ensure variable names start with `NEXT_PUBLIC_` for client-side access
- Redeploy after adding/changing environment variables
- Check that variables are set for the correct environment

### API Calls Failing

- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check CORS settings on your backend
- Ensure your backend API is accessible from Vercel's servers

## Getting Your Live URL

After deployment, your live URLs will be:

- **Production**: `https://your-project-name.vercel.app`
- **Custom Domain** (if configured): `https://yourdomain.com`
- **Preview Deployments**: `https://your-project-name-{hash}.vercel.app`

You can find all URLs in the Vercel Dashboard under your project's "Deployments" tab.

## Monitoring and Analytics

Vercel provides built-in analytics:
- Go to your project dashboard
- Click "Analytics" to see:
  - Page views
  - User interactions
  - Performance metrics
  - Web Vitals scores

## Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment Documentation](https://nextjs.org/docs/deployment)
- [Environment Variables in Vercel](https://vercel.com/docs/concepts/projects/environment-variables)
