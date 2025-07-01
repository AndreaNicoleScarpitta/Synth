# main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import init_db
import models.models      # load all SQLModel models so metadata is aware
from api.routes import router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

if __name__ == "__main__":
    init_db()
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
