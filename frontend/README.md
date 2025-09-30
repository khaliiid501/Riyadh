# Riyadh Real Estate AI - Frontend

A modern Next.js 14 application for the Riyadh Real Estate AI platform, built with TypeScript and Tailwind CSS.

## Features

- 🚀 Next.js 14 with App Router
- 💎 TypeScript for type safety
- 🎨 Tailwind CSS for styling
- 📦 Environment-based configuration
- 🔧 API integration ready

## Prerequisites

- Node.js 18.17 or later
- npm, yarn, pnpm, or bun

## Getting Started

### 1. Environment Setup

Copy the environment template and configure your API URL:

```bash
cp .env.local.template .env.local
```

Edit `.env.local` and set your API base URL:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

For production, set this to your production API URL.

### 2. Install Dependencies

```bash
npm install
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

### 4. Build for Production

```bash
npm run build
```

### 5. Start Production Server

```bash
npm start
```

## Available Scripts

- `npm run dev` - Start development server on http://localhost:3000
- `npm run build` - Create an optimized production build
- `npm start` - Start the production server
- `npm run lint` - Run ESLint to check code quality

## Project Structure

```
frontend/
├── src/
│   ├── app/           # Next.js App Router pages
│   │   ├── layout.tsx # Root layout
│   │   └── page.tsx   # Home page
│   └── lib/           # Utility functions
│       └── api.ts     # API configuration and helpers
├── public/            # Static assets
├── .env.local         # Local environment variables (not committed)
├── .env.local.template # Environment template
└── package.json       # Dependencies and scripts
```

## API Integration

The application uses the `NEXT_PUBLIC_API_URL` environment variable to configure the API base URL. 

See `src/lib/api.ts` for the API configuration and helper functions:

```typescript
import { API_BASE_URL, apiCall } from '@/lib/api';

// Make an API call
const data = await apiCall('/properties');
```

## Deploy on Vercel

The easiest way to deploy this Next.js app is to use the [Vercel Platform](https://vercel.com).

### Deployment Steps

1. **Push your code to GitHub** (if not already done)

2. **Import to Vercel:**
   - Go to [Vercel](https://vercel.com/new)
   - Import your GitHub repository
   - Vercel will automatically detect it's a Next.js project

3. **Configure Environment Variables:**
   - In the Vercel dashboard, go to your project settings
   - Navigate to "Environment Variables"
   - Add: `NEXT_PUBLIC_API_URL` with your production API URL
   - Example: `https://api.yourdomain.com/api`

4. **Deploy:**
   - Click "Deploy"
   - Vercel will build and deploy your application
   - You'll receive a live URL like: `https://your-app.vercel.app`

### Vercel CLI Deployment

Alternatively, use the Vercel CLI:

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Deploy to production
vercel --prod
```

### Environment Variables in Vercel

Set environment variables via CLI:

```bash
vercel env add NEXT_PUBLIC_API_URL production
```

Or via the Vercel Dashboard:
1. Go to Project Settings → Environment Variables
2. Add `NEXT_PUBLIC_API_URL` 
3. Set the value to your production API URL
4. Select the appropriate environment (Production/Preview/Development)

## Learn More

- [Next.js Documentation](https://nextjs.org/docs) - Learn about Next.js features and API
- [Next.js Deployment](https://nextjs.org/docs/app/building-your-application/deploying) - Deployment documentation
- [Vercel Documentation](https://vercel.com/docs) - Vercel platform documentation
- [Tailwind CSS](https://tailwindcss.com/docs) - Styling documentation

## Support

For issues and questions, please refer to the main repository.
