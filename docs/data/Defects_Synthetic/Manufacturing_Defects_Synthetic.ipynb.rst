
Manufacturing Defects Synthetic Data
====================================

In this notebook we generate some data that will represent measurements
of defects in a manufacturing setting.

.. code:: python

    import numpy as np
    import pandas as pd

.. code:: python

    #generate synthetic data
    Factors = []
    Outcome = []
    numpoints = 2000
    for workday, time_per_task  in zip(np.random.normal(loc=.3, scale=.05, size=numpoints), np.random.normal(loc=.05, scale=.01, size=numpoints)):
        Factors.append([workday, time_per_task])
        Outcome.append( 0*workday**2/(time_per_task**2) + 1/time_per_task**1.5 + 1000*workday**1.5)

.. code:: python

    data = pd.DataFrame(Factors, columns=['Workday', 'Time per Task'])
    data['Defect Rate'] = Outcome
    data['Defect Rate']/= data['Defect Rate'].max()*10
    data['Defect Rate'] += np.random.normal(scale=.003, size=len(data['Defect Rate']))
    data.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Workday</th>
          <th>Time per Task</th>
          <th>Defect Rate</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>0.357563</td>
          <td>0.036497</td>
          <td>0.066678</td>
        </tr>
        <tr>
          <th>1</th>
          <td>0.300276</td>
          <td>0.035329</td>
          <td>0.063891</td>
        </tr>
        <tr>
          <th>2</th>
          <td>0.301040</td>
          <td>0.054992</td>
          <td>0.049828</td>
        </tr>
        <tr>
          <th>3</th>
          <td>0.290333</td>
          <td>0.046289</td>
          <td>0.046932</td>
        </tr>
        <tr>
          <th>4</th>
          <td>0.384306</td>
          <td>0.050605</td>
          <td>0.064480</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    data.to_csv('Manufacturing_Defects_Synthetic_Data.csv')

