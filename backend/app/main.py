import sqlite3
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="FastAPI Backend",
    description="Starter backend framework for React frontend integration",
    version="0.1.0",
)

DB_PATH = Path(__file__).resolve().parent / "mario.db"


class SaveStateIn(BaseModel):
    level: int = Field(ge=1)
    lives: int = Field(ge=0)
    coins: int = Field(ge=0)


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS save_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                level INTEGER NOT NULL,
                lives INTEGER NOT NULL,
                coins INTEGER NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict:
    return {"service": "backend", "status": "running"}


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "service": "fastapi"}


@app.get("/api/message")
def message() -> dict:
    return {"message": "Hello from FastAPI!", "version": app.version}


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/api/game/save")
def get_save_state() -> dict:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT level, lives, coins, updated_at FROM save_state WHERE id = 1"
        ).fetchone()

    if row is None:
        return {"exists": False, "state": None}

    return {
        "exists": True,
        "state": {
            "level": row["level"],
            "lives": row["lives"],
            "coins": row["coins"],
            "updated_at": row["updated_at"],
        },
    }


@app.post("/api/game/save")
def save_game_state(payload: SaveStateIn) -> dict:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO save_state (id, level, lives, coins, updated_at)
            VALUES (1, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET
                level=excluded.level,
                lives=excluded.lives,
                coins=excluded.coins,
                updated_at=CURRENT_TIMESTAMP
            """,
            (payload.level, payload.lives, payload.coins),
        )
        connection.commit()

    return {"ok": True}
