# Dashboard API

This document describes the authenticated Dashboard endpoints served by the API. All endpoints require a Supabase JWT in the `Authorization` header using the HTTP Bearer scheme.

- Base path: `/api/v1`
- Auth: `Authorization: Bearer <SUPABASE_JWT>`

Examples assume the server is running at `http://localhost:8000`.

## Authentication

- Header: `Authorization: Bearer <token>` (required)
- The token is validated via Supabase Auth. Requests without a valid token will receive `401 Unauthorized`.

----

## GET /dashboard

Summary and weekly breakdown for the current user.

- Path: `/api/v1/dashboard`
- Query params:
  - `timeRange`: `this_week` (default) | `last_week`

Response (200):
```json
{
  "user": {
    "id": "uuid",
    "displayName": "Jane Doe",
    "email": "jane@example.com"
  },
  "timeRange": "this_week",
  "metrics": [
    {
      "title": "Total Time",
      "value": 14040,
      "change_percent": 15.0,
      "trend": "up",
      "improvement_label": "slightly_better"
    },
    {
      "title": "Productive Time",
      "value": 7200,
      "change_percent": 10.0,
      "trend": "up",
      "improvement_label": "slightly_better"
    },
    {
      "title": "Social Time",
      "value": 1800,
      "change_percent": -8.0,
      "trend": "down",
      "improvement_label": "slight_worse"
    },
    {
      "title": "Entertainment Time",
      "value": 3000,
      "change_percent": 5.0,
      "trend": "up",
      "improvement_label": "slightly_better"
    }
  ],
  "weeklyData": [
    { "day": "Mon", "Productive": 150, "Social": 100, "Entertainment": 80 },
    { "day": "Tue", "Productive": 180, "Social": 120, "Entertainment": 100 },
    { "day": "Wed", "Productive": 200, "Social": 150, "Entertainment": 120 },
    { "day": "Thu", "Productive": 280, "Social": 180, "Entertainment": 200 },
    { "day": "Fri", "Productive": 150, "Social": 120, "Entertainment": 180 },
    { "day": "Sat", "Productive": 100, "Social": 180, "Entertainment": 250 },
    { "day": "Sun", "Productive": 80,  "Social": 150, "Entertainment": 240 }
  ]
}
```

Notes:
- `metrics[].value` is returned in seconds.
- Category mapping uses user-defined patterns from `public.user_domain_categories`.

Curl:
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/dashboard?timeRange=this_week"
```

----

## GET /dashboard/insights

Insights including a summary score, alerts, weekly progress against simple goals, emotional balance, and content category distribution.

- Path: `/api/v1/dashboard/insights`
- Query params:
  - `timeRange`: `this_week` (default) | `last_week`

Response (200):
```json
{
  "timeRange": "this_week",
  "summary": {
    "overallHealthScore": 72,
    "productiveTimeRatio": 48,
    "weeklyImprovementPercent": 15
  },
  "alerts": [
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
    },
    {
      "id": "alert_progress",
      "type": "success",
      "title": "Great Progress!",
      "description": "Great job! Your productive screen time increased by 15% compared to last period."
    }
  ],
  "weeklyProgress": [
    { "goalId": "reduce_social_media", "label": "Reduce Social Media Time", "progressPercent": 65 },
    { "goalId": "increase_productive_hours", "label": "Increase Productive Hours", "progressPercent": 80 },
    { "goalId": "diversify_content", "label": "Diversify Content Sources", "progressPercent": 45 }
  ],
  "emotionalBalance": {
    "balanceScore": 72,
    "segments": [
      { "type": "positive", "value": 45 },
      { "type": "neutral",  "value": 30 },
      { "type": "negative", "value": 15 },
      { "type": "biased",   "value": 10 }
    ]
  },
  "contentCategories": [
    { "category": "technology", "percentage": 35 },
    { "category": "entertainment", "percentage": 25 },
    { "category": "news", "percentage": 18 },
    { "category": "social", "percentage": 15 },
    { "category": "other", "percentage": 7 }
  ]
}
```

Notes:
- Emotional balance aggregates `happy`, `sad+angry`, `neutral` from `public.content_analysis` for the period.
- Alerts are heuristic and compare current vs previous equal-length period.

Curl:
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/dashboard/insights?timeRange=this_week"
```

----

## GET /dashboard/settings

Combined per-domain settings view showing category and daily limit (if any). Sources:

- Distinct recent domains from `public.page_view_sessions`
- User patterns from `public.user_domain_categories`
- User limits from `public.user_domain_limits`

- Path: `/api/v1/dashboard/settings`

Response (200):
```json
{
  "websites": [
    { "name": "github.com",  "category": "Productivity",  "limit": 60 },
    { "name": "youtube.com", "category": null,            "limit": null },
    { "name": "twitter.com", "category": "Social Media", "limit": 30 }
  ]
}
```

Notes:
- `category` is derived from best substring match against `domain_pattern` (nullable).
- `limit` is `allowed_minutes` per day from `user_domain_limits` (nullable, integer minutes).

Curl:
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/dashboard/settings"
```

----

## Errors

- `401 Unauthorized`: Missing or invalid Bearer token.
- `502 Bad Gateway`: Upstream Supabase/table issues.
- `400 Bad Request`: Malformed parameters or missing user id in auth payload.

----

## Data Sources (tables)

Defined in `docs/schema.sql`:
- `public.page_view_sessions`
- `public.user_domain_categories`
- `public.user_domain_limits`
- `public.content_analysis`
