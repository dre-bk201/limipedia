from typing import Optional, List

from pydantic import BaseModel
from .weapons import BasicInfo, Stats, Skill, ReforgeInfo, AwakeningMaterials, AwakeningInfo, Item


class DefGear(BaseModel):
    id: int
    name: str
    icon_xl: str
    thumbnail: str
    basic_info: BasicInfo
    stats: Stats
    skill: Optional[Skill] = None
    reforge_info: ReforgeInfo
    awakening_materials: Optional[AwakeningMaterials] = None
    awakening_info: Optional[AwakeningInfo] = None
