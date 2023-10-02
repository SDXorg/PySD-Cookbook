.. PySD-Cookbook documentation master file, created by
   sphinx-quickstart on Fri Jun 26 17:44:52 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The PySD Cookbook
=================
Simple recipes for powerful analysis of system dynamics models

Quickstart
----------
1. `Install PySD <https://pysd.readthedocs.io/en/master/installation.html>`_ (we recommend using the latest available PySD version) and needed `requirements for the notebooks <https://github.com/SDXorg/PySD-Cookbook/blob/master/requirements.txt>`_
2. `Download this cookbook <https://github.com/SDXorg/PySD-Cookbook/archive/master.zip>`_
   and unzip it to a working directory
3. Navigate your command prompt to the working directory just created
4. Launch ipython notebook with the command :code:`ipython notebook` at your command prompt
5. In the ipython browser, open :code:`source\analyses\getting_started\Hello_World_Teacup.ipynb`


How to use this cookbook
------------------------
Every recipe in this cookbook is an executable ipython notebook. Because of this, I recommend
that you download a copy of the cookbook, and follow along by executing the steps in each
notebook as you read, playing with the parameters, etc.

If you want to implement a recipe, you can then make a copy of the notebook you are interested
in, and modify it to analyze your own problem with your own data.

To download the cookbook in its entirity, use
`this link <https://github.com/SDXorg/PySD-Cookbook/archive/master.zip>`_ or visit
the cookbook's `Github Page <https://github.com/SDXorg/PySD-Cookbook>`_
and select one of the options in the righthand panel.


Contents
--------

.. toctree::
   :maxdepth: 2

   analyses/getting_started/index_getting_started
   analyses/data_handling/index_data_handling
   analyses/design_policy/index_desing_policy.rst
   analyses/visualization/index_visualization
   analyses/fitting/index_fitting
   analyses/geo/index_geo
   analyses/model_comparison/index_model_comparison.rst
   analyses/sensitivity/index_sensitivity.rst
   analyses/surrogating_functions/index_surrogate
   analyses/testing/index_testing.rst
   analyses/realtime/index_realtime
   analyses/workflow/index_workflow
   analyses/wrapper_EMAWorkbench/index_wrapper_EMAWorkbench.rst

   data/index_data
   future
   endnotes

Extra Resources
---------------
The `PySD Documentation <http://pysd.readthedocs.org/>`_ can answer most questions
about how PySD itself should be used,
with `basic examples <http://pysd.readthedocs.org/en/latest/basic_usage.html>`_
and `function reference <http://pysd.readthedocs.org/en/latest/functions.html>`_.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

