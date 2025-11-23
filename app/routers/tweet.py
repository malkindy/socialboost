from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.database.models import Token

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/tweet", summary="Validate token from QR scan and redirect")
def tweet(token: str = Query(..., description="Token from QR code"), db: Session = Depends(get_db)):
    """
    Validates the token and redirects to a Twitter share page.
    """
    db_token = db.query(Token).filter(Token.token == token).first()

    if not db_token:
        raise HTTPException(status_code=404, detail="Invalid token")

    # Construct the URL to redirect to (Twitter share or any landing page)
    redirect_url = f"https://twitter.com/intent/tweet?text=Check+this+out+with+token:{db_token.token}"

    return RedirectResponse(url=redirect_url)
