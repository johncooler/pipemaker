from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    ssh_url: str


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    creator_id: int

    class Config:
        orm_mode = True
