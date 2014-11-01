PYTHON := $(shell which python2.7)
ENV := $(CURDIR)/env
SHELL := /bin/bash
export PATH := $(ENV)/bin:$(PATH)

.PHONY: test run clean distclean

test: $(ENV)/bin/coverage $(ENV)/bin/django-admin
	coverage erase
	coverage run \
		--source='.' \
		--omit='env/**/*.py,**/test*,**/__init__*,passportd/manage.py' \
		passportd/manage.py test && (coverage report; coverage html)

run: $(ENV)/bin/django-admin
	python passportd/manage.py runserver 0.0.0.0:3000

clean:
	rm -rf .coverage htmlcov/ db.sqlite3

distclean:
	git clean -dfx

manage:
	echo '#!/bin/bash' >> $@
	echo "$(ENV)/bin/python $(CURDIR)/passportd/manage.py \$$*" >> $@
	chmod +x $@

$(ENV)/bin/django-admin: | $(ENV)
	pip install -r requirements/base.txt

$(ENV)/bin/coverage: | $(ENV)
	pip install -r requirements/test.txt

$(ENV):
	virtualenv --python=$(PYTHON) $(ENV)
