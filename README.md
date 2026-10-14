# Adal Көмек (Адал қоғам) — AI Legal & Anti-Corruption Consultant

An intelligent, production-ready Telegram bot developed for the **MUIT "Adal Qogam" AI Hackathon**. The system acts as a smart legal consultant on the New Constitution of the Republic of Kazakhstan (2026) and core national ideology concepts: *“Adal Azamat”*, *“Taza Qazaqstan”*, and *“Law and Order”* [EF92jK].

The bot analyzes citizen complaints, maps them to ideological dimensions, generates automated legal resolutions via LLM, logs events into an asynchronous database, and exports valid, auto-filled official statements in Microsoft Word (`.docx`) format [EF92jK].

---

## 🏗 System Architecture & Clean Code Design

The project strictly follows the **Separation of Concerns (SoC)** principle and modern asynchronous Python patterns. No monolithic structures. 

```text
adal_cop_bot/
│
├── config/
│   └── settings.py       # Pydantic-style environment loading & validation
│
├── database/
│   ├── base.py           # Async engine setup & session factory (SQLAlchemy + aiosqlite)
│   └── models.py         # Relational database models (Users & Complaints)
│
├── handlers/
│   └── complaints.py     # State Machine (FSM) handlers & UX/UI Telegram routing
│
├── services/
│   ├── ai_service.py     # OpenAI API client with JSON-structured output logic
│   └── doc_service.py    # Auto-generation of official .docx legal forms (Times New Roman)
│
├── .env                  # local secrets (Ignored via .gitignore according to rule 6.4)
├── .gitignore
├── requirements.txt      # Production-pinned dependencies
└── main.py               # Application entrypoint & async polling initializer
```

### Key Technical Highlights:
1. **Frontend (Telegram Interface)**: Built on `aiogram 3.x` using asynchronous message polling and Finite State Machine (FSM) for strict user state management.
2. **Backend**: Implements high-performance `async/await` patterns preventing main-thread blocking during API requests or database writes.
3. **Database Layer**: `SQLAlchemy 2.0` with `aiosqlite`. Uses asynchronous context managers (`AsyncSessionLocal`) ensuring thread-safe database operations.
4. **AI/ML Layer**: Connected via `OpenAI GPT-4o-mini` API. Enforces strict `response_format={"type": "json_object"}` to guarantee flawless dynamic parsing without data corruption.
5. **Document Generation Service**: Uses `python-docx` to dynamically inject client parameters into formatted legal complaints using the official **Times New Roman 12pt** RK formatting standard.

---

## 🚀 Getting Started & Local Setup

### Prerequisites
* Python 3.10 or higher
* Active OpenAI API Key

### 1. Clone the repository
```bash
git clone https://github.com
cd adal_cop_bot
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory. **Do not commit this file to public repositories (Rule 6.4 compliance)**.
```env
TELEGRAM_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Application
The script automatically builds the SQLite relational database schema on the first startup.
```bash
python main.py
```

---

## 🏛 Hackathon Evaluation Criteria Alignment

* **Security First (Rule 6.4)**: All authorization tokens and keys are compartmentalized into decoupled environment files.
* **Data Persistence (Rule 2.1 & 9.2)**: User registration profiles and AI resolution historical data are thoroughly logged into an isolated DB instance.
* **Ideological Knowledge Base Integration (Rule 4.1)**: Prompt engineering safely aligns unstructured user constraints into legally bounded parameters referencing the **New Constitution of the Republic of Kazakhstan (2026)**.
