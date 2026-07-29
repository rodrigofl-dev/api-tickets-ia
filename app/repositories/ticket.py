from sqlalchemy.orm import Session

from app.models.ticket import Ticket


class TicketRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Ticket | None:
        return self.db.query(Ticket).filter(Ticket.id == id).first()

    def get_all(self, limit: int = 20, offset: int = 0) -> list[Ticket]:
        return self.db.query(Ticket).limit(limit).offset(offset).all()

    def count_all(self) -> int:
        return self.db.query(Ticket).count()

    def save(self, ticket: Ticket) -> Ticket:
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket
