from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db

from app.schemas.ticket import TicketCreate, TicketResponse, TicketListResponse
from app.services.ticket import TicketService

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("", response_model=TicketResponse)
def create_ticket(data: TicketCreate, db: Session = Depends(get_db)):
    service = TicketService(db)
    return service.create_ticket(data)

@router.get("", response_model=TicketListResponse)
def list_tickets(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    service = TicketService(db)
    items, total = service.list_tickets(limit, offset)
    return TicketListResponse(items=items, total=total, limit=limit, offset=offset)

@router.post("/{id}/classify", response_model=TicketResponse)
def classify_ticket(id: int, db: Session = Depends(get_db)):
    service = TicketService(db)
    return service.classify_ticket(id)
