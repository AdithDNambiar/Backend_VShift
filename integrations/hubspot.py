import os
import requests
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from redis_client import store_token, get_token

load_dotenv()

router = APIRouter()

HUBSPOT_CLIENT_ID = os.getenv("HUBSPOT_CLIENT_ID")
HUBSPOT_CLIENT_SECRET = os.getenv("HUBSPOT_CLIENT_SECRET")
HUBSPOT_REDIRECT_URI = os.getenv("HUBSPOT_REDIRECT_URI")

@router.get("/auth/hubspot")
def authorize_hubspot():
    url = (
        "https://app.hubspot.com/oauth/authorize"
        f"?client_id={HUBSPOT_CLIENT_ID}"
        f"&redirect_uri={HUBSPOT_REDIRECT_URI}"
        f"&scope=crm.objects.contacts.read crm.objects.contacts.write"
    )
    return RedirectResponse(url)

@router.get("/auth/callback")
def oauth2callback_hubspot(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Authorization code not found."}

    token_url = "https://api.hubapi.com/oauth/v1/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": HUBSPOT_CLIENT_ID,
        "client_secret": HUBSPOT_CLIENT_SECRET,
        "redirect_uri": HUBSPOT_REDIRECT_URI,
        "code": code
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=data, headers=headers)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        store_token("hubspot_access_token", access_token)
        store_token("hubspot_refresh_token", refresh_token)
        return {"message": "Token stored in Redis!"}
    else:
        return {"error": "Token exchange failed", "details": response.text}

@router.get("/hubspot/contacts")
def get_contacts():
    access_token = get_token("hubspot_access_token")
    if not access_token:
        return {"error": "Access token not available"}

    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": "Failed to fetch contacts",
            "details": response.text
        }
