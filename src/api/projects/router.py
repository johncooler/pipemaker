from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from .schemas import ProjectCreate, Project
from .crud import create_project
from session import get_db
from auth.models import User
from auth.security import get_current_user_from_token
from . import crud

router = APIRouter()


@router.post("/create-project/")
async def create_project(project: ProjectCreate,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user_from_token)):
    crud.create_project(db=db, project=project, creator_id=current_user.id)
    return {"message": f"{project.name} project successfully created"}


@router.delete("/delete-project/")
async def delete_project():
    pass


@router.put("/modify-project/")
async def modify_project():
    pass
