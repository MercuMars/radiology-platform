from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
import psycopg2
import os
import jwt
from passlib.context import CryptContext

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = "super_secret_medical_key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL, role VARCHAR(20) DEFAULT 'student'
        );
        CREATE TABLE IF NOT EXISTS cases (
            id SERIAL PRIMARY KEY, title TEXT, study_uid TEXT UNIQUE, modality TEXT
        );
        CREATE TABLE IF NOT EXISTS reports (
            id SERIAL PRIMARY KEY, case_id INTEGER REFERENCES cases(id),
            technique TEXT, findings TEXT, impression TEXT
        );
        CREATE TABLE IF NOT EXISTS comments (
            id SERIAL PRIMARY KEY, case_id INTEGER REFERENCES cases(id),
            user_id INTEGER REFERENCES users(id), content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.on_event("startup")
def startup():
    init_db()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not payload.get("sub"): raise Exception
        return {"user_id": payload.get("user_id"), "username": payload.get("sub")}
    except:
        raise HTTPException(status_code=401, detail="凭证无效或过期")

class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/auth/register")
def register(user: UserCreate):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, hashed_password) VALUES (%s, %s)",
                    (user.username, pwd_context.hash(user.password)))
        conn.commit()
        return {"msg": "注册成功"}
    except:
        raise HTTPException(status_code=400, detail="用户名已存在")
    finally:
        cur.close(); conn.close()

@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, username, hashed_password FROM users WHERE username = %s", (form_data.username,))
    user = cur.fetchone()
    cur.close(); conn.close()

    if not user or not pwd_context.verify(form_data.password, user[2]):
        raise HTTPException(status_code=401, detail="密码错误")

    token = jwt.encode({"sub": user[1], "user_id": user[0], "exp": datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/cases")
def get_cases():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, title, study_uid, modality FROM cases")
    rows = [{"id": r[0], "title": r[1], "study_uid": r[2], "modality": r[3]} for r in cur.fetchall()]
    cur.close(); conn.close()
    return rows

@app.get("/cases/{case_id}/details")
def get_details(case_id: int):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT technique, findings, impression FROM reports WHERE case_id = %s", (case_id,))
    rep = cur.fetchone()
    report = {"technique": rep[0], "findings": rep[1], "impression": rep[2]} if rep else None

    cur.execute("SELECT u.username, c.content, c.created_at FROM comments c JOIN users u ON c.user_id = u.id WHERE c.case_id = %s ORDER BY c.created_at ASC", (case_id,))
    comments = [{"username": r[0], "content": r[1], "time": r[2].strftime("%m-%d %H:%M")} for r in cur.fetchall()]
    cur.close(); conn.close()
    return {"report": report, "comments": comments}

class CommentInput(BaseModel):
    content: str

@app.post("/cases/{case_id}/comments")
def add_comment(case_id: int, comment: CommentInput, current_user: dict = Depends(get_current_user)):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("INSERT INTO comments (case_id, user_id, content) VALUES (%s, %s, %s)",
                (case_id, current_user["user_id"], comment.content))
    conn.commit()
    cur.close(); conn.close()
    return {"status": "ok"}
