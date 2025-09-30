# Creating a Separate Repository for Frontend

This guide explains how to extract the frontend directory and create it as a separate GitHub repository named `real-estate-ai-frontend`.

## Why Separate the Frontend?

Having the frontend in a separate repository offers several benefits:
- Independent deployment and versioning
- Cleaner separation of concerns
- Easier to manage different teams working on frontend vs backend
- Simplified CI/CD pipelines

## Steps to Create the Separate Repository

### Option 1: Manual Method (Recommended)

#### 1. Create New Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `real-estate-ai-frontend`
3. Description: `Frontend for Riyadh Real Estate AI - Next.js 14 with TypeScript and Tailwind CSS`
4. Make it Public
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

#### 2. Prepare the Frontend Directory

```bash
# Navigate to the frontend directory
cd frontend

# Initialize a new git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: Next.js 14 Real Estate AI Frontend

- Next.js 14 with App Router
- TypeScript for type safety
- Tailwind CSS for styling
- Environment-based API configuration
- Comprehensive documentation
- Vercel deployment ready"

# Add the remote repository
git remote add origin https://github.com/khaliiid501/real-estate-ai-frontend.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### 3. Verify the Repository

1. Visit https://github.com/khaliiid501/real-estate-ai-frontend
2. Check that all files are present
3. Verify the README displays correctly

### Option 2: Using Git Subtree

If you want to maintain history from the parent repository:

```bash
# From the parent repository root
git subtree split --prefix=frontend -b frontend-only

# Create the new repository on GitHub first, then:
git push https://github.com/khaliiid501/real-estate-ai-frontend.git frontend-only:main

# Clean up the temporary branch
git branch -D frontend-only
```

## Post-Repository Creation Steps

### 1. Update Repository Settings

On GitHub, go to the repository settings:

1. **About Section** (top right on main page):
   - Add description: "Frontend for Riyadh Real Estate AI - Next.js 14"
   - Add website: Your Vercel deployment URL
   - Add topics: `nextjs`, `typescript`, `tailwindcss`, `real-estate`, `ai`, `frontend`

2. **Repository Settings**:
   - Enable Issues (if you want issue tracking)
   - Enable Discussions (optional)
   - Set up branch protection rules for main branch (optional but recommended)

### 2. Deploy to Vercel

Now that you have a separate repository:

1. Go to https://vercel.com/new
2. Import the `real-estate-ai-frontend` repository
3. Configure environment variables:
   - `NEXT_PUBLIC_API_URL`: Your production API URL
4. Deploy

### 3. Update the Main Repository

Back in the main `Riyadh` repository, update the README to point to the frontend:

```markdown
# Riyadh
Predictive Real Estate Software

## Architecture

This is a monorepo containing multiple components:

- **Frontend**: [real-estate-ai-frontend](https://github.com/khaliiid501/real-estate-ai-frontend) - Next.js 14 web application
- **Backend**: Coming soon
- **ML Models**: Coming soon

## Getting Started

For frontend setup and deployment, see the [frontend repository](https://github.com/khaliiid501/real-estate-ai-frontend).
```

### 4. Set Up GitHub Actions (Optional)

Create `.github/workflows/deploy.yml` in the new frontend repository:

```yaml
name: Deploy to Vercel

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Build
        run: npm run build
        env:
          NEXT_PUBLIC_API_URL: ${{ secrets.NEXT_PUBLIC_API_URL }}
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          vercel-args: '--prod'
```

## Maintaining Two Repositories

### Syncing Changes from Monorepo to Separate Repo

If you continue developing in the monorepo first:

```bash
# In the main Riyadh repo
cd frontend
git init  # if not already initialized
git add .
git commit -m "Update frontend"

# Push to the separate repository
git remote add frontend-repo https://github.com/khaliiid501/real-estate-ai-frontend.git
git push frontend-repo main
```

### Best Practice: Choose One Approach

**Recommended**: Develop directly in the separate `real-estate-ai-frontend` repository and keep only a link in the main repository.

## Verifying Everything Works

After creating the separate repository:

1. ✅ Clone the new repository
2. ✅ Run `npm install`
3. ✅ Copy `.env.local.template` to `.env.local`
4. ✅ Run `npm run dev`
5. ✅ Visit http://localhost:3000
6. ✅ Verify the API URL is displayed correctly

## Getting Your Live URL

Once deployed to Vercel:

1. Your production URL will be: `https://real-estate-ai-frontend.vercel.app`
2. Add this to your repository description
3. Add it to the README
4. Share it with your team

## Support

If you encounter any issues:
- Check the DEPLOYMENT.md guide
- Review the README.md
- Ensure all environment variables are set correctly
- Verify Node.js version is 18.17 or later
