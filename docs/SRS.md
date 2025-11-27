# Software Requirements Specification (SRS)

## CogniSense Backend - Digital Footprint Tracking and Analysis Platform

**Version:** 1.0.0  
**Date:** November 27, 2025  
**Document Status:** Draft  
**Project Phase:** MVP Phase 1

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Features and Requirements](#3-system-features-and-requirements)
4. [External Interface Requirements](#4-external-interface-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [System Architecture](#6-system-architecture)
7. [Data Requirements](#7-data-requirements)
8. [Appendices](#8-appendices)

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification document provides a comprehensive description of the CogniSense Backend system. The document defines functional and non-functional requirements for the digital footprint tracking and analysis platform designed to help users understand their online consumption patterns and the emotional impact of digital content.

The intended audience includes:
- Professor (Project Supervisor)
- Teaching Assistant (TA)
- Project Lead
- Development team members
- Quality assurance engineers
- System architects

### 1.2 Scope

**Product Name:** CogniSense Backend

**Product Description:** CogniSense is a FastAPI-based backend service that powers a digital footprint tracking and analysis platform. The system integrates with browser extensions to capture user browsing activity, performs machine learning-powered analysis on content consumption, and provides comprehensive analytics through dashboard APIs.

**Key Capabilities:**
- Real-time content analysis using machine learning models
- Browsing activity tracking and aggregation
- Sentiment, emotion, and category classification
- User-specific domain categorization
- Dashboard analytics with weekly summaries and insights
- Time limit management for digital wellness
- Secure authentication and user data isolation

**Benefits:**
- Enhanced self-awareness of digital consumption patterns
- Emotional impact assessment of consumed content
- Data-driven insights for improving digital wellness
- Personalized content categorization
- Privacy-focused, user-controlled data management

### 1.3 Definitions, Acronyms, and Abbreviations

| Term | Definition |
|------|------------|
| API | Application Programming Interface |
| ASGI | Asynchronous Server Gateway Interface |
| JWT | JSON Web Token |
| ML | Machine Learning |
| NLP | Natural Language Processing |
| MVP | Minimum Viable Product |
| CORS | Cross-Origin Resource Sharing |
| REST | Representational State Transfer |
| UUID | Universally Unique Identifier |
| JSONB | JSON Binary (PostgreSQL data type) |
| BERT | Bidirectional Encoder Representations from Transformers |
| BART | Bidirectional and Auto-Regressive Transformers |

### 1.4 References

- FastAPI Documentation: https://fastapi.tiangolo.com
- Hugging Face Transformers: https://huggingface.co/docs/transformers
- Supabase Documentation: https://supabase.com/docs
- PostgreSQL Documentation: https://www.postgresql.org/docs
- REST API Design Guidelines: https://restfulapi.net

### 1.5 Document Overview

This document is organized into eight major sections covering introduction, system description, functional requirements, interface specifications, non-functional requirements, architecture, data requirements, and appendices. Each section provides detailed specifications necessary for system implementation and verification.

---

## 2. Overall Description

### 2.1 Product Perspective

CogniSense Backend operates as a standalone RESTful API service that integrates with:

**External Systems:**
- Browser extension (Chrome/Firefox) for data collection
- Supabase for authentication and PostgreSQL database management
- Hugging Face model repository for ML models

**System Context:**
The backend serves as the central processing and storage hub in a client-server architecture where browser extensions act as data collectors, the backend performs analysis and storage, and future frontend applications consume the analytics data.

### 2.2 Product Functions

**Core Functions:**

1. **Content Analysis**
   - Sentiment analysis with confidence scoring
   - Emotion detection across seven emotional states
   - Zero-shot content categorization into 54 categories
   - Text processing and metadata extraction

2. **Activity Tracking**
   - Browser session recording
   - Engagement metrics collection (clicks, keypresses, time)
   - Domain-level activity aggregation
   - Temporal data analysis

3. **User Management**
   - Account registration and authentication
   - Profile management
   - User-specific data isolation
   - Session management with JWT tokens

4. **Dashboard Analytics**
   - Weekly activity summaries
   - Trend analysis and comparisons
   - Category-based time distribution
   - Emotional balance tracking
   - Progress monitoring against goals

5. **Category Management**
   - Predefined category system (54 categories, 8 groups)
   - User-customizable domain categorization
   - Priority-based category assignment
   - Category group organization

6. **Time Limit Management**
   - Daily time limit configuration per domain
   - Usage tracking against limits
   - Alert system for limit violations

### 2.3 User Classes and Characteristics

**End Users:**
- Technical Level: Non-technical to moderate
- Frequency: Daily active users
- Primary Goals: Monitor and improve digital wellness
- Key Needs: Privacy, ease of use, actionable insights

**System Administrators:**
- Technical Level: Advanced
- Responsibilities: System maintenance, monitoring, deployment
- Key Needs: Monitoring tools, logging, error tracking

**Developers:**
- Technical Level: Expert
- Responsibilities: Feature development, bug fixes, optimization
- Key Needs: API documentation, development environment, testing tools

### 2.4 Operating Environment

**Server Environment:**
- Operating System: Linux (Docker containerized)
- Python Runtime: 3.12 or higher
- ASGI Server: Uvicorn
- Database: Supabase-managed PostgreSQL 16
- Authentication: Supabase Auth service
- Cloud Platform: Railway/Render (recommended) or self-hosted

**Client Environment:**
- Browser Extensions: Chrome/Firefox latest versions
- HTTP Protocol: HTTPS (production)
- Network: Standard internet connectivity

**Development Environment:**
- Local: macOS/Linux/Windows with Docker
- Package Manager: Poetry 1.8+
- Version Control: Git

### 2.5 Design and Implementation Constraints

**Technical Constraints:**
- Must use Python and FastAPI framework
- Must use Hugging Face Transformers for ML
- Must maintain backward compatibility with browser extension API
- Must support PostgreSQL database

**Business Constraints:**
- MVP timeline prioritizes speed to market
- Limited DevOps resources requiring simple deployment
- Free-tier hosting compatibility required

**Security Constraints:**
- JWT-based authentication required
- User data must be isolated per account
- Passwords must be hashed using bcrypt
- CORS policies must be enforced

**Performance Constraints:**
- API response time < 2 seconds for analysis endpoints
- ML model loading time < 30 seconds on startup
- Support for concurrent user requests

### 2.6 Assumptions and Dependencies

**Assumptions:**
- Users have modern web browsers with extension support
- Network connectivity is stable for real-time tracking
- Users consent to data collection and analysis
- ML models remain accessible from Hugging Face
- Supabase service (auth and database) remains operational

**Dependencies:**
- Supabase for authentication and managed PostgreSQL database
- Hugging Face model repository availability
- Python package ecosystem (PyPI)
- Docker containerization platform
- Internet connectivity for model downloads and Supabase API access

---

## 3. System Features and Requirements

### 3.1 Authentication and Authorization

**Priority:** High  
**Description:** Secure user registration, login, and session management system.

#### 3.1.1 User Registration

**FR-AUTH-001:** The system shall allow new users to register with email and password.

**Inputs:**
- Email address (valid format)
- Password (minimum length enforced)

**Processing:**
- Validate email format
- Check for existing account
- Hash password using bcrypt
- Create user record in Supabase Auth
- Create corresponding profile record
- Generate JWT access and refresh tokens

**Outputs:**
- User object with UUID identifier
- Session object with JWT tokens
- HTTP 200 on success, 400 on validation failure

#### 3.1.2 User Login

**FR-AUTH-002:** The system shall authenticate users with valid credentials.

**Inputs:**
- Email address
- Password

**Processing:**
- Validate credentials against Supabase Auth
- Verify account status
- Generate new JWT tokens
- Update last sign-in timestamp

**Outputs:**
- User object
- Session object with JWT tokens
- HTTP 200 on success, 401 on invalid credentials

#### 3.1.3 User Session Management

**FR-AUTH-003:** The system shall maintain user sessions using JWT tokens.

**Requirements:**
- Access tokens shall expire after 60 minutes
- Refresh tokens shall be provided for session renewal
- Invalid tokens shall return HTTP 401 Unauthorized
- Token validation shall occur on protected endpoints

#### 3.1.4 User Profile Retrieval

**FR-AUTH-004:** The system shall allow authenticated users to retrieve their profile information.

**Processing:**
- Validate JWT token
- Retrieve user data from Supabase Auth
- Return user profile details

**Outputs:**
- User object with id, email, timestamps, and role
- HTTP 200 on success, 401 on invalid token

### 3.2 Content Analysis

**Priority:** High  
**Description:** Machine learning-powered analysis of web content for sentiment, emotion, and categorization.

#### 3.2.1 Text Content Analysis

**FR-CONTENT-001:** The system shall analyze text content for sentiment classification.

**Inputs:**
- Text content (required, non-empty)
- Optional URL reference
- Analysis flags (sentiment, category, emotions)

**Processing:**
- Use DistilBERT model for sentiment analysis
- Classify as POSITIVE, NEGATIVE, or NEUTRAL
- Generate confidence scores
- Return top prediction with score

**Outputs:**
- Sentiment label
- Confidence score (0-1)
- HTTP 200 on success, 400 on invalid input

**Performance:** Response time < 2 seconds for texts up to 5000 characters

#### 3.2.2 Emotion Detection

**FR-CONTENT-002:** The system shall detect emotional content across seven emotion categories.

**Emotion Categories:**
- Joy
- Anger
- Sadness
- Fear
- Surprise
- Disgust
- Neutral

**Processing:**
- Use emotion-english-distilroberta-base model
- Generate scores for all seven emotions
- Identify dominant emotion
- Calculate confidence metrics

**Outputs:**
- Scores for all seven emotions (0-1 range)
- Dominant emotion label
- Confidence score

#### 3.2.3 Content Categorization

**FR-CONTENT-003:** The system shall classify content into predefined categories using zero-shot classification.

**Category System:**
- Total categories: 54
- Category groups: 8 (Productive, Social, Entertainment, News, Shopping, Health, Finance, Other)

**Processing:**
- Use BART-large-mnli model for zero-shot classification
- Match content against category labels
- Generate probability scores
- Return top-k predictions

**Outputs:**
- Ranked list of category labels
- Confidence scores for each category
- Category group assignment

#### 3.2.4 Combined Analysis

**FR-CONTENT-004:** The system shall support combined analysis requests with configurable analysis modules.

**Requirements:**
- Support selective activation of analysis modules
- Perform requested analyses in parallel when possible
- Return combined results in single response
- Handle partial failures gracefully

### 3.3 Activity Tracking

**Priority:** High  
**Description:** Recording and storage of user browsing activity with automatic ML analysis.

#### 3.3.1 Activity Data Ingestion

**FR-TRACK-001:** The system shall receive and store browsing activity data from browser extensions.

**Required Fields:**
- User ID (UUID)
- URL
- Start timestamp
- End timestamp

**Optional Fields:**
- Page title
- Scraped text content
- Click count
- Keypress count
- Engagement score
- Category override

**Processing:**
- Validate required fields
- Calculate duration if not provided
- Perform automatic ML analysis if text provided
- Store session data in database
- Link to user profile

**Outputs:**
- Stored session record
- Optional analysis results
- HTTP 200 on success

#### 3.3.2 Session Recording

**FR-TRACK-002:** The system shall create page view session records with timing information.

**Database Storage:**
- Table: page_view_sessions
- Fields: session_id, user_id, url, domain, start_time, end_time

**Requirements:**
- Extract domain from URL
- Store timestamps in UTC
- Link to user profile with foreign key
- Support cascade deletion

#### 3.3.3 Engagement Metrics

**FR-TRACK-003:** The system shall track user engagement metrics per session.

**Metrics:**
- Click count
- Keypress count
- Time spent (duration)
- Engagement score (derived)

**Processing:**
- Calculate engagement score from interaction metrics
- Normalize scores to 0-1 range
- Store with session record

#### 3.3.4 Automatic Content Analysis

**FR-TRACK-004:** The system shall automatically analyze page content during activity ingestion when text is provided.

**Processing:**
- Trigger ML analysis for provided text
- Store analysis results in content_analysis table
- Link analysis to URL
- Handle duplicate URLs with update or skip logic

### 3.4 Dashboard Analytics

**Priority:** Medium  
**Description:** Aggregated analytics and insights for user consumption patterns.

#### 3.4.1 Weekly Summary

**FR-DASH-001:** The system shall generate weekly activity summaries for authenticated users.

**Time Ranges:**
- This week (Monday-Sunday)
- Last week (previous Monday-Sunday)

**Metrics:**
- Total time spent
- Time by category (productive, social, entertainment)
- Daily breakdown (7 days)
- Week-over-week change percentages

**Processing:**
- Query page_view_sessions for date range
- Aggregate durations by category
- Calculate change metrics
- Generate trend labels (much_better, slightly_better, no_change, slight_worse, much_worse)

**Outputs:**
- Total seconds by category
- Daily time series data
- Change percentages
- Trend indicators

#### 3.4.2 Category-Based Analytics

**FR-DASH-002:** The system shall categorize sessions using user-defined domain patterns.

**Processing:**
- Load user_domain_categories for user
- Match session domains against patterns
- Apply highest priority match
- Default to "uncategorized" if no match

**Requirements:**
- Support pattern matching (substring)
- Case-insensitive matching
- Priority-based conflict resolution

#### 3.4.3 Insights and Alerts

**FR-DASH-003:** The system shall generate intelligent insights about usage patterns.

**Insight Types:**
- Time limit violations
- Usage pattern changes
- Progress toward goals
- Recommendations

**Requirements:**
- Query user limits from user_domain_limits table
- Compare actual usage against limits
- Generate actionable notifications
- Support pagination and filtering

#### 3.4.4 Settings Management

**FR-DASH-004:** The system shall provide endpoints for managing dashboard settings.

**Capabilities:**
- Configure time limits per domain
- Set category preferences
- Update notification settings
- Manage goal definitions

### 3.5 Category Management

**Priority:** Medium  
**Description:** User-customizable content categorization system.

#### 3.5.1 Predefined Categories

**FR-CAT-001:** The system shall maintain a predefined taxonomy of 54 content categories organized into 8 groups.

**Category Groups:**
1. Productive (Work, Education, Research, Programming, Documentation, etc.)
2. Social (Social Media, Messaging, Forums, Dating, etc.)
3. Entertainment (Streaming, Gaming, Music, Videos, etc.)
4. News (News, Politics, Technology News, etc.)
5. Shopping (E-commerce, Product Reviews, Deal Sites, etc.)
6. Health (Fitness, Mental Health, Nutrition, Medical, etc.)
7. Finance (Banking, Investing, Cryptocurrency, etc.)
8. Other (Uncategorized, Adult Content, etc.)

#### 3.5.2 User Domain Categorization

**FR-CAT-002:** The system shall allow users to define custom domain-to-category mappings.

**Requirements:**
- Store mappings in user_domain_categories table
- Support domain pattern matching
- Enforce unique constraint per user-domain pair
- Support priority levels for conflict resolution

**Inputs:**
- User ID
- Domain pattern
- Category name
- Priority level (default: 1)

**Processing:**
- Validate category against allowed values
- Check for existing mapping
- Create or update mapping record
- Return confirmation

#### 3.5.3 Category Retrieval

**FR-CAT-003:** The system shall provide endpoints to retrieve category information.

**Endpoints:**
- List all available categories
- Get category groups
- Retrieve user-specific domain mappings
- Get category details

#### 3.5.4 Zero-Shot Classification

**FR-CAT-004:** The system shall classify arbitrary text into categories without training.

**Processing:**
- Accept text input via query parameter
- Use BART-large-mnli model
- Match against all 54 categories
- Return ranked predictions

**Outputs:**
- Ordered list of category labels
- Confidence scores
- Category group for top prediction

### 3.6 Time Limit Management

**Priority:** Low  
**Description:** Digital wellness features for managing screen time.

#### 3.6.1 Limit Configuration

**FR-LIMIT-001:** The system shall allow users to set daily time limits per domain.

**Storage:**
- Table: user_domain_limits
- Fields: limit_id, user_id, domain, allowed_minutes

**Requirements:**
- Store limits in minutes
- Enforce unique constraint per user-domain
- Support CRUD operations
- Maintain created_at and updated_at timestamps

#### 3.6.2 Usage Tracking

**FR-LIMIT-002:** The system shall track time spent per domain against configured limits.

**Processing:**
- Aggregate session durations by domain
- Compare against user_domain_limits
- Calculate remaining time
- Identify limit violations

#### 3.6.3 Alert Generation

**FR-LIMIT-003:** The system shall generate alerts when users approach or exceed time limits.

**Alert Thresholds:**
- 75% of limit (warning)
- 100% of limit (exceeded)

**Requirements:**
- Check limits during dashboard queries
- Include alert status in insights API
- Support snooze/dismiss functionality

### 3.7 Health Check and Monitoring

**Priority:** Medium  
**Description:** System health verification and status monitoring.

#### 3.7.1 Basic Health Check

**FR-HEALTH-001:** The system shall provide a basic health check endpoint.

**Endpoint:** GET /api/v1/ping

**Requirements:**
- No authentication required
- Return immediately without external dependencies
- Indicate API availability

**Output:**
```json
{
    "message": "pong",
    "api_version": "v1"
}
```

#### 3.7.2 Detailed Health Check

**FR-HEALTH-002:** The system shall provide a detailed health check endpoint.

**Endpoint:** GET /health

**Requirements:**
- Check ML model loading status
- Verify database connectivity
- Report component health

**Output:**
```json
{
    "status": "healthy",
    "database": "connected",
    "ml_models_loaded": true
}
```

---

## 4. External Interface Requirements

### 4.1 User Interface Requirements

**UI-001:** The system shall provide machine-readable API responses in JSON format for frontend consumption.

**UI-002:** The system shall include auto-generated interactive API documentation at /docs (Swagger UI).

**UI-003:** The system shall include alternative API documentation at /redoc (ReDoc).

### 4.2 Hardware Interface Requirements

**HW-001:** The system shall operate on standard x86-64 server hardware.

**HW-002:** The system shall support containerized deployment via Docker.

**HW-003:** Minimum hardware requirements:
- CPU: 2 cores
- RAM: 2GB (4GB recommended for ML models)
- Storage: 10GB

### 4.3 Software Interface Requirements

#### 4.3.1 Database Interface

**SW-DB-001:** The system shall interface with Supabase-managed PostgreSQL 16 database.

**Connection:**
- Protocol: HTTPS (Supabase REST API)
- Library: supabase-py (Python client)
- Connection pooling: Managed by Supabase
- Authentication: Service role key for admin operations

**Tables:**
- profiles
- page_view_sessions
- content_analysis
- user_domain_categories
- user_domain_limits

#### 4.3.2 Authentication Service Interface

**SW-AUTH-001:** The system shall interface with Supabase Auth service.

**Operations:**
- User registration (sign_up)
- User authentication (sign_in_with_password)
- Token validation
- User retrieval (get_user)
- Session management

**Configuration:**
- Supabase URL (environment variable)
- Supabase anonymous key (environment variable)
- Supabase service role key (environment variable for admin operations)

**Integration:**
- Same client handles both auth and database operations
- JWT tokens validated by Supabase on each request
- Row-level security policies enforce user data isolation

#### 4.3.3 Machine Learning Model Interface

**SW-ML-001:** The system shall interface with Hugging Face Transformers library.

**Models:**
- Sentiment: distilbert-base-uncased-finetuned-sst-2-english
- Emotion: j-hartmann/emotion-english-distilroberta-base
- Zero-shot: facebook/bart-large-mnli

**Loading:**
- Download from Hugging Face Hub on first use
- Cache locally for subsequent requests
- Load into memory on application startup

### 4.4 Communication Interface Requirements

#### 4.4.1 HTTP API

**COMM-001:** The system shall communicate via HTTP/HTTPS protocol.

**Requirements:**
- Protocol: HTTP/1.1, HTTP/2
- Format: JSON request/response bodies
- Encoding: UTF-8
- Port: 8000 (development), 443 (production)

#### 4.4.2 CORS Configuration

**COMM-002:** The system shall enforce CORS policies for browser extension integration.

**Configuration:**
- Allow origins: Configurable via ALLOWED_ORIGINS setting
- Allow credentials: True
- Allow methods: All (*)
- Allow headers: All (*)

#### 4.4.3 API Versioning

**COMM-003:** The system shall use URL path versioning for API endpoints.

**Format:** /api/v1/{resource}

**Requirements:**
- Current version: v1
- Maintain backward compatibility within version
- Deprecation notice period: 90 days minimum

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements

**PERF-001:** Content analysis endpoints shall respond within 2 seconds for texts up to 5000 characters under normal load.

**PERF-002:** ML models shall load within 30 seconds during application startup.

**PERF-003:** Dashboard queries shall return results within 1 second for datasets up to 10,000 sessions.

**PERF-004:** The system shall support at least 100 concurrent users without degradation.

**PERF-005:** Database queries shall use appropriate indexes for time-range queries.

### 5.2 Security Requirements

**SEC-001:** All passwords shall be hashed using bcrypt with minimum 12 rounds.

**SEC-002:** JWT tokens shall expire after 60 minutes and require refresh.

**SEC-003:** API endpoints requiring authentication shall validate JWT tokens on every request.

**SEC-004:** User data shall be isolated per account with foreign key constraints.

**SEC-005:** Supabase API connections shall use HTTPS/TLS for all requests.

**SEC-006:** Sensitive configuration (Supabase URL, API keys) shall be stored in environment variables.

**SEC-007:** CORS policies shall restrict origins to authorized domains only.

**SEC-008:** SQL injection prevention through Supabase client's built-in query sanitization and PostgreSQL prepared statements.

**SEC-009:** Row-level security (RLS) policies shall be configured in Supabase to enforce user data isolation at the database level.

### 5.3 Reliability Requirements

**REL-001:** The system shall have 99.5% uptime during business hours.

**REL-002:** Database transactions shall be atomic to prevent data corruption.

**REL-003:** Failed ML analysis shall not prevent activity data storage.

**REL-004:** The system shall gracefully handle ML model loading failures with error logging.

**REL-005:** Application shall restart automatically on crash in containerized environment.

### 5.4 Availability Requirements

**AVAIL-001:** The system shall be available 24/7 with planned maintenance windows announced 48 hours in advance.

**AVAIL-002:** Planned maintenance shall not exceed 4 hours per month.

**AVAIL-003:** The system shall implement health check endpoints for monitoring.

### 5.5 Maintainability Requirements

**MAINT-001:** Code shall follow PEP 8 Python style guidelines.

**MAINT-002:** All modules shall include docstrings explaining purpose and usage.

**MAINT-003:** The system shall use structured logging with log levels (DEBUG, INFO, WARNING, ERROR).

**MAINT-004:** Dependencies shall be managed via Poetry with locked versions.

**MAINT-005:** The system shall support hot-reloading in development environment.

**MAINT-006:** Configuration shall be externalized via environment variables.

### 5.6 Portability Requirements

**PORT-001:** The system shall run on Linux, macOS, and Windows via Docker.

**PORT-002:** The system shall be deployable to any platform supporting Docker containers.

**PORT-003:** Database schema changes shall be version-controlled in schema.sql files and applied via Supabase dashboard or SQL editor.

**PORT-004:** Environment-specific configuration shall be managed via .env files.

### 5.7 Scalability Requirements

**SCALE-001:** The system architecture shall support horizontal scaling of API servers.

**SCALE-002:** Database schema shall support sharding by user_id for future scaling.

**SCALE-003:** ML model inference shall be stateless to support load balancing.

**SCALE-004:** The system shall support addition of new ML models without code changes to core logic.

### 5.8 Usability Requirements

**USE-001:** API documentation shall be automatically generated and always up-to-date.

**USE-002:** Error messages shall be descriptive and include HTTP status codes following REST conventions.

**USE-003:** API responses shall include request_id for tracing and debugging.

**USE-004:** Timestamp fields shall use ISO 8601 format with UTC timezone.

### 5.9 Compliance Requirements

**COMP-001:** The system shall comply with GDPR requirements for user data storage and deletion.

**COMP-002:** Users shall have the ability to request data export (future implementation).

**COMP-003:** Users shall have the ability to request account deletion with cascade data removal.

---

## 6. System Architecture

### 6.1 Architectural Overview

**Architecture Style:** RESTful API with microservice-ready design

**Layers:**
1. API Layer (FastAPI routes)
2. Business Logic Layer (ML services, data processing)
3. Data Access Layer (Supabase client)
4. External Services Layer (Supabase Auth, Hugging Face)

### 6.2 Component Architecture

#### 6.2.1 API Layer

**Components:**
- main.py: Application entry point and configuration
- api/v1/router.py: Main API router
- api/v1/auth/auth.py: Authentication endpoints
- api/v1/content.py: Content analysis endpoints
- api/v1/tracking.py: Activity tracking endpoints
- api/v1/categories.py: Category management endpoints
- api/v1/dashboard/: Dashboard analytics endpoints

**Responsibilities:**
- HTTP request handling
- Input validation via Pydantic models
- Response formatting
- Error handling and status codes

#### 6.2.2 Business Logic Layer

**Components:**
- ml/sentiment_analyzer.py: Sentiment analysis service
- ml/emotion_detector.py: Emotion detection service
- ml/zero_shot_classifier.py: Content categorization service
- ml/model_manager.py: ML model lifecycle management

**Responsibilities:**
- ML model loading and inference
- Business rule enforcement
- Data transformation and aggregation
- Analysis orchestration

#### 6.2.3 Data Access Layer

**Components:**
- core/supabase_client.py: Supabase client singleton (auth + database)
- Direct Supabase table operations via REST API
- Query building using Supabase query builder

**Responsibilities:**
- Supabase client initialization and configuration
- CRUD operations via Supabase REST API
- Query construction using PostgREST syntax
- User authentication and token management
- Error handling for API responses

#### 6.2.4 Configuration Layer

**Components:**
- core/config.py: Pydantic settings management
- core/logging.py: Logging configuration

**Responsibilities:**
- Environment variable loading
- Configuration validation
- Logging setup and formatting

### 6.3 Deployment Architecture

**Development:**
- Local Python environment with Poetry
- Hot-reloading via uvicorn --reload
- Supabase development project (cloud-hosted or local Supabase instance)

**Production:**
- Docker containerized deployment
- Uvicorn with Gunicorn workers (optional)
- Supabase managed PostgreSQL and authentication
- Cloud hosting (Railway, Render, or AWS)
- Environment variables for Supabase connection

**Scaling:**
- Horizontal scaling via multiple container instances
- Load balancer for request distribution
- Shared database with connection pooling
- ML models loaded per instance (no shared state)

---

## 7. Data Requirements

### 7.1 Logical Data Model

#### 7.1.1 Entity Relationships

**profiles**
- Primary Key: id (UUID, references auth.users)
- Attributes: username, avatar_url
- Relationships: One-to-many with all other tables

**page_view_sessions**
- Primary Key: session_id (BIGSERIAL)
- Foreign Key: user_id → profiles(id)
- Attributes: url, domain, start_time, end_time
- Indexes: (user_id, start_time) for time-range queries

**content_analysis**
- Primary Key: analysis_id (BIGSERIAL)
- Foreign Key: user_id → profiles(id)
- Attributes: page_url, scraped_at, emotion scores, category
- Unique Constraint: page_url (per user implied)

**user_domain_categories**
- Primary Key: user_category_id (BIGSERIAL)
- Foreign Key: user_id → profiles(id)
- Attributes: domain_pattern, category, priority
- Unique Constraint: (user_id, domain_pattern)

**user_domain_limits**
- Primary Key: limit_id (BIGSERIAL)
- Foreign Key: user_id → profiles(id)
- Attributes: domain, allowed_minutes, created_at, updated_at
- Unique Constraint: (user_id, domain)

### 7.2 Data Dictionary

#### 7.2.1 profiles Table

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, REFERENCES auth.users(id) ON DELETE CASCADE | User identifier from Supabase Auth |
| username | TEXT | CHECK (char_length(username) >= 3) | User display name |
| avatar_url | TEXT | NULL | URL to user avatar image |

#### 7.2.2 page_view_sessions Table

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| session_id | BIGSERIAL | PRIMARY KEY | Auto-incrementing session identifier |
| user_id | UUID | NOT NULL, REFERENCES profiles(id) ON DELETE CASCADE | Owner of the session |
| url | TEXT | NOT NULL | Full URL of visited page |
| domain | VARCHAR(255) | NOT NULL | Extracted domain from URL |
| start_time | TIMESTAMPTZ | NOT NULL | Session start timestamp (UTC) |
| end_time | TIMESTAMPTZ | NOT NULL | Session end timestamp (UTC) |

#### 7.2.3 content_analysis Table

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| analysis_id | BIGSERIAL | PRIMARY KEY | Auto-incrementing analysis identifier |
| user_id | UUID | NOT NULL, REFERENCES profiles(id) ON DELETE CASCADE | User who viewed the content |
| page_url | TEXT | NOT NULL, UNIQUE | URL of analyzed page |
| scraped_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Timestamp of analysis |
| happy_score | DECIMAL(5,4) | DEFAULT 0.0 | Joy emotion score (0-1) |
| sad_score | DECIMAL(5,4) | DEFAULT 0.0 | Sadness emotion score (0-1) |
| angry_score | DECIMAL(5,4) | DEFAULT 0.0 | Anger emotion score (0-1) |
| neutral_score | DECIMAL(5,4) | DEFAULT 0.0 | Neutral emotion score (0-1) |
| dominant_emotion | VARCHAR(50) | NULL | Primary detected emotion |
| system_suggested_category | VARCHAR(50) | NULL | ML-suggested content category |

#### 7.2.4 user_domain_categories Table

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| user_category_id | BIGSERIAL | PRIMARY KEY | Auto-incrementing category identifier |
| user_id | UUID | NOT NULL, REFERENCES profiles(id) ON DELETE CASCADE | User who defined the mapping |
| domain_pattern | VARCHAR(255) | NOT NULL | Domain pattern to match |
| category | VARCHAR(50) | NOT NULL | User-assigned category |
| priority | INT | DEFAULT 1 | Priority for conflict resolution |
| UNIQUE | (user_id, domain_pattern) | Constraint | One mapping per user-domain pair |

#### 7.2.5 user_domain_limits Table

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| limit_id | BIGSERIAL | PRIMARY KEY | Auto-incrementing limit identifier |
| user_id | UUID | NOT NULL, REFERENCES profiles(id) ON DELETE CASCADE | User who set the limit |
| domain | VARCHAR(255) | NOT NULL | Domain for which limit applies |
| allowed_minutes | INT | NOT NULL | Daily allowed time in minutes |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Limit creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |
| UNIQUE | (user_id, domain) | Constraint | One limit per user-domain pair |

### 7.3 Data Integrity

**RI-001:** All foreign key relationships shall enforce referential integrity with CASCADE DELETE.

**RI-002:** Timestamps shall be stored in UTC timezone (TIMESTAMPTZ).

**RI-003:** Emotion scores shall be constrained to 0.0-1.0 range via application logic.

**RI-004:** User-specific data shall be isolated via user_id foreign key relationships.

### 7.4 Data Retention

**RET-001:** User data shall be retained indefinitely unless user requests deletion.

**RET-002:** Deleted user accounts shall cascade delete all associated data.

**RET-003:** Session data older than 2 years may be archived (future implementation).

### 7.5 Data Migration

**MIG-001:** Database schema changes shall be documented in version-controlled SQL files (e.g., schema.sql).

**MIG-002:** Schema changes shall be applied via Supabase dashboard SQL editor or migration tools.

**MIG-003:** Schema changes shall be tested on Supabase staging/development projects before production deployment.

---

## 8. Appendices

### 8.1 Machine Learning Models

#### 8.1.1 Sentiment Analysis Model

**Model:** distilbert-base-uncased-finetuned-sst-2-english

**Source:** Hugging Face Transformers

**Parameters:** 67 million

**Classes:**
- POSITIVE
- NEGATIVE

**Performance:**
- Accuracy: ~91% on SST-2 test set
- Inference time: ~100-200ms per text

**Use Cases:**
- Overall content sentiment assessment
- Positive/negative content filtering
- Mood tracking over time

#### 8.1.2 Emotion Detection Model

**Model:** j-hartmann/emotion-english-distilroberta-base

**Source:** Hugging Face Transformers

**Parameters:** 82 million

**Classes:**
- joy
- anger
- sadness
- fear
- surprise
- disgust
- neutral

**Performance:**
- F1 Score: ~66% on emotion detection benchmark
- Inference time: ~150-250ms per text

**Use Cases:**
- Emotional impact assessment
- Content emotional profiling
- Emotional balance tracking

#### 8.1.3 Zero-Shot Classification Model

**Model:** facebook/bart-large-mnli

**Source:** Hugging Face Transformers

**Parameters:** 406 million

**Approach:** Natural Language Inference (NLI)

**Categories:** 54 predefined categories across 8 groups

**Performance:**
- Accuracy: Varies by category, generally 70-85%
- Inference time: ~300-500ms per text

**Use Cases:**
- Content categorization without training data
- Dynamic category addition
- Multi-label classification

### 8.2 Category Taxonomy

#### 8.2.1 Productive Categories
- Work
- Education
- Research
- Programming
- Documentation
- Professional Development
- Business Tools
- Project Management

#### 8.2.2 Social Categories
- Social Media
- Messaging
- Forums
- Dating
- Networking
- Community

#### 8.2.3 Entertainment Categories
- Streaming (Video)
- Streaming (Music)
- Gaming
- Videos
- Podcasts
- Comics/Manga
- Books/Reading

#### 8.2.4 News Categories
- News (General)
- Politics
- Technology News
- Business News
- Sports News
- Science News

#### 8.2.5 Shopping Categories
- E-commerce
- Product Reviews
- Deal Sites
- Marketplace

#### 8.2.6 Health Categories
- Fitness
- Mental Health
- Nutrition
- Medical Information
- Wellness

#### 8.2.7 Finance Categories
- Banking
- Investing
- Cryptocurrency
- Personal Finance
- Financial News

#### 8.2.8 Other Categories
- Uncategorized
- Adult Content
- Utilities
- Reference
- Travel
- Food/Cooking
- Religion/Spirituality

### 8.3 Environment Variables

**Required:**
- SUPABASE_URL: Supabase project URL
- SUPABASE_ANON_KEY: Supabase anonymous key
- SUPABASE_SERVICE_ROLE_KEY: Supabase service role key (admin operations)

**Optional:**
- ALLOWED_ORIGINS: Comma-separated list of allowed CORS origins (default: localhost)
- LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR)
- ENVIRONMENT: Deployment environment (development, staging, production)

### 8.4 API Response Examples

#### 8.4.1 Successful Content Analysis

```json
{
    "text_length": 245,
    "word_count": 42,
    "url": "https://example.com/article",
    "sentiment": {
        "label": "POSITIVE",
        "score": 0.9876
    },
    "category": {
        "labels": ["Technology News", "Education", "Research"],
        "scores": [0.8543, 0.7231, 0.6789],
        "group": "News"
    },
    "emotions": {
        "joy": 0.6234,
        "anger": 0.0123,
        "sadness": 0.0456,
        "fear": 0.0234,
        "surprise": 0.2145,
        "disgust": 0.0098,
        "neutral": 0.0710,
        "dominant": "joy"
    }
}
```

#### 8.4.2 Dashboard Summary Response

```json
{
    "timeRange": "this_week",
    "totals": {
        "total": 86400,
        "productive": 45000,
        "social": 25000,
        "entertainment": 16400
    },
    "changes": {
        "total": 12.5,
        "productive": 25.3,
        "social": -10.2,
        "entertainment": 5.7
    },
    "dailyData": [
        {
            "date": "2025-11-24",
            "productive": 7200,
            "social": 3600,
            "entertainment": 2400
        }
    ],
    "insights": [
        {
            "type": "improvement",
            "message": "Productive time increased 25% this week"
        }
    ]
}
```

### 8.5 Error Response Format

**Standard Error Response:**
```json
{
    "detail": "Error message describing what went wrong",
    "status_code": 400
}
```

**Common Status Codes:**
- 200: Success
- 400: Bad Request (validation error)
- 401: Unauthorized (invalid/missing token)
- 404: Not Found
- 500: Internal Server Error
- 502: Bad Gateway (external service error)

### 8.6 Development Setup

**Prerequisites:**
- Python 3.12+
- Poetry 1.8+
- Supabase account
- Git

**Installation Steps:**
1. Clone repository
2. Install dependencies: `poetry install`
3. Configure environment variables in .env
4. Run development server: `poetry run uvicorn app.main:app --reload`

**Testing:**
- Unit tests: `poetry run pytest`
- Coverage: `poetry run pytest --cov=app`
- Linting: `poetry run ruff check .`

### 8.7 Glossary

**Digital Footprint:** The trail of data created by user's online activities.

**Sentiment Analysis:** NLP technique to determine emotional tone of text.

**Zero-Shot Classification:** ML classification without training on specific categories.

**Engagement Score:** Calculated metric based on user interactions (clicks, keypresses, time).

**Session:** A continuous period of user activity on a single webpage.

**Domain Pattern:** A substring used to match website domains for categorization.

**JWT (JSON Web Token):** Compact token format for secure information transmission.

**ASGI (Asynchronous Server Gateway Interface):** Standard interface between async Python web applications and servers.

---

**Document Control:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-27 | Development Team | Initial SRS creation |

**Approval:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Professor (Project Supervisor) | | | |
| Teaching Assistant (TA) | | | |
| Project Lead | | | |
| Lead Developer | | | |

---

**End of Document**
