setup:
	apt-get install python3-env
	python3 -m venv ~/.TessOCR
	source ~/.TessOCR/bin/activate


install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black *.py mylib/*.py