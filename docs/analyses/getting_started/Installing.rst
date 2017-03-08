
Installation and Setup of Python and PySD
=========================================

Using Anaconda
--------------

The simplest way to get started with Python is to use a prepackaged
version such as Anaconda from Continuum analytics.

PySD works with Python 2.7+ or 3.5+. I recommend using the latest
version of python 3 from the following link:
https://www.continuum.io/downloads

Installing PySD
---------------

With a python environment set up, at the command prompt you can type:

::

    pip install pysd

this should install PySD and all of its dependencies. In some cases you
may need to prepend the command with 'sudo' to give it administrative
priveledges:

::

    sudo pip install pysd

You'll be prompted for your administrator password.

Manually installing PySD's dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On the off chance that pip fails to install the dependencies, you can do
the task yourself.

There are a few packages which form the core of the python scientific
computing stack. They are:

1. numpy - a library for matrix-type numerical computation
2. scipy - a library which extends numpy with a bunch of useful
   features, such as stats, etc.
3. matplotlib - a basic plotting library
4. pandas - a basic data manipulation library
5. ipython - an environment for interacting with python and writing
   clever text/documentation documents, such as this one.

PySD also requires a few additional package beyond the basic data
science stack:

1. parsimonious - a text parsing library
2. yapf - a python code formatting library

To install these packages, use the syntax:

::

    pip install numpy

Run the command once for each package, replacing ``numpy`` with
``scipy``, ``matplotlib``, etc.

Launch Jupyter Notebook, and get started
----------------------------------------

If you used the anaconda graphical installer, you should have a
'Anaconda Launcher' user interface installed. Opening this program and
clicking the 'Jupyter Notebook' will fire up the notebook explorer in
your browser.

Alternately, at your command line type:

::

    jupyter notebook

Your browser should start, and give you a document much like this one
that you can play with.

Upgrading PySD
--------------

PySD is a work in progress, and from time to time, we'll ipgrade its
features. To upgrade to the latest version of PySD (or any of the other
packages, for that matter) use the syntax:

::

    pip install pysd --upgrade
