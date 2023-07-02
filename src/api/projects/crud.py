from sqlalchemy.orm import Session

from .models import Project
from .schemas import ProjectCreate


def create_project(db: Session, project: ProjectCreate, creator_id: int):
    project = Project(name=project.name, ssh_url=project.ssh_url, creator_id=creator_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
