
Getting Started with Python
===========================

Why should system dynamicists learn to code?
--------------------------------------------

There is a whole world of computational and analysis tools being
developed in the larger data science community. If system dynamicists
want to take advantage of these tools, we have two options:

1. we can **replicate each of them within one of the system dynamics
   modeling tools we are familiar with**
2. we can **bring system dynamics models to the environment where these
   tools already exist**.

PySD and this cookbook are an outgrowth of the belief that this second
path is the best use of our time. Bringing the tools of system dynamics
to the wider world of data science allows us to operate within our core
competency as model builders, and avoids doubled effort. It allows those
who are familiar with programming to explore using system dynamics in
their own projects, and ensures that the learning system dynamicists do
to use these external tools will have application in the wider world.

Why Python?
~~~~~~~~~~~

Python is a high-level programming language that allows users to write
code quickly and spend less time mucking about with the boring bits of
programming. As a result, it is `becoming increasingly
popular <http://pypl.github.io/PYPL.html>`__ and is the focus for
development of a wealth of `data science
tools <http://pydata.org/downloads/>`__.

In the pen-strokes of xkcd: |xkcd python|

.. |xkcd python| image:: http://imgs.xkcd.com/comics/python.png

A (very) brief intro to programming in python
---------------------------------------------

Basic Python Data Structures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Everything in python is an object.
-  Objects have different 'types'.
-  Objects can be made up of other objects.
-  Variable names are just labels assigned to point to specific objects.

Variables
^^^^^^^^^

Variables are created by assigning a value to a label.

.. code:: python

    a = 3  # this will be an integer
    b = "bob"  # this will be a string
    c = 23.987  # this will be a float
    
    print a, b, c


.. parsed-literal::

    3 bob 23.987


Lists
^^^^^

Lists are ordered collections of objects (and are objects themselves).

.. code:: python

    my_list = [1, 2, a]
    print my_list


.. parsed-literal::

    [1, 2, 3]


Elements of the list can be accessed or modified by position, with the
first element having the index ``0``.

.. code:: python

    print my_list[2]


.. parsed-literal::

    3


.. code:: python

    my_list[2] = 4
    print my_list


.. parsed-literal::

    [1, 2, 4]


Tuples
^^^^^^

A tuple is an ordered list of python objects that is *immutable*,
meaning that once defined they can't be added to or changed. They are
useful for things like sets of coordinates, where it doesn't make sense
to 'add another dimension'.

From a pragmatic point of view, its mostly important to understand that
they are created with ``(parentheses)`` and are often used in function
calls and returns.

.. code:: python

    my_tuple = (3, 4, 'hi')
    my_tuple = (2,4,6)
    print my_tuple[2]


.. parsed-literal::

    6


.. code:: python

    my_tuple[2] = 'bye'


::


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-17-5f5c7c118dde> in <module>()
    ----> 1 my_tuple[2] = 'bye'
    

    TypeError: 'tuple' object does not support item assignment


Dictionaries
^^^^^^^^^^^^

Dictionaries are named collections of objects which can be accessed by
their label:

.. code:: python

    my_dictionary = {'key 1': 1, 'key 2': b}
    print my_dictionary['key 2']


.. parsed-literal::

    bob


You can add elements to a dictionary by assigning to an undefined
element

.. code:: python

    my_dictionary['key 3'] = 27
    print my_dictionary


.. parsed-literal::

    {'key 1': 1, 'key 2': 'bob', 'key 3': 27}


Python Control Flow
~~~~~~~~~~~~~~~~~~~

``if`` statements
^^^^^^^^^^^^^^^^^

The body of an ``if`` statement must be indented - standard practice is
4 spaces.

.. code:: python

    if True:
        print 'Inside the if statement'


.. parsed-literal::

    Inside the if statement


.. code:: python

    if 5 < 3:
        print 'In the if'
    else:
        if 5 > 3:
            print 'in the elif'
        else:
            print 'In the else'    


.. parsed-literal::

    in the elif


.. code:: python

    if 5 < 3:
        print 'In the if'
    elif 5 >= 3:
        print 'in the elif'
    else:
        print 'in the else'


.. parsed-literal::

    This runs instead


``for`` loops
^^^^^^^^^^^^^

For loops allow you to iterate over lists.

.. code:: python

    my_list = [1, 2, 3, 'bob']
    
    for emile in my_list:
        print emile


.. parsed-literal::

    2
    3
    bob


If we want to iterate over a list of numbers, as is often the case with
a for loop, we can use the ``range`` function to construct the list for
us:

.. code:: python

    for i in range(0, 10):
        if i > 3:
            print i,
        else:
            print 'bob',


.. parsed-literal::

    bob bob bob bob 4 5 6 7 8 9


Python Functions
~~~~~~~~~~~~~~~~

Functions are **def**\ ined using the syntax below. As with ``if`` and
``for``, indentation specifies the scope of the function.

.. code:: python

    def my_function(param1, param2):
        result = param1 + param2
        return result
    
    print my_function(3, 4)


.. parsed-literal::

    7


Functions can have default arguments, making them optional to use in the
function call:

.. code:: python

    def my_other_function(param1=5, param2=10):
        return param1 * param2
    
    print my_other_function(param2=4)


.. parsed-literal::

    20


::


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-35-1b17a9a8d97e> in <module>()
          4 print my_other_function(param2=4)
          5 
    ----> 6 print param2
    

    NameError: name 'param2' is not defined


Methods and Attributes of Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many python objects have their own methods, which are functions that
apply specifically to the object, as in the string manipulation
functions below:

.. code:: python

    my_string = 'How about a beer?'
    print my_string.lower()
    print my_string.upper().rjust(30)  # chained call to method
    print my_string.replace('?', '!')


.. parsed-literal::

    how about a beer?
                 HOW ABOUT A BEER?
    How about a beer!


Some objects have attributes which are not functions that act upon the
object, but components of the object's internal representation.

In the example below, we define a complex number, which has both a real
part and a complex part, which we can access as an attribute.

.. code:: python

    my_variable = 12.3 + 4j
    print my_variable
    print my_variable.real
    print my_variable.imag


.. parsed-literal::

    (12.3+4j)
    12.3
    4.0


Resources for learning to program using Python.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  To get started learning python, an excellent collection of resources
   is available in `The Hitchhiker's Guide to
   Python <http://docs.python-guide.org/en/latest/intro/learning/>`__.
-  To try Python in the browser visit
   `learnpython.org <http://www.learnpython.org/>`__.
-  Check out this `overview of Python for computational
   statistics <https://people.duke.edu/~ccc14/sta-663/IntroductionToPythonSolutions.html>`__
-  Online course on `python for data
   science <https://www.datacamp.com/courses/intro-to-python-for-data-science>`__

and finally...

.. code:: python

    import this


.. parsed-literal::

    The Zen of Python, by Tim Peters
    
    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!

