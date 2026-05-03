from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb://localhost:27017/")
db = client["insider_ai"]
logs = db["employee_logs"]

ALLOWED_IP = "152.57.30.225"   
ALLOWED_BROWSER = "Chrome"    
START_TIME = 7               
END_TIME = 20                

USERS = {
    "emp1": "1234", "emp2": "4567", "emp3": "7890", "emp4": "1357",
    "emp5": "2468", "emp6": "0987", "emp7": "0864", "emp8": "7954",
    "emp9": "8754", "emp10": "3456"
}

CONFIDENTIAL_FILES = [
    "salary.xlsx", "company_strategy.pdf", "employee_db.csv",
    "finance_report.docx", "hr_records.pdf", "client_data.xlsx",
    "admin_keys.txt", "server_config.json", "payroll_2024.xlsx",
    "audit_logs.csv"
]


class LoginData(BaseModel):
    username: str
    password: str

class ActivityData(BaseModel):
    username: str
    file_name: str
    file_size: int
    ip: str
    browser: str


@app.post("/login")
def login(data: LoginData):
    if data.username in USERS and USERS[data.username] == data.password:
        return {"status": "success"}
    return {"status": "failed"}

@app.post("/log")
def log_activity(data: ActivityData):
    now = datetime.now()
    hour = now.hour

    suspicious = False
    reasons = []

    
    if data.ip != ALLOWED_IP:
        suspicious = True
        reasons.append("Invalid IP")

    if data.browser != ALLOWED_BROWSER:
        suspicious = True
        reasons.append("Invalid Browser")

    if hour < START_TIME or hour >= END_TIME:
        suspicious = True
        reasons.append("Outside office hours (7AM–8PM)")

   
    if data.file_name in CONFIDENTIAL_FILES:
        reasons.append("Confidential file")
    

    if not suspicious:
        reasons.insert(0, "All security rules satisfied")

    log = {
        "username": data.username,
        "file_name": data.file_name,
        "file_size": data.file_size,
        "time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "ip": data.ip,
        "browser": data.browser,
        "suspicious": suspicious,
        "reason": ", ".join(reasons)
    }

    logs.insert_one(log)
    return {"message": "Logged", "suspicious": suspicious}


@app.get("/hr-logs")
def hr_logs():
    return list(logs.find({}, {"_id": 0}))


@app.delete("/clear")
def clear_logs():
    logs.delete_many({})
    return {"message": "All logs cleared"}
