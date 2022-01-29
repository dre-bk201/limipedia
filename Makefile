build_scraper: check_scraper test_scraper

test_scraper:
	python src/scraper.test.py

run_scraper: # some cmdline args to differ
	python src/main.py -s

check_scraper: #
	mypy src/scraper/__init__.py 
	
# ----------------------------------------------

build_api: check_api test_api 

test_api:
	python src/api.test.py

run_api:
	python src/main.py

check_api:
	mypy src/api/__init.__py 

