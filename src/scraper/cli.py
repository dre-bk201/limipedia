'''
    Downloads and save supplied webpages given the relative page URL
        NB: Used for gathering data for testing
'''
import httpx
import click

from bs4 import BeautifulSoup
from pathlib import Path

Path.joinpath


@click.command()
@click.option("--filename", '-fn', help="Path to file with urls")
@click.option("--weapon", "-w", is_flag=True, help="Save as a weapon")
@click.option("--defgear", "-d", is_flag=True, help="Save as a defense gear")
@click.option("--monster", "-m", is_flag=True, help="Save as a monster")
@click.option("--ability", "-a", is_flag=True, help="Save as an ability")
@click.option("--furniture", "-f", is_flag=True, help="Save as a furniture")
def save_page(filename: str, weapon: bool, defgear: bool, monster: bool, ability: bool, furniture: bool):
    g_type = ""
    gear_name = ""
    base_url = "http://jam-capture-unisonleague-ww.ateamid.com"

    if not filename:
        return

    if weapon:
        g_type = "weapons"
    elif defgear:
        g_type = "defgears"
    elif monster:
        g_type = "monsters"
    elif furniture:
        g_type = "furnitures"
    elif ability:
        g_type = "abilities"

    path = Path(filename).resolve()

    with open(path, "r") as f:
        pass
        for line in f:
            try:
                click.echo(f"[DOWNLOADING] -> {base_url + line}")
                response = httpx.get(base_url + line.strip())
                print(response.status_code)
                soup = BeautifulSoup(response.content, "lxml")

                gear_name = soup.select_one(
                    ".name__text").text.replace('"', "")

            except:
                click.echo(
                    f"[FAILURE] -> Downloading {gear_name} from {base_url + line}")
                return

            try:
                path = Path(f"./src/scraper/tests/{g_type}").absolute()
                print(path)
                click.echo(
                    f"[WRITING FILE] -> {path.joinpath(gear_name)}.html")

                with open(f"{path.joinpath(gear_name)}.html", "wb") as f:
                    f.write(response.content)

            except Exception as e:
                click.echo(f"[FAILURE] -> {e}")


if __name__ == "__main__":
    save_page()
