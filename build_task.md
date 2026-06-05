# 角色与任务定义
你现在是一个资深的医疗影像全栈工程师。你需要帮我自动化搭建一个“放射科专业病例阅片学习平台”的 MVP 版本。
系统架构为：FastAPI + PostgreSQL + Orthanc + OHIF Viewer + Nginx 统一网关。

## 严格执行要求
1. 请不要省略任何代码，不要使用 `// ... existing code ...` 这种占位符。
2. 请按照下方指定的目录结构和文件路径，逐一创建或覆盖现有文件。
3. 如果遇到没有对应目录的情况，请先创建所需的文件夹。
4. 所有文本和代码文件均使用 UTF-8 编码。

---

## 步骤一：创建项目目录树
请确保当前工作目录下包含以下目录结构：
- `orthanc-config/`
- `backend/`
- `frontend/html/`
- `scripts/`

---

## 步骤二：生成核心配置文件

### 1. `docker-compose.yml` (根目录)
```yaml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./frontend/html:/usr/share/nginx/html:ro
    depends_on:
      - api
      - orthanc
      - viewer

  orthanc:
    image: jodogne/orthanc-plugins:latest
    volumes:
      - ./orthanc-config/orthanc.json:/etc/orthanc/orthanc.json:ro
      - orthanc_db:/var/lib/orthanc/db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=radio
      - POSTGRES_PASSWORD=radio123
      - POSTGRES_DB=cases
    volumes:
      - pgdata:/var/lib/postgresql/data

  api:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://radio:radio123@db/cases
    depends_on:
      - db

  viewer:
    image: ohif/viewer:latest
    environment:
      - APP_CONFIG=/usr/share/nginx/html/app-config.js
    volumes:
      - ./frontend/ohif-config.js:/usr/share/nginx/html/app-config.js:ro

volumes:
  pgdata:
  orthanc_db:
2. nginx.conf (根目录)
Nginx
server {
    listen 80;

    location / {
        root /usr/share/nginx/html;
        index index.html;
    }

    location /api/ {
        proxy_pass http://api:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /dicom-web/ {
        proxy_pass http://orthanc:8042/dicom-web/;
        proxy_set_header Host $host;
    }
    
    location /viewer/ {
        proxy_pass http://viewer:80/;
        proxy_set_header Host $host;
    }
}
3. orthanc-config/orthanc.json
JSON
{
  "Name": "RadioLearning",
  "StorageDirectory": "/var/lib/orthanc/db",
  "DicomWeb": {
    "Enable": true,
    "Root": "/dicom-web/"
  },
  "HttpServerEnabled": true,
  "DicomServerEnabled": true,
  "AuthenticationEnabled": false,
  "RemoteAccessAllowed": true,
  "StoreDicom": true,
  "Plugins": [],
  "CorsRequests": {
    "AllowOrigin": "*",
    "AllowCredentials": true,
    "AllowHeaders": ["Origin", "Accept", "Content-Type", "X-Requested-With", "Authorization"],
    "AllowMethods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
  }
}
##步骤三：生成后端代码 (FastAPI)
1. backend/requirements.txt
Plaintext
fastapi
uvicorn
psycopg2-binary
python-multipart
PyJWT==2.8.0
passlib[bcrypt]==1.7.4
2. backend/Dockerfile
Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
3. backend/main.py
Python
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
##步骤四：生成前端页面与配置
1. frontend/ohif-config.js
JavaScript
window.config = {
  routerBasename: '/viewer',
  servers: {
    dicomWeb: [
      {
        name: 'Orthanc',
        wadoUriRoot: '/dicom-web',
        qidoRoot: '/dicom-web',
        wadoRoot: '/dicom-web',
        qidoSupportsIncludeField: false,
        imageRendering: 'wadors',
        thumbnailRendering: 'wadors',
        requestOptions: { requestFromBrowser: true },
      },
    ],
  },
  studyListFunctionsEnabled: true,
};
2. frontend/html/index.html
HTML
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><title>放射科教学系统</title>
    <style>body{font-family:sans-serif; padding:20px; background:#f4f4f9;} .card{background:white; padding:15px; margin-bottom:10px; border-radius:5px; cursor:pointer; box-shadow:0 2px 4px rgba(0,0,0,0.1);}</style>
</head>
<body>
    <h2>系统大厅</h2>
    <div id="auth-panel">
        <input type="text" id="user" placeholder="用户名">
        <input type="password" id="pwd" placeholder="密码">
        <button onclick="login()">登录</button>
        <button onclick="register()">注册</button>
    </div>
    <h3 id="welcome-msg" style="display:none; color:green;"></h3>
    <hr>
    <h3>可用病例列表</h3>
    <div id="case-list"></div>

    <script>
        const token = localStorage.getItem('radio_token');
        if(token) {
            document.getElementById('auth-panel').style.display = 'none';
            document.getElementById('welcome-msg').style.display = 'block';
            document.getElementById('welcome-msg').innerText = '您已登录，请选择病例学习';
        }

        async function register() {
            const res = await fetch('/api/auth/register', {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: user.value, password: pwd.value})
            });
            alert(res.ok ? "注册成功，请点击登录" : "注册失败(用户名可能存在)");
        }

        async function login() {
            const formData = new URLSearchParams();
            formData.append('username', user.value);
            formData.append('password', pwd.value);
            const res = await fetch('/api/auth/login', { method: 'POST', body: formData });
            if(res.ok) {
                const data = await res.json();
                localStorage.setItem('radio_token', data.access_token);
                window.location.reload();
            } else { alert("账号或密码错误"); }
        }

        async function loadCases() {
            const res = await fetch('/api/cases');
            const cases = await res.json();
            const container = document.getElementById('case-list');
            cases.forEach(c => {
                const div = document.createElement('div');
                div.className = 'card';
                div.innerHTML = `<strong>${c.title}</strong> - [${c.modality}]`;
                div.onclick = () => window.location.href = `/study.html?case_id=${c.id}&study_uid=${c.study_uid}`;
                container.appendChild(div);
            });
        }
        loadCases();
    </script>
</body>
</html>
3. frontend/html/study.html
HTML
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><title>阅片与讨论</title>
    <style>
        body { margin: 0; display: flex; height: 100vh; font-family: sans-serif; background: #121212; color: #e0e0e0; }
        #viewer-container { flex: 65%; border-right: 2px solid #333; }
        iframe { width: 100%; height: 100%; border: none; }
        #panel-container { flex: 35%; display: flex; flex-direction: column; background: #1e1e1e; padding: 20px;}
        .report-section { flex: 1; overflow-y: auto; border-bottom: 1px solid #444; margin-bottom:15px; }
        .comment-item { background: #333; padding: 10px; border-radius: 5px; margin-bottom: 10px; font-size: 14px;}
    </style>
</head>
<body>
    <div id="viewer-container">
        <iframe id="ohif-iframe" src=""></iframe>
    </div>
    <div id="panel-container">
        <div class="report-section">
            <h3 style="color:#4db8ff">影像表现 (Findings)</h3>
            <p id="rep-findings">加载中...</p>
            <h3 style="color:#4db8ff">诊断意见 (Impression)</h3>
            <p id="rep-impression">加载中...</p>
        </div>
        <div style="height: 40%; display: flex; flex-direction: column;">
            <h3>讨论区</h3>
            <div id="comments-list" style="flex:1; overflow-y:auto; margin-bottom:10px;"></div>
            <div style="display:flex; gap:10px;">
                <input type="text" id="comment-text" placeholder="输入留言..." style="flex:1; padding:8px; background:#333; color:white; border:1px solid #555;">
                <button onclick="submitComment()" style="padding:8px 15px; background:#4db8ff; border:none; font-weight:bold; cursor:pointer;">发送</button>
            </div>
        </div>
    </div>

    <script>
        const urlParams = new URLSearchParams(window.location.search);
        const caseId = urlParams.get('case_id');
        const studyUid = urlParams.get('study_uid');

        document.getElementById('ohif-iframe').src = `/viewer?StudyInstanceUIDs=${studyUid}`;

        async function loadDetails() {
            const res = await fetch(`/api/cases/${caseId}/details`);
            const data = await res.json();
            if(data.report) {
                document.getElementById('rep-findings').innerText = data.report.findings || '暂无内容';
                document.getElementById('rep-impression').innerText = data.report.impression || '暂无内容';
            }
            document.getElementById('comments-list').innerHTML = data.comments.map(c => 
                `<div class="comment-item"><strong>${c.username}</strong> <span style="font-size:12px;color:#888;">${c.time}</span><br><div style="margin-top:5px">${c.content}</div></div>`
            ).join('');
        }

        async function submitComment() {
            const token = localStorage.getItem('radio_token');
            if(!token) return alert('请先回首页登录！');
            
            const content = document.getElementById('comment-text').value;
            if(!content.trim()) return;

            const res = await fetch(`/api/cases/${caseId}/comments`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify({ content })
            });
            
            if(res.ok) {
                document.getElementById('comment-text').value = '';
                loadDetails();
            } else {
                alert('登录已过期，请重新登录');
            }
        }
        loadDetails();
    </script>
</body>
</html>
3. scripts/upload_anonymize.py
Python
import os, sys, httpx

ORTHANC_URL = "http://localhost/dicom-web"

def process_dicom(input_dir):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(('.dcm', '.ima')):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    res = httpx.post(f"{ORTHANC_URL}/studies", 
                                     content=f.read(), 
                                     headers={"Content-Type": "application/dicom"})
                    if res.status_code == 200:
                        print(f"Uploaded: {file}")
                    else:
                        print(f"Failed: {file} - {res.status_code}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python upload_anonymize.py <input_dir>")
        sys.exit(1)
    process_dicom(sys.argv[1])
##步骤五：最终检查与启动提醒
请在完成所有文件的创建后，向用户反馈：“文件已全部生成完毕。你可以直接在终端中运行 docker compose up -d --build 来启动服务。”