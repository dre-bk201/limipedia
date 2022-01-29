from typing import Optional, List, Union, TypeVar, Type
from bs4.element import Tag  # type: ignore
from pydantic import BaseModel

from utils import uid

AwakeningMatsType = TypeVar("AwakeningMatsType", bound="AwakeningMaterials")
AbilityEffectType = TypeVar("AbilityEffectType", bound="AbilityEffect")
AwakeningInfoType = TypeVar("AwakeningInfoType", bound="AwakeningInfo")
PassiveSkillType = TypeVar("PassiveSkillType", bound="PassiveSkill")
ReforgeInfoType = TypeVar("ReforgeInfoType", bound="ReforgeInfo")
BasicInfoType = TypeVar("BasicInfoType", bound="BasicInfo")
SkillType = TypeVar("SkillType", bound="Skill")
StatType = TypeVar("StatType", bound="Stats")


class BasicInfo(BaseModel):
    rarity: str
    gear_type: str
    gear_cost: int
    element: str
    infusion_count: int
    max_level: int
    collaboration: Optional[str] = None

    @classmethod
    def new(cls: Type[BasicInfoType], tags: List[str]) -> BasicInfoType:
        if tags:
            return BasicInfo(
                rarity=tags[0],
                gear_type=tags[1],
                gear_cost=tags[2],
                element=tags[3],
                infusion_count=tags[4],
                max_level=tags[5],
                collaboration=tags[6] if len(
                    tags) > 6 else None
            )


class Stats(BaseModel):
    initial: List[str]
    max_1: List[str]
    max_2: Optional[List[str]] = None

    @classmethod
    def new(cls: Type[StatType], stats: List[str]) -> StatType:
        return cls(
            initial=stats[1:5],
            max_1=stats[6:10],
            max_2=stats[11:] if len(stats) > 10 else None
        )


class Skill(BaseModel):
    skill_name: str
    effect: str

    @classmethod
    def new(cls: Type[SkillType], skill: List[str]) -> Union[SkillType, None]:
        if skill:
            return cls(
                skill_name=skill[0],
                effect=skill[1]
            )
        return None


class PassiveSkill(BaseModel):
    skill_name: str
    effect: str

    @classmethod
    def new(cls: Type[PassiveSkillType], passive_skills: List[str]) -> Union[PassiveSkillType, None]:
        if passive_skills is not None and len(passive_skills) > 2:
            return cls(
                skill_name=passive_skills[2],
                effect=passive_skills[3]
            )
        return None


class Item(BaseModel):
    id: int
    icon_url: str
    icon_name: str


class ReforgeInfo(BaseModel):
    before_reforging: Union[Item, str]
    after_reforging: Union[Item, str]

    @classmethod
    def new(cls: Type[ReforgeInfoType], base_url: str, elements: List[Tag]) -> ReforgeInfoType:
        before_reforging = "-" if cls.is_blank(elements[0]) else Item(
            id=uid(elements[0].select_one("a").text.strip()),
            icon_url=base_url +
            elements[0].select_one(".icon")["data-src"],
            icon_name=elements[0].select_one("a").text.strip()
        )

        after_reforging = "-" if cls.is_blank(elements[1]) else Item(
            id=uid(elements[1].select_one("a").text.strip()),
            icon_url=base_url +
            elements[1].select_one(".icon")["data-src"],
            icon_name=elements[1].select_one("a").text.strip()

        )

        return cls(
            before_reforging=before_reforging,
            after_reforging=after_reforging,
        )

    @classmethod
    def is_blank(cls, text: Tag) -> bool:
        if text.text.strip() == "-":
            return True

        return False


class AbilityEffect(BaseModel):
    ability: Item
    effect: str

    @classmethod
    def new(cls: Type[AbilityEffectType], base_url: str, elements: List[Tag]) -> Union[AbilityEffectType, None]:
        if elements:
            return cls(
                ability=Item(
                    id=uid(elements[0].select_one("a").text.strip()),
                    icon_url=base_url +
                    elements[0].select_one(".icon")["data-src"],
                    icon_name=elements[0].select_one("a").text.strip()
                ),
                effect=elements[1].text.strip()
            )
        else:
            return None


class AwakeningInfo(BaseModel):
    before_awakening: Optional[Item] = None
    after_awakening: Optional[Item] = None

    @classmethod
    def new(cls: Type[AwakeningInfoType], base_url: str, tags: List[Tag]):
        if tags:
            return AwakeningInfo(
                before_awakening=Item(
                    id=uid(tags[0].select_one("a").text.strip()),
                    icon_url=base_url +
                    tags[0].select_one(".icon")["data-src"],
                    icon_name=tags[0].select_one("p.evo_name").text.strip()
                ) if tags[0].text.strip() != "-" else None,
                after_awakening=Item(
                    id=uid(tags[1].select_one("p.evo_name").text.strip()),
                    icon_url=base_url +
                    tags[1].select_one(".icon")["data-src"],
                    icon_name=tags[1].select_one("p.evo_name").text.strip()
                ) if len(tags) > 1 else None
            )

        return None

    @classmethod
    def is_blank(cls, text: Tag) -> bool:
        if text.text.strip() == "-":
            return True

        return False


class AwakeningMaterials(BaseModel):
    gears: List[Item]
    items: List[Item]

    @classmethod
    def new(cls: Type[AwakeningInfoType], base_url: str, parents: List[Tag]) -> AwakeningInfoType:
        if parents:
            return cls(
                gears=[Item(
                    id=uid(child.select_one("p").text.strip()),
                    icon_url=base_url+child.select_one(".sp_icon")["data-src"],
                    icon_name=child.select_one("p").text.strip()
                ) for child in parents[0].select(".special_evolution_material")],
                items=[Item(
                    id=uid(child.select_one("p").text.strip()),
                    icon_url=base_url+child.select_one(".sp_icon")["data-src"],
                    icon_name=child.select_one("p").text.strip()
                ) for child in parents[1].select(".special_evolution_material")]
            )


class Weapon(BaseModel):
    id: int
    name: str
    thumbnail: str
    icon_xl: str
    basic_info: BasicInfo
    stats: Stats
    skill: Optional[Skill] = None
    passive_skill: Optional[PassiveSkill] = None
    reforge_info: ReforgeInfo
    ability_effect: Optional[AbilityEffect]
    awakening_materials: Optional[AwakeningMaterials] = None
    awakening_info: Optional[AwakeningInfo] = None
    reforge_materials: Optional[List[Item]] = None
