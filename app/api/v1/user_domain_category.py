from fastapi import APIRouter, HTTPException, Request
from app.core.supabase_client import supabase

router = APIRouter()


@router.post("/user_domain_category/save")
async def save_user_domain_data(request: Request):

    if supabase is None:
        raise HTTPException(status_code=500, detail="Supabase client not initialized")

    body = await request.json()

    required = ["user_id", "domain_pattern", "category", "priority", "allowed_minutes"]
    for field in required:
        if field not in body:
            raise HTTPException(
                status_code=400,
                detail=f"Missing field: {field}"
            )

    user_id = body["user_id"]
    domain_pattern = body["domain_pattern"]
    category = body["category"]
    priority = body["priority"]
    allowed_minutes = body["allowed_minutes"]

    # ----------- INSERT INTO user_domain_categories -----------
    try:
        category_response = (
            supabase
            .table("user_domain_categories")
            .insert({
                "user_id": user_id,
                "domain_pattern": domain_pattern,
                "category": category,
                "priority": priority
            })
            .execute()
        )

        if category_response.error:
            msg = category_response.error.message

            if "duplicate key" in msg.lower():
                category_response = {
                    "warning": f"Category already exists for pattern '{domain_pattern}'"
                }
            else:
                raise HTTPException(status_code=400, detail=msg)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        limit_response = (
            supabase
            .table("user_domain_limits")
            .insert({
                "user_id": user_id,
                "domain": domain_pattern,
                "allowed_minutes": allowed_minutes
            })
            .execute()
        )

        if limit_response.error:
            msg = limit_response.error.message

            if "duplicate key" in msg.lower():
                limit_response = {
                    "warning": f"Limit already exists for domain '{domain_pattern}'"
                }
            else:
                raise HTTPException(status_code=400, detail=msg)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "success": True,
        "category_result": category_response,
        "limit_result": limit_response
    }
