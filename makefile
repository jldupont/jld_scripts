## @author: Jean-Lou Dupont

clean:
	find -iname *.pyc -exec rm {} \;

all:
	find -iname *.pyc -exec rm {} \;
	python setup.py sdist upload
