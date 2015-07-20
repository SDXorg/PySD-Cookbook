
Unit Testing
============

In this notebook we'll demonstrate some basic unit testing for models.

We build on the standard python unittest libarary, which is documented
`here <https://docs.python.org/2/library/unittest.html>`__. Other
testing suites are available, with their own advantages, but this is the
most basic, so we'll use it for our demonstration.

Unit testing us usually done not in the ipython notebook, but in a
standalone python file. Tests for this demo are found in the
accompanying file ``testsite.py``:

.. literalinclude:: ../../../source/analyses/workflow/testsuite.py
   :language: python

.. code:: python

    %run testsuite.py


.. parsed-literal::

    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.053s
    
    OK

