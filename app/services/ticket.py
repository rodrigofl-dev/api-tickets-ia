from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.ticket import TicketRepository
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate

from google import genai
from app.core.config import settings


class TicketService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = TicketRepository(db)

    # API #

    def create_ticket(self, data: TicketCreate) -> Ticket:
        ticket = Ticket(
            title=data.title,
            description=data.description,
        )

        return self.repository.save(ticket)

    def list_tickets(self, limit: int, offset: int) -> tuple[list[Ticket], int]:
        items = self.repository.get_all(limit=limit, offset=offset)
        total = self.repository.count_all()

        return items, total

    def classify_ticket(self, id: int) -> Ticket:
        ticket = self.repository.get_by_id(id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
        prompt = f"""
        Analise o seguinte ticket de suporte técnico. 
        Título: {ticket.title}
        Descrição: {ticket.description}
        
        Responda em uma linha dizendo se o tom do cliente é irritado, neutro ou positivo, e qual a urgência (Alta, Média, Baixa).
        """

        client = genai.Client(api_key=settings.google_api_key)

        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
            )
    
            ai_response = response.text
            ticket.ai_classification = ai_response

            return self.repository.save(ticket)
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
