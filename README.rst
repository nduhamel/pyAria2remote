=============
pyAira2remote
=============

pyAria2remote is a console frontend for `aria2 <http://aria2.sourceforge.net/>`_.

Features
========

* aria2 remote controle
* add link from file
* handle direct download site with debrider
* simple plugin system

Installation
============

Use virtualenvwrapper.

    $ mkvirtualenv aria2remote

    $ python setup.py develop

Launch with: **aria2remote**

Config
======

At first launch, it create a config file in **~/.config/mypyapp/aria2remote.ini**


Plugins
=======

* `Alldebrid <http://www.alldebrid.com>`_
* Filesonic Folder
* Fileserve Folder
