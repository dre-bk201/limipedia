from pathlib import Path
import re
import hashlib

from typing import Any, Dict, List, Optional
from fastapi import HTTPException
from pydantic import BaseModel
from operator import itemgetter
from tinydb import TinyDB
from tinydb.queries import where
from tinydb.storages import MemoryStorage

from models import monsters as M


def camel_to_snake(string: str) -> str:
    return "".join([f"_{ch.lower()}" if ch.isupper() else ch for ch in string]).lstrip(
        "_"
    )


def key_exists(l: BaseModel, keys: str) -> bool:
    return False if l.__fields__.get(camel_to_snake(keys)) is None else True


def __get_field(item: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
    return {k: v for k, v in item.items() if k in fields}


def uid(text: str) -> str:
    return str(int(hashlib.md5(text.encode()).hexdigest(), 16))[0:12]


def reassign(arr: List[Any], extended: List[Any]) -> List[Any]:
    arr.clear()
    arr.extend(extended)


def get_fields(
    model: BaseModel, items: List[Dict[str, Any]], field_str: str
) -> List[Dict[str, Any]]:

    fields = field_str.split(",")
    for field in fields:

        if not key_exists(model, field):
            raise HTTPException(
                status_code=400, detail=f"Resource '{field}' does not exist"
            )

    return [
        __get_field(item, [camel_to_snake(f) for f in field_str.split(",")])
        for item in items
    ]


class QueryParams:
    @classmethod
    def search_param(
        cls,
        database: TinyDB,
        search: Optional[str],
    ) -> List[Dict[str, Any]]:
        if search:
            return database.search(
                where("name").matches(r".*{}.*".format(search), flags=re.I)
            )

        return database.all()

    @classmethod
    def slice_param(
        cls,
        array: List[Dict[str, Any]],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        return array[
            offset
            if offset
            else 0: limit + (offset if offset else 0)
            if limit
            else len(array)
        ]

    @classmethod
    def sort_param(
        self, model: BaseModel, array: List[Dict[str, Any]], sort: Optional[str] = None
    ) -> None:
        if sort != None:
            # reverses order of sorting conditions
            sort_conds = sort.split(",")[::-1]

            for sort_cond in sort_conds:
                if "_asc" in sort_cond.lower() or "_desc" in sort_cond.lower():
                    if len(sort_cond.split("_")) > 2:
                        raise HTTPException(
                            status_code=400,
                            detail="Invalid 'sort' query parameter. ~sort=id_asc,name_desc",
                        )

                    resource, sort_type = sort_cond.split("_")

                    if key_exists(model, resource):
                        if "asc" in sort_type:
                            reassign(array, sorted(
                                array, key=itemgetter(resource)))
                        elif "desc" in sort_type:
                            reassign(array, sorted(
                                array, key=itemgetter(resource), reverse=True
                            ))
                    elif camel_to_snake(resource) == "gear_cost":
                        def sort_func(x): return x["basic_info"]["gear_cost"]
                        if "asc" in sort_type:
                            reassign(

                                array, sorted(array, key=sort_func)
                            )
                        elif "desc" in sort_type:
                            reassign(
                                array, sorted(
                                    array,
                                    key=sort_func,
                                    reverse=True,
                                )
                            )

                    else:
                        raise HTTPException(
                            status_code=404, detail=f"Resource '{resource}' not found"
                        )

                else:
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid 'sort' query parameter. ~sort=id_asc,name_desc",
                    )
        # array

    @classmethod
    def field_param(cls, model: BaseModel, array: List[Dict[str, Any]], field_str: Optional[str] = None):
        if field_str:
            filtered = get_fields(model, array, field_str)
            reassign(array, filtered)

    @classmethod
    def skill_name_param(cls, array: List[Dict[str, Any]], skill: Optional[str] = None):
        if skill:
            database = TinyDB(storage=MemoryStorage)
            database.insert_multiple(array)

            reassign(array,
                     database.search(where("skill")["skill_name"].matches(
                         fr'.*{skill}.*', flags=re.I))
                     )
            database.close()

    @classmethod
    def skill_effect_param(cls, array: List[Dict[str, Any]], effect: Optional[str] = None):
        if effect:
            database = TinyDB(storage=MemoryStorage)
            database.insert_multiple(array)

            reassign(array,
                     database.search(where("skill")["effect"].matches(
                         fr'.*{effect}.*', flags=re.I))
                     )
            database.close()


def process_query_params(
    model: BaseModel,
    sort: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    fields: Optional[str] = None,
    search: Optional[str] = None,
    skill_name: Optional[str] = None,
    skill_effect: Optional[str] = None,
    db_name: str = ""
):
    print(Path(db_name).resolve())
    database = TinyDB(Path(db_name).resolve())

    query_results = QueryParams.search_param(database, search)

    QueryParams.sort_param(M.Monster, query_results, sort)
    QueryParams.field_param(model, query_results, fields)
    QueryParams.skill_name_param(query_results, skill_name)
    QueryParams.skill_effect_param(query_results, skill_effect)

    return QueryParams.slice_param(query_results, offset, limit)
