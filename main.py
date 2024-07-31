from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes.route import router

app = FastAPI()

origins = [
    "http://localhost:5173",  # Update this to your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
