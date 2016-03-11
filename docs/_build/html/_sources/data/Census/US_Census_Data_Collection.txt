
Collecting US decennial census data
===================================

In this notebook, we'll collect demographic data from the US decennial
census, by county.

The census website has an API, which is good, because everything else
about the census website is close to unusable. The api is described
here:
http://www.census.gov/data/developers/data-sets/decennial-census-data.html

As a quick demonstration, we can use the API to get population data for
every county in the US:

.. code:: python

    import pandas as pd

.. code:: python

    df = pd.read_json('http://api.census.gov/data/2010/sf1?get=P0120001&for=county:*')
    df.columns = df.iloc[0]
    df.drop(df.index[0], inplace=True)
    df.head()




.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>P0120001</th>
          <th>state</th>
          <th>county</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1</th>
          <td>54571</td>
          <td>01</td>
          <td>001</td>
        </tr>
        <tr>
          <th>2</th>
          <td>182265</td>
          <td>01</td>
          <td>003</td>
        </tr>
        <tr>
          <th>3</th>
          <td>27457</td>
          <td>01</td>
          <td>005</td>
        </tr>
        <tr>
          <th>4</th>
          <td>22915</td>
          <td>01</td>
          <td>007</td>
        </tr>
        <tr>
          <th>5</th>
          <td>57322</td>
          <td>01</td>
          <td>009</td>
        </tr>
      </tbody>
    </table>
    </div>



The census code descriptions can also be accessed via the API. A listing
of the field names is available here:
http://api.census.gov/data/2010/sf1/variables.html

.. code:: python

    pd.read_json('http://api.census.gov/data/2010/sf1/variables/P0120001.json', typ='ser')




.. parsed-literal::

    concept    P12. Sex By Age [49]
    label          Total population
    name                   P0120001
    dtype: object



Collect data on male population by age, county
----------------------------------------------

For now I'm only going to look at males. This is probably a bad idea in
general.

Start with the 2010 census
~~~~~~~~~~~~~~~~~~~~~~~~~~

The male population is broken down into some somewhat arbitrary cohorts,
each with its own name. We want all of the fields between ``P0120003``
and ``P0120025``.

We'll do some data munging to get it in numeric format, and to take care
of the labels and indicies.

.. code:: python

    fields = ['P01200%02i'%i for i in range(3,26)]
    url = 'http://api.census.gov/data/2010/sf1?get=%s&for=county:*'%','.join(fields)
    print url
    pops2010 = pd.read_json(url)
    pops2010.columns = pops2010.iloc[0]
    pops2010.drop(pops2010.index[0], inplace=True)
    pops2010 = pops2010.applymap(float)
    pops2010.set_index(['state', 'county'], inplace=True)
    pops2010.head()


.. parsed-literal::

    http://api.census.gov/data/2010/sf1?get=P0120003,P0120004,P0120005,P0120006,P0120007,P0120008,P0120009,P0120010,P0120011,P0120012,P0120013,P0120014,P0120015,P0120016,P0120017,P0120018,P0120019,P0120020,P0120021,P0120022,P0120023,P0120024,P0120025&for=county:*




.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>P0120003</th>
          <th>P0120004</th>
          <th>P0120005</th>
          <th>P0120006</th>
          <th>P0120007</th>
          <th>P0120008</th>
          <th>P0120009</th>
          <th>P0120010</th>
          <th>P0120011</th>
          <th>P0120012</th>
          <th>...</th>
          <th>P0120016</th>
          <th>P0120017</th>
          <th>P0120018</th>
          <th>P0120019</th>
          <th>P0120020</th>
          <th>P0120021</th>
          <th>P0120022</th>
          <th>P0120023</th>
          <th>P0120024</th>
          <th>P0120025</th>
        </tr>
        <tr>
          <th>state</th>
          <th>county</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">1</th>
          <th>1</th>
          <td>1866</td>
          <td>2001</td>
          <td>2171</td>
          <td>1417</td>
          <td>796</td>
          <td>350</td>
          <td>279</td>
          <td>910</td>
          <td>1543</td>
          <td>1594</td>
          <td>...</td>
          <td>1866</td>
          <td>1524</td>
          <td>494</td>
          <td>785</td>
          <td>418</td>
          <td>596</td>
          <td>807</td>
          <td>546</td>
          <td>295</td>
          <td>159</td>
        </tr>
        <tr>
          <th>3</th>
          <td>5614</td>
          <td>5832</td>
          <td>6076</td>
          <td>3704</td>
          <td>2226</td>
          <td>1013</td>
          <td>862</td>
          <td>2918</td>
          <td>5183</td>
          <td>5317</td>
          <td>...</td>
          <td>6425</td>
          <td>5943</td>
          <td>2301</td>
          <td>3427</td>
          <td>2054</td>
          <td>2841</td>
          <td>3663</td>
          <td>2644</td>
          <td>1735</td>
          <td>1176</td>
        </tr>
        <tr>
          <th>5</th>
          <td>847</td>
          <td>826</td>
          <td>820</td>
          <td>559</td>
          <td>360</td>
          <td>190</td>
          <td>192</td>
          <td>666</td>
          <td>1212</td>
          <td>1162</td>
          <td>...</td>
          <td>1000</td>
          <td>910</td>
          <td>358</td>
          <td>501</td>
          <td>280</td>
          <td>351</td>
          <td>436</td>
          <td>303</td>
          <td>195</td>
          <td>129</td>
        </tr>
        <tr>
          <th>7</th>
          <td>712</td>
          <td>759</td>
          <td>771</td>
          <td>513</td>
          <td>293</td>
          <td>122</td>
          <td>167</td>
          <td>522</td>
          <td>987</td>
          <td>1013</td>
          <td>...</td>
          <td>847</td>
          <td>734</td>
          <td>294</td>
          <td>390</td>
          <td>188</td>
          <td>268</td>
          <td>347</td>
          <td>232</td>
          <td>138</td>
          <td>73</td>
        </tr>
        <tr>
          <th>9</th>
          <td>1805</td>
          <td>1936</td>
          <td>2113</td>
          <td>1340</td>
          <td>799</td>
          <td>340</td>
          <td>294</td>
          <td>943</td>
          <td>1735</td>
          <td>1730</td>
          <td>...</td>
          <td>1972</td>
          <td>1810</td>
          <td>716</td>
          <td>984</td>
          <td>546</td>
          <td>806</td>
          <td>1039</td>
          <td>684</td>
          <td>418</td>
          <td>234</td>
        </tr>
      </tbody>
    </table>
    <p>5 rows × 23 columns</p>
    </div>



Get data from 2000
~~~~~~~~~~~~~~~~~~

The 2000 census (logically) has different codes for its data, and (even
more logically) breaks the cohorts down differently. In this case, we
can get data for each age year with codes ``PCT012003`` through
``PCT012104``. The api limits us to only 50 columns at a time, so we'll
do it in chunks and stitch them together.

.. code:: python

    fields = ['PCT012%03i'%i for i in range(3,105)]
    
    dflist = []
    chunkSize = 40
    for i in range(0, len(fields), chunkSize):
        chunk = fields[i:i+chunkSize]
        url = 'http://api.census.gov/data/2000/sf1?get=%s&for=county:*'%','.join(chunk)
        print url
        df_chunk = pd.read_json(url)
        df_chunk.columns = df_chunk.iloc[0]
        df_chunk.drop(df_chunk.index[0], inplace=True)
        df_chunk = df_chunk.applymap(float)
        df_chunk.set_index(['state', 'county'], inplace=True)
        dflist.append(df_chunk)
    
    pops2000 = pd.concat(dflist,axis=1)
    pops2000 = pops2000.applymap(float)
    pops2000.head()


.. parsed-literal::

    http://api.census.gov/data/2000/sf1?get=PCT012003,PCT012004,PCT012005,PCT012006,PCT012007,PCT012008,PCT012009,PCT012010,PCT012011,PCT012012,PCT012013,PCT012014,PCT012015,PCT012016,PCT012017,PCT012018,PCT012019,PCT012020,PCT012021,PCT012022,PCT012023,PCT012024,PCT012025,PCT012026,PCT012027,PCT012028,PCT012029,PCT012030,PCT012031,PCT012032,PCT012033,PCT012034,PCT012035,PCT012036,PCT012037,PCT012038,PCT012039,PCT012040,PCT012041,PCT012042&for=county:*
    http://api.census.gov/data/2000/sf1?get=PCT012043,PCT012044,PCT012045,PCT012046,PCT012047,PCT012048,PCT012049,PCT012050,PCT012051,PCT012052,PCT012053,PCT012054,PCT012055,PCT012056,PCT012057,PCT012058,PCT012059,PCT012060,PCT012061,PCT012062,PCT012063,PCT012064,PCT012065,PCT012066,PCT012067,PCT012068,PCT012069,PCT012070,PCT012071,PCT012072,PCT012073,PCT012074,PCT012075,PCT012076,PCT012077,PCT012078,PCT012079,PCT012080,PCT012081,PCT012082&for=county:*
    http://api.census.gov/data/2000/sf1?get=PCT012083,PCT012084,PCT012085,PCT012086,PCT012087,PCT012088,PCT012089,PCT012090,PCT012091,PCT012092,PCT012093,PCT012094,PCT012095,PCT012096,PCT012097,PCT012098,PCT012099,PCT012100,PCT012101,PCT012102,PCT012103,PCT012104&for=county:*




.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>PCT012003</th>
          <th>PCT012004</th>
          <th>PCT012005</th>
          <th>PCT012006</th>
          <th>PCT012007</th>
          <th>PCT012008</th>
          <th>PCT012009</th>
          <th>PCT012010</th>
          <th>PCT012011</th>
          <th>PCT012012</th>
          <th>...</th>
          <th>PCT012095</th>
          <th>PCT012096</th>
          <th>PCT012097</th>
          <th>PCT012098</th>
          <th>PCT012099</th>
          <th>PCT012100</th>
          <th>PCT012101</th>
          <th>PCT012102</th>
          <th>PCT012103</th>
          <th>PCT012104</th>
        </tr>
        <tr>
          <th>state</th>
          <th>county</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">1</th>
          <th>1</th>
          <td>264</td>
          <td>305</td>
          <td>293</td>
          <td>331</td>
          <td>309</td>
          <td>364</td>
          <td>342</td>
          <td>374</td>
          <td>382</td>
          <td>411</td>
          <td>...</td>
          <td>6</td>
          <td>2</td>
          <td>0</td>
          <td>7</td>
          <td>2</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>1</td>
          <td>0</td>
        </tr>
        <tr>
          <th>3</th>
          <td>877</td>
          <td>865</td>
          <td>845</td>
          <td>873</td>
          <td>926</td>
          <td>856</td>
          <td>951</td>
          <td>981</td>
          <td>1031</td>
          <td>1118</td>
          <td>...</td>
          <td>31</td>
          <td>28</td>
          <td>14</td>
          <td>13</td>
          <td>2</td>
          <td>5</td>
          <td>6</td>
          <td>4</td>
          <td>5</td>
          <td>0</td>
        </tr>
        <tr>
          <th>5</th>
          <td>185</td>
          <td>184</td>
          <td>196</td>
          <td>173</td>
          <td>191</td>
          <td>223</td>
          <td>187</td>
          <td>236</td>
          <td>193</td>
          <td>234</td>
          <td>...</td>
          <td>3</td>
          <td>3</td>
          <td>5</td>
          <td>3</td>
          <td>2</td>
          <td>2</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>7</th>
          <td>179</td>
          <td>146</td>
          <td>150</td>
          <td>145</td>
          <td>157</td>
          <td>148</td>
          <td>183</td>
          <td>140</td>
          <td>147</td>
          <td>151</td>
          <td>...</td>
          <td>6</td>
          <td>2</td>
          <td>2</td>
          <td>2</td>
          <td>3</td>
          <td>2</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>9</th>
          <td>344</td>
          <td>347</td>
          <td>374</td>
          <td>394</td>
          <td>376</td>
          <td>377</td>
          <td>400</td>
          <td>361</td>
          <td>402</td>
          <td>366</td>
          <td>...</td>
          <td>6</td>
          <td>9</td>
          <td>1</td>
          <td>6</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>3</td>
          <td>5</td>
          <td>0</td>
        </tr>
      </tbody>
    </table>
    <p>5 rows × 102 columns</p>
    </div>



Align the datasets
------------------

As they have different cohorts, we need to do some summation before we
can merge the two census years into a single table. I'll break the data
down into 10-year cohorts by selecting columns to stitch together. We'll
set breakpoints by the last few digits of the field name, and label our
new cohorts according to which decade of your life they are. We're using
1-based indexing here for the cohort names.

.. code:: python

    pops2010d = pd.DataFrame(index=pops2010.index)
    
    decades = ['dec_%i'%i for i in range(1,10)]
    breakpoints_2010 = [3, 5, 8, 12, 14, 16, 18, 22, 24, 26]
    for dec, s, f in zip(decades, breakpoints_2010[:-1], breakpoints_2010[1:]):
        pops2010d[dec] = pops2010[['P0120%03i'%i for i in range(s,f)]].sum(axis=1)
        
    pops2010d.head()




.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>dec_1</th>
          <th>dec_2</th>
          <th>dec_3</th>
          <th>dec_4</th>
          <th>dec_5</th>
          <th>dec_6</th>
          <th>dec_7</th>
          <th>dec_8</th>
          <th>dec_9</th>
        </tr>
        <tr>
          <th>state</th>
          <th>county</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">1</th>
          <th>1</th>
          <td>3867</td>
          <td>4384</td>
          <td>3082</td>
          <td>3598</td>
          <td>4148</td>
          <td>3390</td>
          <td>2293</td>
          <td>1353</td>
          <td>454</td>
        </tr>
        <tr>
          <th>3</th>
          <td>11446</td>
          <td>12006</td>
          <td>9976</td>
          <td>11042</td>
          <td>12517</td>
          <td>12368</td>
          <td>10623</td>
          <td>6307</td>
          <td>2911</td>
        </tr>
        <tr>
          <th>5</th>
          <td>1673</td>
          <td>1739</td>
          <td>2260</td>
          <td>2208</td>
          <td>2233</td>
          <td>1910</td>
          <td>1490</td>
          <td>739</td>
          <td>324</td>
        </tr>
        <tr>
          <th>7</th>
          <td>1471</td>
          <td>1577</td>
          <td>1798</td>
          <td>2016</td>
          <td>1928</td>
          <td>1581</td>
          <td>1140</td>
          <td>579</td>
          <td>211</td>
        </tr>
        <tr>
          <th>9</th>
          <td>3741</td>
          <td>4252</td>
          <td>3312</td>
          <td>3719</td>
          <td>4129</td>
          <td>3782</td>
          <td>3052</td>
          <td>1723</td>
          <td>652</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    pops2000d = pd.DataFrame(index=pops2000.index)
    
    decades = ['dec_%i'%i for i in range(1,10)]
    breakpoints_2000 = [3, 13, 23, 33, 43, 53, 63, 73, 83, 104]
    for dec, s, f in zip(decades, breakpoints_2000[:-1], breakpoints_2000[1:]):
        pops2000d[dec] = pops2000[['PCT012%03i'%i for i in range(s,f)]].sum(axis=1)
    
    pops2000d.head()




.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>dec_1</th>
          <th>dec_2</th>
          <th>dec_3</th>
          <th>dec_4</th>
          <th>dec_5</th>
          <th>dec_6</th>
          <th>dec_7</th>
          <th>dec_8</th>
          <th>dec_9</th>
        </tr>
        <tr>
          <th>state</th>
          <th>county</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">1</th>
          <th>1</th>
          <td>3375</td>
          <td>3630</td>
          <td>2461</td>
          <td>3407</td>
          <td>3283</td>
          <td>2319</td>
          <td>1637</td>
          <td>825</td>
          <td>284</td>
        </tr>
        <tr>
          <th>3</th>
          <td>9323</td>
          <td>10094</td>
          <td>7600</td>
          <td>9725</td>
          <td>10379</td>
          <td>8519</td>
          <td>6675</td>
          <td>4711</td>
          <td>1822</td>
        </tr>
        <tr>
          <th>5</th>
          <td>2002</td>
          <td>2198</td>
          <td>2412</td>
          <td>2465</td>
          <td>2178</td>
          <td>1699</td>
          <td>1026</td>
          <td>689</td>
          <td>301</td>
        </tr>
        <tr>
          <th>7</th>
          <td>1546</td>
          <td>1460</td>
          <td>1680</td>
          <td>1762</td>
          <td>1624</td>
          <td>1237</td>
          <td>774</td>
          <td>475</td>
          <td>187</td>
        </tr>
        <tr>
          <th>9</th>
          <td>3741</td>
          <td>3615</td>
          <td>3393</td>
          <td>3901</td>
          <td>3773</td>
          <td>3007</td>
          <td>2227</td>
          <td>1269</td>
          <td>550</td>
        </tr>
      </tbody>
    </table>
    </div>



Now that the data have been formatted in the same way, we'll concatenate
them. We also drop any rows that don't show up in both datasets.

.. code:: python

    frame = pd.concat([pops2000d, pops2010d], keys=[2000, 2010], axis=1)
    frame.dropna(inplace=True)
    frame.head()




.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr>
          <th></th>
          <th></th>
          <th colspan="9" halign="left">2000</th>
          <th colspan="9" halign="left">2010</th>
        </tr>
        <tr>
          <th></th>
          <th></th>
          <th>dec_1</th>
          <th>dec_2</th>
          <th>dec_3</th>
          <th>dec_4</th>
          <th>dec_5</th>
          <th>dec_6</th>
          <th>dec_7</th>
          <th>dec_8</th>
          <th>dec_9</th>
          <th>dec_1</th>
          <th>dec_2</th>
          <th>dec_3</th>
          <th>dec_4</th>
          <th>dec_5</th>
          <th>dec_6</th>
          <th>dec_7</th>
          <th>dec_8</th>
          <th>dec_9</th>
        </tr>
        <tr>
          <th>state</th>
          <th>county</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">1</th>
          <th>1</th>
          <td>3375</td>
          <td>3630</td>
          <td>2461</td>
          <td>3407</td>
          <td>3283</td>
          <td>2319</td>
          <td>1637</td>
          <td>825</td>
          <td>284</td>
          <td>3867</td>
          <td>4384</td>
          <td>3082</td>
          <td>3598</td>
          <td>4148</td>
          <td>3390</td>
          <td>2293</td>
          <td>1353</td>
          <td>454</td>
        </tr>
        <tr>
          <th>3</th>
          <td>9323</td>
          <td>10094</td>
          <td>7600</td>
          <td>9725</td>
          <td>10379</td>
          <td>8519</td>
          <td>6675</td>
          <td>4711</td>
          <td>1822</td>
          <td>11446</td>
          <td>12006</td>
          <td>9976</td>
          <td>11042</td>
          <td>12517</td>
          <td>12368</td>
          <td>10623</td>
          <td>6307</td>
          <td>2911</td>
        </tr>
        <tr>
          <th>5</th>
          <td>2002</td>
          <td>2198</td>
          <td>2412</td>
          <td>2465</td>
          <td>2178</td>
          <td>1699</td>
          <td>1026</td>
          <td>689</td>
          <td>301</td>
          <td>1673</td>
          <td>1739</td>
          <td>2260</td>
          <td>2208</td>
          <td>2233</td>
          <td>1910</td>
          <td>1490</td>
          <td>739</td>
          <td>324</td>
        </tr>
        <tr>
          <th>7</th>
          <td>1546</td>
          <td>1460</td>
          <td>1680</td>
          <td>1762</td>
          <td>1624</td>
          <td>1237</td>
          <td>774</td>
          <td>475</td>
          <td>187</td>
          <td>1471</td>
          <td>1577</td>
          <td>1798</td>
          <td>2016</td>
          <td>1928</td>
          <td>1581</td>
          <td>1140</td>
          <td>579</td>
          <td>211</td>
        </tr>
        <tr>
          <th>9</th>
          <td>3741</td>
          <td>3615</td>
          <td>3393</td>
          <td>3901</td>
          <td>3773</td>
          <td>3007</td>
          <td>2227</td>
          <td>1269</td>
          <td>550</td>
          <td>3741</td>
          <td>4252</td>
          <td>3312</td>
          <td>3719</td>
          <td>4129</td>
          <td>3782</td>
          <td>3052</td>
          <td>1723</td>
          <td>652</td>
        </tr>
      </tbody>
    </table>
    </div>



I'm happy with this format, so we'll save it to csv:

.. code:: python

    frame.to_csv('Males by decade and county.csv')

As our dataframe has a
`MultiIndex <http://pandas.pydata.org/pandas-docs/stable/advanced.html>`__
we have to take care when re-importing from the csv to get the index and
header columns correct.

.. code:: python

    pd.read_csv('Males by decade and county.csv', header=[0,1], index_col=[0,1])




.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr>
          <th></th>
          <th></th>
          <th colspan="9" halign="left">2000</th>
          <th colspan="9" halign="left">2010</th>
        </tr>
        <tr>
          <th></th>
          <th></th>
          <th>dec_1</th>
          <th>dec_2</th>
          <th>dec_3</th>
          <th>dec_4</th>
          <th>dec_5</th>
          <th>dec_6</th>
          <th>dec_7</th>
          <th>dec_8</th>
          <th>dec_9</th>
          <th>dec_1</th>
          <th>dec_2</th>
          <th>dec_3</th>
          <th>dec_4</th>
          <th>dec_5</th>
          <th>dec_6</th>
          <th>dec_7</th>
          <th>dec_8</th>
          <th>dec_9</th>
        </tr>
        <tr>
          <th>state</th>
          <th>county</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="30" valign="top">1</th>
          <th>1</th>
          <td>3375</td>
          <td>3630</td>
          <td>2461</td>
          <td>3407</td>
          <td>3283</td>
          <td>2319</td>
          <td>1637</td>
          <td>825</td>
          <td>284</td>
          <td>3867</td>
          <td>4384</td>
          <td>3082</td>
          <td>3598</td>
          <td>4148</td>
          <td>3390</td>
          <td>2293</td>
          <td>1353</td>
          <td>454</td>
        </tr>
        <tr>
          <th>3</th>
          <td>9323</td>
          <td>10094</td>
          <td>7600</td>
          <td>9725</td>
          <td>10379</td>
          <td>8519</td>
          <td>6675</td>
          <td>4711</td>
          <td>1822</td>
          <td>11446</td>
          <td>12006</td>
          <td>9976</td>
          <td>11042</td>
          <td>12517</td>
          <td>12368</td>
          <td>10623</td>
          <td>6307</td>
          <td>2911</td>
        </tr>
        <tr>
          <th>5</th>
          <td>2002</td>
          <td>2198</td>
          <td>2412</td>
          <td>2465</td>
          <td>2178</td>
          <td>1699</td>
          <td>1026</td>
          <td>689</td>
          <td>301</td>
          <td>1673</td>
          <td>1739</td>
          <td>2260</td>
          <td>2208</td>
          <td>2233</td>
          <td>1910</td>
          <td>1490</td>
          <td>739</td>
          <td>324</td>
        </tr>
        <tr>
          <th>7</th>
          <td>1546</td>
          <td>1460</td>
          <td>1680</td>
          <td>1762</td>
          <td>1624</td>
          <td>1237</td>
          <td>774</td>
          <td>475</td>
          <td>187</td>
          <td>1471</td>
          <td>1577</td>
          <td>1798</td>
          <td>2016</td>
          <td>1928</td>
          <td>1581</td>
          <td>1140</td>
          <td>579</td>
          <td>211</td>
        </tr>
        <tr>
          <th>9</th>
          <td>3741</td>
          <td>3615</td>
          <td>3393</td>
          <td>3901</td>
          <td>3773</td>
          <td>3007</td>
          <td>2227</td>
          <td>1269</td>
          <td>550</td>
          <td>3741</td>
          <td>4252</td>
          <td>3312</td>
          <td>3719</td>
          <td>4129</td>
          <td>3782</td>
          <td>3052</td>
          <td>1723</td>
          <td>652</td>
        </tr>
        <tr>
          <th>11</th>
          <td>840</td>
          <td>885</td>
          <td>1059</td>
          <td>952</td>
          <td>968</td>
          <td>628</td>
          <td>390</td>
          <td>238</td>
          <td>179</td>
          <td>697</td>
          <td>702</td>
          <td>892</td>
          <td>884</td>
          <td>876</td>
          <td>905</td>
          <td>553</td>
          <td>287</td>
          <td>116</td>
        </tr>
        <tr>
          <th>13</th>
          <td>1497</td>
          <td>1766</td>
          <td>1076</td>
          <td>1219</td>
          <td>1496</td>
          <td>1199</td>
          <td>832</td>
          <td>599</td>
          <td>334</td>
          <td>1440</td>
          <td>1494</td>
          <td>1112</td>
          <td>1115</td>
          <td>1188</td>
          <td>1477</td>
          <td>1120</td>
          <td>600</td>
          <td>292</td>
        </tr>
        <tr>
          <th>15</th>
          <td>7212</td>
          <td>8032</td>
          <td>7544</td>
          <td>7613</td>
          <td>8237</td>
          <td>6544</td>
          <td>4535</td>
          <td>2846</td>
          <td>1137</td>
          <td>7586</td>
          <td>8279</td>
          <td>8185</td>
          <td>7041</td>
          <td>7723</td>
          <td>8030</td>
          <td>5842</td>
          <td>3185</td>
          <td>1305</td>
        </tr>
        <tr>
          <th>17</th>
          <td>2543</td>
          <td>2540</td>
          <td>2185</td>
          <td>2437</td>
          <td>2504</td>
          <td>2088</td>
          <td>1474</td>
          <td>992</td>
          <td>522</td>
          <td>2062</td>
          <td>2302</td>
          <td>1905</td>
          <td>1954</td>
          <td>2325</td>
          <td>2427</td>
          <td>1907</td>
          <td>1045</td>
          <td>436</td>
        </tr>
        <tr>
          <th>19</th>
          <td>1552</td>
          <td>1506</td>
          <td>1424</td>
          <td>1664</td>
          <td>1726</td>
          <td>1598</td>
          <td>1322</td>
          <td>717</td>
          <td>285</td>
          <td>1453</td>
          <td>1729</td>
          <td>1224</td>
          <td>1504</td>
          <td>1893</td>
          <td>1999</td>
          <td>1773</td>
          <td>1002</td>
          <td>311</td>
        </tr>
        <tr>
          <th>21</th>
          <td>2957</td>
          <td>2904</td>
          <td>2656</td>
          <td>2872</td>
          <td>2882</td>
          <td>2317</td>
          <td>1612</td>
          <td>1002</td>
          <td>379</td>
          <td>3024</td>
          <td>3137</td>
          <td>2671</td>
          <td>3015</td>
          <td>2988</td>
          <td>2970</td>
          <td>2163</td>
          <td>1181</td>
          <td>459</td>
        </tr>
        <tr>
          <th>23</th>
          <td>1097</td>
          <td>1164</td>
          <td>839</td>
          <td>956</td>
          <td>1080</td>
          <td>1010</td>
          <td>710</td>
          <td>430</td>
          <td>203</td>
          <td>875</td>
          <td>931</td>
          <td>673</td>
          <td>755</td>
          <td>914</td>
          <td>1002</td>
          <td>837</td>
          <td>479</td>
          <td>222</td>
        </tr>
        <tr>
          <th>25</th>
          <td>2130</td>
          <td>2247</td>
          <td>1496</td>
          <td>1785</td>
          <td>1904</td>
          <td>1521</td>
          <td>1120</td>
          <td>654</td>
          <td>323</td>
          <td>1590</td>
          <td>1975</td>
          <td>1279</td>
          <td>1371</td>
          <td>1728</td>
          <td>1751</td>
          <td>1348</td>
          <td>830</td>
          <td>342</td>
        </tr>
        <tr>
          <th>27</th>
          <td>939</td>
          <td>1025</td>
          <td>854</td>
          <td>992</td>
          <td>983</td>
          <td>844</td>
          <td>664</td>
          <td>432</td>
          <td>217</td>
          <td>850</td>
          <td>982</td>
          <td>716</td>
          <td>815</td>
          <td>988</td>
          <td>972</td>
          <td>787</td>
          <td>493</td>
          <td>230</td>
        </tr>
        <tr>
          <th>29</th>
          <td>965</td>
          <td>1031</td>
          <td>879</td>
          <td>1061</td>
          <td>1048</td>
          <td>906</td>
          <td>643</td>
          <td>349</td>
          <td>155</td>
          <td>991</td>
          <td>1062</td>
          <td>827</td>
          <td>893</td>
          <td>1084</td>
          <td>1043</td>
          <td>916</td>
          <td>466</td>
          <td>171</td>
        </tr>
        <tr>
          <th>31</th>
          <td>2903</td>
          <td>3246</td>
          <td>2986</td>
          <td>3006</td>
          <td>3067</td>
          <td>2628</td>
          <td>1826</td>
          <td>1189</td>
          <td>452</td>
          <td>3403</td>
          <td>3448</td>
          <td>3581</td>
          <td>3279</td>
          <td>3415</td>
          <td>3065</td>
          <td>2448</td>
          <td>1430</td>
          <td>615</td>
        </tr>
        <tr>
          <th>33</th>
          <td>3606</td>
          <td>3773</td>
          <td>3156</td>
          <td>3740</td>
          <td>3939</td>
          <td>3310</td>
          <td>2458</td>
          <td>1632</td>
          <td>697</td>
          <td>3211</td>
          <td>3654</td>
          <td>3004</td>
          <td>3076</td>
          <td>3738</td>
          <td>3837</td>
          <td>2976</td>
          <td>1778</td>
          <td>885</td>
        </tr>
        <tr>
          <th>35</th>
          <td>1008</td>
          <td>1069</td>
          <td>762</td>
          <td>838</td>
          <td>914</td>
          <td>865</td>
          <td>579</td>
          <td>458</td>
          <td>174</td>
          <td>801</td>
          <td>965</td>
          <td>668</td>
          <td>634</td>
          <td>833</td>
          <td>994</td>
          <td>855</td>
          <td>423</td>
          <td>239</td>
        </tr>
        <tr>
          <th>37</th>
          <td>813</td>
          <td>872</td>
          <td>814</td>
          <td>1005</td>
          <td>966</td>
          <td>712</td>
          <td>529</td>
          <td>387</td>
          <td>134</td>
          <td>614</td>
          <td>798</td>
          <td>534</td>
          <td>660</td>
          <td>831</td>
          <td>987</td>
          <td>752</td>
          <td>361</td>
          <td>190</td>
        </tr>
        <tr>
          <th>39</th>
          <td>2403</td>
          <td>2608</td>
          <td>2068</td>
          <td>2458</td>
          <td>2643</td>
          <td>2211</td>
          <td>1809</td>
          <td>1237</td>
          <td>555</td>
          <td>2431</td>
          <td>2527</td>
          <td>1984</td>
          <td>2097</td>
          <td>2452</td>
          <td>2731</td>
          <td>2119</td>
          <td>1328</td>
          <td>619</td>
        </tr>
        <tr>
          <th>41</th>
          <td>921</td>
          <td>1026</td>
          <td>766</td>
          <td>807</td>
          <td>944</td>
          <td>826</td>
          <td>549</td>
          <td>431</td>
          <td>193</td>
          <td>909</td>
          <td>1007</td>
          <td>734</td>
          <td>793</td>
          <td>942</td>
          <td>973</td>
          <td>780</td>
          <td>403</td>
          <td>173</td>
        </tr>
        <tr>
          <th>43</th>
          <td>5230</td>
          <td>5602</td>
          <td>5008</td>
          <td>5695</td>
          <td>5596</td>
          <td>4595</td>
          <td>3351</td>
          <td>2230</td>
          <td>907</td>
          <td>5177</td>
          <td>5563</td>
          <td>4825</td>
          <td>5104</td>
          <td>5649</td>
          <td>5456</td>
          <td>4369</td>
          <td>2526</td>
          <td>1050</td>
        </tr>
        <tr>
          <th>45</th>
          <td>3860</td>
          <td>3656</td>
          <td>3712</td>
          <td>3650</td>
          <td>3446</td>
          <td>2659</td>
          <td>1806</td>
          <td>1162</td>
          <td>405</td>
          <td>3624</td>
          <td>3417</td>
          <td>3868</td>
          <td>3224</td>
          <td>3190</td>
          <td>3259</td>
          <td>2395</td>
          <td>1308</td>
          <td>540</td>
        </tr>
        <tr>
          <th>47</th>
          <td>3477</td>
          <td>3901</td>
          <td>2486</td>
          <td>2587</td>
          <td>3044</td>
          <td>2317</td>
          <td>1658</td>
          <td>1121</td>
          <td>501</td>
          <td>3195</td>
          <td>3298</td>
          <td>2413</td>
          <td>2124</td>
          <td>2584</td>
          <td>2902</td>
          <td>2127</td>
          <td>1129</td>
          <td>472</td>
        </tr>
        <tr>
          <th>49</th>
          <td>4615</td>
          <td>4491</td>
          <td>4493</td>
          <td>4697</td>
          <td>4571</td>
          <td>3768</td>
          <td>2540</td>
          <td>1663</td>
          <td>670</td>
          <td>5191</td>
          <td>5134</td>
          <td>4267</td>
          <td>4732</td>
          <td>4876</td>
          <td>4574</td>
          <td>3618</td>
          <td>1925</td>
          <td>796</td>
        </tr>
        <tr>
          <th>51</th>
          <td>4684</td>
          <td>4939</td>
          <td>4945</td>
          <td>5530</td>
          <td>5172</td>
          <td>3825</td>
          <td>2361</td>
          <td>1336</td>
          <td>548</td>
          <td>5110</td>
          <td>5556</td>
          <td>5093</td>
          <td>5410</td>
          <td>5785</td>
          <td>5262</td>
          <td>3858</td>
          <td>1890</td>
          <td>725</td>
        </tr>
        <tr>
          <th>53</th>
          <td>2559</td>
          <td>2757</td>
          <td>2949</td>
          <td>2955</td>
          <td>3078</td>
          <td>2224</td>
          <td>1585</td>
          <td>927</td>
          <td>441</td>
          <td>2337</td>
          <td>2501</td>
          <td>2582</td>
          <td>3078</td>
          <td>2895</td>
          <td>2818</td>
          <td>1928</td>
          <td>1193</td>
          <td>434</td>
        </tr>
        <tr>
          <th>55</th>
          <td>6842</td>
          <td>7225</td>
          <td>6406</td>
          <td>6824</td>
          <td>7328</td>
          <td>6187</td>
          <td>4167</td>
          <td>3261</td>
          <td>1266</td>
          <td>6551</td>
          <td>7323</td>
          <td>6029</td>
          <td>6317</td>
          <td>7055</td>
          <td>7222</td>
          <td>5647</td>
          <td>3039</td>
          <td>1443</td>
        </tr>
        <tr>
          <th>57</th>
          <td>1199</td>
          <td>1363</td>
          <td>1071</td>
          <td>1213</td>
          <td>1310</td>
          <td>1162</td>
          <td>847</td>
          <td>536</td>
          <td>234</td>
          <td>1057</td>
          <td>1279</td>
          <td>902</td>
          <td>953</td>
          <td>1187</td>
          <td>1232</td>
          <td>1017</td>
          <td>615</td>
          <td>265</td>
        </tr>
        <tr>
          <th>59</th>
          <td>2108</td>
          <td>2303</td>
          <td>2255</td>
          <td>2221</td>
          <td>2091</td>
          <td>1758</td>
          <td>1391</td>
          <td>871</td>
          <td>330</td>
          <td>2266</td>
          <td>2228</td>
          <td>2109</td>
          <td>2132</td>
          <td>2130</td>
          <td>2003</td>
          <td>1565</td>
          <td>978</td>
          <td>417</td>
        </tr>
        <tr>
          <th>...</th>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th rowspan="7" valign="top">55</th>
          <th>129</th>
          <td>911</td>
          <td>1301</td>
          <td>661</td>
          <td>1017</td>
          <td>1256</td>
          <td>1107</td>
          <td>891</td>
          <td>615</td>
          <td>312</td>
          <td>879</td>
          <td>907</td>
          <td>655</td>
          <td>791</td>
          <td>1121</td>
          <td>1332</td>
          <td>1214</td>
          <td>710</td>
          <td>315</td>
        </tr>
        <tr>
          <th>131</th>
          <td>8537</td>
          <td>9141</td>
          <td>6305</td>
          <td>9977</td>
          <td>9934</td>
          <td>6906</td>
          <td>4025</td>
          <td>2589</td>
          <td>1194</td>
          <td>8759</td>
          <td>9196</td>
          <td>6665</td>
          <td>8111</td>
          <td>11050</td>
          <td>10028</td>
          <td>6446</td>
          <td>3288</td>
          <td>1850</td>
        </tr>
        <tr>
          <th>133</th>
          <td>24815</td>
          <td>27971</td>
          <td>17718</td>
          <td>26947</td>
          <td>32031</td>
          <td>22825</td>
          <td>13003</td>
          <td>8520</td>
          <td>3653</td>
          <td>24294</td>
          <td>28104</td>
          <td>19344</td>
          <td>21650</td>
          <td>30470</td>
          <td>31667</td>
          <td>19754</td>
          <td>10176</td>
          <td>5896</td>
        </tr>
        <tr>
          <th>135</th>
          <td>3451</td>
          <td>4069</td>
          <td>2595</td>
          <td>3789</td>
          <td>4098</td>
          <td>2996</td>
          <td>2080</td>
          <td>1821</td>
          <td>1000</td>
          <td>3182</td>
          <td>3531</td>
          <td>2655</td>
          <td>2964</td>
          <td>3954</td>
          <td>4179</td>
          <td>2931</td>
          <td>1726</td>
          <td>1325</td>
        </tr>
        <tr>
          <th>137</th>
          <td>1373</td>
          <td>1784</td>
          <td>977</td>
          <td>1510</td>
          <td>1812</td>
          <td>1456</td>
          <td>1396</td>
          <td>992</td>
          <td>369</td>
          <td>1250</td>
          <td>1524</td>
          <td>1282</td>
          <td>1473</td>
          <td>1977</td>
          <td>2142</td>
          <td>1633</td>
          <td>1100</td>
          <td>512</td>
        </tr>
        <tr>
          <th>139</th>
          <td>10095</td>
          <td>11708</td>
          <td>12046</td>
          <td>12620</td>
          <td>12521</td>
          <td>8297</td>
          <td>5210</td>
          <td>3777</td>
          <td>1875</td>
          <td>10105</td>
          <td>11085</td>
          <td>13374</td>
          <td>10920</td>
          <td>12568</td>
          <td>11968</td>
          <td>7363</td>
          <td>4065</td>
          <td>2504</td>
        </tr>
        <tr>
          <th>141</th>
          <td>5065</td>
          <td>5916</td>
          <td>4018</td>
          <td>5515</td>
          <td>5946</td>
          <td>4268</td>
          <td>2874</td>
          <td>2215</td>
          <td>1213</td>
          <td>4555</td>
          <td>5065</td>
          <td>4112</td>
          <td>4095</td>
          <td>5486</td>
          <td>5714</td>
          <td>3886</td>
          <td>2366</td>
          <td>1498</td>
        </tr>
        <tr>
          <th rowspan="23" valign="top">56</th>
          <th>1</th>
          <td>1666</td>
          <td>2803</td>
          <td>4997</td>
          <td>1859</td>
          <td>2005</td>
          <td>1555</td>
          <td>848</td>
          <td>545</td>
          <td>251</td>
          <td>1890</td>
          <td>2615</td>
          <td>6309</td>
          <td>2129</td>
          <td>1645</td>
          <td>1995</td>
          <td>1380</td>
          <td>603</td>
          <td>331</td>
        </tr>
        <tr>
          <th>3</th>
          <td>860</td>
          <td>1032</td>
          <td>514</td>
          <td>639</td>
          <td>817</td>
          <td>713</td>
          <td>558</td>
          <td>403</td>
          <td>199</td>
          <td>796</td>
          <td>867</td>
          <td>605</td>
          <td>593</td>
          <td>710</td>
          <td>869</td>
          <td>740</td>
          <td>457</td>
          <td>245</td>
        </tr>
        <tr>
          <th>5</th>
          <td>2728</td>
          <td>3245</td>
          <td>2306</td>
          <td>2475</td>
          <td>3515</td>
          <td>1823</td>
          <td>748</td>
          <td>366</td>
          <td>102</td>
          <td>3896</td>
          <td>3480</td>
          <td>4008</td>
          <td>3564</td>
          <td>3295</td>
          <td>3788</td>
          <td>1528</td>
          <td>497</td>
          <td>202</td>
        </tr>
        <tr>
          <th>7</th>
          <td>985</td>
          <td>1206</td>
          <td>1027</td>
          <td>1221</td>
          <td>1523</td>
          <td>1143</td>
          <td>666</td>
          <td>414</td>
          <td>191</td>
          <td>1150</td>
          <td>999</td>
          <td>1172</td>
          <td>1143</td>
          <td>1218</td>
          <td>1313</td>
          <td>912</td>
          <td>434</td>
          <td>212</td>
        </tr>
        <tr>
          <th>9</th>
          <td>900</td>
          <td>1043</td>
          <td>557</td>
          <td>788</td>
          <td>1118</td>
          <td>772</td>
          <td>441</td>
          <td>286</td>
          <td>102</td>
          <td>994</td>
          <td>995</td>
          <td>796</td>
          <td>852</td>
          <td>972</td>
          <td>1135</td>
          <td>742</td>
          <td>350</td>
          <td>181</td>
        </tr>
        <tr>
          <th>11</th>
          <td>358</td>
          <td>532</td>
          <td>246</td>
          <td>345</td>
          <td>502</td>
          <td>420</td>
          <td>334</td>
          <td>163</td>
          <td>79</td>
          <td>510</td>
          <td>479</td>
          <td>352</td>
          <td>382</td>
          <td>491</td>
          <td>596</td>
          <td>480</td>
          <td>261</td>
          <td>97</td>
        </tr>
        <tr>
          <th>13</th>
          <td>2539</td>
          <td>3099</td>
          <td>1872</td>
          <td>2187</td>
          <td>2880</td>
          <td>2181</td>
          <td>1511</td>
          <td>1061</td>
          <td>410</td>
          <td>3032</td>
          <td>2746</td>
          <td>2529</td>
          <td>2286</td>
          <td>2490</td>
          <td>3006</td>
          <td>2168</td>
          <td>1149</td>
          <td>624</td>
        </tr>
        <tr>
          <th>15</th>
          <td>816</td>
          <td>1022</td>
          <td>674</td>
          <td>716</td>
          <td>974</td>
          <td>779</td>
          <td>576</td>
          <td>442</td>
          <td>235</td>
          <td>735</td>
          <td>921</td>
          <td>858</td>
          <td>766</td>
          <td>888</td>
          <td>1111</td>
          <td>836</td>
          <td>526</td>
          <td>265</td>
        </tr>
        <tr>
          <th>17</th>
          <td>246</td>
          <td>359</td>
          <td>187</td>
          <td>248</td>
          <td>400</td>
          <td>338</td>
          <td>273</td>
          <td>200</td>
          <td>97</td>
          <td>264</td>
          <td>284</td>
          <td>235</td>
          <td>222</td>
          <td>298</td>
          <td>404</td>
          <td>326</td>
          <td>229</td>
          <td>115</td>
        </tr>
        <tr>
          <th>19</th>
          <td>419</td>
          <td>540</td>
          <td>291</td>
          <td>375</td>
          <td>566</td>
          <td>510</td>
          <td>365</td>
          <td>292</td>
          <td>118</td>
          <td>565</td>
          <td>497</td>
          <td>414</td>
          <td>516</td>
          <td>515</td>
          <td>730</td>
          <td>620</td>
          <td>318</td>
          <td>190</td>
        </tr>
        <tr>
          <th>21</th>
          <td>5759</td>
          <td>6176</td>
          <td>6018</td>
          <td>6631</td>
          <td>6274</td>
          <td>4698</td>
          <td>2751</td>
          <td>1878</td>
          <td>801</td>
          <td>6631</td>
          <td>6015</td>
          <td>6869</td>
          <td>5759</td>
          <td>6306</td>
          <td>6475</td>
          <td>4473</td>
          <td>2216</td>
          <td>1131</td>
        </tr>
        <tr>
          <th>23</th>
          <td>1133</td>
          <td>1391</td>
          <td>642</td>
          <td>873</td>
          <td>1249</td>
          <td>868</td>
          <td>617</td>
          <td>408</td>
          <td>179</td>
          <td>1487</td>
          <td>1382</td>
          <td>899</td>
          <td>1257</td>
          <td>1189</td>
          <td>1410</td>
          <td>984</td>
          <td>485</td>
          <td>209</td>
        </tr>
        <tr>
          <th>25</th>
          <td>4578</td>
          <td>5435</td>
          <td>4221</td>
          <td>4335</td>
          <td>5649</td>
          <td>3824</td>
          <td>2262</td>
          <td>1950</td>
          <td>618</td>
          <td>5363</td>
          <td>4945</td>
          <td>5691</td>
          <td>4987</td>
          <td>4940</td>
          <td>5877</td>
          <td>3404</td>
          <td>1677</td>
          <td>1098</td>
        </tr>
        <tr>
          <th>27</th>
          <td>141</td>
          <td>187</td>
          <td>71</td>
          <td>145</td>
          <td>206</td>
          <td>149</td>
          <td>140</td>
          <td>86</td>
          <td>49</td>
          <td>127</td>
          <td>155</td>
          <td>92</td>
          <td>114</td>
          <td>144</td>
          <td>208</td>
          <td>152</td>
          <td>117</td>
          <td>50</td>
        </tr>
        <tr>
          <th>29</th>
          <td>1508</td>
          <td>2107</td>
          <td>1287</td>
          <td>1526</td>
          <td>2154</td>
          <td>1723</td>
          <td>1130</td>
          <td>765</td>
          <td>362</td>
          <td>1669</td>
          <td>1844</td>
          <td>1688</td>
          <td>1453</td>
          <td>1660</td>
          <td>2319</td>
          <td>1924</td>
          <td>976</td>
          <td>488</td>
        </tr>
        <tr>
          <th>31</th>
          <td>529</td>
          <td>703</td>
          <td>391</td>
          <td>491</td>
          <td>705</td>
          <td>627</td>
          <td>455</td>
          <td>306</td>
          <td>139</td>
          <td>428</td>
          <td>522</td>
          <td>408</td>
          <td>412</td>
          <td>555</td>
          <td>744</td>
          <td>680</td>
          <td>373</td>
          <td>181</td>
        </tr>
        <tr>
          <th>33</th>
          <td>1549</td>
          <td>2061</td>
          <td>1402</td>
          <td>1482</td>
          <td>2249</td>
          <td>1879</td>
          <td>1116</td>
          <td>844</td>
          <td>419</td>
          <td>1844</td>
          <td>1840</td>
          <td>1672</td>
          <td>1691</td>
          <td>1844</td>
          <td>2485</td>
          <td>1790</td>
          <td>884</td>
          <td>515</td>
        </tr>
        <tr>
          <th>35</th>
          <td>374</td>
          <td>469</td>
          <td>267</td>
          <td>412</td>
          <td>554</td>
          <td>433</td>
          <td>294</td>
          <td>140</td>
          <td>80</td>
          <td>707</td>
          <td>643</td>
          <td>731</td>
          <td>845</td>
          <td>830</td>
          <td>898</td>
          <td>555</td>
          <td>238</td>
          <td>103</td>
        </tr>
        <tr>
          <th>37</th>
          <td>2770</td>
          <td>3508</td>
          <td>2326</td>
          <td>2523</td>
          <td>3628</td>
          <td>2314</td>
          <td>1096</td>
          <td>598</td>
          <td>263</td>
          <td>3626</td>
          <td>3189</td>
          <td>3583</td>
          <td>3212</td>
          <td>2935</td>
          <td>3421</td>
          <td>1830</td>
          <td>730</td>
          <td>323</td>
        </tr>
        <tr>
          <th>39</th>
          <td>982</td>
          <td>1112</td>
          <td>2006</td>
          <td>1731</td>
          <td>1763</td>
          <td>1222</td>
          <td>582</td>
          <td>250</td>
          <td>85</td>
          <td>1216</td>
          <td>1018</td>
          <td>1979</td>
          <td>2079</td>
          <td>1576</td>
          <td>1623</td>
          <td>1097</td>
          <td>442</td>
          <td>161</td>
        </tr>
        <tr>
          <th>41</th>
          <td>1701</td>
          <td>2131</td>
          <td>1121</td>
          <td>1294</td>
          <td>1842</td>
          <td>1068</td>
          <td>456</td>
          <td>321</td>
          <td>120</td>
          <td>1821</td>
          <td>1724</td>
          <td>1288</td>
          <td>1408</td>
          <td>1300</td>
          <td>1682</td>
          <td>898</td>
          <td>363</td>
          <td>178</td>
        </tr>
        <tr>
          <th>43</th>
          <td>517</td>
          <td>781</td>
          <td>358</td>
          <td>496</td>
          <td>661</td>
          <td>537</td>
          <td>360</td>
          <td>287</td>
          <td>135</td>
          <td>598</td>
          <td>610</td>
          <td>417</td>
          <td>470</td>
          <td>527</td>
          <td>637</td>
          <td>516</td>
          <td>297</td>
          <td>183</td>
        </tr>
        <tr>
          <th>45</th>
          <td>359</td>
          <td>551</td>
          <td>347</td>
          <td>425</td>
          <td>627</td>
          <td>434</td>
          <td>301</td>
          <td>230</td>
          <td>99</td>
          <td>450</td>
          <td>448</td>
          <td>472</td>
          <td>481</td>
          <td>534</td>
          <td>652</td>
          <td>398</td>
          <td>208</td>
          <td>147</td>
        </tr>
      </tbody>
    </table>
    <p>3137 rows × 18 columns</p>
    </div>



