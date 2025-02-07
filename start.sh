#!/bin/bash

# Kill any existing processes on ports 8000 and 5173 (default ports for FastAPI and Vite)
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:5173 | xargs kill -9 2>/dev/null

# Start the API server
echo "Starting FastAPI backend..."
cd api && uvicorn main:app --reload &

# Wait a moment for the API to start
sleep 2

# Start the frontend development server
echo "Starting Svelte frontend..."
cd frontend && npm run dev -- --open &

# Keep script running and show logs
wait
