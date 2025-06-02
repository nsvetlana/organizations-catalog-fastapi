from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.domains.organization import schemas, service
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.Organization])
def read_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of organizations.
    """
    organizations = service.list_organizations(db, skip=skip, limit=limit)
    return organizations

@router.get("/{organization_id}", response_model=schemas.Organization)
def read_organization(organization_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single organization by its ID.
    """
    try:
        organization = service.get_organization_details(db, organization_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.post("/", response_model=schemas.Organization, status_code=201)
def create_organization(org: schemas.OrganizationCreate, db: Session = Depends(get_db)):
    """
    Create a new organization.
    """
    new_org = service.create_new_organization(db, org)
    return new_org
