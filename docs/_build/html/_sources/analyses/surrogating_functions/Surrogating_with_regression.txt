
Surrogating a function with a machine learning estimator
========================================================

System dynamics generally represents the relationships between model
elements as either analytical equations, or lookup tables. However, in
some situations we may be presented with relationships that are not well
estimated by equations, but involve more than a single input leading to
a single output. When confrontied with this situation, other paradigms

.. image:: ../../../source/models/Manufacturing_Defects/Defects.png
   :width: 400 px

.. code:: python

    %pylab inline
    import pysd
    import numpy as np
    import pandas as pd


.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib


.. parsed-literal::

    /Users/houghton/anaconda/lib/python2.7/site-packages/pandas/computation/__init__.py:19: UserWarning: The installed version of numexpr 2.4.4 is not supported in pandas and will be not be used
    
      UserWarning)


.. code:: python

    model = pysd.read_vensim('../../models/Manufacturing_Defects/Defects.mdl')

.. code:: python

    data = pd.read_csv('../../data/Defects_Synthetic/Manufacturing_Defects_Synthetic_Data.csv')
    data.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Unnamed: 0</th>
          <th>Workday</th>
          <th>Time per Task</th>
          <th>Defect Rate</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>0</td>
          <td>0.357563</td>
          <td>0.036497</td>
          <td>0.066678</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1</td>
          <td>0.300276</td>
          <td>0.035329</td>
          <td>0.063891</td>
        </tr>
        <tr>
          <th>2</th>
          <td>2</td>
          <td>0.301040</td>
          <td>0.054992</td>
          <td>0.049828</td>
        </tr>
        <tr>
          <th>3</th>
          <td>3</td>
          <td>0.290333</td>
          <td>0.046289</td>
          <td>0.046932</td>
        </tr>
        <tr>
          <th>4</th>
          <td>4</td>
          <td>0.384306</td>
          <td>0.050605</td>
          <td>0.064480</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    plt.scatter(data['Workday'], data['Time per Task'], c=data['Defect Rate'], linewidth=0, alpha=.6)
    plt.ylabel('Time per Task')
    plt.xlabel('Length of Workday')
    plt.xlim(0.15, .45)
    plt.ylim(.01, .09)
    plt.box('off')
    plt.colorbar()
    plt.title('Defect Rate Measurements')
    plt.figtext(.88, .5, 'Defect Rate', rotation=90, verticalalignment='center');



.. image:: Surrogating_with_regression_files/Surrogating_with_regression_5_0.png


.. code:: python

    from sklearn.svm import SVR
    
    Factors = data[['Workday','Time per Task']].values
    Outcome = data['Defect Rate'].values
    regression = SVR()
    regression.fit(Factors, Outcome)




.. parsed-literal::

    SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma=0.0,
      kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)



.. code:: python

    def new_defect_function():
        """ Replaces the original defects equation with a regression model"""
        workday = model.components.length_of_workday()
        time_per_task = model.components.time_allocated_per_unit()
        return regression.predict([workday, time_per_task])[0]
    
    model.components.defect_rate = new_defect_function

.. code:: python

    model.components.defect_rate()




.. parsed-literal::

    0.059499757838150001



.. code:: python

    model.run().plot();



.. image:: Surrogating_with_regression_files/Surrogating_with_regression_9_0.png


