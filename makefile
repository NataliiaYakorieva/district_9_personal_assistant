install:
	pip3 install -r requirements.txt

test:
	python3 -m unittest discover -s tests

check_formatting:
	flake8 .

fix_formatting:
	autopep8 --in-place --aggressive --aggressive --recursive .

run:
	python3 main.py