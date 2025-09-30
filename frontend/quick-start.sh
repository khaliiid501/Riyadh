#!/bin/bash

# Quick Start Script for Riyadh Real Estate AI Frontend
# This script helps you set up and run the frontend application

set -e

echo "🚀 Riyadh Real Estate AI Frontend - Quick Start"
echo "================================================"
echo ""

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "📝 Creating .env.local from template..."
    cp .env.local.template .env.local
    echo "✅ .env.local created!"
    echo ""
    echo "⚠️  Please edit .env.local and set your API URL"
    echo "   Current default: http://localhost:8000/api"
    echo ""
    read -p "Press Enter to continue or Ctrl+C to exit and configure first..."
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo "✅ Dependencies installed!"
    echo ""
fi

# Ask what to do
echo "What would you like to do?"
echo "1) Start development server (npm run dev)"
echo "2) Build for production (npm run build)"
echo "3) Start production server (npm start)"
echo "4) Run linter (npm run lint)"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🔧 Starting development server..."
        echo "Visit http://localhost:3000 in your browser"
        echo ""
        npm run dev
        ;;
    2)
        echo ""
        echo "🏗️  Building for production..."
        npm run build
        echo ""
        echo "✅ Build complete!"
        echo "Run './quick-start.sh' and choose option 3 to start the production server"
        ;;
    3)
        echo ""
        echo "🚀 Starting production server..."
        echo "Visit http://localhost:3000 in your browser"
        echo ""
        npm start
        ;;
    4)
        echo ""
        echo "🔍 Running linter..."
        npm run lint
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
