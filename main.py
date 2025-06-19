from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from integrations import hubspot

app = FastAPI()

# Allow requests from frontend (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend is working!"}

# to activate HubSpot routes
app.include_router(hubspot.router)
