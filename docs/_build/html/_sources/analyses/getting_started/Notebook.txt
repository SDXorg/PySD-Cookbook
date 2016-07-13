
Using the Jupyter Notebook
==========================

The Jupyter (formerly iPython) Notebook is a browser-based interactive
coding environment that allows cells of text (such as this one) to be
interspersed with cells of code (such as the next cell), and the output
of that code (immediately following)

.. code:: python

    string = 'Hello, World!'
    print string


.. parsed-literal::

    Hello, World!


Code Cells
^^^^^^^^^^

To add cells to the notebook, click the **[+]** button in the notebook's
tool pane. A new cell will appear below the one which is selected. By
default this cell is set for writing code snippets.

To execute code in a cell such as this, select it and press either the
play **[>\|]** button in the tool pane, or press ``<shift><enter>``. The
results of the cell's computation will be displaced below.

Once a cell has been run, the variables declared in that cell are
available to any other cell in the notebook:

.. code:: python

    print string[:6] + ' Programmer!'


.. parsed-literal::

    Hello, Programmer!


Text Cells
^^^^^^^^^^

To format a cell as text, with the desired cell highlighted, click the
dropdown in the tool pane showing the word ``Code``, and select
``Markdown``.

`Markdown <https://daringfireball.net/projects/markdown/>`__ is a simple
syntax for formatting text. Headings are indicated with pound signs
``#``:

::

    ### Heading

    Heading
    ~~~~~~~

*Italics* and **bold** are indicated with one and two preceeding and
following asterisks respectively: ``*Italics*`` : *Italics*,
``**Bold**`` : **Bold**

Code is blocked with tick fences (same key as tilde, not single quotes):

::

    ```
    Code goes here
    ```

and quotes are preceeded with the right-pointy chevron '``>``\ ' > "This
is not my quote." - *Benjamin Franklin*

Tab-completion
~~~~~~~~~~~~~~

While you're typing code, it's often possible to just start the word you
want, and hit the ``<tab>`` key. iPython will give you a list of
suggestions for how to complete that term.

For example, in the box below, if you place the cursor after ``my``,
ipython will show the above two variable names as options, which you can
select and enter.

.. code:: python

    my_very_long_variable_name = 2
    my_fairly_long_variable_name = 3
    my

Context help
~~~~~~~~~~~~

It is sometimes hard to remember what arguments a function takes (or
what order they come in).

If you type the name of the function and the open parenthesis, and then
press ``<shift><tab>``, a tooltip will come up showing you what
arguments the function expects.

.. code:: python

    sum(

References
----------

-  A `comprehensive
   tutorial <http://bebi103.caltech.edu/2015/tutorials/t0b_intro_to_jupyter_notebooks.html>`__
   to using the Jupyter Notebook
