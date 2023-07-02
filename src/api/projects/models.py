from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ssh_url = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="projects")
