from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .schemas import ProjectCreate, ProjectUpdate
from session import get_db
from auth.models import User
from auth.security import get_current_user_from_token
from . import crud

router = APIRouter()


@router.post("/create-project/")
async def create_project(project: ProjectCreate,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user_from_token)):
    crud.create_project(project=project, creator_id=current_user.id, db=db)
    return {"message": f"{project.name} project successfully created"}


@router.put("/update-project/{project_id}")
async def update_a_project(project_id: int,
                           project: ProjectUpdate,
                           db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user_from_token)):
    project = crud.update_project(project_id=project_id,
                                  current_user_id=current_user.id,
                                  project=project, db=db)
    if isinstance(project, dict):
        if project["error"] == 403:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Only the author can modify the project")
        elif project["error"] == 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Project does not exist")
    return {"message": f"Project successfully modified"}


@router.delete("/delete-project/{project_id}")
async def delete_project(project_id: int,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user_from_token)):
    deleting_of_the_project = crud.delete_project(project_id=project_id,
                                                  current_user_id=current_user.id,
                                                  db=db)
    if isinstance(deleting_of_the_project, dict):
        if deleting_of_the_project["error"] == 403:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Only the author can delete the project")
        elif deleting_of_the_project["error"] == 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Project does not exist")
    return {"message": f"Project successfully deleted"}
