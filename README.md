# API de Tickets com IA

API REST para abertura e gerenciamento de tickets de suporte técnico, com **classificação automática de sentimento e urgência do cliente** feita por IA (Google Gemini).

Inclui uma interface web simples (HTML + JS puro) para criar tickets, listá-los e disparar a análise por IA com um clique.

🔗 **Demo online:** a API está publicada em [https://seu-link-aqui.com](https://seu-link-aqui.com) para fins de teste/demonstração. A documentação interativa pode ser acessada em `https://seu-link-aqui.com/docs`.

## Funcionalidades

- **Criação de tickets** com título e descrição do problema
- **Listagem paginada** de tickets (`limit`/`offset`)
- **Classificação por IA**: envia o conteúdo do ticket para o modelo Gemini, que retorna o tom do cliente (irritado, neutro ou positivo) e o nível de urgência (Alta, Média, Baixa)
- **Persistência** dos tickets e do resultado da classificação em banco de dados relacional
- **Frontend embutido**: painel HTML servido diretamente pela API para testar o fluxo sem precisar de ferramentas externas

## Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** — framework web assíncrono
- **[SQLAlchemy](https://www.sqlalchemy.org/)** (ORM, `Mapped`/`mapped_column`) — persistência de dados
- **[Pydantic](https://docs.pydantic.dev/) / pydantic-settings** — validação de dados e configuração via variáveis de ambiente
- **[Google Gen AI SDK](https://ai.google.dev/)** (`google-genai`) — integração com o modelo Gemini para classificação de sentimento/urgência
- **HTML + JavaScript puro** — interface do painel de tickets

## Arquitetura

O projeto segue uma separação em camadas inspirada em Clean Architecture / Repository Pattern:

```
app/
├── core/            # Configuração, conexão com banco e injeção de dependências
│   ├── config.py     # Settings (variáveis de ambiente via pydantic-settings)
│   ├── database.py   # Engine e sessão do SQLAlchemy
│   └── deps.py        # Dependency injection (get_db)
├── models/          # Modelos ORM (SQLAlchemy)
│   └── ticket.py
├── schemas/         # Schemas de entrada/saída (Pydantic)
│   ├── common.py      # Schema genérico de paginação
│   └── ticket.py
├── repositories/    # Acesso a dados (camada de persistência)
│   └── ticket.py
├── services/        # Regras de negócio e integração com a IA
│   └── ticket.py
├── routes/          # Endpoints da API (controllers)
│   └── ticket.py
├── index.html       # Frontend simples servido pela API
└── main.py          # Ponto de entrada da aplicação (FastAPI app)
```

Fluxo de uma requisição: **Route → Service → Repository → Model**, com os schemas Pydantic garantindo a validação e o formato dos dados de entrada/saída em cada camada.

## Endpoints

| Método | Rota                     | Descrição                                              |
|--------|--------------------------|----------------------------------------------------------|
| `POST` | `/tickets`               | Cria um novo ticket                                       |
| `GET`  | `/tickets`               | Lista tickets de forma paginada                            |
| `POST` | `/tickets/{id}/classify` | Envia o ticket para a IA e salva a classificação retornada |
| `GET`  | `/`                      | Serve o painel web (frontend)                              |

### Exemplo — criar ticket

```bash
curl -X POST http://localhost:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{"title": "Sistema lento", "description": "O sistema está travando toda vez que tento gerar um relatório."}'
```

### Exemplo — classificar ticket com IA

```bash
curl -X POST http://localhost:8000/tickets/1/classify
```

Resposta (`ai_classification`) trazendo o tom do cliente e a urgência identificados pela IA, ex: `"Tom: irritado. Urgência: Alta."`

## Como rodar localmente

### Pré-requisitos

- Python 3.11+
- Uma chave de API do Google (Gemini) — [obtenha aqui](https://ai.google.dev/)

### Passos

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd <nome-do-projeto>

# 2. Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings google-genai

# 4. Configure as variáveis de ambiente
```

Crie um arquivo `.env` na raiz do projeto:

```env
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:8000,http://localhost:5500
DATABASE_URL=sqlite:///./tickets.db
GOOGLE_API_KEY=sua_chave_da_api_google_aqui
```

```bash
# 5. Rode a aplicação
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000` e o painel web na raiz (`/`). A documentação interativa (Swagger) fica em `http://localhost:8000/docs`.

## Possíveis evoluções

- Autenticação e autorização de usuários/atendentes
- Webhooks/notificações quando um ticket é classificado como urgência alta
- Migrations com Alembic
- Testes automatizados (unitários e de integração)
- Deploy em containers (Docker)

## Sobre o projeto

Projeto desenvolvido para praticar arquitetura em camadas com FastAPI e integração de um serviço de IA generativa em um fluxo de negócio real (triagem automática de suporte ao cliente).
