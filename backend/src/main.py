from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import workspaces, projects, notebooks, jobs

app = FastAPI(title="NotebookRunner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workspaces.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(notebooks.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
