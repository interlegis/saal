saal
====

Sistema de Apoio à Administração Legislativa

Installation instructions for Ubuntu 12.04
------------------------------------------

* Set eXecutable flag for script install.sh
  * chmod a+x install.sh
* Run install.sh server|dev [--options], where
  * server: Install in server mode, with wsgi & apache2 proxy
  * dev: Install in developer mode, using a virtualenv.
  * for more informations about install.sh, run install.sh --help
