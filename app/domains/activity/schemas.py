from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel

class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    pass

# Level 3: No further nesting allowed.
class ActivityReadLevel3(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None

    class Config:
        orm_mode = True

# Level 2: Children can be Level 3 objects.
class ActivityReadLevel2(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    children: List[ActivityReadLevel3] = []

    class Config:
        orm_mode = True

# Level 1 (root): Children can be Level 2 objects, thereby ensuring a max of three levels.
class ActivityRead(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    children: List[ActivityReadLevel2] = []

    class Config:
        orm_mode = True
