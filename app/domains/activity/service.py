from sqlalchemy.orm import Session
from app.domains.activity import repository, schemas

def get_activity_details(db: Session, activity_id: int):
    activity = repository.get_activity(db, activity_id)
    if activity is None:
        raise ValueError(f"Activity with id {activity_id} not found")
    return activity

def list_activities(db: Session, skip: int = 0, limit: int = 100):
    return repository.get_activities(db, skip=skip, limit=limit)

def _get_activity_depth(db: Session, activity_id: int) -> int:
    """Helper function that computes the current depth of the parent chain.
       Level 1: root (no parent)
       Level 2: child of root, etc.
    """
    depth = 1
    current = repository.get_activity(db, activity_id)
    while current is not None and current.parent_id is not None:
        depth += 1
        current = repository.get_activity(db, current.parent_id)
    return depth

def create_new_activity(db: Session, activity_data: schemas.ActivityCreate):
    # If a parent is provided, check the nesting depth.
    if activity_data.parent_id is not None:
        depth = _get_activity_depth(db, activity_data.parent_id)
        # Adding a new child would increase the depth by 1.
        if depth >= 3:
            raise ValueError("Maximum nesting level of 3 exceeded")
    return repository.create_activity(db, activity_data)
