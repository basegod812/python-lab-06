"""FastAPI: JSON endpoint, SQLite CRUD, WebSocket local chat."""
from contextlib import closing
from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

app = FastAPI(title="ЛР №6 — Вариант 2")
DB = Path(__file__).with_name("tasks.sqlite3")


def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with closing(connect()) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )""")
        conn.commit()


init_db()


class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    done: bool = False


@app.get("/api/hello")
def hello():
    """Среднее №7: JSON endpoint."""
    return {"message": "Привет, FastAPI!", "variant": 2}


@app.get("/api/tasks")
def get_tasks():
    with closing(connect()) as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM tasks ORDER BY id")]


@app.post("/api/tasks", status_code=201)
def create_task(task: TaskIn):
    with closing(connect()) as conn:
        cursor = conn.execute("INSERT INTO tasks(title) VALUES (?)", (task.title,))
        conn.commit()
        return {"id": cursor.lastrowid, "title": task.title, "done": False}


@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    with closing(connect()) as conn:
        cursor = conn.execute(
            "UPDATE tasks SET title=?, done=? WHERE id=?",
            (task.title, int(task.done), task_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(404, "Задача не найдена")
        return {"id": task_id, "title": task.title, "done": task.done}


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    with closing(connect()) as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(404, "Задача не найдена")
        return {"deleted": task_id}


class ChatRoom:
    def __init__(self):
        self.clients: set[WebSocket] = set()

    async def broadcast(self, text: str):
        for client in tuple(self.clients):
            await client.send_text(text)


room = ChatRoom()


@app.websocket("/ws")
async def chat(websocket: WebSocket):
    """Повышенное №6: локальный WebSocket-чат."""
    await websocket.accept()
    room.clients.add(websocket)
    try:
        await room.broadcast("Новый участник подключился")
        while True:
            message = await websocket.receive_text()
            await room.broadcast(message)
    except WebSocketDisconnect:
        pass
    finally:
        room.clients.discard(websocket)
