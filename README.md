peek-passportd
==============

API backend service for the
"[passport](https://github.com/memoia/passport)" app.


Requirements
------------

1. GNU Make (and probably GCC, etc. for some Python dependencies)
2. Python 2.7
3. [virtualenv](https://pypi.python.org/pypi/virtualenv) installed
   at the system level.

Aside from installing virtualenv, this should "just work" on recent
versions of OS X with Xcode / comand line tools installed.


Make it run
-----------

* ``make``: grabs dependencies, runs units and coverage
* ``make start``: start app using django devserver
* ``make func``: run complete test suite

All dependencies are installed within the project folder; no need
for any special shell variable tweaking or virtualenv activation.

The ``make run`` target is also useful to run both the passport node
app and the api service in tandem. This will grab my version of the
passport app and load it into the ``client/`` folder.


Some thoughts
-------------

Aside from the data modeling and web API stuff, this seems
to suggest a variant of the knapsack optimization problem. We want
to fit as many groups as we can onto the boats that we have
available at any given timeslot. Or, maybe in the future we'd like
to, but for now we don't care.
