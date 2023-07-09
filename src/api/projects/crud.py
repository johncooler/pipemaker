from sqlalchemy.orm import Session

from .models import Project
from .schemas import ProjectCreate, ProjectUpdate


def get_project_by_id(project_id: int, db: Session):
    project = db.query(Project).filter(Project.id == project_id).first()
    return project


def create_project(project: ProjectCreate, creator_id: int, db: Session):
    project = Project(name=project.name, ssh_url=project.ssh_url, creator_id=creator_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(project_id: id,
                   current_user_id: int,
                   project: ProjectUpdate,
                   db: Session):
    project_in_db = get_project_by_id(project_id=project_id,
                                      db=db)
    if not project_in_db:
        return {"error": 404}  # project does not exist
    if not project_in_db.creator_id == current_user_id:
        return {"error": 403}  # not creator tries to modify the project
    project_in_db.name = project.name
    project_in_db.ssh_url = project.ssh_url
    db.add(project_in_db)
    db.commit()
    return project_in_db


def delete_project(project_id: int, current_user_id: id, db: Session):
    project_in_db = get_project_by_id(project_id=project_id,
                                      db=db)
    if not project_in_db:
        return {"error": 404}  # project does not exist
    if not project_in_db.creator_id == current_user_id:
        return {"error": 403}  # not creator tries to delete the project
    db.delete(project_in_db)
    db.commit()
