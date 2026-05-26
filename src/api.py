import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from src.agente import executar, inicializar

load_dotenv()

DB_PATH = "registros.db"


def _inicializar_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS duvidas (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            usuario   TEXT,
            pergunta  TEXT,
            resposta  TEXT,
            urgencia  TEXT,
            fontes    TEXT,
            latencia  REAL
        )
    """)
    con.commit()
    con.close()


def _registrar(dados: dict):
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "INSERT INTO duvidas (timestamp, usuario, pergunta, resposta, urgencia, fontes, latencia) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            datetime.now().isoformat(),
            dados.get("usuario_id", "anonimo"),
            dados.get("pergunta", ""),
            dados.get("resposta", ""),
            dados.get("urgencia", "baixa"),
            ", ".join(dados.get("fontes", [])),
            dados.get("latencia_s", 0),
        ),
    )
    con.commit()
    con.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    _inicializar_db()
    inicializar()
    yield


app = FastAPI(title="Assistente de Regulamento Esportivo", version="1.0", lifespan=lifespan)


class TicketIn(BaseModel):
    pergunta: str
    usuario_id: str = "anonimo"


class TicketOut(BaseModel):
    resposta: str
    fontes: list[str]
    urgencia: str
    tools_utilizadas: list[str]
    latencia_s: float


@app.post("/perguntar", response_model=TicketOut)
def perguntar(req: TicketIn):
    try:
        resultado = executar(req.pergunta, req.usuario_id)
        _registrar({**resultado, "pergunta": req.pergunta, "usuario_id": req.usuario_id})
        return resultado
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/health")
def health():
    return {"status": "ok"}
