# Project Setup and Run Guide

This is a full-stack application with a FastAPI backend and React frontend.

## Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** and **Yarn** (for frontend)
- **MongoDB Atlas** (cloud MongoDB - cluster0.oaalese.mongodb.net)
- **Google Gemini API Key** (for AI chat functionality)

## Backend Setup

### 1. Navigate to backend directory
```bash
cd backend
```

### 2. Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
Create a `.env` file in the `backend` directory with the following variables:

```env
MONGO_URL=mongodb+srv://admin:YOUR_PASSWORD@cluster0.oaalese.mongodb.net/?retryWrites=true&w=majority
DB_NAME=cleardemand
GEMINI_API_KEY=xxxx
CORS_ORIGINS=http://localhost:3000
```

**Note:** 
- Replace `YOUR_PASSWORD` in `MONGO_URL` with your actual MongoDB Atlas password
- The connection string format is: `mongodb+srv://username:password@cluster0.oaalese.mongodb.net/?retryWrites=true&w=majority`
- Replace `GEMINI_API_KEY` with your Google Gemini API key
- Adjust `CORS_ORIGINS` if your frontend runs on a different port
- Make sure your MongoDB Atlas IP whitelist allows connections (add `0.0.0.0/0` for development)

### 5. Run the backend server
**Important:** Make sure you're in the `backend` directory when running this command:

```bash
# Make sure you're in the backend directory
cd backend
source venv/bin/activate  # Activate virtual environment if not already active
uvicorn server:app --reload --port 8000
```

The backend will run on `http://localhost:8000` by default.

**Note:** If you're running from the parent directory, use: `uvicorn backend.server:app --reload --port 8000`

## Frontend Setup

### 1. Navigate to frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
yarn install
```

### 3. Create `.env` file
Create a `.env` file in the `frontend` directory with:

```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

**Note:** Adjust the URL if your backend runs on a different port or host.

### 4. Run the frontend
```bash
yarn start
```

The frontend will run on `http://localhost:3000` and automatically open in your browser.

## Running the Complete Application

### Option 1: Run in separate terminals

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # If using virtual environment
uvicorn server:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
yarn start
```

### Option 2: Using a process manager (optional)

You can use tools like `concurrently` or `foreman` to run both servers together.

## Verification

1. **Backend**: Visit `http://localhost:8000/api/` - you should see `{"message": "ClearDemand AI Pricing Analyst API"}`

2. **Frontend**: Visit `http://localhost:3000` - you should see the ClearDemand chat interface

3. **Test Chat**: Send a message in the chat interface - it should get a response from Gemini AI

## Troubleshooting

### Backend Issues
- **MongoDB Connection Error**: 
  - Ensure `MONGO_URL` is correct and includes your password
  - Check that your MongoDB Atlas cluster is running
  - Verify your IP address is whitelisted in MongoDB Atlas (Network Access)
  - Make sure the database user has proper permissions
- **Module Not Found**: Make sure all dependencies are installed with `pip install -r requirements.txt`
- **Port Already in Use**: Change the port with `--port 8001` or kill the process using port 8000
- **Gemini API Errors**: Check that your `GEMINI_API_KEY` is valid and has proper permissions

### Frontend Issues
- **Cannot connect to backend**: Check that `REACT_APP_BACKEND_URL` matches your backend URL
- **CORS errors**: Ensure `CORS_ORIGINS` in backend `.env` includes your frontend URL
- **Dependencies not installing**: Try deleting `node_modules` and `yarn.lock`, then run `yarn install` again

## Environment Variables Summary

### Backend (`backend/.env`)
- `MONGO_URL` - MongoDB connection string (required)
- `DB_NAME` - Database name (required)
- `GEMINI_API_KEY` - Google Gemini API key (required for AI functionality)
- `CORS_ORIGINS` - Comma-separated list of allowed frontend origins (required)

### Frontend (`frontend/.env`)
- `REACT_APP_BACKEND_URL` - Backend API URL (default: `http://localhost:8000`)

## Project Structure

```
app/
├── backend/
│   ├── server.py          # FastAPI application
│   ├── requirements.txt   # Python dependencies
│   └── .env              # Backend environment variables (create this)
├── frontend/
│   ├── src/              # React source code
│   ├── package.json      # Node dependencies
│   └── .env             # Frontend environment variables (create this)
└── SETUP.md             # This file
```

## Getting a Gemini API Key

If you need a Gemini API key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `backend/.env` file as `GEMINI_API_KEY`

