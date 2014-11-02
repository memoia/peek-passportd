PYTHON := $(shell which python2.7)
ENV := $(CURDIR)/env
SHELL := /bin/bash
export PATH := $(ENV)/bin:$(PATH)

.PHONY: test start clean distclean func run

test: $(ENV)/bin/coverage $(ENV)/bin/django-admin
	cd passportd; ( \
	  coverage erase; \
	  coverage run \
	    --branch \
	    --source='.' \
	    --omit='manage.py,passportd/**,**/test*,**/__init__*,api/migrations/**' \
	    manage.py test && ( \
	      coverage report; \
	      coverage html -d $(CURDIR)/htmlcov ))

start: manage
	./manage migrate
	./manage runserver 0.0.0.0:3000

clean:
	rm -rf passportd/.coverage htmlcov/ db.sqlite3

distclean:
	git clean -dfx

manage: $(ENV)/bin/django-admin
	echo '#!/bin/bash' >> $@
	echo "$(ENV)/bin/python $(CURDIR)/passportd/manage.py \$$*" >> $@
	chmod +x $@

$(ENV)/bin/django-admin: | $(ENV)
	pip install -r requirements/base.txt

$(ENV)/bin/coverage: | $(ENV)
	pip install -r requirements/test.txt

$(ENV):
	virtualenv --python=$(PYTHON) $(ENV)

# overkill!

$(CURDIR)/client:
	mkdir $@
	curl -k -L https://github.com/memoia/passport/tarball/nitpicky | \
	  tar --strip-components=1 -C $@ -xvzf -
	cd $@; npm install

Procfile:
	echo "api: make start" >> $@
	echo "client: cd client && npm start" >> $@
	echo "func: $(ENV)/bin/python func.py" >> $@

func: Procfile test
	honcho start api func

run: Procfile $(CURDIR)/client
	honcho start api client
