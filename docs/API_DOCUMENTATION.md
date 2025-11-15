# CogniSense API Documentation

## Overview

The CogniSense API is a FastAPI-based backend service that provides content analysis capabilities for digital footprint tracking. The API offers sentiment analysis, emotion detection, content categorization, and user authentication features.

**Base URL**: `http://localhost:8000` (development)  
**API Version**: v1  
**API Prefix**: `/api/v1`

---

## Authentication

The API uses Bearer token authentication with Supabase integration for user management.

### Headers
```
Authorization: Bearer <token>
Content-Type: application/json
```

---

## Endpoints

### 1. Health Check

#### `GET /api/v1/ping`

Simple health check endpoint to verify API availability.

**Request**
- No parameters required
- No authentication required

**Response**
```json
{
  "message": "pong",
  "api_version": "v1"
}
```

**Status Codes**
- `200`: API is healthy and running

---

## Authentication Endpoints

### 2. User Registration

#### `POST /api/v1/auth/signup`

Register a new user account with email and password.

**Request Body**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Parameters**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string (EmailStr) | Yes | Valid email address |
| password | string | Yes | User password |

**Response**
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

**Status Codes**
- `200`: User created successfully
- `400`: Invalid request data or signup failed
- `500`: Server configuration error

**Error Response**
```json
{
  "detail": "Signup failed: [error message]"
}
```

---

### 3. User Login

#### `POST /api/v1/auth/login`

Authenticate a user with email and password.

**Request Body**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Parameters**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string (EmailStr) | Yes | Registered email address |
| password | string | Yes | User password |

**Response**
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

**Status Codes**
- `200`: Login successful
- `401`: Invalid credentials or login failed
- `500`: Server configuration error

**Error Response**
```json
{
  "detail": "Login failed: [error message]"
}
```

---

### 4. Get Current User

#### `GET /api/v1/auth/me`

Retrieve the authenticated user's information.

**Authentication Required**: Yes

**Request**
- Headers: `Authorization: Bearer <token>`

**Response**
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

**Status Codes**
- `200`: User information retrieved successfully
- `401`: Invalid or expired token
- `500`: Server configuration error

**Error Response**
```json
{
  "detail": "Invalid or expired token"
}
```

---

## Content Analysis Endpoints

### 5. Analyze Content

#### `POST /api/v1/content/analyze`

Analyze text content for sentiment, emotions, and content categorization.

**Request Body**
```json
{
  "text": "I had an amazing day at work today! Really excited about the new project.",
  "url": "https://example.com/page",
  "analyze_sentiment": true,
  "analyze_category": true,
  "analyze_emotions": true
}
```

**Parameters**
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| text | string | Yes | - | Text content to analyze |
| url | string | No | null | Source URL of the content |
| analyze_sentiment | boolean | No | true | Enable sentiment analysis |
| analyze_category | boolean | No | true | Enable content categorization |
| analyze_emotions | boolean | No | true | Enable emotion detection |

**Response**
```json
{
  "text_length": 76,
  "word_count": 15,
  "url": "https://example.com/page",
  "sentiment": {
    "label": "POSITIVE",
    "score": 0.9998
  },
  "category": {
    "primary": "Productivity",
    "confidence": 0.85,
    "all_categories": [
      {
        "label": "Productivity",
        "score": 0.85
      },
      {
        "label": "Technology",
        "score": 0.12
      },
      {
        "label": "Other",
        "score": 0.03
      }
    ]
  },
  "emotions": {
    "dominant": {
      "label": "joy",
      "score": 0.89
    },
    "all_emotions": [
      {
        "label": "joy",
        "score": 0.89
      },
      {
        "label": "excitement",
        "score": 0.07
      },
      {
        "label": "optimism",
        "score": 0.03
      },
      {
        "label": "neutral",
        "score": 0.01
      }
    ],
    "balance": {
      "positive_score": 0.99,
      "negative_score": 0.01,
      "balance": 0.99
    }
  }
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| text_length | integer | Character count of analyzed text |
| word_count | integer | Word count of analyzed text |
| url | string | Source URL (if provided) |
| sentiment.label | string | Sentiment classification (POSITIVE, NEGATIVE, NEUTRAL) |
| sentiment.score | float | Confidence score (0.0-1.0) |
| category.primary | string | Primary content category |
| category.confidence | float | Confidence score for primary category |
| category.all_categories | array | Top 3 categories with scores |
| emotions.dominant | object | Highest scoring emotion |
| emotions.all_emotions | array | Top 5 emotions with scores |
| emotions.balance.positive_score | float | Sum of positive emotion scores |
| emotions.balance.negative_score | float | Sum of negative emotion scores |
| emotions.balance.balance | float | Emotional balance ratio (0.0=negative, 1.0=positive) |

**Available Content Categories**
- Productivity
- Social Media
- Entertainment
- News
- Shopping
- Education
- Health & Wellness
- Technology
- Finance
- Other

**Available Emotions**
- joy
- sadness
- anger
- fear
- disgust
- surprise
- love
- optimism
- excitement
- neutral

**Status Codes**
- `200`: Analysis completed successfully
- `400`: Invalid request data (missing text)
- `500`: Analysis processing error

**Error Response**
```json
{
  "detail": "Text content is required"
}
```

**Error Response (Processing Error)**
```json
{
  "detail": "Analysis failed: [error message]"
}
```

---

### 6. Batch Content Analysis

#### `POST /api/v1/content/analyze/batch`

Analyze multiple text contents in a single request.

**Request Body**
```json
{
  "texts": [
    "I love this new productivity app!",
    "Breaking news: Major tech announcement today",
    "Checking social media updates"
  ]
}
```

**Parameters**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| texts | array[string] | Yes | Array of text strings to analyze |

**Response**
```json
[
  {
    "text_length": 33,
    "word_count": 6,
    "url": null,
    "sentiment": {
      "label": "POSITIVE",
      "score": 0.9956
    },
    "category": {
      "primary": "Productivity",
      "confidence": 0.92,
      "all_categories": [
        {
          "label": "Productivity",
          "score": 0.92
        },
        {
          "label": "Technology",
          "score": 0.06
        },
        {
          "label": "Other",
          "score": 0.02
        }
      ]
    },
    "emotions": {
      "dominant": {
        "label": "joy",
        "score": 0.87
      },
      "all_emotions": [
        {
          "label": "joy",
          "score": 0.87
        },
        {
          "label": "love",
          "score": 0.10
        },
        {
          "label": "excitement",
          "score": 0.03
        }
      ],
      "balance": {
        "positive_score": 1.0,
        "negative_score": 0.0,
        "balance": 1.0
      }
    }
  },
  {
    "text_length": 42,
    "word_count": 7,
    "url": null,
    "sentiment": {
      "label": "NEUTRAL",
      "score": 0.8234
    },
    "category": {
      "primary": "News",
      "confidence": 0.95,
      "all_categories": [
        {
          "label": "News",
          "score": 0.95
        },
        {
          "label": "Technology",
          "score": 0.04
        },
        {
          "label": "Other",
          "score": 0.01
        }
      ]
    },
    "emotions": {
      "dominant": {
        "label": "neutral",
        "score": 0.65
      },
      "all_emotions": [
        {
          "label": "neutral",
          "score": 0.65
        },
        {
          "label": "excitement",
          "score": 0.20
        },
        {
          "label": "curiosity",
          "score": 0.15
        }
      ],
      "balance": {
        "positive_score": 0.35,
        "negative_score": 0.0,
        "balance": 1.0
      }
    }
  }
]
```

**Response**
- Returns an array of analysis results, one for each input text
- Each result follows the same structure as the single analysis endpoint
- Failed analyses will include an `"error"` field instead of analysis data

**Status Codes**
- `200`: Batch analysis completed (individual items may have errors)
- `400`: Invalid request data (empty array)

**Error Response**
```json
{
  "detail": "At least one text required"
}
```

**Individual Item Error Response**
```json
{
  "error": "[error message for this specific text]"
}
```

---

## Rate Limiting

Currently, there are no rate limits implemented, but they may be added in future versions.

---

## Error Handling

### Standard Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Invalid or missing authentication |
| 404 | Not Found - Endpoint doesn't exist |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server-side processing error |

---

## Data Models

### Sentiment Analysis Result
```json
{
  "label": "POSITIVE|NEGATIVE|NEUTRAL",
  "score": 0.0-1.0
}
```

### Emotion Detection Result
```json
{
  "label": "emotion_name",
  "score": 0.0-1.0
}
```

### Category Classification Result
```json
{
  "primary": "category_name",
  "confidence": 0.0-1.0,
  "all_categories": [
    {
      "label": "category_name",
      "score": 0.0-1.0
    }
  ]
}
```

### Emotional Balance Metrics
```json
{
  "positive_score": 0.0-1.0,
  "negative_score": 0.0-1.0,
  "balance": 0.0-1.0
}
```

---

## Example Usage

### cURL Examples

#### Health Check
```bash
curl -X GET "http://localhost:8000/api/v1/ping"
```

#### User Signup
```bash
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

#### Content Analysis
```bash
curl -X POST "http://localhost:8000/api/v1/content/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I absolutely love this new productivity tool!",
    "url": "https://example.com/review",
    "analyze_sentiment": true,
    "analyze_category": true,
    "analyze_emotions": true
  }'
```

#### Authenticated Request
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### JavaScript/Fetch Examples

#### Content Analysis
```javascript
const analyzeContent = async (text, url = null) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/content/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        url,
        analyze_sentiment: true,
        analyze_category: true,
        analyze_emotions: true
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Analysis failed:', error);
    throw error;
  }
};

// Usage
analyzeContent("This is an amazing article about productivity!")
  .then(result => console.log(result))
  .catch(error => console.error(error));
```

#### User Authentication
```javascript
const login = async (email, password) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }
    
    const result = await response.json();
    
    // Store the token for future requests
    localStorage.setItem('access_token', result.session.access_token);
    
    return result;
  } catch (error) {
    console.error('Login failed:', error);
    throw error;
  }
};
```

---

## Development Notes

### Text Processing Limitations
- Text inputs are automatically truncated to 512 words for optimal model performance
- Empty or whitespace-only text will return default/neutral results with appropriate error messages

### Model Information
- **Sentiment Analysis**: Uses pre-trained transformer models via Hugging Face
- **Emotion Detection**: Multi-label emotion classification with confidence scores
- **Category Classification**: Zero-shot classification for content categorization
- **Model Loading**: Models are loaded once at startup and cached in memory

### CORS Configuration
The API is configured with CORS middleware to allow requests from browser extensions and web applications.

---

## Support

For questions or issues with the API, please refer to the project documentation or create an issue in the repository.

**Repository**: [cognisense-backend](https://github.com/DhruvPokhriyal/cognisense-backend)  
**API Version**: 1.0.0  
**Last Updated**: November 2025