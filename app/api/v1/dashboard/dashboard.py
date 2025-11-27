from datetime import datetime, timedelta, timezone
from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException

from app.core.config import settings
from app.core.supabase_client import supabase
from app.api.v1.auth.auth import get_current_user
from app.ml.zero_shot_classifier import get_dashboard_bucket_mapping

router = APIRouter()


# Central source of truth for bucket mapping
CATEGORY_TO_BUCKET = get_dashboard_bucket_mapping()


def _get_time_range(range_name: str):
    now = datetime.now(timezone.utc)
    if range_name == "this_week":
        # week starting Monday
        start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=7)
    elif range_name == "last_week":
        start = (now - timedelta(days=now.weekday() + 7)).replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=7)
    else:
        # default to this_week
        start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=7)
    return start, end


def _label_for_change(pct: float) -> str:
    if pct >= 10:
        return "much_better"
    if 0 < pct < 10:
        return "slightly_better"
    if pct == 0:
        return "no_change"
    if -10 < pct < 0:
        return "slight_worse"
    return "much_worse"


@router.get("")
async def dashboard(timeRange: str = "this_week", current_user=Depends(get_current_user)) -> Dict:
    """Return dashboard summary for authenticated user.

    Aggregates durations from `page_view_sessions` and categorizes by
    user-domain categories stored in `user_domain_categories`.
    """
    user_id = current_user.get("id") if isinstance(current_user, dict) else getattr(current_user, "id", None)
    if not user_id:
        raise HTTPException(status_code=400, detail="Unable to determine user id from auth payload")

    start, end = _get_time_range(timeRange)
    prev_start = start - (end - start)
    prev_end = start

    # Fetch sessions in range (include url to match content_analysis)
    resp = supabase.table("page_view_sessions").select("domain,start_time,end_time,url").eq("user_id", user_id).gte("start_time", start.isoformat()).lt("start_time", end.isoformat()).execute()
    if getattr(resp, "error", None):
        raise HTTPException(status_code=502, detail="Failed to fetch sessions")
    sessions = getattr(resp, "data", []) or []

    # Build URL set to look up analysis categories
    url_set = {s.get("url") for s in sessions if s.get("url")}
    url_list = list(url_set)

    # Fetch content analysis for these URLs to use system_suggested_category
    analysis_map: Dict[str, str] = {}
    if url_list:
        # Batch the IN queries to avoid size limits
        batch_size = 100
        for i in range(0, len(url_list), batch_size):
            batch = url_list[i:i+batch_size]
            aresp = supabase\
                .table("content_analysis")\
                .select("page_url,system_suggested_category")\
                .eq("user_id", user_id)\
                .in_("page_url", batch)\
                .execute()
            if getattr(aresp, "data", None):
                for row in aresp.data:
                    analysis_map[row.get("page_url")] = row.get("system_suggested_category")

    # Fetch user domain categories
    cat_resp = supabase.table("user_domain_categories").select("domain_pattern,category").eq("user_id", user_id).execute()
    categories = getattr(cat_resp, "data", []) or []

    # helper to categorize domain/url -> fine category
    def categorize(domain: str, url: str | None = None) -> str:
        if not domain:
            return "uncategorized"
        # Prefer system_suggested_category from content_analysis when available
        if url and url in analysis_map:
            return analysis_map.get(url) or "uncategorized"
        domain_l = domain.lower()
        for c in categories:
            pattern = (c.get("domain_pattern") or "").lower()
            if not pattern:
                continue
            if pattern in domain_l:
                return c.get("category") or "uncategorized"
        return "uncategorized"

    totals = {"total": 0, "productive": 0, "social": 0, "entertainment": 0}
    # weekly buckets (Mon-Sun)
    days = []
    for i in range(7):
        day = (start + timedelta(days=i)).date()
        days.append({"date": day, "productive": 0, "social": 0, "entertainment": 0})

    for s in sessions:
        try:
            st = datetime.fromisoformat(s.get("start_time"))
            et = datetime.fromisoformat(s.get("end_time"))
        except Exception:
            continue
        seconds = max(0, (et - st).total_seconds())
        totals["total"] += seconds
        cat = categorize(s.get("domain"), s.get("url"))
        bucket = CATEGORY_TO_BUCKET.get(cat)
        if not bucket:
            lc = (cat or "").lower()
            if lc in ("productive", "social", "entertainment"):
                bucket = lc
            else:
                bucket = "productive"  # default fallback to ensure totals match
        if bucket == "productive" or cat.lower() == "productive":
            totals["productive"] += seconds
        elif bucket == "social" or cat.lower() in ("social", "social_media", "socialmedia", "social-media"):
            totals["social"] += seconds
        elif bucket == "entertainment" or cat.lower() in ("entertainment",):
            totals["entertainment"] += seconds
        # add to daily
        day_index = (st.date() - start.date()).days
        if 0 <= day_index < 7:
            if bucket == "productive" or cat.lower() == "productive":
                days[day_index]["productive"] += seconds
            elif bucket == "social" or cat.lower() in ("social", "social_media", "socialmedia", "social-media"):
                days[day_index]["social"] += seconds
            elif bucket == "entertainment" or cat.lower() == "entertainment":
                days[day_index]["entertainment"] += seconds

    # previous period totals for change percent
    prev_resp = supabase.table("page_view_sessions").select("domain,start_time,end_time").eq("user_id", user_id).gte("start_time", prev_start.isoformat()).lt("start_time", prev_end.isoformat()).execute()
    prev_sessions = getattr(prev_resp, "data", []) or []
    prev_totals = {"total": 0, "productive": 0, "social": 0, "entertainment": 0}
    for s in prev_sessions:
        try:
            st = datetime.fromisoformat(s.get("start_time"))
            et = datetime.fromisoformat(s.get("end_time"))
        except Exception:
            continue
        seconds = max(0, (et - st).total_seconds())
        prev_totals["total"] += seconds
        cat = categorize(s.get("domain"), s.get("url"))
        bucket = CATEGORY_TO_BUCKET.get(cat)
        if not bucket:
            lc = (cat or "").lower()
            if lc in ("productive", "social", "entertainment"):
                bucket = lc
            else:
                bucket = "productive"
        if bucket == "productive" or cat.lower() == "productive":
            prev_totals["productive"] += seconds
        elif bucket == "social" or cat.lower() in ("social", "social_media", "socialmedia", "social-media"):
            prev_totals["social"] += seconds
        elif bucket == "entertainment" or cat.lower() == "entertainment":
            prev_totals["entertainment"] += seconds

    def make_metric(title: str, key: str):
        cur = totals.get(key, 0)
        prev = prev_totals.get(key, 0)
        if prev > 0:
            pct = round(((cur - prev) / prev) * 100, 2)
        else:
            pct = 0.0
        trend = "up" if pct > 0 else ("down" if pct < 0 else "flat")
        return {
            "title": title,
            "value": int(cur),
            "change_percent": pct,
            "trend": trend,
            "improvement_label": _label_for_change(pct),
        }

    metrics = [
        make_metric("Total Time", "total"),
        make_metric("Productive Time", "productive"),
        make_metric("Social Time", "social"),
        make_metric("Entertainment Time", "entertainment"),
    ]

    weekly_data = []
    weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, d in enumerate(days):
        weekly_data.append({
            "day": weekday_names[i],
            "Productive": int(d["productive"]),
            "Social": int(d["social"]),
            "Entertainment": int(d["entertainment"]),
        })

    return {
        "user": {"id": user_id, "displayName": current_user.get("user_metadata", {}).get("full_name") if isinstance(current_user, dict) else None, "email": current_user.get("email") if isinstance(current_user, dict) else None},
        "timeRange": timeRange,
        "metrics": metrics,
        "weeklyData": weekly_data,
    }


