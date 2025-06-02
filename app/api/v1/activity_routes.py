from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.domains.activity import schemas, service
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.ActivityRead])
def get_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of activities.
    """
    return service.list_activities(db, skip=skip, limit=limit)

@router.get("/{activity_id}", response_model=schemas.ActivityRead)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an activity and its nested children by activity ID.
    """
    try:
        activity = service.get_activity_details(db, activity_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.post("/", response_model=schemas.ActivityRead, status_code=201)
def create_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    """
    Create a new activity. Creating a child activity when the parent is already at level 3 is forbidden.
    """
    try:
        new_activity = service.create_new_activity(db, activity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return new_activity
