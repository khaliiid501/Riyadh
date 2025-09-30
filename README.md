# Riyadh
Predictive Real Estate Software

## Overview

Riyadh is an AI-powered real estate platform that provides predictive analytics and insights for the real estate market.

## Project Structure

This repository contains:

- **`/frontend`** - Next.js 14 web application with TypeScript and Tailwind CSS
  - Modern, responsive UI
  - Server-side rendering and static generation
  - API integration ready
  - Vercel deployment configured

## Getting Started

### Frontend

The frontend is a standalone Next.js 14 application located in the `./frontend` directory.

#### Quick Start

```bash
cd frontend
./quick-start.sh
```

Or manually:

```bash
cd frontend
cp .env.local.template .env.local
npm install
npm run dev
```

Visit http://localhost:3000 to see the application.

#### Documentation

- [Frontend README](./frontend/README.md) - Setup and development guide
- [Deployment Guide](./frontend/DEPLOYMENT.md) - Vercel deployment instructions
- [Separate Repository Guide](./frontend/SEPARATE_REPO_GUIDE.md) - How to extract frontend to its own repo

#### Environment Configuration

The frontend requires the following environment variable:

- `NEXT_PUBLIC_API_URL` - Backend API base URL (default: `http://localhost:8000/api`)

## Features

### Current
- ✅ Modern Next.js 14 frontend with TypeScript
- ✅ Tailwind CSS for styling
- ✅ Environment-based configuration
- ✅ API integration utilities
- ✅ Production-ready build
- ✅ Vercel deployment ready

### Planned
- 🔄 Backend API
- 🔄 Machine learning models for price prediction
- 🔄 Property search and filtering
- 🔄 Real-time market analytics
- 🔄 User authentication
- 🔄 Dashboard and visualizations

## Technology Stack

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Backend**: TBD
- **Database**: TBD
- **ML/AI**: TBD
- **Deployment**: Vercel (Frontend), TBD (Backend)

## Development

### Prerequisites

- Node.js 18.17 or later
- npm, yarn, pnpm, or bun

### Commands

```bash
# Frontend development
cd frontend
npm run dev      # Start development server
npm run build    # Build for production
npm start        # Start production server
npm run lint     # Run ESLint
```

## Deployment

### Frontend to Vercel

The frontend can be deployed to Vercel in minutes:

1. Push code to GitHub
2. Import repository to Vercel
3. Set `NEXT_PUBLIC_API_URL` environment variable
4. Deploy

See [Frontend Deployment Guide](./frontend/DEPLOYMENT.md) for detailed instructions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is private and proprietary.

## Support

For questions and support, please open an issue in this repository.

