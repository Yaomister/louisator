# Louisator

Real-time computer-vision dashboard that streams live camera footage, tracks objects, and recognizes known faces. The system surfaces activity metrics and event notifications over WebSockets while persisting known-face metadata to a database and image storage to S3.

## Highlights
- Live video stream with object detection overlays (YOLO + OpenCV)
- Face recognition with a simple “known faces” upload flow
- Real-time event feed and activity analytics via WebSockets
- React + TypeScript dashboard with charts and alerts

## Tech Stack
- Frontend: React, TypeScript, Vite, Recharts, Axios
- Backend: FastAPI, SQLAlchemy (async), OpenCV, Ultralytics YOLO, face_recognition
- Data: PostgreSQL, AWS S3

## Architecture
- `backend/background_runner.py` runs a continuous CV pipeline: captures frames, detects objects, recognizes faces, and emits events
- `backend/main.py` exposes REST + WebSocket endpoints for video, metrics, and event streams
- `frontend/pages/Dashboard.tsx` renders live video, charts, and a rolling event log

## Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL
- AWS S3 bucket for known faces
- Local camera device

### Environment variables
Create a `.env` in `backend/`:
```
ACCESS_KEY=...
SECRET_ACCESS_KEY=...
DB=...
DB_HOST=...
DB_PORT=5432
DB_USER=...
DB_PASSWORD=...
```

### Backend
```
cd backend
python -m venv .venv
source .venv/bin/activate
# install dependencies for FastAPI, OpenCV, Ultralytics, face_recognition, SQLAlchemy
uvicorn main:app --reload --port 8000
```

### Frontend
```
cd frontend
npm install
npm run dev
```

## Key Endpoints
- `POST /known-faces` uploads a labeled face image
- `WS /camera` streams JPEG frames
- `WS /data` streams activity metrics
- `WS /events` streams detection events

## Resume Notes
This project demonstrates real-time CV processing, async backend design, WebSocket streaming, and a responsive analytics UI. It integrates ML inference, image storage, and database-backed metadata into a cohesive full-stack system.
