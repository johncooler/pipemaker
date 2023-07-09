from fastapi import FastAPI

from auth.router import router as auth_router
from projects.router import router as projects_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(projects_router, prefix="/projects", tags=["projects"])


@app.get("/", tags=["home"])
def root():
    return {"message": "Welcome to Pipemaker!"}
