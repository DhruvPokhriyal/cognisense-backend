from datetime import datetime, timedelta, timezone
from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException

from app.core.config import settings
from app.core.supabase_client import supabase
from app.api.v1.auth.auth import get_current_user

router = APIRouter()


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

    # Fetch sessions in range
    resp = supabase.table("page_view_sessions").select("domain,start_time,end_time").eq("user_id", user_id).gte("start_time", start.isoformat()).lt("start_time", end.isoformat()).execute()
    if getattr(resp, "error", None):
        raise HTTPException(status_code=502, detail="Failed to fetch sessions")
    sessions = getattr(resp, "data", []) or []

    # Fetch user domain categories
    cat_resp = supabase.table("user_domain_categories").select("domain_pattern,category").eq("user_id", user_id).execute()
    categories = getattr(cat_resp, "data", []) or []

    # helper to categorize domain
    def categorize(domain: str) -> str:
        if not domain:
            return "uncategorized"
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
        cat = categorize(s.get("domain"))
        if cat.lower() == "productive":
            totals["productive"] += seconds
        elif cat.lower() in ("social", "social_media", "socialmedia", "social-media"):
            totals["social"] += seconds
        elif cat.lower() in ("entertainment",):
            totals["entertainment"] += seconds
        # add to daily
        day_index = (st.date() - start.date()).days
        if 0 <= day_index < 7:
            if cat.lower() == "productive":
                days[day_index]["productive"] += seconds
            elif cat.lower() in ("social", "social_media", "socialmedia", "social-media"):
                days[day_index]["social"] += seconds
            elif cat.lower() == "entertainment":
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
        cat = categorize(s.get("domain"))
        if cat.lower() == "productive":
            prev_totals["productive"] += seconds
        elif cat.lower() in ("social", "social_media", "socialmedia", "social-media"):
            prev_totals["social"] += seconds
        elif cat.lower() == "entertainment":
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


