from sqlalchemy.orm import Session
from app.domains.building import repository, schemas, models

def get_building_details(db: Session, building_id: int):
    building = repository.get_building(db, building_id)
    if building is None:
        raise ValueError(f"Building with id {building_id} not found")
    return building

def list_buildings(db: Session, skip: int = 0, limit: int = 100):
    return repository.get_buildings(db, skip=skip, limit=limit)

def create_new_building(db: Session, building_data: schemas.BuildingCreate):
    building = models.Building(**building_data.dict())
    return repository.create_building(db, building)

def list_buildings_in_bounds(db: Session, lat_min: float, lat_max: float, lon_min: float, lon_max: float):
    return repository.get_buildings_in_bounds(db, lat_min, lat_max, lon_min, lon_max)
