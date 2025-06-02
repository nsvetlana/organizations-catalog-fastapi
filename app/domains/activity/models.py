from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)

    # Self-referencing relationship: an activity can have many child activities.
    children = relationship(
        "Activity",
        backref="parent",
        remote_side=[id]
    )
