from typing import Dict, List, Optional, Set

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.auth.auth import get_current_user
from app.core.supabase_client import supabase

router = APIRouter()


def _unique(seq: List[str]) -> List[str]:
    seen: Set[str] = set()
    out: List[str] = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


@router.get("")
async def dashboard_settings(current_user=Depends(get_current_user)) -> Dict:
    """Return settings view: union of domains the user has activity on, plus
    domains present in user limits and patterns, with nullable category and limit.
    """
    user_id = current_user.get("id") if isinstance(current_user, dict) else getattr(current_user, "id", None)
    if not user_id:
        raise HTTPException(status_code=400, detail="Unable to determine user id from auth payload")

    # 1) Distinct domains from recent sessions (cap to 1000 recent rows for practicality)
    sess_resp = (
        supabase
        .table("page_view_sessions")
        .select("domain,start_time")
        .eq("user_id", user_id)
        .order("start_time", desc=True)
        .limit(1000)
        .execute()
    )
    sessions = getattr(sess_resp, "data", []) or []
    session_domains = [str((row.get("domain") or "").lower()) for row in sessions if row.get("domain")]  # type: ignore

    # 2) User limits domains
    lim_resp = supabase.table("user_domain_limits").select("domain,allowed_minutes").eq("user_id", user_id).execute()
    limits_rows = getattr(lim_resp, "data", []) or []
    limit_map = {str((r.get("domain") or "").lower()): int(r.get("allowed_minutes") or 0) for r in limits_rows if r.get("domain")}

    # 3) User categories patterns (this may include patterns not present in sessions yet)
    cat_resp = supabase.table("user_domain_categories").select("domain_pattern,category").eq("user_id", user_id).execute()
    category_rows = getattr(cat_resp, "data", []) or []
    patterns = [str((r.get("domain_pattern") or "").lower()) for r in category_rows if r.get("domain_pattern")]

    # Build the union set of names to show
    names = _unique(session_domains + list(limit_map.keys()) + patterns)

    # Helper to find category by best pattern match (substring)
    def find_category(name: str) -> Optional[str]:
        nl = name.lower()
        best_len = -1
        best_cat: Optional[str] = None
        for r in category_rows:
            pat = str((r.get("domain_pattern") or "").lower())
            cat = r.get("category")
            if not pat:
                continue
            if pat in nl:
                # Prefer the longest matching pattern as "best" match
                if len(pat) > best_len:
                    best_len = len(pat)
                    best_cat = cat
        return best_cat

    websites = []
    for name in names:
        cat = find_category(name)
        limit = limit_map.get(name)
        websites.append({
            "name": name,
            "category": cat,  # nullable
            "limit": limit,    # nullable if not set
        })

    return {"websites": websites}
