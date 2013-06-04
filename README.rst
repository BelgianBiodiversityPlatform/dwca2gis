dwca2cartodb
============

What is it ?
------------

A simple command-line tool that allows to directly import a `Darwin Core Archive`_ (DwC-A) file into `CartoDB`_ to allow quick & easy exploration, online collaboration and use of biodiversity data.

Status
------

IN DEVELOPMENT. Very basic use works, but there are many missing important pieces:

* Ability to (smartly) guess location from multiple fields. For now, it is simply read from the decimalLatitude and decimalLongitude fields.
* Ability to configure imported (other than location) fields.
* Implement automated tests to make the script more robust.

Requirements
------------

* cartodb==0.6
* python-dwca-reader==0.1.1

Use
---

::
    
    $ python dwca2cartodb.py --domain niconoe --api-key <YOUR_API_KEY> --table <YOUR_TABLE_NAME> your-dwca.zip --truncate


.. _Darwin Core Archive: http://en.wikipedia.org/wiki/Darwin_Core_Archive
.. _CartoDB: http://cartodb.com/