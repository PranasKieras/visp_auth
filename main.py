# backend/main.py
from fastapi import FastAPI, Depends, Body, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import List
from pydantic import BaseModel
import data_access
from data_access import ViispLoginData

import jwt_token
from generate_xml import get_auth_request_body, get_data_request_body
from xml_utils import extract_ticket, extract_login_info
import requests



app = FastAPI(title="My API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This would be configured with your third-party auth provider's settings
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Ticket(BaseModel):
    ticketId: str

# Verify token function
async def verify_token(token: str = Depends(oauth2_scheme)):

    try:
        full_name, personal_code, country = jwt_token.extract_token_info(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if personal_code is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return personal_code, full_name, country

@app.get("/api/data", response_model=List[ViispLoginData])
async def get_data(user_data: (str,str,str) = Depends(verify_token)):
    return data_access.get_data(user_data[0])

@app.get("/api/info")
async def get_data(user_data: (str,str,str) = Depends(verify_token)):
    return {"name": user_data[1], "country": user_data[2]}

@app.post("/api/ticket")
async def get_ticket():
    body = get_auth_request_body()
    ticket = requests.post(url="https://test.epaslaugos.lt/services/services/auth",
        data=body,
        headers = {"Content-Type": "text/xml"})
    content = ticket.content
    ticket = extract_ticket(content)
    return {"ticket": ticket}

@app.post("/api/token")
async def get_token(ticket: Ticket = Body(...)):
    body = get_data_request_body(ticket.ticketId)
    response = requests.post(
        "https://test.epaslaugos.lt/services/services/auth",
        data=body,
        headers={"Content-Type": "text/xml"})
    if response.status_code == 500:
        raise HTTPException(status_code=401, detail="Internal server error in the called service")
    elif response.status_code == 200:
        login_info = extract_login_info(response.content)
        return jwt_token.issue_token(*login_info)
    else:
        raise HTTPException(status_code=response.status_code, detail="Unexpected response from the called service")

@app.get("/api/validate-token")
async def validate_token(user_id: str = Depends(verify_token)):
    return {"valid": True, "user_id": user_id}

