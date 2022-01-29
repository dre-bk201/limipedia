
import click

from api import start_api_svc
from scraper import LimipediaScraper


@click.command()
@click.option("--scrape_wpn", "-sw", is_flag=True, help="Scrapes Weapons. [NB]:by default runs api")
@click.option("--scrape_def", "-sd", is_flag=True, help="Scrapes Defgears. [NB]:by default runs api")
@click.option("--scrape_abl", "-sa", is_flag=True, help="Scrapes Abilities. [NB]:by default runs api")
@click.option("--scrape_mon", "-sm", is_flag=True, help="Scrapes Monsters. [NB]:by default runs api")
def limipedia_cli(scrape_wpn: bool, scrape_def: bool, scrape_abl: bool, scrape_mon: bool):

    if scrape_wpn:
        LimipediaScraper().scrape_weapons()

    elif scrape_def:
        LimipediaScraper().scrape_defgears()

    elif scrape_abl:
        LimipediaScraper().scrape_abilities()

    elif scrape_mon:
        LimipediaScraper().scrape_monsters()

    else:
        start_api_svc()


if __name__ == "__main__":
    limipedia_cli()
