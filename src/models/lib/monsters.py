from typing import List, Optional, Union, Type, TypeVar
from pydantic import BaseModel
from bs4.element import Tag


import models.lib.weapons as weapons

from utils import group_as, uid


BurstSkillsType = TypeVar("BurstSkillsType", bound="BurstSkills")
HiddenPotentialType = TypeVar("HiddenPotentialType", bound="HiddenPotential")
RandomStatsType = TypeVar("RandomStatsType", bound="RandomStats")
StatsVariantType = TypeVar("StatsVariantType", bound="StatsVariant")
EnlighteningInfoType = TypeVar(
    "EnlighteningInfoType", bound="EnlighteningInfo")


class RandomStats(BaseModel):
    initial: List[str]
    max_1: List[str]
    max_2: Optional[List[str]] = None

    @classmethod
    def new(cls: Type[RandomStatsType], tags: List[Tag]) -> RandomStatsType:
        return cls(
            initial=tags[1:3],
            max_1=tags[4:6],
            max_2=tags[7:] if len(tags) > 7 else None
        )


class StatsVariant(BaseModel):
    @classmethod
    def new(cls: Type[StatsVariantType], tags: List[Tag]) -> Union[weapons.Stats, RandomStats]:
        if len(tags) < 10:
            return RandomStats.new(tags)
        else:
            return weapons.Stats.new(tags)


class PassiveSkill(BaseModel):
    skill_name: str
    effect: str

    @classmethod
    def new(cls, tags: List[Tag]):
        infos = group_as(list(map(lambda e: e.text, tags)), group=2)[2:]
        skill_name, effect = None, None

        if not len(infos):
            return None

        elif "-Burst-" not in infos[0][1]:
            for info in infos:
                if info[0].lower() == "skill name":
                    skill_name = info[1]
                if info[0].lower() == "effect":
                    effect = info[1]

        if not skill_name or not effect:
            return None

        return cls(
            skill_name=skill_name,
            effect=effect
        )


class EnlighteningInfo(BaseModel):
    before_enlightening: Union[weapons.Item, str]
    after_enlightening: Union[weapons.Item, str]

    @classmethod
    def new(cls: Type[EnlighteningInfoType], base_url: str, tags: List[Tag]) -> EnlighteningInfoType:
        if tags:
            return cls(
                before_enlightening=weapons.Item(
                    id=uid(tags[0].select_one("a").text.strip()),
                    icon_url=base_url +
                    tags[0].select_one(".icon")["data-src"],
                    icon_name=tags[0].select_one("p.evo_name").text.strip()
                ) if tags[0].text.strip() != "-" else "-",
                after_enlightening=weapons.Item(
                    id=uid(tags[1].select_one("p.evo_name").text.strip()),
                    icon_url=base_url +
                    tags[1].select_one(".icon")["data-src"],
                    icon_name=tags[1].select_one("p.evo_name").text.strip()
                ) if len(tags) > 1 else "-"
            )
        return None

    @classmethod
    def is_blank(cls, text: Tag) -> bool:
        if text == None:
            return False

        elif text.text.strip() == "-":
            return True

        return False


class EnlighteningMaterials(BaseModel):
    gears: List[weapons.Item]
    items: List[weapons.Item]

    @classmethod
    def new(cls, base_url: str, tags: List[Tag]):
        if tags:
            return cls(
                gears=[weapons.Item(
                    id=uid(child.select_one("p").text.strip()),
                    icon_url=base_url+child.select_one(".sp_icon")["data-src"],
                    icon_name=child.select_one("p").text.strip()
                ) for child in tags[0].select(".special_evolution_material")],
                items=[weapons.Item(
                    id=uid(child.select_one("p").text.strip()),
                    icon_url=base_url+child.select_one(".sp_icon")["data-src"],
                    icon_name=child.select_one("p").text.strip()
                ) for child in tags[1].select(".special_evolution_material")]
            )


class BurstSkills(BaseModel):
    skill_name: str
    effect: str

    @classmethod
    def new(cls: Type[BurstSkillsType], tags: List[Tag]) -> Optional[BurstSkillsType]:
        infos = group_as(list(map(lambda t: t.text, tags)), group=2)[2:]
        skill_name, effect = None, None

        for info in infos:
            if info[0].lower() == "skill name":
                skill_name = info[1]
            if info[0].lower() == "effect":
                effect = info[1]

        if not skill_name or not effect:
            return None

        return cls(
            skill_name=skill_name,
            effect=effect
        )


class BasicInfo(BaseModel):
    rarity: str
    gear_type: str
    gear_cost: int
    element: str
    potential_count: int
    max_level: int
    collaboration: Optional[str]

    @ classmethod
    def new(cls, items: List[str]):
        return BasicInfo(
            rarity=items[0],
            gear_type=items[1],
            gear_cost=items[2],
            element=items[3],
            potential_count=items[4],
            max_level=items[5],
            collaboration=items[6] if len(items) > 6 else None,
        )


class HiddenPotential(BaseModel):
    lv_1_effect: str
    lv_2_effect: str
    lv_3_effect: str
    lv_4_effect: str
    lv_5_effect: Optional[str] = None
    restrictions: Optional[str] = None

    @classmethod
    def new(cls: Type[HiddenPotentialType], tags: List[Tag]) -> HiddenPotentialType:
        pots = []
        restr = None
        infos = group_as(list(map(lambda t: t.text, tags)), group=2)[2:]

        for info in infos:
            if "lv" in info[0].lower():
                pots.append(info[1])

            if "restrictions" == info[0].lower():
                restr = info[1]

        if len(pots):
            return cls(lv_1_effect=pots[0],
                       lv_2_effect=pots[1],
                       lv_3_effect=pots[2],
                       lv_4_effect=pots[3],
                       lv_5_effect=pots[4] if len(pots) > 4 else None, restrictions=restr if restr else None)
        return None


class Monster(BaseModel):
    id: int
    name: str
    icon_xl: str
    thumbnail: str
    basic_info: BasicInfo
    skill: weapons.Skill
    reforge_info: weapons.ReforgeInfo
    stats: Union[weapons.Stats, RandomStats]
    hidden_potential: Optional[HiddenPotential] = None
    passive_skill: Optional[PassiveSkill] = None
    burst_skills: Optional[BurstSkills] = None
    enlightening_info: Optional[EnlighteningInfo] = None
    enlightening_materials: Optional[EnlighteningMaterials] = None
