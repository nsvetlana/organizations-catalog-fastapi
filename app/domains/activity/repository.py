from sqlalchemy.orm import Session
from app.domains.activity.models import Activity
from app.domains.activity import schemas

def get_activity(db: Session, activity_id: int) -> Activity:
    return db.query(Activity).filter(Activity.id == activity_id).first()

def get_activities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Activity).offset(skip).limit(limit).all()

def create_activity(db: Session, activity: schemas.ActivityCreate) -> Activity:
    db_activity = Activity(name=activity.name, parent_id=activity.parent_id)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity
