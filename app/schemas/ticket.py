from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.common import PaginatedResponse


class TicketCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)

class TicketResponse(TicketCreate):
    id: int
    status: str
    ai_classification: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

TicketListResponse = PaginatedResponse[TicketResponse]
