
Surrogating a function with a machine learning estimator
========================================================

System dynamics generally represents the relationships between model
elements as either analytical equations, or lookup tables. However, in
some situations we may be presented with relationships that are not well
estimated by equations, but involve more than a single input leading to
a single output. When confrontied with this situation, other paradigms

.. code:: python

    %pylab inline
    import pysd
    import numpy as np
    import pandas as pd

.. code:: python

    model = pysd.read_vensim('../../models/Manufacturing_Defects/Defects.mdl')

.. code:: python

    data = pd.read_csv('../../data/Defects_Synthetic/Manufacturing_Defects_Synthetic_Data.csv')
    data.head()

.. code:: python

    plt.<<...>>(data['Workday'], data['Time per Task'], c=data['Defect Rate'], linewidth=0, alpha=.6)
    plt.ylabel('Time per Task')
    plt.xlabel('Length of Workday')
    plt.xlim(0.15, .45)
    plt.ylim(.01, .09)
    plt.box('off')
    plt.colorbar()
    plt.title('Defect Rate Measurements')
    plt.figtext(.88, .5, 'Defect Rate', rotation=90, verticalalignment='center');

.. code:: python

    from sklearn.svm import <<...>>
    
    Factors = data[['Workday','Time per Task']].values
    Outcome = data['Defect Rate'].values
    regression = SVR()
    regression.<<..>>(Factors, Outcome)

.. code:: python

    def new_defect_function():
        """ Replaces the original defects equation with a regression model"""
        workday = model.<<...>>.length_of_workday()
        time_per_task = model.components.time_allocated_per_unit<<...>>
        return regression.predict([<<...>>])[0]

.. code:: python

    model.components.defect_rate = <<...>>
    
    print model.components.defect_rate()


.. code:: python

    model.run().plot();

