install:
	pip3 install -r requirements.txt

test:
	python3 -m unittest discover -s tests

pylint:
	pylint .

fix_formatting:
	black .

run:
	python3 main.py