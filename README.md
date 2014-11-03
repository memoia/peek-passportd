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


Discussion
----------

Aside from the data modeling and web API stuff, this seems
to suggest a variant of the knapsack optimization problem. We want
to fit as many groups as we can onto the boats that we have
available at any given timeslot. Or, maybe in the future we'd like
to, but for now we don't care.

I'm very doubtful the current data model would hold up in the "real world."
I spent a little time working out alternate models to solve the problem,
but nothing stood out that would both be "better" and "plug-and-play"
with the client software. There are probably ways to optimize the
way the various pieces of the data model work with each-other; maybe
best saved for a later iteration.

In its current state, the cross-table lookups and aggregations are
pretty awful. I usually shoot for a star schema when designing data
models; this is an interesting exercise because parts of the data
model are implied, and a client already exists. The relationships
between boats, timeslots, bookings and assignments have overlaps that
make it difficult to decide how to best organize the information.

Additionally, there's very little validation and error messaging.
I couldn't find anything in the spec that indicated how errors were
to be handled (i.e., how they should be passed back to clients), so
for now, I'm just letting database constraints and other exceptions
cause 500's, which doesn't seem to phase the client app. There are
some instances where I return 400-level error codes, but again,
client don't care.

Thus, there are many ways to break this application. I wish I had more
time to introduce new test scenarios, but I don't. Hopefully the
near-complete unit coverage and functional test bundle is a reasonable
substitute. I chose not to introduce anything outside the scope of the
spec so as to reduce potential for "cool feature bugs."

I chose Django for this project because of all the great things it
comes with; a reasonable choice for an exercise like this one. There
are also downsides to convenience. For example, the ORM makes it more
difficult to construct performant queries. There are probably
non-relational databases that would be better for this problem, but
"normal" Django is pretty RDBMS-centric.

Reiterating the most important question: "What is my availability today?"
If we approach it from that angle alone, maybe we could find a way to
either use a single table to represent all requirements, or, we could
at least try splitting things up into implied relationships that are
denormalized, moving more responsibility to application logic for
keeping things consistent.

Also---the knapsack problem. I took a really simple greedy-ish approach
to choosing assignments for bookings, but there's probably a better way
for that one, too.
