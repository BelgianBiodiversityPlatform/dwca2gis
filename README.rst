dwca2gis
========

What is it ?
------------

A collection of tools to convert `Darwin Core Archive`_ (DwC-A) files to other file formats and tools. In its current form, it contains the following scripts:

* dwca2cartodb: A simple command-line tool that allows to directly import a `Darwin Core Archive`_ (DwC-A) file into `CartoDB`_ to allow quick & easy exploration, online collaboration and use of biodiversity data.
* dwca2shp: A command-line tool to convert a DwC-A files to a `Shapefile`_.

Status
------

IN DEVELOPMENT. Basic use works, but its currently missing important pieces and features.

Install & Requirements
----------------------

For now, clone this repository and install the following dependencies via easy_install / pip. Once the project is a little more mature, a proper Python package will be availabe on PyPI.

* cartodb==0.6
* python-dwca-reader==0.1.1
* pyshp==1.1.4
* pyproj==1.9.3
* GDAL==1.9.1

dwca2cartodb
------------

Prerequisites:  

* a free account at `CartoDB`_.
* a DwC-A file to import(for example from `this list of IPT instances <http://gbrds.gbif.org/browse/start?agentType=14100&filterValue=IPT&pageNo=1&pageSize=100>`_).

1. Run dwca2cartodb:
::
    
    $ python dwca2cartodb.py --domain <YOUR_CARTODB_DOMAIN> --api-key <YOUR_API_KEY> --table <YOUR_TABLE_NAME> dwcafile.zip.zip

You can add "--truncate" to truncate existing CartoDB table before importing new data (useful for multiple imports in a row).

2. Visualize and share your data online:

.. image:: doc/images/cartodb_screenshot.jpg

dwca2shp
--------

Example use
::

    $ python dwca2gis dwcafile.zip ./my_shapefile

Will output a Shapefile in ./my_shapefile/shapefile.shp using the EPSG:4326 CRS.

You can also generate a Shapefile using another CRS:
::

    $ python dwca2gis dwcafile.zip ./my_shapefile --crs epsg:3857

Will output a Shepefile using the famous EPSG:3857 CRS (aka Sperical Mercator, Google projection, 900913, EPSG:3587, ...)

For each Darwin Core term in the "Core file" of the source DwC-A, an attribute will be set in the resulting shapefile.

Running tests
-------------

The test suite uses `nose`_:

::
    
    $ pip install nose
    $ nosetests


.. _Darwin Core Archive: http://en.wikipedia.org/wiki/Darwin_Core_Archive
.. _CartoDB: http://cartodb.com/
.. _Shapefile: https://en.wikipedia.org/wiki/Shapefile
.. _nose: https://nose.readthedocs.org/en/latest/