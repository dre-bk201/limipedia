from pydantic import BaseModel
from typing import List, Optional, Union
from bs4.element import Tag

from models.lib.weapons import Item  # type: ignore
from utils import group_as, uid


class BasicInfo(BaseModel):
    effect: str
    combo_effect: str
    cost: int
    cooldown: str
    class_type: List[str]

    @classmethod
    def new(cls, basic_info: Tag, base_url: str):
        s = basic_info.select("dd")
        basic_info = [i.text for i in s[:-1]]

        return cls(
            effect=basic_info[0],
            combo_effect=basic_info[1],
            cost=basic_info[2],
            cooldown=basic_info[3],
            class_type=[base_url + href["data-src"]
                        for href in s[4].select("img")]
        )


class MethodLearned(BaseModel):
    how_to_obtain: str
    class_type: Optional[str] = None
    proficiency_req: Optional[int] = None

    @classmethod
    def new(cls, methods: Tag):
        if "acquired from" in methods.select_one("dt").text.lower():
            gear_acquired_from: List[Item] = []

            for icon, name in group_as(methods.select("dd img, dd p"), group=2):
                gear_acquired_from.append(
                    Item(
                        id=uid(name.text),
                        icon_url=icon["data-src"],
                        icon_name=name.text
                    )
                )

            return MethodLearnedVariant(
                gear_acquired_from=gear_acquired_from
            )

        s = group_as(
            list(map(lambda e: e.text, [t for t in methods.select("dt, dd")])), group=2)

        how_to_obtain: Optional[str] = None
        class_type: Optional[str] = None
        proficiency_req: Optional[int] = None

        for item in s:
            if "obtain" in item[0].lower():
                how_to_obtain = item[1].strip()
            elif "class" in item[0].lower():
                class_type = item[1].strip()
            elif "req." in item[0].lower():
                proficiency_req = item[1].strip()

        return cls(
            how_to_obtain=how_to_obtain,
            class_type=class_type,
            proficiency_req=proficiency_req
        )


class MethodLearnedVariant(BaseModel):
    gear_acquired_from: List[Item]

    @classmethod
    def new(cls):
        pass


class Ability(BaseModel):
    id: int
    name: str
    thumbnail: str
    basic_info: BasicInfo
    method_learned: Union[MethodLearned, MethodLearnedVariant]
    # method_learned: MethodLearned
