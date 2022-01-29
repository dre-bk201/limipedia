from tinydb import TinyDB
from fastapi import FastAPI
from typing import Optional

import uvicorn

from .utils import process_query_params

from models import monsters as mon
from models import weapons as wpn
from models import defgears as gear
from scraper import LimipediaScraper

import models.lib.monsters as mon
import models.lib.weapons as wpn
import models.lib.defgears as gear

app = FastAPI()


@app.get("/monsters")
async def monsters_query(
    sort: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    fields: Optional[str] = None,
    search: Optional[str] = None,
    skill_name: Optional[str] = None,
    skill_effect: Optional[str] = None
):
    return process_query_params(
        mon.Monster, sort, offset,
        limit, fields, search, skill_name,
        skill_effect, db_name="src/data/monsters.json"
    )


@app.get("/monsters/{id}")
async def monster_id(id: int):
    database = TinyDB("src/data/monsters.json")
    return database.get(doc_id=id)


@app.get("/weapons")
async def weapons_query(
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        fields: Optional[str] = None,
        search: Optional[str] = None,
        skill_name: Optional[str] = None,
        skill_effect: Optional[str] = None
):
    return process_query_params(process_query_params(
        wpn.Weapon, sort, offset,
        limit, fields, search, skill_name,
        skill_effect, db_name="src\data\weapons.json")
    )


@app.get("/weapons/{id}")
async def weapon_id(id: int):
    database = TinyDB("src/data/weapons.json")
    return database.get(doc_id=id)


@app.get("/defgears")
async def defgears_query(
        sort: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        fields: Optional[str] = None,
        search: Optional[str] = None,  skill_name: Optional[str] = None,
        skill_effect: Optional[str] = None
):
    return process_query_params(
        gear.DefGear,  sort, offset,
        limit, fields, search, skill_name,
        skill_effect, db_name="src/data/defgears.json"
    )


@app.get("/defgears/{id}")
async def weapon_id(id: int):
    database = TinyDB("src/data/defgears.json")
    return database.get(doc_id=id)


def start_api_svc():
    uvicorn.run("api:app", port=4352, reload=True)
