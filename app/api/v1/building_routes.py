from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.domains.building import schemas, service
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Building])
def get_buildings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all buildings.
    """
    return service.list_buildings(db, skip=skip, limit=limit)

@router.get("/{building_id}", response_model=schemas.Building)
def get_building(building_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single building by its ID.
    """
    try:
        building = service.get_building_details(db, building_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Building not found")
    return building

@router.get("/bounds", response_model=List[schemas.Building])
def get_buildings_by_bounds(
    lat_min: float = Query(..., description="Minimum latitude"),
    lat_max: float = Query(..., description="Maximum latitude"),
    lon_min: float = Query(..., description="Minimum longitude"),
    lon_max: float = Query(..., description="Maximum longitude"),
    db: Session = Depends(get_db)
):
    """
    Retrieve buildings within the specified geo-boundaries.
    """
    return service.list_buildings_in_bounds(db, lat_min, lat_max, lon_min, lon_max)

@router.post("/", response_model=schemas.Building, status_code=201)
def create_building(building: schemas.BuildingCreate, db: Session = Depends(get_db)):
    """
    Create a new building record.
    """
    return service.create_new_building(db, building)
