tests:
	nosetests --cover-package otc tests

clean:
	find -name \*.pyc -print0 | xargs -0 rm

.PHONY: clean tests
