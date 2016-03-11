
Installation and Setup of PySD
==============================

Using Anaconda
--------------

The simplest way to get started with Python is to use a prepackaged
version such as Anaconda from Continuum analytics.

Download and install version 2.7 from the following link:
https://www.continuum.io/downloads

Installing Python on its own
----------------------------

If you have an existing python installation, or you've worked
extensively with python in the past, you might prefer to just use basic
unpackaged python. This will give you some more control, but you'll have
to do more of your own dependency resolution.

To check if you have python already, at a command prompt, type:

::

    python -V

If python is installed, you should see some information about the
version you are running. For example:

::

    Python 2.7.6

If you get an error, you probably need to install python from scratch.
To do so, visit https://www.python.org/downloads/ and download the
latest version beginning with ``2.``. Some of the python utilities we
will be using are not yet available in Python 3.

Installing pip
^^^^^^^^^^^^^^

Pip is the primary python package distribution utility. Depending on how
you set up python, you may have Pip already installed. To test this, at
your command prompt, type:

::

    pip list

If pip is installed, you will see a list of installed packages managed
by pip.

If you get an error, you will need to install pip from scratch. To do
this, follow the instructions here:
https://pip.pypa.io/en/latest/installing.html

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

To install these packages, use the syntax:

::

    pip install numpy

Run the command once for each package, replacing ``numpy`` with
``scipy`` etc.

PySD also requires one additional package beyond the basic data science
stack, called ``parsimonious``. Use pip to install it:

::

    pip install parsimonious

Launch iPython Notebook, and get started
----------------------------------------

Now at your command line type:

::

    ipython notebook

Your browser should start, and give you a document much like this one
that you can play with.

Upgrading PySD
--------------

PySD is a work in progress, and from time to time, we'll ipgrade its
features. To upgrade to the latest version of PySD (or any of the other
packages, for that matter) use the syntax:

::

    pip install pysd --upgrade
