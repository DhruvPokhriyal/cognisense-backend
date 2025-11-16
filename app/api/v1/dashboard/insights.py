from datetime import datetime, timedelta, timezone
from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException

from app.core.config import settings
from app.core.supabase_client import supabase
from app.api.v1.auth.auth import get_current_user
from .dashboard import _get_time_range

router = APIRouter()

@router.get("")
async def dashboard_insights(timeRange: str = "this_week", current_user=Depends(get_current_user)) -> Dict:
    user_id = current_user.get("id") if isinstance(current_user, dict) else getattr(current_user, "id", None)
    if not user_id:
        raise HTTPException(status_code=400, detail="Unable to determine user id from auth payload")

    start, end = _get_time_range(timeRange)
    prev_start = start - (end - start)
    prev_end = start

    s_cur = supabase.table("page_view_sessions").select("domain,start_time,end_time").eq("user_id", user_id).gte("start_time", start.isoformat()).lt("start_time", end.isoformat()).execute()
    s_prev = supabase.table("page_view_sessions").select("domain,start_time,end_time").eq("user_id", user_id).gte("start_time", prev_start.isoformat()).lt("start_time", prev_end.isoformat()).execute()
    sessions = getattr(s_cur, "data", []) or []
    prev_sessions = getattr(s_prev, "data", []) or []

    cat_resp = supabase.table("user_domain_categories").select("domain_pattern,category").eq("user_id", user_id).execute()
    categories = getattr(cat_resp, "data", []) or []

    def categorize(domain: str) -> str:
        if not domain:
            return "uncategorized"
        domain_l = domain.lower()
        for c in categories:
            pattern = (c.get("domain_pattern") or "").lower()
            if pattern and pattern in domain_l:
                return (c.get("category") or "uncategorized").lower()
        return "uncategorized"

    def aggregate_times(s_list: List[Dict]):
        totals = {"total": 0.0, "productive": 0.0, "social": 0.0, "entertainment": 0.0}
        for s in s_list:
            try:
                st = datetime.fromisoformat(s.get("start_time"))
                et = datetime.fromisoformat(s.get("end_time"))
            except Exception:
                continue
            seconds = max(0.0, (et - st).total_seconds())
            totals["total"] += seconds
            cat = categorize(s.get("domain"))
            if cat == "productive":
                totals["productive"] += seconds
            elif cat in ("social", "social_media", "socialmedia", "social-media"):
                totals["social"] += seconds
            elif cat == "entertainment":
                totals["entertainment"] += seconds
        return totals

    cur_totals = aggregate_times(sessions)
    prev_totals = aggregate_times(prev_sessions)

    def pct_change(cur: float, prev: float) -> float:
        if prev <= 0:
            return 0.0
        return round(((cur - prev) / prev) * 100.0, 2)

    ca_cur = supabase.table("content_analysis").select("happy_score,sad_score,angry_score,neutral_score,dominant_emotion,system_suggested_category,scraped_at").eq("user_id", user_id).gte("scraped_at", start.isoformat()).lt("scraped_at", end.isoformat()).execute()
    ca_prev = supabase.table("content_analysis").select("happy_score,sad_score,angry_score,neutral_score,dominant_emotion,system_suggested_category,scraped_at").eq("user_id", user_id).gte("scraped_at", prev_start.isoformat()).lt("scraped_at", prev_end.isoformat()).execute()
    ca_rows = getattr(ca_cur, "data", []) or []
    ca_prev_rows = getattr(ca_prev, "data", []) or []

    pos = sum(float(r.get("happy_score") or 0) for r in ca_rows)
    neg = sum(float(r.get("sad_score") or 0) + float(r.get("angry_score") or 0) for r in ca_rows)
    neu = sum(float(r.get("neutral_score") or 0) for r in ca_rows)
    total_em = pos + neg + neu
    if total_em > 0:
        pos_pct = round(pos / total_em * 100.0, 2)
        neu_pct = round(neu / total_em * 100.0, 2)
        neg_pct = round(neg / total_em * 100.0, 2)
    else:
        pos_pct = neu_pct = neg_pct = 0.0
    emotional_balance = {
        "balanceScore": int(round(pos_pct * 0.6 + (100 - neg_pct) * 0.4)),
        "segments": [
            {"type": "positive", "value": round(pos_pct, 2)},
            {"type": "neutral", "value": round(neu_pct, 2)},
            {"type": "negative", "value": round(neg_pct, 2)},
            {"type": "biased", "value": 0},
        ],
    }

    cat_counts: Dict[str, int] = {}
    for r in ca_rows:
        c = (r.get("system_suggested_category") or "other").lower()
        cat_counts[c] = cat_counts.get(c, 0) + 1
    total_docs = sum(cat_counts.values())
    content_categories = []
    if total_docs > 0:
        for c, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
            content_categories.append({"category": c, "percentage": round(count * 100.0 / total_docs, 2)})

    prod_ratio = round((cur_totals["productive"] / cur_totals["total"] * 100.0), 2) if cur_totals["total"] > 0 else 0.0
    prev_prod_ratio = round((prev_totals["productive"] / prev_totals["total"] * 100.0), 2) if prev_totals["total"] > 0 else 0.0
    weekly_improvement = round(prod_ratio - prev_prod_ratio, 2)

    social_ratio = round((cur_totals["social"] / cur_totals["total"] * 100.0), 2) if cur_totals["total"] > 0 else 0.0
    overall_health = int(round(0.5 * prod_ratio + 0.3 * (100 - social_ratio) + 0.2 * (emotional_balance["segments"][0]["value"])) )

    summary = {
        "overallHealthScore": max(0, min(100, overall_health)),
        "productiveTimeRatio": int(round(prod_ratio)),
        "weeklyImprovementPercent": int(round(weekly_improvement)),
    }

    prev_pos = sum(float(r.get("happy_score") or 0) for r in ca_prev_rows)
    prev_neg = sum(float(r.get("sad_score") or 0) + float(r.get("angry_score") or 0) for r in ca_prev_rows)
    prev_neu = sum(float(r.get("neutral_score") or 0) for r in ca_prev_rows)
    prev_total_em = prev_pos + prev_neg + prev_neu
    prev_neg_pct = round(prev_neg / prev_total_em * 100.0, 2) if prev_total_em > 0 else 0.0
    neg_increase = round(neg_pct - prev_neg_pct, 2)

    alerts = []
    if neg_increase >= 5:
        alerts.append({
            "id": "alert_neg_content",
            "type": "warning",
            "title": "Negative Content Alert",
            "description": f"Your negative content consumption increased by {neg_increase}% this period. Consider diversifying your sources.",
        })

    if content_categories:
        top_cat = content_categories[0]
        if top_cat.get("percentage", 0) >= 60:
            alerts.append({
                "id": "alert_bubble",
                "type": "info",
                "title": "Content Bubble Detected",
                "description": f"You've been in a {top_cat['category']} content bubble. Try exploring other topics for a balanced perspective.",
            })

    if weekly_improvement >= 10:
        alerts.append({
            "id": "alert_progress",
            "type": "success",
            "title": "Great Progress!",
            "description": f"Great job! Your productive screen time increased by {int(round(weekly_improvement))}% compared to last period.",
        })

    limits_resp = supabase.table("user_domain_limits").select("domain,allowed_minutes").eq("user_id", user_id).execute()
    limits = getattr(limits_resp, "data", []) or []
    if limits:
        days_count = int((end - start).days)
        for lim in limits:
            dom = (lim.get("domain") or "").lower()
            allowed_sec = int(lim.get("allowed_minutes") or 0) * 60 * max(1, days_count)
            used_sec = 0
            for s in sessions:
                d = (s.get("domain") or "").lower()
                if dom and dom in d:
                    try:
                        st = datetime.fromisoformat(s.get("start_time"))
                        et = datetime.fromisoformat(s.get("end_time"))
                        used_sec += max(0.0, (et - st).total_seconds())
                    except Exception:
                        continue
            if allowed_sec > 0 and used_sec > allowed_sec:
                over_pct = int(round((used_sec - allowed_sec) * 100.0 / allowed_sec))
                alerts.append({
                    "id": "alert_social_limit",
                    "type": "warning",
                    "title": "Social Media Limit",
                    "description": f"Your usage for '{dom}' is {over_pct}% above your target for this period. Consider setting app limits.",
                })

    social_change = pct_change(cur_totals["social"], prev_totals["social"])
    prod_change = pct_change(cur_totals["productive"], prev_totals["productive"])

    def clamp01(x: float) -> float:
        return max(0.0, min(100.0, x))

    reduce_social_progress = clamp01(50 - social_change * 0.5)
    increase_productive_progress = clamp01(50 + prod_change * 0.5)
    top_share = content_categories[0]["percentage"] if content_categories else 0
    diversify_progress = clamp01(100 - top_share)

    weekly_progress = [
        {"goalId": "reduce_social_media", "label": "Reduce Social Media Time", "progressPercent": int(round(reduce_social_progress))},
        {"goalId": "increase_productive_hours", "label": "Increase Productive Hours", "progressPercent": int(round(increase_productive_progress))},
        {"goalId": "diversify_content", "label": "Diversify Content Sources", "progressPercent": int(round(diversify_progress))},
    ]

    return {
        "timeRange": timeRange,
        "summary": summary,
        "alerts": alerts,
        "weeklyProgress": weekly_progress,
        "emotionalBalance": emotional_balance,
        "contentCategories": content_categories,
    }
