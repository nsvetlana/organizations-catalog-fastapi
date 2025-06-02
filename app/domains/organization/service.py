from sqlalchemy.orm import Session
from app.domains.organization import repository, schemas

def get_organization_details(db: Session, organization_id: int):
    org = repository.get_organization(db, organization_id)
    if org is None:
        raise ValueError(f"Organization with id {organization_id} not found")
    return org

def list_organizations(db: Session, skip: int = 0, limit: int = 100):
    return repository.get_organizations(db, skip=skip, limit=limit)

def create_new_organization(db: Session, org_data: schemas.OrganizationCreate):
    return repository.create_organization(db, org_data)
