# enter into virtualenv
executable=python

all: test build

test: venv
	echo "testing this"
	${executable} -m unittest -v test

build: venv
	echo "building this"

venv:
	source venv/bin/activate
