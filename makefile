## @author: Jean-Lou Dupont

clean:
	find -iname *.pyc -exec rm {} \;

egg:
	find -iname *.pyc -exec rm {} \;
	python setup.py sdist


all:
	find -iname *.pyc -exec rm {} \;
	python setup.py sdist upload
