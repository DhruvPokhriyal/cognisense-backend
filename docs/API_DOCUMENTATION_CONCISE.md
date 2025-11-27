# CogniSense API - Concise Documentation

## Base URL
```
http://localhost:8000/api/v1/
```

## Overview
FastAPI service for digital footprint tracking with ML-powered content analysis, sentiment detection, emotion analysis, and dashboard analytics.

## Authentication
Most endpoints require JWT token in header: `Authorization: Bearer <token>`

---

## Endpoints

### Health Check
- **GET** `/ping` - Health check (no auth required)
  ```json
  {"message": "pong", "api_version": "v1"}
  ```

### Authentication
- **POST** `/auth/signup` - Register user
  ```json
  {
    "user": {"id": "uuid", "email": "user@example.com"},
    "session": {"access_token": "jwt-token", "expires_in": 3600}
  }
  ```
- **POST** `/auth/login` - Login user
  ```json
  {
    "user": {"id": "uuid", "email": "user@example.com"},
    "session": {"access_token": "jwt-token", "expires_in": 3600}
  }
  ```
- **GET** `/auth/me` - Get current user info
  ```json
  {
    "user": {"id": "uuid", "email": "user@example.com", "role": "authenticated"}
  }
  ```

### Content Analysis
- **POST** `/content/analyze` - Analyze text for sentiment, emotions, categorization
  ```json
  {
    "sentiment": {"label": "POSITIVE", "score": 0.99},
    "category": {"primary": "Programming", "confidence": 0.82},
    "emotions": {"dominant": {"label": "joy", "score": 0.99}}
  }
  ```
- **POST** `/content/analyze/batch` - Batch analyze multiple texts
  ```json
  [
    {"sentiment": {"label": "POSITIVE", "score": 0.99}},
    {"sentiment": {"label": "NEGATIVE", "score": 0.85}}
  ]
  ```

### Activity Tracking
- **POST** `/tracking/ingest` - Ingest activity data with ML analysis
  ```json
  {"status": "ok", "ingested": 1}
  ```
- **GET** `/tracking/activity/{user_id}` - Get user activity records
  ```json
  {
    "user_id": "user123", "count": 50,
    "items": [{"url": "https://example.com", "duration_seconds": 600}]
  }
  ```
- **DELETE** `/tracking/activity/{user_id}` - Clear user activity data
  ```json
  {"status": "ok", "removed": 25}
  ```

### Categories
- **GET** `/categories/labels` - Get all 54 content categories
  ```json
  {"categories": ["Programming", "Social Media", "Gaming"], "total": 54}
  ```
- **GET** `/categories/groups` - Get categories organized by groups
  ```json
  {"groups": {"Productive": ["Programming"], "Social": ["Social Media"]}}
  ```
- **GET** `/categories/classify?text=<text>` - Classify text into categories
  ```json
  {"labels": ["Programming"], "scores": [0.82]}
  ```
- **POST** `/categories/user/{user_id}/sites` - Set user site preferences
  ```json
  {"status": "ok", "site": "github.com", "category": "Programming"}
  ```
- **GET** `/categories/user/{user_id}/sites` - Get user site preferences
  ```json
  {"user_id": "user123", "preferences": {"github.com": "Programming"}}
  ```

### Dashboard (Auth Required)
- **GET** `/dashboard?timeRange=this_week` - Main dashboard with metrics
  ```json
  {
    "metrics": [{"title": "Total Time", "value": 14400, "change_percent": 15.5}],
    "weeklyData": [{"day": "Mon", "Productive": 1200}]
  }
  ```
- **GET** `/dashboard/insights?timeRange=this_week` - Detailed insights & alerts
  ```json
  {
    "summary": {"overallHealthScore": 75},
    "alerts": [{"type": "success", "title": "Great Progress!"}],
    "weeklyProgress": [{"goalId": "reduce_social_media", "progressPercent": 65}]
  }
  ```
- **GET** `/dashboard/settings` - User domain categorization settings
  ```json
  {
    "websites": [{"name": "github.com", "category": "productive", "limit": 480}]
  }
  ```

---

## Key Request/Response Examples

### Content Analysis
```bash
POST /content/analyze
{
  "text": "Building a React app",
  "analyze_sentiment": true,
  "analyze_emotions": true
}

Response:
{
  "sentiment": {"label": "POSITIVE", "score": 0.99},
  "category": {"primary": "Programming", "confidence": 0.82},
  "emotions": {"dominant": {"label": "joy", "score": 0.99}}
}
```

### Activity Ingestion
```bash
POST /tracking/ingest
{
  "user_id": "user123",
  "url": "https://github.com/repo",
  "title": "GitHub Repo",
  "text": "Python ML project",
  "duration_seconds": 600,
  "clicks": 15,
  "keypresses": 245
}

Response: {"status": "ok", "ingested": 1}
```

### Dashboard Data
```bash
GET /dashboard?timeRange=this_week
Authorization: Bearer <token>

Response:
{
  "metrics": [
    {"title": "Total Time", "value": 14400, "change_percent": 15.5},
    {"title": "Productive Time", "value": 7200, "change_percent": 25.0}
  ],
  "weeklyData": [
    {"day": "Mon", "Productive": 1200, "Social": 600}
  ]
}
```

---

## ML Models
- **Sentiment**: `distilbert-base-uncased-finetuned-sst-2-english`
- **Emotions**: `j-hartmann/emotion-english-distilroberta-base`
- **Categories**: `typeform/distilbert-base-uncased-mnli` (Zero-shot)

## Categories (54 total)
**Groups**: Productive, Social, Entertainment, Information, Lifestyle, Commerce, Problematic, Other

**Examples**: Programming, Social Media, Gaming, News, Shopping, Finance, Adult Content, etc.

## Common Status Codes
- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `422`: Validation Error
- `500`: Server Error

## Authentication Flow
1. **POST** `/auth/signup` or `/auth/login`
2. Use returned `access_token` in `Authorization: Bearer <token>` header
3. Access protected endpoints like `/dashboard`