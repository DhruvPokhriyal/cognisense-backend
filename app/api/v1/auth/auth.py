from fastapi import APIRouter, Depends, HTTPException, Request, status, Header
from supabase import create_client, Client

from app.core.config import settings

router = APIRouter()

def get_bearer_token(authorization: str) -> str:
    """Extract Bearer token from Authorization header. Raises HTTPException if malformed."""
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected 'Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return parts[1]


async def get_current_user(request: Request, authorization: str = Header(...)):
    """Verify token with Supabase and return the user payload using supabase-py library."""
    token = get_bearer_token(authorization)

    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="SUPABASE_URL or SUPABASE_KEY not configured")

    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    try:
        user = supabase.auth.get_user(token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid or expired token: {str(e)}")

    if not user or not getattr(user, "user", None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    return user.user


@router.get("/me")
async def read_current_user(current_user=Depends(get_current_user)):
    """Return the authenticated Supabase user payload."""
    return {"user": current_user}
