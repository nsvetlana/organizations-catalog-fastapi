from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base import Base

# Association table for many-to-many relationship between organizations and activities.
# (Assumes an "activities" table exists in another domain.)
organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id")),
    Column("activity_id", Integer, ForeignKey("activities.id"))
)


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    building_id = Column(Integer, ForeignKey("building.id"), nullable=False)

    # One-to-many: Organization can have multiple phone numbers.
    phone_numbers = relationship("PhoneNumber", back_populates="organization", cascade="all, delete-orphan")

    # Many-to-many: Organization can have multiple activities.
    activities = relationship("Activity", secondary=organization_activity, back_populates="organizations")


class PhoneNumber(Base):
    __tablename__ = "phone_numbers"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    # Relationship: Each phone number belongs to one organization.
    organization = relationship("Organization", back_populates="phone_numbers")

# Note: The "Activity" and "Building" models are assumed to exist in their respective domains.
