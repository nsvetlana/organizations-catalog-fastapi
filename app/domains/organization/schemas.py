from typing import List, Optional
from pydantic import BaseModel

# --- Phone Number Schemas ---
class PhoneNumberBase(BaseModel):
    number: str

class PhoneNumberCreate(PhoneNumberBase):
    pass

class PhoneNumber(PhoneNumberBase):
    id: int

    class Config:
        orm_mode = True

# --- Organization Schemas ---
class OrganizationBase(BaseModel):
    name: str
    building_id: int

class OrganizationCreate(OrganizationBase):
    phone_numbers: Optional[List[PhoneNumberCreate]] = []
    # If needed, add a field: activity_ids: Optional[List[int]] = []

class Organization(OrganizationBase):
    id: int
    phone_numbers: List[PhoneNumber] = []
    # If desired, include activities: activities: List[Activity] = []

    class Config:
        orm_mode = True
