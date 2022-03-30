from typing import List, Optional
from tinydb import TinyDB
from tinydb.table import Document
from bs4.element import Tag

from utils import uid

import bs4
import httpx

import models.lib.monsters as monsters  # type: ignore
import models.lib.weapons as weapons  # type: ignore
import models.lib.defgears as defgears  # type: ignore
import models.lib.abilities as abilities  # type: ignore


# TODO: Collision in database with Yuletide Dress, Celestial Clothing, Royal Barrette -> solution append gear_type to gear_name and encode for doc_id

class LimipediaScraper:
    base_url: str = "http://jam-capture-unisonleague-ww.ateamid.com"

    def as_soup(self, url: str) -> bs4.BeautifulSoup:
        r = httpx.get(url)
        return bs4.BeautifulSoup(r.content, "lxml")

    def get_gear_type(self, page: bs4.BeautifulSoup):
        pass

    def select_text(self, soup: Tag, selector: str) -> List[str]:
        # returns a list of text extracted from tags
        return [s.text for s in soup.select(selector)]

    def scrape(self, name: str, page: Tag, kind: str, anchor: Optional[Tag] = None, test: bool = False):
        if anchor:
            thumbnail = f'{self.base_url}{anchor.select_one("img.icon.lazyload")["data-src"]}'
        elif test == True:
            thumbnail = f"{self.base_url}"

        if kind == "wpn":
            tags = page.select("dd.detail__material_evo--last")
            return weapons.Weapon(
                id=uid(name),
                name=name,
                thumbnail=thumbnail,
                icon_xl=f'{self.base_url}',
                basic_info=weapons.BasicInfo.new(
                    self.select_text(page, ".detail__data dd")
                ),
                stats=weapons.Stats.new(
                    self.select_text(
                        page, ".detail__status--min dd, .detail__status--max dd")
                ),
                skill=weapons.Skill.new(
                    self.select_text(
                        page, ".detail__skill .detail__evo dd")

                ),
                passive_skill=weapons.PassiveSkill.new(
                    self.select_text(
                        page,  ".detail__skill .detail__evo dd")
                ),
                reforge_info=weapons.ReforgeInfo.new(
                    self.base_url,
                    page.select(
                        ".title_bar ~ .detail__evo dd.detail__evo--last"
                    ),
                ),
                ability_effect=weapons.AbilityEffect.new(
                    self.base_url,
                    page.select(
                        ".detail__ability--txt dd"),
                ),
                reforge_materials=None
                if not tags
                else [
                    weapons.Item(
                        id=uid(name),
                        icon_url=f'{self.base_url}{tag.select_one(".icon")["data-src"]}',
                        icon_name=tag.select_one("a").text.strip(),
                    )
                    for tag in tags
                ],
                awakening_info=weapons.AwakeningInfo.new(
                    self.base_url,
                    page.select(
                        ".detail__reincarnation dd"),
                ),
                awakening_materials=weapons.AwakeningMaterials.new(
                    self.base_url, page.select(
                        ".sp_evo_contents")
                ),
            )
        elif kind == "mob":
            return monsters.Monster(
                id=uid(name),
                name=name,
                thumbnail=thumbnail,
                icon_xl=f'{self.base_url}{page.select_one("img.detail__img")["data-src"]}',
                basic_info=monsters.BasicInfo.new(
                    self.select_text(
                        page,  ".detail__data dd")
                ),
                skill=weapons.Skill.new(
                    self.select_text(
                        page,  ".detail__skill .detail__evo dd")
                ),
                stats=monsters.StatsVariant.new(
                    self.select_text(
                        page,  ".detail__status--min dd, .detail__status--max dd")
                ),
                burst_skills=monsters.BurstSkills.new(
                    page.select(
                        ".detail__skill dt, .detail__skill dd"
                    )
                ),
                hidden_potential=monsters.HiddenPotential.new(
                    page.select(
                        ".detail__skill dt, .detail__skill dd"
                    )
                ),
                reforge_info=weapons.ReforgeInfo.new(
                    self.base_url,
                    page.select(
                        ".title_bar ~ .detail__evo dd.detail__evo--last"
                    ),
                ),
                enlightening_info=monsters.EnlighteningInfo.new(
                    self.base_url,
                    page.select(
                        ".detail__reincarnation dd"
                    )
                ),
                enlightening_materials=monsters.EnlighteningMaterials.new(
                    self.base_url, page.select(
                        ".sp_evo_contents")
                ),
                passive_skill=monsters.PassiveSkill.new(
                    page.select(
                        ".detail__skill .detail__evo dt, .detail__skill .detail__evo dd"
                    )
                ),
            )
        elif kind == "gear":
            return defgears.DefGear(
                id=uid(name),
                name=name,
                thumbnail=thumbnail,
                icon_xl=self.base_url
                + page.select_one("img.detail__img")["data-src"],
                basic_info=defgears.BasicInfo.new(
                    self.select_text(page, ".detail__data dd")
                ),
                skill=weapons.Skill.new(
                    self.select_text(page, ".detail__skill .detail__evo dd")
                ),
                stats=defgears.Stats.new(
                    self.select_text(
                        page, ".detail__status--min dd, .detail__status--max dd"
                    )
                ),
                reforge_info=defgears.ReforgeInfo.new(
                    self.base_url,
                    page.select(
                        ".title_bar ~ .detail__evo dd.detail__evo--last"
                    ),
                ),
                awakening_info=defgears.AwakeningInfo.new(
                    self.base_url,
                    page.select(
                        ".detail__reincarnation dd"),
                ),
                awakening_materials=defgears.AwakeningMaterials.new(
                    self.base_url, page.select(
                        ".sp_evo_contents")
                ),
            )
        elif kind == "ability":
            return abilities.Ability(
                id=uid(name),
                name=name,
                thumbnail=self.base_url + page.select_one(
                    ".detail__img.lazyload")["data-src"],
                basic_info=abilities.BasicInfo.new(
                    page.select_one(
                        ".detail__ability__desc"),
                    self.base_url
                ),
                method_learned=abilities.MethodLearned.new(
                    page.select(
                        ".detail__ability__desc")[1]
                )
            )

    def scrape_abilities(self):
        database = TinyDB("src/data/abilities.json")
        abilities_url = "/en/ability_list/index.html?filter="
        abilities_scraper = self.as_soup(self.base_url + abilities_url)

        ability_links = [
            self.base_url + link["href"] for link in abilities_scraper.select("a")
        ]

        for idx, ability_link in enumerate(ability_links):
            detail_page = self.as_soup(ability_link)
            name = detail_page.select_one(".name__text")

            if name is not None:
                if not database.contains(doc_id=int(uid(name.text))):

                    a = self.scrape(name.text, detail_page, "ability")

                    database.insert(
                        Document(a.dict(), doc_id=uid(name.text)))
                else:
                    print(f"[SKIPPING] -----> [{idx}.] {name.text}")

    def scrape_defgears(self):
        database = TinyDB("src/data/defgears.json")
        defgear_url = "/en/equip_list/23_5.html?filter=#5"
        defgear_scraper = self.as_soup(self.base_url + defgear_url)

        page_links = [
            self.base_url + link["href"] for link in defgear_scraper.select("a")[:5]
        ]

        for page_link in page_links:
            items_list_page = self.as_soup(page_link)

            for idx, anchor in enumerate(items_list_page.select("a")[7:]):
                details_page = self.as_soup(self.base_url + anchor["href"])
                name = details_page.select_one(".name__text")

                if name is not None:
                    if not database.contains(doc_id=int(uid(name.text))):

                        d = self.scrape(
                            name.text, details_page, "gear", anchor)

                        print(f"[DOWNLOADED] ----> [{idx}.] {name.text}")

                        database.insert(
                            Document(d.dict(), doc_id=uid(name.text)))
                    else:
                        print(f"[SKIPPING] -----> [{idx}.] {name.text}")

    def scrape_monsters(self):
        database = TinyDB("src/data/monsters.json")
        monster_url = "/en/equip_list/4_5.html?filter=#5"
        monster_scraper = self.as_soup(self.base_url + monster_url)

        page_links = [
            self.base_url + link["href"] for link in monster_scraper.select("a")[:5]
        ]

        for page_link in page_links:
            items_list_page = self.as_soup(page_link)
            for idx, anchor in enumerate(items_list_page.select("a")[7:]):
                details_page = self.as_soup(self.base_url + anchor["href"])
                name = details_page.select_one(".name__text")

                if name is not None:
                    if not database.contains(doc_id=int(uid(name.text))):
                        m = self.scrape(
                            name.text, details_page, "mob", anchor=anchor)
                        print(f"[DOWNLOADED] ----> [{idx}.] {name.text}")

                        database.insert(
                            Document(m.dict(), doc_id=uid(name.text)))
                    else:
                        print(f"[SKIPPING] -----> [{idx}.] {name.text}")

    def scrape_weapons(self):
        database = TinyDB("src/data/weapons.json")

        wpn_url = "/en/equip_list/1_5.html?filter=init#5"
        wpn_scraper = self.as_soup(self.base_url + wpn_url)

        page_links = [
            self.base_url + link["href"] for link in wpn_scraper.select("a")[:5]
        ]

        for page_link in page_links:
            items_list_page = self.as_soup(page_link)
            for idx, anchor in enumerate(items_list_page.select("a")[7:]):
                details_page = self.as_soup(self.base_url + anchor["href"])

                name = anchor.select_one(".list_item_name")

                if name is not None:
                    if not database.contains(doc_id=uid(name.text)):
                        w = self.scrape(name.text, details_page,
                                        "wpn", anchor=anchor)
                        print(
                            f"[DOWNLOADED] ----> [{idx}.] {name.text}"
                        )

                        database.insert(
                            Document(w.dict(), doc_id=uid(name.text)))
                    else:
                        print(f"[SKIPPING] -----> [{idx}.] {name.text}")

        database.close()


if __name__ == "__main__":
    LimipediaScraper()
