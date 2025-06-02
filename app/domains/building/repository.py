from sqlalchemy.orm import Session
from app.domains.building.models import Building

def get_building(db: Session, building_id: int):
    return db.query(Building).filter(Building.id == building_id).first()

def get_buildings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Building).offset(skip).limit(limit).all()

def create_building(db: Session, building: Building):
    db.add(building)
    db.commit()
    db.refresh(building)
    return building

def get_buildings_in_bounds(db: Session, lat_min: float, lat_max: float, lon_min: float, lon_max: float):
    return db.query(Building).filter(
        Building.latitude >= lat_min,
        Building.latitude <= lat_max,
        Building.longitude >= lon_min,
        Building.longitude <= lon_max
    ).all()
