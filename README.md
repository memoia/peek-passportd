peek-passportd
==============

API backend service for the "passport" app.


Requirements
------------

1. GNU Make (and probably GCC, etc)
2. Python 2.7
3. [virtualenv](https://pypi.python.org/pypi/virtualenv)


Make it run
-----------

``make && make start``


Some thoughts
-------------

Aside from the data modeling and web API stuff, this seems
like a variant of the knapsack optimization problem. We want
to fit as many groups as we can onto the boats that we have
available at any given timeslot.
