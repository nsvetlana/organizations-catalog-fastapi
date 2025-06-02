from sqlalchemy.orm import Session
from app.domains.organization import models, schemas


def get_organization(db: Session, organization_id: int):
    return db.query(models.Organization).filter(models.Organization.id == organization_id).first()


def get_organizations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Organization).offset(skip).limit(limit).all()


def create_organization(db: Session, org: schemas.OrganizationCreate):
    db_org = models.Organization(name=org.name, building_id=org.building_id)

    # Create related phone numbers if provided.
    if org.phone_numbers:
        db_org.phone_numbers = [models.PhoneNumber(number=phone.number) for phone in org.phone_numbers]

    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org
