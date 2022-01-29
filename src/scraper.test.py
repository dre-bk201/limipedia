import unittest
import os
import bs4  # type: ignore

from tinydb import TinyDB
from tinydb.table import Document

from scraper import LimipediaScraper
from utils import uid


class ScraperTest(unittest.TestCase):

    def test_weapons(self):
        testpath = "src/scraper/tests/weapons"
        database = TinyDB(f"{testpath}/batch.json")
        scraper = LimipediaScraper()
        print("\nWeapons\n----------------------------------------")

        for test, name in [(f'{testpath}/{p}', p[:-5]) for p in os.listdir(testpath) if ".html" in p]:
            with open(test, "rb") as fd:
                soup = bs4.BeautifulSoup(fd.read(), "lxml")

                test_result = scraper.scrape(name, soup, "wpn", test=True)
                answer = database.get(doc_id=uid(name))
                print(
                    "[TEST] -> {} {}".format(name, ('✅' if test_result.dict() == answer else '')))

                self.assertEqual(test_result.dict(), answer)

        database.close()

    def test_monsters(self):
        testpath = "src/scraper/tests/monsters"
        database = TinyDB(f"{testpath}/batch.json")
        scraper = LimipediaScraper()
        print("\nMonsters\n----------------------------------------")

        for test, name in [(f'{testpath}/{p}', p[:-5]) for p in os.listdir(testpath) if ".html" in p]:
            with open(test, "rb") as fd:
                soup = bs4.BeautifulSoup(fd.read(), "lxml")

                test_result = scraper.scrape(name, soup, "mob", test=True)
                answer = database.get(doc_id=uid(name))
                print(
                    "[TEST] -> {} {}".format(name, ('✅' if test_result == answer else '')))
                self.assertEqual(test_result, answer)

        database.close()

    def test_defgears(self):
        testpath = "src/scraper/tests/defgears"
        database = TinyDB(f"{testpath}/batch.json")
        scraper = LimipediaScraper()
        print("\Defgears\n----------------------------------------")

        for test, name in [(f'{testpath}/{p}', p[:-5]) for p in os.listdir(testpath) if ".html" in p]:
            with open(test, "rb") as fd:
                soup = bs4.BeautifulSoup(fd.read(), "lxml")

                test_result = scraper.scrape(name, soup, "gear", test=True)
                answer = database.get(doc_id=uid(name))
                print(
                    "[TEST] -> {} {}".format(name, ('✅' if test_result == answer else '')))
                self.assertEqual(test_result, answer)

        database.close()

    def test_abilities(self):
        testpath = "src/scraper/tests/abilities"
        database = TinyDB(f"{testpath}/batch.json")
        scraper = LimipediaScraper()
        print("\Abilities\n----------------------------------------")

        for test, name in [(f'{testpath}/{p}', p[:-5]) for p in os.listdir(testpath) if ".html" in p]:
            with open(test, "rb") as fd:
                soup = bs4.BeautifulSoup(fd.read(), "lxml")

                test_result = scraper.scrape(
                    name, soup, "ability", test=True)

                answer = database.get(doc_id=uid(name))

                print(
                    "[TEST] -> {} {}".format(name, ('✅' if test_result.dict() == answer else '')))
                self.assertEqual(test_result.dict(), answer)

        database.close()


def scrape_and_insert_stable(gear_type: str):
    testpath = f"src/scraper/tests/{gear_type}"
    database = TinyDB(f"{testpath}/batch.json")
    scraper = LimipediaScraper()

    for test, name in [(f'{testpath}/{p}', p[:-5]) for p in os.listdir(testpath) if ".html" in p]:
        with open(test, "rb") as fd:
            soup = bs4.BeautifulSoup(fd.read(), "lxml")

            wpn = scraper.scrape(name, soup, "ability", test=True)
            database.insert(Document(wpn.dict(), doc_id=wpn.dict()["id"]))

    database.close()


if __name__ == "__main__":
    unittest.main()
