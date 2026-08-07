from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.database.models import VisitorLog
from pydantic import BaseModel

router = APIRouter()

class TelemetryPayload(BaseModel):
    device: str
    page_section: str

@router.post("/log")
async def register_interaction(
    payload: TelemetryPayload,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Logs visitor metrics, device types, and target locations into the tracking database.
    """
    client_host = request.client.host if request.client else "unknown"
    
    # Simple localization placeholder (can be linked to Geolocation tools down the line)
    country_origin = "Local Network Cluster" 
    
    new_log = VisitorLog(
        ip_address=client_host,
        device=payload.device,
        country=country_origin,
        active_section=payload.page_section
    )
    
    db.add(new_log)
    db.commit()
    
    # Return count statistics to update the frontend footer counter widget
    total_views = db.query(VisitorLog).count()
    return {"status": "telemetry logged", "total_visitors": total_views}