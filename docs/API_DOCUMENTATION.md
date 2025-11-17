# API Documentation

## CogniSense Backend API

### Overview
CogniSense Backend is a FastAPI service that provides comprehensive digital footprint tracking with ML-powered content analysis. The system tracks user activity, analyzes content sentiment and emotions, categorizes browsing behavior, and provides dashboard analytics for insights.

### Base URL
```
http://localhost:8000
```

### API Version
All endpoints are versioned under `/api/v1/`

## Core Features

### 🔍 **Content Analysis**
- Real-time sentiment analysis with 99%+ confidence
- Emotion detection across 7 emotional states
- Zero-shot content categorization with 54 detailed categories

### 📊 **Activity Tracking** 
- Browser extension integration for seamless data collection
- Engagement metrics (clicks, keypresses, time spent)
- Automatic ML analysis pipeline

### 🎯 **Category Management**
- 54 comprehensive content categories organized into 8 groups
- User-customizable site preferences
- Intelligent content classification

### 📈 **Enhanced Dashboard Analytics**
- **Main Dashboard**: Weekly activity summaries with trend analysis and improvement tracking
- **Insights & Alerts**: Intelligent notifications about usage patterns, limits, and progress
- **Settings Management**: Domain categorization and time limit configuration
- **Health Scoring**: Overall digital wellness metrics and recommendations
- **Progress Tracking**: Goal-based progress monitoring with actionable insights
- **Emotional Analysis**: Content consumption emotional balance tracking

### 🔐 **Authentication & Security**
- Supabase-powered user authentication
- JWT token-based secure API access
- User-specific data isolation and privacy

---

## Endpoints Reference

### Default/Health

#### GET /

Root endpoint to verify service is running.

**Request:**
- No parameters required
- No authentication required

**Response:**
```json
{
    "status": "healthy",
    "service": "CogniSense Backend",
    "version": "1.0.0"
}
```

**Status Codes:**
- `200`: Service is healthy and running

---

#### GET /health

Detailed health check with ML model status.

**Request:**
- No parameters required
- No authentication required

**Response:**
```json
{
    "status": "healthy",
    "database": "connected",
    "ml_models_loaded": true
}
```

**Status Codes:**
- `200`: API is healthy and running

---

#### GET /api/v1/ping

Simple health check endpoint to verify API availability.

**Request:**
- No parameters required
- No authentication required

**Response:**
```json
{
    "message": "pong",
    "api_version": "v1"
}
```

**Status Codes:**
- `200`: API is healthy and running

---

### Authentication

#### POST /api/v1/auth/signup

Register a new user account with email and password.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string (EmailStr) | Yes | Valid email address |
| password | string | Yes | User password |

**Response:**
```json
{
    "user": {
        "id": "uuid-string",
        "email": "user@example.com",
        "created_at": "2025-11-16T12:00:00Z",
        "email_confirmed_at": null,
        "last_sign_in_at": null,
        "role": "authenticated",
        "updated_at": "2025-11-16T12:00:00Z"
    },
    "session": {
        "access_token": "jwt-token-string",
        "refresh_token": "refresh-token-string",
        "expires_in": 3600,
        "token_type": "bearer"
    }
}
```

**Status Codes:**
- `200`: User created successfully
- `400`: Invalid request data or signup failed
- `500`: Server configuration error

#### POST /api/v1/auth/login

Authenticate a user with email and password.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

**Response:**
```json
{
    "user": {
        "id": "uuid-string",
        "email": "user@example.com",
        "created_at": "2025-11-16T12:00:00Z",
        "email_confirmed_at": "2025-11-16T12:05:00Z",
        "last_sign_in_at": "2025-11-16T15:30:00Z",
        "role": "authenticated",
        "updated_at": "2025-11-16T15:30:00Z"
    },
    "session": {
        "access_token": "jwt-token-string",
        "refresh_token": "refresh-token-string",
        "expires_in": 3600,
        "token_type": "bearer"
    }
}
```

**Status Codes:**
- `200`: Login successful
- `401`: Invalid credentials or login failed
- `500`: Server configuration error

#### GET /api/v1/auth/me

Retrieve the authenticated user's information.

**Authentication Required:** Yes

**Request:**
- Headers: `Authorization: Bearer <token>`

**Response:**
```json
{
    "user": {
        "id": "uuid-string",
        "email": "user@example.com",
        "created_at": "2025-11-16T12:00:00Z",
        "email_confirmed_at": "2025-11-16T12:05:00Z",
        "last_sign_in_at": "2025-11-16T15:30:00Z",
        "role": "authenticated",
        "updated_at": "2025-11-16T15:30:00Z"
    }
}
```

**Status Codes:**
- `200`: User information retrieved successfully
- `401`: Invalid or expired token
- `500`: Server configuration error

---

### Content Analysis

#### POST /api/v1/content/analyze

Analyzes provided content for sentiment, emotion, and categorization.

**Request Body:**
```json
{
    "text": "This is a sample text to analyze",
    "url": "https://example.com",
    "analyze_sentiment": true,
    "analyze_category": true,
    "analyze_emotions": true
}
```

**Parameters:**
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| text | string | Yes | - | Text content to analyze |
| url | string | No | null | Source URL of the content |
| analyze_sentiment | boolean | No | true | Enable sentiment analysis |
| analyze_category | boolean | No | true | Enable content categorization |
| analyze_emotions | boolean | No | true | Enable emotion detection |

**Response:**
```json
{
    "text_length": 33,
    "word_count": 7,
    "url": "https://example.com",
    "sentiment": {
        "label": "POSITIVE",
        "score": 0.9999
    },
    "category": {
        "primary": "Programming",
        "confidence": 0.8234,
        "all_categories": [
            {"label": "Programming", "score": 0.8234},
            {"label": "Documentation", "score": 0.1123},
            {"label": "Learning", "score": 0.0643}
        ]
    },
    "emotions": {
        "dominant": {"label": "joy", "score": 0.9909},
        "all_emotions": [
            {"label": "joy", "score": 0.9909},
            {"label": "optimism", "score": 0.0046},
            {"label": "love", "score": 0.0023},
            {"label": "admiration", "score": 0.0011},
            {"label": "approval", "score": 0.0006}
        ],
        "balance": {
            "positive_score": 0.99,
            "negative_score": 0.01,
            "balance": 0.99,
            "is_balanced": false
        }
    }
}
```

#### POST /api/v1/content/analyze/batch

Analyze multiple text contents in a single request.

**Request Body:**
```json
{
    "texts": [
        "I love this new productivity app!",
        "Breaking news: Major tech announcement today",
        "Checking social media updates"
    ]
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| texts | array[string] | Yes | Array of text strings to analyze |

**Response:**
Returns an array of analysis results, one for each input text. Each result follows the same structure as the single analysis endpoint. Failed analyses will include an `"error"` field instead of analysis data.

**Status Codes:**
- `200`: Batch analysis completed (individual items may have errors)
- `400`: Invalid request data (empty array)

---

### Activity Tracking

#### POST /api/v1/tracking/ingest

Ingests activity data from browser extension with real-time ML analysis.

**Request Body:**
```json
{
    "user_id": "user123",
    "url": "https://github.com/example/repo",
    "title": "GitHub Repository",
    "text": "Python machine learning project with advanced algorithms",
    "start_ts": 1704067200.0,
    "end_ts": 1704067800.0,
    "duration_seconds": 600,
    "clicks": 15,
    "keypresses": 245,
    "engagement_score": 0.85
}
```

**Response:**
```json
{
    "status": "ok",
    "ingested": 1
}
```

#### GET /api/v1/tracking/activity/{user_id}

Retrieves recent activity records for a user.

**Query Parameters:**
- `limit` (optional): Number of records to return (1-1000, default: 100)

**Example:**
```bash
curl "http://localhost:8000/api/v1/tracking/activity/user123?limit=50"
```

**Response:**
```json
{
    "user_id": "user123",
    "count": 50,
    "items": [
        {
            "user_id": "user123",
            "url": "https://github.com/example/repo",
            "title": "GitHub Repository", 
            "text": "Python machine learning project with advanced algorithms",
            "duration_seconds": 600.0,
            "clicks": 15,
            "keypresses": 245,
            "sentiment": {
                "label": "POSITIVE",
                "confidence": 0.9999
            },
            "classified_category": "Programming",
            "category_group": "Productive",
            "emotions": {
                "joy": 0.9909,
                "optimism": 0.0046
            },
            "received_at": 1704067800.0
        }
    ]
}
```

#### DELETE /api/v1/tracking/activity/{user_id}

Clears all activity data for a user (useful for testing).

**Response:**
```json
{
    "status": "ok",
    "removed": 25
}
```

---

### Category Management

#### GET /api/v1/categories/labels

Returns all 54 available content categories.

**Response:**
```json
{
    "categories": [
        "Programming", "Documentation", "Code Review", "Technical Writing",
        "Social Media", "Messaging", "Video Calls", "Forums",
        "Streaming", "Gaming", "Music", "Videos", "Reading",
        "News", "Research", "Learning", "Reference",
        "Shopping", "Finance", "Travel", "Health",
        "Email", "Calendar", "Notes", "Utilities",
        "Adult Content", "Gambling", "Excessive Gaming",
        "Uncategorized", "Personal", "Other"
    ],
    "total": 54
}
```

#### GET /api/v1/categories/groups

Returns categories organized by functional groups.

**Response:**
```json
{
    "groups": {
        "Productive": ["Programming", "Documentation", "Code Review", "Technical Writing", "Project Management", "Development Tools", "Design"],
        "Social": ["Social Media", "Messaging", "Video Calls", "Forums", "Dating", "Community"],
        "Entertainment": ["Streaming", "Gaming", "Music", "Videos", "Reading", "Sports", "Hobbies"],
        "Information": ["News", "Research", "Learning", "Reference", "Science", "Technology"],
        "Lifestyle": ["Shopping", "Finance", "Travel", "Health", "Food", "Fitness", "Fashion"],
        "Commerce": ["Business", "Marketing", "Sales", "E-commerce", "Banking", "Investment"],
        "Problematic": ["Adult Content", "Gambling", "Excessive Gaming", "Harmful Content"],
        "Other": ["Uncategorized", "Personal", "Utilities", "Email", "Calendar", "Notes"]
    }
}
```

#### GET /api/v1/categories/classify

Classifies text using zero-shot classification.

**Query Parameters:**
- `text` (required): Text to classify

**Example:**
```bash
curl "http://localhost:8000/api/v1/categories/classify?text=Building%20a%20React%20application"
```

**Response:**
```json
{
    "labels": ["Programming", "Documentation", "Learning"],
    "scores": [0.8234, 0.1123, 0.0643]
}
```

#### GET /api/v1/categories/classify/grouped

Classifies text and returns both specific category and broad group.

**Query Parameters:**
- `text` (required): Text to classify

**Response:**
```json
{
    "labels": ["Programming", "Documentation"],
    "scores": [0.8234, 0.1123],
    "category_group": "Productive",
    "top_category": "Programming",
    "confidence": 0.8234
}
```

#### POST /api/v1/categories/user/{user_id}/sites

Sets user preference for site categorization.

**Request Body:**
```json
{
    "user_id": "user123",
    "site": "github.com",
    "category": "Programming"
}
```

**Response:**
```json
{
    "status": "ok",
    "site": "github.com",
    "category": "Programming"
}
```

#### GET /api/v1/categories/user/{user_id}/sites

Retrieves user's site categorization preferences.

**Response:**
```json
{
    "user_id": "user123",
    "preferences": {
        "github.com": "Programming",
        "youtube.com": "Entertainment",
        "stackoverflow.com": "Learning"
    }
}
```

#### POST /api/v1/user-domain-category/user_domain_category/save

Save user domain category and time limit settings.

**Request Body:**
```json
{
    "user_id": "user123",
    "domain_pattern": "github.com",
    "category": "Productivity",
    "priority": 1,
    "allowed_minutes": 480
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| user_id | string | Yes | User identifier |
| domain_pattern | string | Yes | Domain pattern to match |
| category | string | Yes | Category label |
| priority | integer | Yes | Priority for matching (higher = more important) |
| allowed_minutes | integer | Yes | Daily time limit in minutes |

**Response:**
```json
{
    "success": true,
    "category_result": {
        "user_id": "user123",
        "domain_pattern": "github.com",
        "category": "Productivity",
        "priority": 1
    },
    "limit_result": {
        "user_id": "user123",
        "domain": "github.com",
        "allowed_minutes": 480
    }
}
```

**Status Codes:**
- `200`: Settings saved successfully
- `400`: Invalid request data or duplicate key
- `500`: Server error

---

### Dashboard Analytics

All dashboard endpoints require authentication via Supabase JWT token.

**Authentication Required:** Yes (All endpoints)

**Request Header:**
```
Authorization: Bearer <SUPABASE_JWT_TOKEN>
```

#### GET /api/v1/dashboard

Returns main dashboard summary with time-based activity aggregation for the authenticated user.

**Query Parameters:**
- `timeRange` (optional): "this_week" or "last_week" (default: "this_week")

**Example:**
```bash
curl "http://localhost:8000/api/v1/dashboard?timeRange=this_week" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
    "user": {
        "id": "user-uuid",
        "displayName": "John Doe",
        "email": "user@example.com"
    },
    "timeRange": "this_week",
    "metrics": [
        {
            "title": "Total Time",
            "value": 14400,
            "change_percent": 15.5,
            "trend": "up",
            "improvement_label": "slightly_better"
        },
        {
            "title": "Productive Time",
            "value": 7200,
            "change_percent": 25.0,
            "trend": "up",
            "improvement_label": "much_better"
        },
        {
            "title": "Social Time",
            "value": 3600,
            "change_percent": -10.0,
            "trend": "down",
            "improvement_label": "slightly_better"
        },
        {
            "title": "Entertainment Time",
            "value": 3600,
            "change_percent": 5.0,
            "trend": "up",
            "improvement_label": "no_change"
        }
    ],
    "weeklyData": [
        {"day": "Mon", "Productive": 1200, "Social": 600, "Entertainment": 400},
        {"day": "Tue", "Productive": 1000, "Social": 500, "Entertainment": 600},
        {"day": "Wed", "Productive": 1100, "Social": 400, "Entertainment": 500},
        {"day": "Thu", "Productive": 1300, "Social": 700, "Entertainment": 600},
        {"day": "Fri", "Productive": 900, "Social": 800, "Entertainment": 700},
        {"day": "Sat", "Productive": 800, "Social": 300, "Entertainment": 900},
        {"day": "Sun", "Productive": 1100, "Social": 300, "Entertainment": 400}
    ]
}
```

**Notes:**
- `metrics[].value` is returned in **seconds**
- `weeklyData` values (Productive, Social, Entertainment) are in **minutes**
- Category mapping uses user-defined patterns from `user_domain_categories` table
- Compares current period with previous equal-length period for trend analysis

**Status Codes:**
- `200`: Dashboard data retrieved successfully
- `401`: Invalid or expired token
- `400`: Unable to determine user ID from auth payload

---

#### GET /api/v1/dashboard/insights

Provides detailed insights, alerts, and progress tracking for the authenticated user.

**Authentication Required:** Yes

**Query Parameters:**
- `timeRange` (optional): "this_week" or "last_week" (default: "this_week")

**Request:**
```bash
curl "http://localhost:8000/api/v1/dashboard/insights?timeRange=this_week" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
    "timeRange": "this_week",
    "summary": {
        "overallHealthScore": 75,
        "productiveTimeRatio": 50,
        "weeklyImprovementPercent": 15
    },
    "alerts": [
        {
            "id": "alert_progress",
            "type": "success",
            "title": "Great Progress!",
            "description": "Great job! Your productive screen time increased by 15% compared to last period."
        },
        {
            "id": "alert_social_limit",
            "type": "warning",
            "title": "Social Media Limit",
            "description": "Your usage for 'twitter.com' is 25% above your target for this period. Consider setting app limits."
        },
        {
            "id": "alert_neg_content",
            "type": "warning",
            "title": "Negative Content Alert",
            "description": "Your negative content consumption increased by 8% this period. Consider diversifying your sources."
        },
        {
            "id": "alert_bubble",
            "type": "info",
            "title": "Content Bubble Detected",
            "description": "You've been in a tech content bubble. Try exploring other topics for a balanced perspective."
        }
    ],
    "weeklyProgress": [
        {
            "goalId": "reduce_social_media",
            "label": "Reduce Social Media Time",
            "progressPercent": 65
        },
        {
            "goalId": "increase_productive_hours",
            "label": "Increase Productive Hours",
            "progressPercent": 75
        },
        {
            "goalId": "diversify_content",
            "label": "Diversify Content Sources",
            "progressPercent": 40
        }
    ],
    "emotionalBalance": {
        "balanceScore": 72,
        "segments": [
            {"type": "positive", "value": 45.2},
            {"type": "neutral", "value": 35.8},
            {"type": "negative", "value": 19.0},
            {"type": "biased", "value": 0}
        ]
    },
    "contentCategories": [
        {"category": "technology", "percentage": 35.5},
        {"category": "entertainment", "percentage": 25.0},
        {"category": "news", "percentage": 20.0},
        {"category": "social", "percentage": 15.5},
        {"category": "other", "percentage": 4.0}
    ]
}
```

**Notes:**
- Emotional balance aggregates emotions from `content_analysis` table for the period
- Alerts are heuristic and compare current vs previous equal-length period
- Progress tracking is based on simple goal metrics

**Status Codes:**
- `200`: Insights retrieved successfully
- `401`: Invalid or expired token
- `400`: Unable to determine user ID from auth payload

---

#### GET /api/v1/dashboard/settings

Returns user's domain categorization and time limit settings for the authenticated user.

**Authentication Required:** Yes

**Request:**
```bash
curl "http://localhost:8000/api/v1/dashboard/settings" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
    "websites": [
        {
            "name": "github.com",
            "category": "productive",
            "limit": 480
        },
        {
            "name": "twitter.com",
            "category": "social",
            "limit": 60
        },
        {
            "name": "youtube.com",
            "category": "entertainment",
            "limit": 120
        },
        {
            "name": "stackoverflow.com",
            "category": null,
            "limit": null
        }
    ]
}
```

**Notes:**
- `category` is derived from best substring match against `domain_pattern` in `user_domain_categories` (nullable)
- `limit` is `allowed_minutes` per day from `user_domain_limits` table (nullable, integer minutes)
- Combines data from recent sessions, user category patterns, and user time limits

**Status Codes:**
- `200`: Settings retrieved successfully
- `401`: Invalid or expired token
- `400`: Unable to determine user ID from auth payload

---

### Dashboard Summary

#### GET /api/v1/dashboard-summary/summary/{user_id}

Provides aggregated activity summary with time-based filtering.

**Query Parameters:**
- `period` (optional): "daily" or "weekly" (default: "weekly")

**Example:**
```bash
curl "http://localhost:8000/api/v1/dashboard-summary/summary/user123?period=weekly"
```

**Response:**
```json
{
    "user_id": "user123",
    "summary": {
        "period": "weekly",
        "records_counted": 42,
        "total_time_seconds": 14400,
        "top_sites": [
            {"site": "https://github.com", "time_seconds": 7200},
            {"site": "https://youtube.com", "time_seconds": 3600},
            {"site": "https://twitter.com", "time_seconds": 1800}
        ],
        "categories": [
            {"category": "Programming", "value": 7200, "proportion": 0.5},
            {"category": "Entertainment", "value": 3600, "proportion": 0.25},
            {"category": "Social Media", "value": 1800, "proportion": 0.125}
        ],
        "sentiments": [
            {"sentiment": "POSITIVE", "count": 30, "proportion": 0.71},
            {"sentiment": "NEGATIVE", "count": 12, "proportion": 0.29}
        ]
    }
}
```

**Status Codes:**
- `200`: Summary retrieved successfully
- `400`: Invalid request parameters

---

#### GET /api/v1/dashboard-summary/sites/{user_id}

Returns table view of sites with aggregated metrics.

**Query Parameters:**
- `limit` (optional): Number of sites to return (1-1000, default: 100)

**Example:**
```bash
curl "http://localhost:8000/api/v1/dashboard-summary/sites/user123?limit=50"
```

**Response:**
```json
{
    "user_id": "user123",
    "sites": [
        {
            "site": "https://github.com",
            "time_seconds": 7200,
            "visits": 15,
            "category": "Programming"
        },
        {
            "site": "https://youtube.com",
            "time_seconds": 3600,
            "visits": 8,
            "category": "Entertainment"
        },
        {
            "site": "https://twitter.com",
            "time_seconds": 1800,
            "visits": 12,
            "category": "Social Media"
        }
    ]
}
```

**Status Codes:**
- `200`: Sites data retrieved successfully
- `400`: Invalid request parameters

---

## Machine Learning Models

The API uses state-of-the-art transformer models for real-time analysis:

### **Sentiment Analysis**
- **Model**: `distilbert-base-uncased-finetuned-sst-2-english`
- **Capability**: Binary sentiment classification (POSITIVE/NEGATIVE)
- **Accuracy**: 99%+ confidence on clear sentiment expressions
- **Performance**: Optimized for real-time processing

### **Emotion Detection** 
- **Model**: `j-hartmann/emotion-english-distilroberta-base`
- **Emotions**: joy, sadness, anger, fear, surprise, disgust, optimism, love, admiration, approval, excitement, caring
- **Output**: Probability distribution across all emotions
- **Use Case**: Detailed emotional state analysis of browsing content

### **Content Categorization**
- **Model**: `typeform/distilbert-base-uncased-mnli` (Zero-shot)
- **Categories**: 54 detailed categories across 8 functional groups
- **Approach**: Zero-shot classification for maximum flexibility
- **Coverage**: Programming, Social Media, Entertainment, Learning, Shopping, etc.

## Integration Examples

### Browser Extension Integration

```javascript
// Ingest activity with content analysis
async function trackActivity(activityData) {
    const response = await fetch('http://localhost:8000/api/v1/tracking/ingest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_id: 'user123',
            url: window.location.href,
            title: document.title,
            text: extractPageText(),
            start_ts: Date.now() / 1000,
            duration_seconds: getSessionDuration(),
            clicks: getClickCount(),
            keypresses: getKeypressCount()
        })
    });
    return response.json();
}

// Get dashboard summary
async function getDashboard(userId, period = 'weekly') {
    const response = await fetch(
        `http://localhost:8000/api/v1/dashboard/summary/${userId}?period=${period}`
    );
    return response.json();
}
```

### Python Client Example

```python
import requests

# Analyze content
def analyze_content(text, url, user_id):
    response = requests.post('http://localhost:8000/api/v1/content/analyze', json={
        'text': text,
        'url': url,
        'user_id': user_id
    })
    return response.json()

# Get available categories
def get_categories():
    response = requests.get('http://localhost:8000/api/v1/categories/labels')
    return response.json()['categories']

# Classify text
def classify_text(text):
    response = requests.get(
        'http://localhost:8000/api/v1/categories/classify', 
        params={'text': text}
    )
    return response.json()
```

## Error Responses

#### 400 Bad Request
```json
{
    "detail": "user_id and url required"
}
```

#### 422 Unprocessable Entity  
```json
{
    "detail": [
        {
            "loc": ["body", "text"],
            "msg": "field required", 
            "type": "value_error.missing"
        }
    ]
}
```

#### 500 Internal Server Error
```json
{
    "detail": "Classification failed: Model not loaded"
}
```

## Performance & Deployment

### Model Loading
- **Strategy**: Lazy loading to optimize startup time
- **Memory**: Models load on first request to minimize resource usage
- **Caching**: Models remain in memory for subsequent requests

### Scalability Considerations
- **Phase 1**: In-memory storage for rapid prototyping
- **Phase 2**: Database integration planned for production scale
- **Optimization**: Model instances are shared across requests

### Rate Limiting
Currently no rate limiting is implemented, but will be added for production deployment.

### Authentication
Optional Supabase integration available. Authentication can be enabled through environment configuration for production use.